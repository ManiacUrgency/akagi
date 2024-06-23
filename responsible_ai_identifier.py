import fitz  # PyMuPDF
import openai
import os
import json
import tempfile
import requests
import csv
from reader_constants import *

# Common headers to mimic a browser request
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

def query_openai_for_definition(text, term):
    from langchain_openai import ChatOpenAI
    from langchain.prompts import PromptTemplate
    
    prompt = PromptTemplate(
        input_variables=["term", "text"], 
        template=DEFAULT_TEMPLATE
    )

    request = prompt.format(term=term, text=text)

    OPENAI_API_QUERY_KEY = os.environ["OPENAI_API_QUERY_KEY"]
    query_llm = ChatOpenAI(
        openai_api_key=OPENAI_API_QUERY_KEY,
        model_name='gpt-4o',
        temperature=1.0,
        streaming=True
    )
    print("Sending request to OpenAI for definition extraction.")
    response = query_llm.invoke(request)
    print("\n\n\nResponse from OpenAI:", response, "\n\n")
    response = response.content
    return response

def download_pdf(url):
    print(f"Downloading PDF from URL: {url}")
    
    session = requests.Session()
    session.headers.update(HEADERS)
    
    try:
        print(f"Request headers: {session.headers}")
        # Make a request to get cookies
        initial_response = session.get(url)
        print(f"Initial response status code: {initial_response.status_code}")
        print(f"Initial response headers: {initial_response.headers}")
        print(f"Initial response cookies: {initial_response.cookies}")
        
        # Now make the request to download the PDF
        response = session.get(url, stream=True)
        response.raise_for_status()
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_file.write(response.content)
        temp_file.close()
        print(f"PDF downloaded and saved to: {temp_file.name}")
        return temp_file.name
    except requests.exceptions.RequestException as e:
        print(f"Failed to download PDF from URL: {url}. Error: {e}")
        print(f"Response content: {initial_response.content}")
        raise Exception(f"Failed to download PDF. Status code: {initial_response.status_code}")

def extract_text_from_pdf(pdf_path, num_pages=7):
    print(f"Extracting text from PDF: {pdf_path}")
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(min(num_pages, len(document))):
        page = document.load_page(page_num)
        text += page.get_text()
    print(f"Extracted text from first {num_pages} pages of the PDF.")
    return text

def extract_text_from_url(pdf_url, num_pages=5):
    pdf_path = download_pdf(pdf_url)
    text = extract_text_from_pdf(pdf_path, num_pages)
    os.remove(pdf_path)
    print(f"Temporary PDF file removed: {pdf_path}")
    return text

def process_pdf(pdf_url, term):
    print(f"Processing PDF URL: {pdf_url}")
    text = extract_text_from_url(pdf_url)
    author_title_def = query_openai_for_definition(text, term)
    return author_title_def

def process_documents(documents, term, prompt):
    papers = {
        "documents": []
    }
    for i, doc in enumerate(documents):
        doc = doc.strip()  # Remove any leading/trailing whitespace
        print(f"\nProcessing line {i+1}: {doc}")
        try:
            reader = csv.reader([doc])
            for row in reader:
                if len(row) != 2:
                    print(f"Skipping line {i+1}: Invalid format {row}")
                    i -= 1
                    continue
                title, url = row[0].strip(), row[1].strip()

                print(f"Title: {title}")
                print(f"URL: {url}")

                try:
                    definition = process_pdf(url, term)
                    papers["documents"].append({
                        "id": str(i),
                        "name": title,
                        "URL": url,
                        "answer": definition
                    })
                except Exception as e:
                    print(f"Error processing URL: {url}, error: {e}")
                    print(f"Skipping line {i+1}")
        except Exception as e:
            print(f"Error processing line {i+1}: {e}")

    print("\n\nFinal papers data structure: ", papers)
    return papers

def main(input_dir, output_json, term):
    file_path = os.path.dirname(os.path.realpath(__file__))
    csv_path = os.path.join(file_path, input_dir, "papers_on15pages.csv")
    print(f"Reading CSV file from path: {csv_path}")
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        documents = list(reader)
    
    formatted_documents = []
    for row in documents:
        formatted_documents.append(', '.join(row))
    
    print("Documents extracted from CSV: ", formatted_documents)
    
    # Process the documents
    papers = process_documents(formatted_documents, term, prompt)
    
    # Write the results to a JSON file
    with open(output_json, 'w') as outfile:
        json.dump(papers, outfile, indent=4)
    print(f"Results written to JSON file: {output_json}")

# Directory Path
input_dir = "responsible_ai_research_papers"

output_json = "output_definitions_json/responsible_ai_definitions.json"
main(input_dir, output_json, term="Responsible Artificial Intelligence")
