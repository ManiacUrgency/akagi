import os
import json
from prompt_templates.distiller_constants import *

def get_definition(keyword):
    print("\n\n keyword: ", keyword, "\n\n") 
    from langchain_openai import ChatOpenAI

    OPENAI_API_QUERY_KEY = os.environ.get("OPENAI_API_QUERY_KEY")
    if not OPENAI_API_QUERY_KEY:
        raise ValueError("OPENAI_API_QUERY_KEY environment variable is not set")

    query_llm = ChatOpenAI(
        openai_api_key=OPENAI_API_QUERY_KEY,
        model_name='gpt-4o',
        temperature=1.0,
    )

    from langchain.prompts import PromptTemplate

    keyword_definition_prompt = PromptTemplate(
        input_variables=["documents", "keyword"], 
        template=KEYWORD_DEFINITION_TEMPLATE
    )
    
    json_file_path = f'output_definitions_json/{keyword}_definitions.json'
    print(f"Reading from {json_file_path}")

    # Check if the file exists
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"{json_file_path} does not exist")

    with open(json_file_path, 'r') as file:
        doc_data = json.load(file)

    documents = '\n'
    for document in doc_data['documents']:
        document_id = document['id']
        document_name = document['name']
        document_url = document['URL']
        answer = document['answer']
        documents += "<Document>\n"
        documents += "\t<Name>" + document_name + "</Name>\n"
        documents += "\t<Answer>" + answer + "</Answer>\n"
        documents += "</Document>\n"

    try:
        print("\n\n\n documents: ", documents, "\n\n\n")
        print("document type: ", type(documents))
        print("keyword: ", keyword)
        print("keyword type: ", type(keyword))
        print("Template being used: ", KEYWORD_DEFINITION_TEMPLATE)
        request = keyword_definition_prompt.format(documents=documents, keyword=keyword)
        print("Formatted request: ", request)
    except Exception as e:
        print("Error in formatting request:", e)
        raise

    response_keyword = query_llm.invoke(request)
    
    # Output the result as a JSON object
    output = {
        "keyword": keyword,
        "definition": response_keyword.content
    }
    
    # Ensure the output directory exists
    output_dir = "output_json"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save the JSON object to a file
    output_json_path = os.path.join(output_dir, f"{keyword}_definition.json")
    with open(output_json_path, 'w') as outfile:
        json.dump(output, outfile, indent=4)

def main():
    with open("output_csv/keywords.csv", 'r') as file:
        keywords = file.read()
        keyword_list = keywords.split(",")
    
    for keyword in keyword_list:
        get_definition(keyword)

main()
