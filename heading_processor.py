import os
import json
from collections import Counter
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from prompt_templates.heading_processing_constants import *

# Function to log debug messages
DEBUG_FILE = 'debug_log.txt'

def log_debug(message):
    with open(DEBUG_FILE, 'a') as f:
        f.write(message + '\n')

def log_separator():
    log_debug("\n" + "-"*80 + "\n")

# Function to read JSON data from a file
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to organize headings using OpenAI API
def organize_headings_with_openai(data):

    # Extract headings and combine them into a single string
    all_headings = "\n".join(data["headings"])
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    query_llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model_name='gpt-4',
        temperature=0.5,
        streaming=False
    )

    numbering_headings_template = PromptTemplate(
        input_variables=["titles"], 
        template=NUMBER_HEADINGS_TEMPLATE
    )

    # print("\nall headings:\n", all_headings) 
    print("\nall headings type:\n", type(all_headings))
    
    numbering_headings_prompt = numbering_headings_template.format(titles = all_headings)
    numbered_headings = query_llm.invoke(numbering_headings_prompt)

    print("\n\n\nresponse:\n", numbered_headings.content.strip())
    print("\n\n\nresponse type:\n", type(numbered_headings.content))

    numbered_headings = numbered_headings.content.strip()

    process_headings_template = PromptTemplate(
        input_variables=["titles"], 
        template=DEFAULT_TEMPLATE
    )    

    process_headings_prompt = process_headings_template.format(titles = numbered_headings)

    processed_headings = query_llm.invoke(process_headings_prompt)

    print("\n\n\nresponse:\n", processed_headings.content.strip())
    print("\n\n\nresponse type:\n", type(processed_headings.content))
    log_debug("Response from OpenAI: " + processed_headings.content.strip())

    processed_headings = processed_headings.content.strip()

    # Validate response content before parsing
    if not response_content:
        log_debug("Error: Received empty response from OpenAI.")
        log_separator()
        return []

    # Remove the delimiters and the JSON identifier
    response_content = response_content.replace("```json", "").replace("```", "").strip()

    # Ensure response content is enclosed in a JSON array
    if response_content.startswith('{') and not response_content.startswith('['):
        response_content = f'[{response_content}]'

    # Parse the response as JSON
    try:
        organized_headings = json.loads(response_content)
    except json.JSONDecodeError as e:
        log_debug(f"Error parsing JSON response: {e}")
        organized_headings = []

    log_separator()
    return organized_headings

# Function to write organized headings to a JSON file
def write_organized_headings_to_json(organized_headings, output_file):
    with open(output_file, 'w') as file:
        json.dump(organized_headings, file, indent=4)

# Main function
def main():
    file_path = os.path.dirname(os.path.realpath(__file__))
    # Clear the debug log file
    if os.path.exists(DEBUG_FILE):
        os.remove(DEBUG_FILE)

    # Path to JSON file
    json_file_path = file_path + '/headings.json'  # JSON with the provided format

    # Read JSON data from file
    data = read_json(json_file_path)

    # Organize headings using OpenAI API
    organized_headings = organize_headings_with_openai(data)

    # Write organized headings to JSON file
    output_file = file_path + '/organized_headings.json'
    write_organized_headings_to_json(organized_headings, output_file)

    print("Organized headings have been written to organized_headings.json")
    print(f"Debug logs have been written to {DEBUG_FILE}")

if __name__ == "__main__":
    main()
