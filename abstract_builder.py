import os
import json
from prompt_templates.abstract_constants import *
from prompt_templates.subpillar_constants import *

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
        input_variables=["definitions", "keywords"], 
        template=DEFINITION_GENERATION_PROMPT
    )

    abstract_prompt = PromptTemplate(
        input_variables=["definition"], 
        template=ABSTRACT_GENERATION_TEMPLATE
    ) 

    all_definitions = ''

    # Traverse the directory recursively and read all JSON files
    for root, _, files in os.walk('output_json'):
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    doc_data = json.load(file)
                    definition = doc_data['definition']
                    all_definitions += definition + "\n===\n"
    #Get keyworsd
    with open("output_csv/keywords.csv", 'r') as file:
        keywords = file.read()
    # Get the definition
    request = definition_prompt.format(definitions=all_definitions, keywords=keywords)
    print("\n\nprompt: ", request, "\n\n")
    response_definition = query_llm.invoke(request)
    
    request = abstract_prompt.format(definition=response_definition)
    abstract = query_llm.invoke(request)
    # Ensure the output directory for text file exists
    output_text_dir = "output_text"
    if not os.path.exists(output_text_dir):
        os.makedirs(output_text_dir)

    # Save the definition to a text file
    definition_text_path = os.path.join(output_text_dir, "definition_consensus.txt")
    with open(definition_text_path, 'w') as file:
        file.write(abstract.content)

main()
