import os
import requests
import tempfile
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal, LTChar

def extract_text_with_attributes(pdf_path):
    text_elements = []

    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, LTTextBoxHorizontal):
                for text_line in element:
                    if isinstance(text_line, LTTextLineHorizontal):
                        # Check if any character in the text line is rotated
                        is_rotated = any(abs(round(char.matrix[1])) != 0 for char in text_line if isinstance(char, LTChar))
                        if is_rotated:
                            continue  # Ignore rotated text lines

                        for char in text_line:
                            if isinstance(char, LTChar):
                                char_data = {
                                    "text": char.get_text(),
                                    "font_size": char.size,
                                    "fontname": char.fontname,
                                    "x0": char.x0,
                                    "x1": char.x1,
                                    "y0": char.y0,
                                    "y1": char.y1,
                                }
                                text_elements.append(char_data)

    return text_elements

def determine_common_text_attributes(text_elements):
    font_sizes = {}
    font_names = {}

    for element in text_elements:
        if element["font_size"]:
            font_sizes[element["font_size"]] = font_sizes.get(element["font_size"], 0) + 1
        if element["fontname"]:
            font_names[element["fontname"]] = font_names.get(element["fontname"], 0) + 1

    common_font_size = round(max(font_sizes, key=font_sizes.get))
    common_fontname = max(font_names, key=font_names.get)

    return common_font_size, common_fontname

def save_text_elements_to_txt(text_elements, output_path, common_font_size, common_fontname):
    with open(output_path, 'w') as txt_file:
        previous_x1 = None
        for element in text_elements:
            char = element["text"]
            font_size = round(element["font_size"])

            if font_size < common_font_size:
                continue

            if previous_x1 is not None and element["x0"] > previous_x1 + 1:
                txt_file.write(" ")

            txt_file.write(char)
            previous_x1 = element["x1"]

def download_pdf(url):
    print(f"Downloading PDF from URL: {url}")
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    session = requests.Session()
    session.headers.update(HEADERS)
    
    try:
        response = session.get(url, stream=True)
        response.raise_for_status()
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_file.write(response.content)
        temp_file.close()
        print(f"PDF downloaded and saved to: {temp_file.name}")
        return temp_file.name
    except requests.exceptions.RequestException as e:
        print(f"Failed to download PDF from URL: {url}. Error: {e}")
        raise Exception(f"Failed to download PDF. Status code: {response.status_code}")

def main(pdf_url):
    output_path = "raw_text.txt"

    pdf_path = download_pdf(pdf_url)
    text_elements = extract_text_with_attributes(pdf_path)
    common_font_size, common_fontname = determine_common_text_attributes(text_elements)

    print("common font size: ", common_font_size)
    print("common font name: ", common_fontname)

    save_text_elements_to_txt(text_elements, output_path, common_font_size, common_fontname)

    print(f"Character-by-character text extraction saved to {output_path}")
    os.remove(pdf_path)
    print(f"Temporary PDF file removed: {pdf_path}")

