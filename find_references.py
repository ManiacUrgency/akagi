import os
import json

def get_id_to_title_map(reference_hash_map):
    id_to_title = {}
    for paper in reference_hash_map["papers"]:
        id_to_title[paper['id']] = paper['paper_title']
    return id_to_title

file_path = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(file_path, "papers_reference_check.txt") 

input_reference_json_file = os.path.join(file_path, "processed_rai_definitions.json") 
with open(input_reference_json_file, "r") as file:
    reference_hash_map = json.load(file)  

id_to_title_map = get_id_to_title_map(reference_hash_map)

with open(input_file, "r") as file:
    content = file.read()
    count = 0
    for number in range(1, 64):
        try:
            title = id_to_title_map[number]
        except:
            title = "<Not in processed_rai_definitions.json>"

        pattern = f"[{number}]"
        if pattern in content:
            print(f"YES [{number}] ", title)
        else:
            print(f"NO  [{number}] ", title)
            count += 1

print("number of no references: ", count)
print("number of references:", 63 - count)