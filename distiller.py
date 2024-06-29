import os
import json
import csv
from prompt_templates.distiller_constants import *
'''
This script is supposed to generate a synthesize definition of Responsible AI along with identifying the "keywords" or subpillars
used to define Responsible AI.

***This script needs to be split into two scripts one defining the other identifying. A new prompt needs to be crafted.***
'''
def main():
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

    definition_prompt = PromptTemplate(
        input_variables=["documents"], 
        template=DEFAULT_TEMPLATE
    )

    keyword_identifier_prompt = PromptTemplate(
        input_variables=["documents"], 
        template=KEYWORD_TEMPLATE
    )

    # Read the JSON file "responsible_ai_definitions.json" from the local directory
    with open('output_definitions_json/responsible_ai_definitions.json', 'r') as file:
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

    # Get the definition
    request = definition_prompt.format(documents=documents)
    response_definition = query_llm.invoke(request)

    # Ensure the output directory for JSON exists
    output_json_dir = "output_json"
    if not os.path.exists(output_json_dir):
        os.makedirs(output_json_dir)

    # Save the definition to a JSON file
    definition_json_path = os.path.join(output_json_dir, "definition_consensus.json")
    with open(definition_json_path, 'w') as file:
        json.dump({"definition": response_definition.content}, file, indent=4)

    # Get the keywords
    request = keyword_identifier_prompt.format(documents=documents)
    response_keyword = query_llm.invoke(request)

    # Ensure the output directory for CSV exists
    output_csv_dir = "output_csv"
    if not os.path.exists(output_csv_dir):
        os.makedirs(output_csv_dir)

    # Write the keywords to a CSV file
    keywords_csv_path = os.path.join(output_csv_dir, "keywords.csv")
    with open(keywords_csv_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Keywords"])
        writer.writerow([response_keyword.content])

main()
