import os
import json
from research_paper_distiller import main
from prompt_templates.reader_constants import *

prompt = DEFAULT_TEMPLATE
term = "Responsible Artificial Intelligence"
input_dir = "responsible_ai_research_papers"
output_json = "output_definitions_json/responsible_ai_keywords.json"
# main(input_dir, output_json, term, prompt)

def extract_and_store_answers_from_file(file_path, output_path):
    # Read the JSON data from the file
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Extract the "answer" key from each document
    answers = [doc['answer'] for doc in data['documents']]
    
    concatenated_answers = ' '.join(answers)

    from langchain_openai import ChatOpenAI
    from langchain.prompts import PromptTemplate
    
    prompt = PromptTemplate(
        input_variables=["term", "text"], 
        template=DEFAULT_TEMPLATE
    )

    request = prompt.format(term=term, text=concatenated_answers)

    OPENAI_API_QUERY_KEY = os.environ["OPENAI_API_QUERY_KEY"]
    query_llm = ChatOpenAI(
        openai_api_key=OPENAI_API_QUERY_KEY,
        model_name='gpt-4o',
        temperature=1.0,
        streaming=True
    )
    print("Sending request to OpenAI for definition extraction.")
    response = query_llm.invoke(request)
    print("\n\n\nResponse from OpenAI:", response, "\n\n")
    response_content = response.content

    # Save the response in JSON format
    output_data = {
        "term": term,
        "response": response_content
    }
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as outfile:
        json.dump(output_data, outfile, indent=4)

# Example usage
file_path = os.path.dirname(os.path.realpath(__file__)) + '/output_definitions_json/responsible_ai_keywords.json'
output_path = 'output_json/responsible_ai_keywords.json'
extract_and_store_answers_from_file(file_path, output_path)
