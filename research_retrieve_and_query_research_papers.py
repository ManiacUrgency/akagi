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
                text = "<text> " + chunk["text"] + "</text>\n<reference>" + chunk["reference"] + "</reference>"
                print("\nDOCUMENT:\n", text)
                return text
    return ""

# Function to handle queries
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
    
    request = prompt.format(context=context.strip(), question=question)
    print("\n\n\nAI Response: \n")
    response_text = ""
    async for chunk in stream_llm_responses(llm, request):
        response_text += chunk
        print(chunk, end="")
    
    return response_text

# Main function to perform retrieval-augmented generation
async def retrieval_augmented_generation(input_json_file, output_json_file):
    with open(input_json_file, "r") as file:
        hash_map = json.load(file)
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

    question = "How is Responsible AI conceptualized and defined in this research paper? If the paper provides an explicit definition of Responsible AI, describe it in detail. If no explicit definition is given, identify any conceptual frameworks or broader categories used to define Responsible AI. For instance, consider whether the paper classifies Responsible AI in terms of broader concepts such as competence/functionality (e.g., performance, usability, impact) and ethical considerations (e.g., explainability, safety). If the paper discusses sub-pillars, identify which sub-pillar is most prominently featured or emphasized and elaborate on how this primary sub-pillar contributes to a comprehensive understanding of Responsible AI. Briefly mention any secondary sub-pillars discussed, noting if multiple sub-pillars are given equal emphasis. Additionally, explain how the paper's focus on specific sub-pillars or broader conceptual frameworks might influence or shape its overall approach to Responsible AI. If the paper neither defines Responsible AI nor discusses relevant sub-pillars or frameworks, please state this clearly."
    
    # Initialize the output JSON file with an empty structure if it does not exist
    if not os.path.exists(output_json_file):
        with open(output_json_file, "w") as outfile:
            json.dump({"papers": []}, outfile, indent=4)
    
    # Read the existing content
    with open(output_json_file, "r") as infile:
        output_data = json.load(infile)

    with open(input_json_file, "r") as file:
        data = json.load(file)
        for paper in data["papers"]:
            paper_title = paper["paper_title"]
            retriever = setup_retriever(vectorstore, paper_title)
            
            response = await handle_query(question, retriever, prompt, query_llm, hash_map)

            output_data["papers"].append({
                "paper_title": paper_title,
                "rai_definition_1": response
            })
    
            with open(output_json_file, "w") as outfile:
                json.dump(output_data, outfile, indent=4)

# Define the async function to run the main logic
async def main():
    file_path = os.path.dirname(os.path.realpath(__file__))
    input_json_file = os.path.join(file_path, "processed_hash_map.json") 
    output_json_file = os.path.join(file_path, "rai_definitions.json")
    
    await retrieval_augmented_generation(input_json_file, output_json_file)

# Run the main function
asyncio.run(main())
