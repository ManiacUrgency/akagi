import os
import json
import asyncio
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

from prompt_templates.query_constants import *

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
def setup_retriever(vectorstore):
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "namespace": "explainable_ai",
            "k": 10
        }
    )
    return retriever

# Function to retrieve the full text using the id from the hash map
def get_text_by_id(chunk_id, hash_map):
    for paper in hash_map["papers"]:
        for chunk in paper["chunks"]:
            if chunk["id"] == chunk_id:
                text = "<text> " + chunk["text"] + "</text>\n<reference>" + chunk["reference"] + "</reference>"

                print("\nDOCUMENT:\n", text)
                return text
    return ""

# Function to handle queries
async def handle_query(query, retriever, prompt, llm, hash_map):
    id_and_metadata_dict = retriever.invoke(query)

    print("\n\nId and Metadata: ", id_and_metadata_dict, "\n\n")
    
    context = ""

    for doc in id_and_metadata_dict:
        chunk_id = doc.page_content
        if chunk_id:
            text = get_text_by_id(chunk_id, hash_map)
            if text:
                # print("\nDOUCMENT:\n", text)
                context += text + "\n"

    
    request = prompt.format(context=context.strip(), question=query)
    print("\n\nPrompt AFTER formatting:\n", request)

    print("\n\n\nAI Response: \n")
    response = ''
    async for chunk in stream_llm_responses(llm, request):
        print(chunk, end="")
        response += chunk
    return response

# Main function to perform retrieval-augmented generation
async def retrieval_augmented_generation(hash_map):
    # Initialize OpenAI embeddings
    OPENAI_API_EMBEDDINGS_KEY = os.environ["OPENAI_API_EMBEDDINGS_KEY"]
    embed = initialize_openai_embeddings("text-embedding-3-large", OPENAI_API_EMBEDDINGS_KEY)

    # Initialize Pinecone
    PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
    index_name = "research-papers"  # Ensure this matches the index used in the embedding script
    text_field = "id"  # Updated to reflect the changes in metadata
    
    index = initialize_pinecone(PINECONE_API_KEY, index_name)
    vectorstore = PineconeVectorStore(index, embed, text_field)

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
        template=MULTIPLE_REFERENCES_RESPONSE_TEMPLATE
    )

    print("\n\nPrompt BEFORE formatting:\n", prompt)
    while True:
        query = input("\n>>> ")
        if query.lower() == "quit":
            break
        
        retriever = setup_retriever(vectorstore)
        
        response = await handle_query(query, retriever, prompt, query_llm, hash_map)

# Define the async function to run the main logic
async def main():
    file_path = os.path.dirname(os.path.realpath(__file__))
    json_file_path = file_path + "/xai_hash_map.json"
    with open(json_file_path, "r") as file:
        hash_map = json.load(file)
    await retrieval_augmented_generation(hash_map)

# Run the main function
asyncio.run(main())
