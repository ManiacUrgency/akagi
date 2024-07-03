import os
from prompt_templates.reference_generator_constants import *
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

def main(reference_data):
    OPENAI_API_QUERY_KEY = os.environ.get("OPENAI_API_QUERY_KEY")

    query_llm = ChatOpenAI(
        openai_api_key=OPENAI_API_QUERY_KEY,
        model_name='gpt-4o',
        temperature=1.0,
    )

    from langchain.prompts import PromptTemplate

    prompt = PromptTemplate(
        input_variables=["reference_data"], 
        template=DEFAULT_TEMPLATE
    )

    request = prompt.format(reference_data = reference_data)
    reference = query_llm.invoke(request)

    print(reference)
    return reference

# reference_data = "Explainable Artificial Intelligence (XAI): Concepts, taxonomies, opportunities and challenges toward responsible AI" + "AB Arrieta, N D\u00edaz-Rodr\u00edguez, J Del Ser, A Bennetot\u2026" + "Information fusion - Elsevier" + "2020" + "https://arxiv.org/pdf/1910.10045"
# main(reference_data)