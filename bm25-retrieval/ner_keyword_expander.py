import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import bm25_templates 

class NERKeywordExpander:
    def __init__(self):
        OPENAI_API_QUERY_KEY = os.environ["OPENAI_API_QUERY_KEY"]
        self.llm = ChatOpenAI(
            openai_api_key=OPENAI_API_QUERY_KEY,
            model_name="gpt-4o",
            temperature=0.0,
            streaming=True
        )

    async def query_llm(self, query):
        response = ''
        async for chunk in self.llm.astream(query):
            print(chunk.content, end="")
            response += chunk.content
        return response

    async def expand(self, input):
        prompt = PromptTemplate(
            input_variables=["input"], 
            template=bm25_templates.NER_KEYWORD_EXTRACT_TEMPLATE
        )

        request = prompt.format(input=input)

        print("\n\nPrompt AFTER formatting:\n", request)
        print("\n\nUser input: ", input)
        print("\n\nAI Response: \n")
        response = await self.query_llm(request)
        return response

