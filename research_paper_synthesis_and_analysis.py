import os
import json
import asyncio
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

from prompt_templates.research_analysis_constants import *
from prompt_templates.query_constants import *
from prompt_templates.analysis_classification_constants import *

# Asynchronous function to stream LLM responses
async def stream_llm_responses(llm, request):
    async for chunk in llm.astream(request):
        yield chunk.content.replace("\n", "\n\t")

# Function to handle queries
async def handle_query(query_prompt, llm, context):
    print("context:\n\n", context)

    query_request = query_prompt.format(definitions = context)
    # query_request = query_prompt.format(context = context, question = analysis_prompt)
    print("\n\n\n---------------------------------------------QUERY REQUEST START---------------------------------------------\n\n\n", query_request)
    print("\n\n\n---------------------------------------------QUERY REQUEST END---------------------------------------------\n\n\n")
        
    response = ""
    print("\n\n\nAI Response: \n")
    # async for chunk in stream_llm_responses(llm, query_request):
    #     print(chunk, end="")
    #     response += chunk
    
    return response

# Main function to perform retrieval-augmented generation
async def retrieval_augmented_generation(input_json_file_path, output_txt_file_path):
    with open(input_json_file_path, "r") as file:
        definitions = json.load(file)

        context = ""
        for i, paper in enumerate(definitions["papers"]):
            context += "Definition " + str(i + 1) + ": " + paper["rai_definition_1"] + "\n\n"

        OPENAI_API_QUERY_KEY = os.environ["OPENAI_API_QUERY_KEY"]
        query_llm = ChatOpenAI(
            openai_api_key=OPENAI_API_QUERY_KEY,
            model_name="gpt-4o",
            temperature=0.0,
            streaming=True
        )

        # Define prompt template
        # query_prompt = PromptTemplate(
        #     input_variables=["context", "question"], 
        #     template=MULTIPLE_REFERENCES_RESPONSE_TEMPLATE
        # )

        query_prompt = PromptTemplate(
            input_variables=["definitions"], 
            template=FRAMEWORK_CLASSIFICATION
        ) 
        # thematic_prompt = THEMATIC_ANALYSIS_TEMPLATE

        response = await handle_query(query_prompt, query_llm, context)

        with open(output_txt_file_path, "w") as file:
            file.write(response)
        # comparative_prompt = COMPARATIVE_ANALYSIS_TEMPLATE

        # comparative_response = await handle_query(comparative_prompt, query_prompt, query_llm, context)

        # opportunity_prompt = OPPORTUNITY_ANALYSIS_TEMPLATE

        # opporutnity_response = await handle_query(opportunity_prompt, query_prompt, query_llm, context)

        # output_json = {
        #     "thematic_analysis": thematic_response,
        #     "comparative_analysis": comparative_response,
        #     "opportunity_analysis": opporutnity_response

        # }

# Define the async function to run the main logic
async def main():
    file_path = os.path.dirname(os.path.realpath(__file__))
    input_json_file_path = file_path + "/rai_definitions.json"
    output_txt_file_path = file_path + "/output_analysis.txt"
    
    await retrieval_augmented_generation(input_json_file_path, output_txt_file_path)

# Run the main function
asyncio.run(main())
