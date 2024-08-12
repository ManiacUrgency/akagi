import os
import json
import asyncio
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from ner_keyword_expander import *

import sys
# Get the absolute path of the current script
current_script_path = os.path.abspath(__file__)
# Get the parent directory of the current script
parent_dir = os.path.dirname(os.path.dirname(current_script_path))
# Add the parent directory to sys.path
sys.path.append(parent_dir)
from prompt_templates.query_constants import *

import pickle
from nltk.tokenize import word_tokenize

from enum import Enum
class RetrievalMethod(Enum):
    VECTOR_DB = 'vector_db'
    BM25 = 'bm25'

class BM25Retriever:
    def __init__(self, bm25_index, top_n, ids):
        self.bm25 = bm25_index
        self.top_n = top_n
        self.ids = ids
        self.ner_keyword_extractor = NERKeywordExpander()

    async def invoke(self, query):
        query = await self.ner_keyword_extractor.expand(query) 
        #print("\n\nExpanded query:", query)
        tokenized_query = word_tokenize(query.lower().replace(',', ''))
        print("\n\nTokenized query:", tokenized_query)
        scores = self.bm25.get_scores(tokenized_query)
        top_n_indices = scores.argsort()[-self.top_n:][::-1]
        ids = []
        for idx in top_n_indices:
            print(f"\nScore: {scores[idx]:.4f}")
            ids.append(self.ids[idx])
        return ids

# Initialize OpenAI embeddings and Pinecone
def initialize_openai_embeddings(model_name, api_key):
    return OpenAIEmbeddings(model=model_name, openai_api_key=api_key)

def initialize_pinecone(api_key, index_name):
    pc = Pinecone(api_key=api_key)
    index = pc.Index(index_name)
    return index

# Asynchronous function to stream LLM responses
async def stream_llm_responses(llm, request):
    async for chunk in llm.astream(request):
        yield chunk.content.replace("\n", "\n\t")

# Function to setup retriever
def get_openai_retriever():
    # Initialize OpenAI embeddings
    OPENAI_API_EMBEDDINGS_KEY = os.environ["OPENAI_API_EMBEDDINGS_KEY"]
    embed = initialize_openai_embeddings("text-embedding-3-large", OPENAI_API_EMBEDDINGS_KEY)

   # Initialize Pinecone
    PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
    index_name = "research-papers"  # Ensure this matches the index used in the embedding script
    text_field = "id"  # Updated to reflect the changes in metadata
    
    index = initialize_pinecone(PINECONE_API_KEY, index_name)
    vectorstore = PineconeVectorStore(index, embed, text_field)    
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "namespace": "responsible_ai",# "explainable_ai",  
            "k": 10
        }
    )
    return retriever

def get_bm25_retriever(data):
    file_path = os.path.dirname(os.path.realpath(__file__))
    index_file = os.path.join(file_path, "papers_index.pkl")
    if not os.path.exists(index_file):
        print(f"error: index file {index_file} does not exist. please run user_index_paper.py to create the index.")
        sys.exit(1)

    print("loading existing bm25 index...")
    with open(index_file, 'rb') as f:
        bm25 = pickle.load(f)

    ids = []
    for paper in data['papers']:
        for chunk in paper['chunks']:
            ids.append(chunk['id'])
    print(f"Number of self.ids: {len(ids)}")

    retriever = BM25Retriever(bm25, 10, ids)
    return retriever

# function to retrieve the full text using the id from the hash map
def get_text_by_id(chunk_id, hash_map):
    for paper in hash_map["papers"]:
        for chunk in paper["chunks"]:
            if chunk["id"] == chunk_id:
                text = "<text> " + chunk["text"] + "</text>\n<reference>" + chunk["reference"] + "</reference>"

                print("\nDOCUMENT:\n", text)
                return text
    return ""

# Function to handle queries
async def handle_query(query, retriever, retrieval_method, prompt, llm, hash_map):
    id_and_metadata_dict = await retriever.invoke(query)

    print("\n\nId and Metadata: ", id_and_metadata_dict, "\n\n")
    
    context = ""
    for doc in id_and_metadata_dict:
        if retrieval_method == RetrievalMethod.VECTOR_DB:
            chunk_id = doc.page_content
        elif retrieval_method == RetrievalMethod.BM25:
            chunk_id = doc
        if chunk_id:
            text = get_text_by_id(chunk_id, hash_map)
            if text:
                # print("\nDOUCMENT:\n", text)
                context += text + "\n"
 
    request = prompt.format(context=context.strip(), question=query)

    #print("\n\nPrompt AFTER formatting:\n", request)
    print("\n\nUser question: ", query)
    print("\nAI Response: \n")

    response = ''
    async for chunk in stream_llm_responses(llm, request):
        print(chunk, end="")
        response += chunk
    return response

# Main function to perform retrieval-augmented generation
async def retrieval_augmented_generation(hash_map, retrieval_method):
    # Setup LLM
    OPENAI_API_QUERY_KEY = os.environ["OPENAI_API_QUERY_KEY"]
    query_llm = ChatOpenAI(
        openai_api_key=OPENAI_API_QUERY_KEY,
        model_name="gpt-4o",
        temperature=0.0,
        streaming=True
    )

    # Define prompt template
    prompt = PromptTemplate(
        input_variables=["context", "question"], 
        template=MULTIPLE_REFERENCES_RESPONSE_TEMPLATE_V2
    )

    # print("\n\nPrompt BEFORE formatting:\n", prompt)
    while True:
        query = input("\n\nPlease enter your query:\n>>> ")
        if query.lower() == "quit":
            break
        if query.strip() == '':
            continue

        if retrieval_method == RetrievalMethod.VECTOR_DB:
            retriever = get_openai_retriever()
        elif retrieval_method == RetrievalMethod.BM25:
            retriever = get_bm25_retriever(hash_map)
        await handle_query(query, retriever, retrieval_method, prompt, query_llm, hash_map)

# Define the async function to run the main logic
async def main():
    # Choose the retrival method 
    #retrieval_method = RetrievalMethod.VECTOR_DB
    retrieval_method = RetrievalMethod.BM25

    file_path = os.path.dirname(os.path.realpath(__file__))
    input_file = os.path.join(file_path, "..", "processed_rai_hash_map.json") 
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    await retrieval_augmented_generation(data, retrieval_method)

# Run the main function
asyncio.run(main())
