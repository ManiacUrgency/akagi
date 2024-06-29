import os
import json
import re
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from io import StringIO
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import tiktoken

# Define file paths
file_path = os.path.dirname(os.path.realpath(__file__))
pdf_path = os.path.join(file_path, 'XAI.pdf')
output_file = 'RAI_paper.json'
debug_file = 'RAI_extracted_text.txt'
cleaned_output_file_json = 'RAI_cleaned_paper.json'
cleaned_output_file_txt = 'RAI_cleaned_paper.txt'

# Create a string buffer
output_string = StringIO()

# Define layout analysis parameters
laparams = LAParams(
    line_overlap=0.5,
    char_margin=2.0,
    line_margin=0.5,
    word_margin=0.1,
    boxes_flow=0.5,
    detect_vertical=False,
    all_texts=False  # Set to False to ignore non-text elements
)

# Extract text
try:
    with open(pdf_path, 'rb') as fp:
        extract_text_to_fp(fp, output_string, laparams=laparams)
    extracted_text = output_string.getvalue()
    print("Extracted text:", extracted_text[:1000])  # Print first 1000 characters for debug
except Exception as e:
    print(f"Error extracting text: {e}")

# Save extracted text to a debug file
try:
    with open(debug_file, 'w') as f:
        f.write(extracted_text)
except Exception as e:
    print(f"Error saving debug file: {e}")

# Save extracted text to a JSON file with the specified structure
try:
    with open(output_file, 'w') as f:
        json.dump({"paper_title": "", "subtitles": [], "text": extracted_text}, f, indent=4)
except Exception as e:
    print(f"Error saving output JSON file: {e}")

print(f"Text extracted to {debug_file} and saved as JSON to {output_file}")

def clean_text(text):
    # Remove non-alphanumeric characters except spaces and basic punctuation
    text = re.sub(r'[^a-zA-Z0-9\s.,;?!]', '', text)
    
    # Remove repetitive words
    text = re.sub(r'\b(\w+)( \1\b)+', r'\1', text)
    
    # Correct simple grammar and punctuation mistakes
    text = text.replace(' ,', ',')
    text = text.replace(' .', '.')
    text = text.replace(' ;', ';')
    text = text.replace(' ?', '?')
    text = text.replace(' !', '!')
    
    return text

def split_into_chunks(text, max_tokens=2000):
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)

    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        yield tokenizer.decode(chunk_tokens)

# Clean the text
cleaned_text = clean_text(extracted_text)

# Split the cleaned text into chunks
chunks = list(split_into_chunks(cleaned_text))
total_chunks = len(chunks)

# Load OpenAI API key from environment variable
OPENAI_API_QUERY_KEY = os.getenv("OPENAI_API_QUERY_KEY")

# Initialize the OpenAI API client
query_llm = ChatOpenAI(
    openai_api_key=OPENAI_API_QUERY_KEY,
    model_name='gpt-3.5-turbo-0125',
    temperature=0.7,
    streaming=True
)

# Define the prompt template
prompt_template = """Clean the provided text by removing instances of gibberish, which include scrambled letters, nonsensical combinations, random words, and repetitive sequences of numbers without context. Ensure all titles, headers, and numbered sections are preserved exactly as they appear, without altering any part of the text except for obvious instances of gibberish or repetitive words. The output should solely consist of the cleaned text, maintaining the original formatting and structure without any additional introductions or formatting changes. Here are some examples of gibberish:

1. alsdfjll
2. [5, 10, 24, 32, 33, 34, 35, 36, 37]
3. (love)(love)(love)
4. Https/love
5. 23applesalsdfjlj124

Here is the text:
```{text}```
"""

# Process each chunk using OpenAI API with progress tracking
final_cleaned_text = ""
for i, chunk in enumerate(chunks):
    prompt = prompt_template.format(text=chunk)
    response = query_llm.invoke(prompt)
    final_cleaned_text += response.content + " "
    print(f"Processed chunk {i+1}/{total_chunks}")

# Save final cleaned text to a JSON file
try:
    cleaned_research_papers = [{"paper_title": "", "subtitles": [], "text": final_cleaned_text.strip()}]
    with open(cleaned_output_file_json, 'w') as f:
        json.dump({"research_papers": cleaned_research_papers}, f, indent=4)
    print(f"Cleaned text saved as JSON to {cleaned_output_file_json}")
except Exception as e:
    print(f"Error saving cleaned output JSON file: {e}")

# Save final cleaned text to a text file
try:
    with open(cleaned_output_file_txt, 'w') as f:
        f.write(final_cleaned_text.strip())
    print(f"Cleaned text saved as TXT to {cleaned_output_file_txt}")
except Exception as e:
    print(f"Error saving cleaned output TXT file: {e}")
