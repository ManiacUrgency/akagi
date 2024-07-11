import json
import os
from uuid import uuid4
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from pinecone import ServerlessSpec
from tqdm.auto import tqdm
from research_paper_reference_generator import main as reference_generator_main

def initialize_openai_embeddings(model_name, api_key):
    return OpenAIEmbeddings(model=model_name, openai_api_key=api_key)

def initialize_pinecone(api_key, index_name):
    pc = Pinecone(api_key=api_key)

    try:
        pc.describe_index(index_name)
    except:
        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=3072,
                metric="cosine",
                spec=ServerlessSpec(    
                    cloud='aws', 
                    region='us-west-2'
                ) 
            ) 

    return pc.Index(index_name)

def create_and_upsert_embedding(text, metadata, embed, index):
    embedding_id = str(uuid4())
    embeds = embed.embed_documents([text])
    metadata["id"] = embedding_id
    metadata["text_snippet"] = " ".join(text.split()[:50])  # Add first 50 words to metadata
    index.upsert(vectors=[(embedding_id, embeds[0], metadata)], namespace = "explainable_ai")
    print(f"Embedding created and upserted for ID: {embedding_id}")
    return embedding_id

def process_json_and_create_embeddings(json_file, embed, index, hash_map):
    with open(json_file, "r") as file:
        data = json.load(file)

    reference_data = data["paper_title"] + data["authors"] + data["publication_info"] + data["publication_year"] + data["url"]
    reference = reference_generator_main(reference_data).content

    print("\n\nAI Generated Reference: \n\n", reference, "\n\n")

    paper_data = {
        "paper_title": data["paper_title"],
        "authors": data["authors"],
        "publication_info": data["publication_info"],
        "paper_url": data["url"],
        "chunks": []
    }
    
    for heading in tqdm(data["headings"]):

        if heading["title"].lower() == "references":
            continue
        
        title = heading["title"]
        text = heading["text"]
        metadata = {
            "paper_title": data["paper_title"],
            "authors": data["authors"],
            "publication_info": data["publication_info"],
            "publication_year": data["publication_year"],
            "paper_url": data["url"],
            "heading_title": title,
        }

        
        chunk_id = create_and_upsert_embedding(text, metadata, embed, index)
        paper_data["chunks"].append({"id": chunk_id, "text": text, "reference": reference})
    
    hash_map["papers"].append(paper_data)

def main():
    # Environment Variables
    OPENAI_API_KEY = os.environ["OPENAI_API_EMBEDDINGS_KEY"]
    PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]

    # Initialize OpenAI embeddings
    model_name = "text-embedding-3-large"
    embed = initialize_openai_embeddings(model_name, OPENAI_API_KEY)

    # Initialize Pinecone
    index_name = "research-papers"
    index = initialize_pinecone(PINECONE_API_KEY, index_name)

    # Read existing hash map from JSON file
    if os.path.exists("xai_hash_map.json"):
        try:
            with open("xai_hash_map.json", "r") as infile:
                content = infile.read().strip()
                if content:
                    hash_map = json.loads(content)
                else:
                    hash_map = {"papers": []}
        except (json.JSONDecodeError, ValueError):
            # Handle empty or malformed JSON file
            hash_map = {"papers": []}
    else:
        hash_map = {"papers": []}

    # Process JSON and create embeddings
    json_file_path = "headings_with_text.json"
    process_json_and_create_embeddings(json_file_path, embed, index, hash_map)

    # Save updated hash map to JSON file
    with open("xai_hash_map.json", "w") as outfile:
        json.dump(hash_map, outfile, indent=4)
