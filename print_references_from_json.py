import json
import re

def remove_retrieval_info(text):
    # Regex pattern to match "Retrieved from" and everything after it
    pattern = r'Retrieved from.*$'
    # Replace the pattern with an empty string
    cleaned_text = re.sub(pattern, '', text).strip()
    return cleaned_text

def process_json_file(input_file_path, output_file_path):
    # Read the JSON file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    text = ''
    for paper in data['papers']:
        reference = "[" + str(paper['id']) + "] " + paper['reference']
        reference = remove_retrieval_info(reference)
        text += reference + "\n"
    # Write the cleaned data back to the output JSON file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(text)

# Specify the path to the JSON file
input_file_path = 'processed_rai_definitions.json'
output_file_path = 'references.txt'
process_json_file(input_file_path, output_file_path)