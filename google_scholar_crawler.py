import fitz  # PyMuPDF
import re

def extract_text_from_first_pages(pdf_path, num_pages=5):
    """
    Extract text from the first few pages of a PDF file.

    :param pdf_path: Path to the PDF file
    :param num_pages: Number of pages to extract text from
    :return: Extracted text
    """
    document = fitz.open(pdf_path)
    text = ""
    
    for page_num in range(min(num_pages, len(document))):
        page = document.load_page(page_num)
        text += page.get_text()
    
    return text

def find_definition(text, term):
    """
    Find the definition of a term in the text.

    :param text: Text to search within
    :param term: Term to find the definition for
    :return: Definition of the term if found, otherwise None
    """
    # Use regex to find sentences containing the term "Responsible Artificial Intelligence"
    pattern = re.compile(r"([^.]*?{}[^.]*\.)".format(re.escape(term)), re.IGNORECASE)
    matches = pattern.findall(text)
    
    if matches:
        # Return the first match (assuming the first match is the definition)
        return matches[0]
    else:
        return None

def extract_definition_from_pdf(pdf_path, term="Responsible Artificial Intelligence"):
    """
    Extract the definition of a term from a PDF file.

    :param pdf_path: Path to the PDF file
    :param term: Term to find the definition for
    :return: Definition of the term if found, otherwise None
    """
    text = extract_text_from_first_pages(pdf_path)
    definition = find_definition(text, term)
    
    return definition

# Example usage
pdf_path = 'path/to/your/research_paper.pdf'
term = "Responsible Artificial Intelligence"
definition = extract_definition_from_pdf(pdf_path, term)

if definition:
    print(f"The definition of '{term}' is:\n{definition}")
else:
    print(f"The term '{term}' was not found in the PDF.")

