import os
import json
import asyncio
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

from prompt_templates.query_constants import *

# Load the JSON hash map
with open("hash_map.json", "r") as file:
    hash_map = json.load(file)

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
def setup_retriever(vectorstore, paper_title):
    filter_request_json = {
            "paper_title": {"$eq": paper_title}
    }
    
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 6,
            "filter": filter_request_json
        }
    )
    return retriever

# Function to retrieve the full text using the id from the hash map
def get_text_by_id(chunk_id, hash_map):
    for paper in hash_map["papers"]:
        for chunk in paper["chunks"]:
            if chunk["id"] == chunk_id:
                text = chunk["text"] + "\n" + chunk["reference"]

                print("\nDOCUMENT:\n", text)
                return text
    return ""

# Function to handle queries
async def handle_query(question, retriever, prompt, llm):
    id_and_metadata_dict = retriever.invoke(question)

    print("\n\nId and Metadata: ", id_and_metadata_dict, "\n\n")
    
    context = ""

    for doc in id_and_metadata_dict:
        chunk_id = doc.page_content
        if chunk_id:
            text = get_text_by_id(chunk_id, hash_map)
            if text:
                context += text + "\n"
    
    
    request = prompt.format(context=context.strip(), question = question)
    
    print("\n\n\nAI Response: \n")
    async for chunk in stream_llm_responses(llm, request):
        print(chunk, end="")

# Main function to perform retrieval-augmented generation
async def retrieval_augmented_generation(pdf_file_path):
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
        input_variables=["context", "question"], 
        template=SINGLE_REFERENCE_RESPONSE_TEMPLATE
    )

    question = "How is Responsible AI conceptualized and defined in this research paper? If the paper does not provide an explicit definition of Responsible AI, does it discuss any sub-pillars of RAI? If so, which sub-pillar is most prominently featured or emphasized in the paper? Elaborate on how this primary sub-pillar contributes to a comprehensive understanding of Responsible AI, and briefly mention any secondary sub-pillars discussed. If multiple sub-pillars are given equal emphasis, please note this. Additionally, explain how the paper's focus on specific sub-pillar(s) might influence or shape its overall approach to Responsible AI. If the paper neither defines RAI nor discusses relevant sub-pillars, please state this clearly."

    retriever = setup_retriever(vectorstore, "Socially responsible ai algorithms: Issues, purposes, and challenges")
    await handle_query(question, retriever, prompt, query_llm)

    # with open(pdf_file_path, "r") as file:
    #     data = json.load(file)
    #     for paper in data["papers"]:
    #         paper_title = paper["paper_title"]
    #         retriever = setup_retriever(vectorstore, paper_title)
            
    #         await handle_query(retriever, prompt, query_llm)

# Define the async function to run the main logic
async def main():
    file_path = os.path.dirname(os.path.realpath(__file__))
    pdf_file_path = file_path + "hash_map.json"
    await retrieval_augmented_generation(pdf_file_path)

# Run the main function
asyncio.run(main())
