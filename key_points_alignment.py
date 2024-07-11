import os
import json
import asyncio
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

from prompt_templates.analysis_classification_constants import *

def initialize_openai_embeddings(model_name, api_key):
    return OpenAIEmbeddings(model=model_name, openai_api_key=api_key)

def initialize_pinecone(api_key, index_name):
    pc = Pinecone(api_key=api_key)
    index = pc.Index(index_name)
    return index

async def stream_llm_responses(llm, request):
    async for chunk in llm.astream(request):
        yield chunk.content.replace("\n", "\n\t")

def setup_retriever(vectorstore, paper_title):
    filter_request_json = {
        "paper_title": {"$eq": paper_title}
    }
    
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "namespace": "responsible_ai",
            "k": 10,
            #"filter": filter_request_json
        }
    )
    return retriever

def get_text_by_id(chunk_id, hash_map):
    for paper in hash_map["papers"]:
        for chunk in paper["chunks"]:
            if chunk["id"] == chunk_id:
                text = "<text> " + chunk["text"] + "</text>\n<reference>" + chunk["reference"] + "</reference>"
                print("\nDOCUMENT:\n", text)
                return text
    return ""

async def handle_query(question, retriever, prompt, llm, hash_map):
    id_and_metadata_dict = retriever.invoke(question)
    print("\n\nId and Metadata: ", id_and_metadata_dict, "\n\n")
    
    context = ""
    for doc in id_and_metadata_dict:
        chunk_id = doc.page_content
        if chunk_id:
            text = get_text_by_id(chunk_id, hash_map)
            if text:
                context += text + "\n"
    
    request = prompt.format(context=context.strip())
    print("\n\n\nAI Response: \n")
    response_text = ""
    async for chunk in stream_llm_responses(llm, request):
        response_text += chunk
        print(chunk, end="")
    
    return response_text

def get_id_to_title_map(reference_hash_map):
    id_to_title = {}
    for paper in reference_hash_map["papers"]:
        id_to_title[paper['id']] = paper['paper_title']
    return id_to_title

async def retrieval_augmented_generation(input_text_json_file, input_reference_json_file):
    with open(input_text_json_file, "r") as file:
        hash_map = json.load(file)

    with open(input_reference_json_file, "r") as file:
        reference_hash_map = json.load(file)    
    
    # Initialize OpenAI embeddings
    OPENAI_API_EMBEDDINGS_KEY = os.environ["OPENAI_API_EMBEDDINGS_KEY"]
    embed = initialize_openai_embeddings("text-embedding-3-large", OPENAI_API_EMBEDDINGS_KEY)

    # Initialize Pinecone
    PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
    index_name = "research-papers"
    text_field = "id"
    
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
        input_variables=["context"], 
        template=KEY_POINTS_ALIGNMENT_PROMPT
    )

    #question = "Functionality, Security, Legality, Fairness, Privacy, Transparency,  Explainability for Understandability, Sustainability, Truthfulness, Maintainability, Contestability, Auditability, Accountability"
    question = "governance"
    
    id_to_title_map = get_id_to_title_map(reference_hash_map)
    print(id_to_title_map, "\n\n")

    print("\n\nPrompt BEFORE formatting:\n", prompt)
    while True:
        print("\nPlease enter the id of the reference:")
        query = input("\n>>> ")
        if query.lower() == "quit":
            break

        paper_title = id_to_title_map[int(query.strip())].strip()
        print("Analyze paper: ", paper_title)
        retriever = setup_retriever(vectorstore, paper_title)
        
        await handle_query(question, retriever, prompt, query_llm, hash_map)


# Define the async function to run the main logic
async def main():
    file_path = os.path.dirname(os.path.realpath(__file__))
    input_text_json_file = os.path.join(file_path, "processed_hash_map.json") 
    input_reference_json_file = os.path.join(file_path, "processed_rai_definitions.json") 
    
    await retrieval_augmented_generation(input_text_json_file, input_reference_json_file)

# Run the main function
asyncio.run(main())