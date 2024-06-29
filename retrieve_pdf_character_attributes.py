import os
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTPage, LTTextContainer, LTTextLine, LTChar, LTFigure

def parse_obj(objs, output_file):
    for obj in objs:
        if isinstance(obj, LTPage):
            output_file.write(f"Page {obj.pageid}\n")
            parse_obj(obj._objs, output_file)
        elif isinstance(obj, LTTextContainer):
            output_file.write("  Text Container:\n")
            for text_line in obj:
                if isinstance(text_line, LTTextLine):
                    output_file.write("    Text Line:\n")
                    parse_obj(text_line._objs, output_file)
        elif isinstance(obj, LTChar):
            output_file.write(f"      Character: '{obj.get_text()}' at ({obj.x0}, {obj.y0}, {obj.x1}, {obj.y1}) with font size {obj.size}, font name {obj.fontname}, and rotation {obj.matrix[1]}\n")
        elif isinstance(obj, LTFigure):
            output_file.write("    Figure:\n")
            parse_obj(obj._objs, output_file)
        else:
            output_file.write(f"    Other: {type(obj).__name__}\n")

def extract_pdf_structure(pdf_path, output_path):
    with open(output_path, 'w', encoding='utf-8') as output_file:
        for page_layout in extract_pages(pdf_path):
            parse_obj([page_layout], output_file)

# Example usage
pdf_path = 'HumanSimulacra.pdf'
output_path = 'pdf_structure.txt'
extract_pdf_structure(pdf_path, output_path)


