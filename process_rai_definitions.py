import json
import re

def remove_bracketed_numbers(text):
    # Regex pattern to match single numbers or comma-separated lists of numbers enclosed in square brackets
    pattern = r'\[\d+(,\s*\d+)*\]'
    # Replace the pattern with an empty string
    cleaned_text = re.sub(pattern, '', text).strip()
    return cleaned_text


def remove_spaces_tabs_bracketed_numbers(text):
    # Regex pattern to match single numbers or comma-separated lists of numbers enclosed in square brackets
    pattern = r"\n\t\n\t\[1\]"
    # Replace the pattern with an empty string
    cleaned_text = re.sub(pattern, '', text).strip()
    return cleaned_text

def remove_reference(text):
    pattern = r"(\n\t\n\t\[1\] .*)"
    # Find the reference section
    match = re.search(pattern, text)
    reference = ''
    if match:
        # Extract the reference section
        reference = match.group(1)
        reference = remove_spaces_tabs_bracketed_numbers(reference)
        # Remove the reference section from the text
        text = text[:match.start()].rstrip()
    #print("text:", text, "\n\nreference:" , reference , "\n\n")
    return text, reference

def process_json_file(input_file_path, output_file_path):
    # Read the JSON file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Iterate over each paper and its chunks
    for paper in data['papers']:
        paper['rai_definition_1'], reference  = remove_reference(paper['rai_definition_1']) 
        paper['reference'] = reference 
        paper['rai_definition_1'] = remove_bracketed_numbers(paper['rai_definition_1'])

    # Write the cleaned data back to the output JSON file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Specify the path to the JSON file
input_file_path = 'rai_definitions.json'
output_file_path = 'processed_rai_definitions.json'
process_json_file(input_file_path, output_file_path)
