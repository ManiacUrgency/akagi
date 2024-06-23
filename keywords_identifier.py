import os
from responsible_ai_definitions import main
from reader_constants import *

'''
Gets the definition of each keyword per every Responsible AI related research paper that was used to generate the broad definition of Responsible AI.
'''
input_dir = "responsible_ai_research_papers"

with open("output_csv/keywords.csv", 'r') as file:
    keywords = file.read()
    keyword_list = keywords.split(",")

for word in keyword_list:
    prompt = KEYWORD_DEFINITION_TEMPLATE
    output_json = "output_definitions_json/" + word + "_definitions.json"
    main(input_dir, output_json, word, prompt)
