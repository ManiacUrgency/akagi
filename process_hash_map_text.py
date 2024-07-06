import json
import re

def remove_bracketed_numbers(text):
    # Regex pattern to match single numbers or comma-separated lists of numbers enclosed in square brackets
    pattern = r'\[\d+(,\s*\d+)*\]'
    # Replace the pattern with an empty string
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

def process_json_file(input_file_path, output_file_path):
    # Read the JSON file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Iterate over each paper and its chunks
    for paper in data['papers']:
        for chunk in paper['chunks']:
            chunk['text'] = remove_bracketed_numbers(chunk['text'])

    # Write the cleaned data back to the output JSON file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Specify the path to the JSON file
input_file_path = 'hash_map.json'
output_file_path = 'processed_hash_map.json'
process_json_file(input_file_path, output_file_path)
