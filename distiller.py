import os
import json
from distiller_constants import *

from langchain_openai import ChatOpenAI

OPENAI_API_QUERY_KEY = os.environ["OPENAI_API_QUERY_KEY"]
query_llm = ChatOpenAI(
    openai_api_key=OPENAI_API_QUERY_KEY,
    model_name='gpt-4o',
    temperature=1.0,
)

from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["documents"], 
    template=DEFAULT_TEMPLATE
)

# Read the json file "example_docs_data.json" from the local directory
with open('definitions.json', 'r') as file:
    doc_data = json.load(file)
#print(json.dumps(doc_data, indent=4))

documents = '\n';
for document in doc_data['documents']:
    document_id = document['id']
    document_name = document['name']
    document_url = document['URL']
    answer = document['answer']
    documents += "<Document>\n";
    documents += "\t<Name>" + document_name + "</Name>\n"
    documents += "\t<Answer>" + answer + "</Answer>\n"
    documents += "</Document>\n";

request = prompt.format(documents=documents)
print(request)

response = query_llm.invoke(request)
print(f"<Response>\n{response.content}\n</Response>")
