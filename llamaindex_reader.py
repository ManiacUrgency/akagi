import fitz  # PyMuPDF
import openai
import os
import json
import tempfile
import requests
import mimetypes
import re
from llama_index.core import SimpleDirectoryReader

def query_openai_for_definition(text, term="Responsible Artificial Intelligence"):
    from langchain_openai import ChatOpenAI
    from langchain.prompts import PromptTemplate

    PROMPT_TEMPLATE = """
    Task:
    Please analyze the following text from a research paper and identify how the author defines "Responsible AI." The definition should be described through related concepts such as privacy, accountability, fairness, etc. Provide a nuanced, concise, and detailed five to six sentence summary of the author's definition of "Responsible AI." Refer to the following example output.

    <<Example Output>>
    ```
    The authors define \"Responsible AI\" through a systematic, value-driven approach emphasizing principles such as Fairness, Transparency, Accountability, Reliability and Safety, Privacy and Security, and Inclusiveness. They propose that the means to achieve Responsible AI consist of developing Socially Responsible AI Algorithms, and the objective is to enhance both AI's capabilities and its benefits to society. The framework, inspired by Carroll\u2019s Pyramid of Corporate Social Responsibility, categorizes AI responsibilities into functional, legal, ethical, and philanthropic, thereby ensuring a holistic and multidimensional perspective on AI's social responsibilities. Functional responsibilities require AI systems to perform in a manner consistent with profits maximization, operating efficiency, and other key performance indicators. Legal responsibilities require AI systems to at least meet the minimal legal requirements. Ethical responsibilities are the obligation to do what is right, just, and fair, and to prevent or mitigate negative impact on stakeholders (e.g., users, the environment). Philanthropic responsibilities, expect AI systems to be good AI citizens and to contribute to tackling societal challenges such as cancer and climate change.
    ```

    Text:
    {text}

    Only return the definition.

    """
    prompt = PromptTemplate(
        input_variables=["term", "text"], 
        template=PROMPT_TEMPLATE
    )

    request = prompt.format(term=term, text=text)

    OPENAI_API_QUERY_KEY = os.environ["OPENAI_API_QUERY_KEY"]
    query_llm = ChatOpenAI(
        openai_api_key=OPENAI_API_QUERY_KEY,
        model_name='gpt-4o',
        temperature=1.0,
        streaming=True
    )
    response = query_llm.invoke(request)
    print("\n\n\nresponse:", response, "\n\n")
    response = response.content
    return response

def download_pdf(url):
    response = requests.get(url)
    if response.status_code == 200:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_file.write(response.content)
        temp_file.close()
        return temp_file.name
    else:
        raise Exception(f"Failed to download PDF. Status code: {response.status_code}")

def extract_text_from_pdf(pdf_path, num_pages=7):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(min(num_pages, len(document))):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

def extract_text_from_url(pdf_url, num_pages=5):
    pdf_path = download_pdf(pdf_url)
    text = extract_text_from_pdf(pdf_path, num_pages)
    os.remove(pdf_path)
    return text

def process_pdf(pdf_url, term):
    text = extract_text_from_url(pdf_url)
    author_title_def = query_openai_for_definition(text, term)
    
    return author_title_def

def is_pdf_url(url):
    response = requests.head(url, allow_redirects=True)
    content_type = response.headers.get('Content-Type')
    if content_type == 'application/pdf':
        return True
    return False

def process_documents(documents, term="Responsible Artificial Intelligence"):
    papers = {
        "documents": []
    }
    for i, doc in enumerate(documents):
        match = re.search(r'^(.*?),\s*(https?://\S+)$', doc)
        if match:
            title = match.group(1)
            url = match.group(2)

            print("\ntitle: ", title)
            print("\ntitle type: ", type(title))
            print("\nurl: ", url)
            print("\nurl type: ", type(url)) 
        
        if is_pdf_url(url):
            definition = process_pdf(url, term)
        else:
            definition = "Not a PDF document"
        
        papers["documents"].append({
        "id" : str(i),
        "name": title,
        "URL": url,
        "answer": definition
      })
        
    print("\n\n papers: ", papers)
    print("papers type: ", type(papers))
    return papers

def main(input_dir, output_json, term="Responsible Artificial Intelligence"):
    # Read all documents using SimpleDirectoryReader
    reader = SimpleDirectoryReader(input_dir=input_dir, recursive=True)
    documents = reader.load_data()
    documents = documents[0].text.split("\n")
    print("documents: ", documents)  
    # Process the documents
    papers = process_documents(documents, term)
    
    # Write the results to a JSON file
    with open(output_json, 'w') as outfile:
        json.dump(papers, outfile, indent=4)

# Directory Path
file_path = os.path.dirname(os.path.realpath(__file__))
input_dir = file_path + "/responsible_ai_research_papers"
output_json = "definitions.json"
main(input_dir, output_json)
