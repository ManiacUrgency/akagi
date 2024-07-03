import os

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal, LTPage, LTChar

import json
from collections import Counter

import string

# List of Roman numerals
roman_numerals = [
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX",
    "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI", "XXVII", "XXVIII", "XXIX", "XXX"
]

def is_same_line(current_y0, previous_y0):
    if (current_y0 == None or previous_y0 == None):
        print("Last line of text.")
    else:
        if (abs(previous_y0 - current_y0) < 0.5):
            return True
        else:
            return False
    
def count_digits_in_line(text_elements, start_index, common_fontname, digits):
    if start_index >= len(text_elements):
        return 0

    digit_count = 0
    i = start_index
    next_y0 = text_elements[i+1]["y0"] 

    # print("\n\ncurrent_y0: ", text_elements[i]["y0"])
    # print("next_y0: ", next_y0)
    # print("Line Changed (TF): ", is_same_line(text_elements[i]["y0"], next_y0))
    
    while (i < len(text_elements)) and is_same_line(text_elements[i]["y0"], next_y0) and (text_elements[i]["fontname"] != common_fontname):
        # print("\n\ncurrent_y0: ", text_elements[i]["y0"])
        # print("next_y0: ", next_y0)
        # print("Line Changed (TF): ", is_same_line(text_elements[i]["y0"], next_y0))
        next_y0 = text_elements[i+1]["y0"]
        # print("Digit Counting... Layer 1 Passed")
        if text_elements[i]["text"] in digits:
            digit_count += 1
        i += 1

    return digit_count

def extract_text_with_attributes(pdf_path):
    text_elements = []

    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, LTTextBoxHorizontal):
                for text_line in element:
                    if isinstance(text_line, LTTextLineHorizontal):
                        # Check if any character in the text line is rotated
                        is_rotated = any(abs(char.matrix[1]) > 1e-6 for char in text_line if isinstance(char, LTChar))
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

def check_no_normal_text_on_line(start_index, current_y0, text_elements, common_fontname):
    i = start_index
    while text_elements[i]["y0"] == current_y0:
        if text_elements[i]["fontname"] == common_fontname:
            return False
        i += 1
    return True

def filter_number_headings(text_elements, common_font_size, common_fontname, headings, digits):

    print("Running Filter Number Headings")
    heading_type = ""
    temp_heading = ""
    heading_detected = False
    print("common font name: ", common_fontname)
    print("commmon font size: ", common_font_size)
    print("text elements length: ", len(text_elements))

    j = 0
    while j < len(text_elements):
        font_size = round(text_elements[j]["font_size"])
        font_name = text_elements[j]["fontname"]
        char = text_elements[j]["text"]
        current_y0 = text_elements[j]["y0"]
        previous_y0 = text_elements[j-1]["y0"] if j > 0 else None
        num_digits = None
        
        if font_name != common_fontname and (is_same_line(current_y0, previous_y0) == False):
            if check_no_normal_text_on_line(j, text_elements[j]["y0"], text_elements, common_fontname):
                temp = ""
                for k in range(8):
                    if (j + k) < len(text_elements):
                        temp += text_elements[j + k]["text"]
                if temp.strip().lower() == "abstract":
                    headings["main_headings"].append(temp.strip())
                    print("\n---------------Starting!!!----------------\n")
                    break
        j += 1

    i = j
    while i < len(text_elements):
        font_size = round(text_elements[i]["font_size"])
        font_name = text_elements[i]["fontname"]
        char = text_elements[i]["text"]
        current_y0 = text_elements[i]["y0"]
        previous_y0 = text_elements[i-1]["y0"] if i > 0 else None
        num_digits = None
        
        if font_name != common_fontname and (is_same_line(current_y0, previous_y0) == False) and font_size >= common_font_size:
            if check_no_normal_text_on_line(i, text_elements[i]["y0"], text_elements, common_fontname):
                temp = ""
                for k in range(10):
                    if (i + k) < len(text_elements):
                        temp += text_elements[i + k]["text"]
                if temp.strip().lower() == "references":
                    headings["main_headings"].append(temp.strip())
                    print("---------------Breaking!!!----------------")
                    break
        
        if font_size < common_font_size:
            # print("Skipping: ", text_elements[i])
            i += 1
            continue

        # print(f"character {i}: ", char)
        # print("\n\nfont size: ", font_size, "\n\n")

        if (is_same_line(current_y0, previous_y0) == False) and (font_name != common_fontname) and (char in digits):
            heading_detected = True
            num_digits = count_digits_in_line(text_elements, i, common_fontname, digits)
            # print("+- 10 elements discovered: ", text_elements[i-10:i+10])
            # print("element discovered: ", text_elements[i]["text"])
            print("\nnum digits: ", num_digits, "\n")

            if num_digits == 1:
                if check_no_normal_text_on_line(i, current_y0, text_elements, common_fontname):
                    print("----------Digit 1 Activation----------")
                    heading_type = "main_headings"
                    j = i
                    while j < len(text_elements) and (text_elements[j]["fontname"] != common_fontname):
                        temp_heading += text_elements[j]["text"]
                        j += 1
                    i = j
            elif num_digits == 2:
                if check_no_normal_text_on_line(i, current_y0, text_elements, common_fontname):
                    # print("----------Digit 2 Activation----------")
                    heading_type = "sub_headings"
                    j = i
                    while j < len(text_elements) and (text_elements[j]["fontname"] != common_fontname):
                        temp_heading += text_elements[j]["text"]
                        j += 1
                    i = j
            elif num_digits == 3:
                # print("----------Digit 3 Activation----------")
                heading_type = "sub_sub_headings"
                j = i
                while j < len(text_elements) and (text_elements[j]["fontname"] != common_fontname):
                    temp_heading += text_elements[j]["text"]
                    j += 1
                i = j

        # print("Same line? ", is_same_line(text_elements[i]["y0"], previous_y0))
        if heading_detected and (i < len(text_elements)) and (is_same_line(text_elements[i]["y0"], previous_y0) == False):
            # print("Adding Heading")
            heading_detected = False
            # print("\ntemp heading: ", temp_heading)
            # print("\nheading type: ", heading_type)
            headings[heading_type].append(temp_heading)
            temp_heading = ""
            heading_type = ""
        i += 1
    
    print("\n\n\nHeadings: ", headings, "\n\n\n")
    return headings

def is_roman_numeral(text):
    return text in roman_numerals
    
def detect_roman_numeral(start_index, text_elements):
    # print("start index: ", start_index)
    i = start_index
    punctuation_except_periods = string.punctuation.replace(".", "")

    current_y0 = text_elements[i]["y0"]
    next_y0 = text_elements[i+1]["y0"]
    text = ""

    while (i < len(text_elements) and is_same_line(current_y0, next_y0) and (text_elements[i]["text"].isupper()) and (text_elements[i]["text"] != ".")):
        text += text_elements[i]["text"]
        i += 1

    if is_roman_numeral(text):
        if (text_elements[i]["text"] == "."):
            # print("Roman Numeral: ", text, "character after roman numeral: ", text_elements[i]["text"])
            k = i+1
            while is_same_line(text_elements[k]["y0"], text_elements[k-1]["y0"]):
                # print("text: ", text_elements[k]["text"])
                if (text_elements[k]["text"] in punctuation_except_periods) == False:
                    if ((text_elements[k]["text"].isupper() == False) or (text_elements[k]["text"].isalpha() == False)):
                        # print("Roman Numeral: ", text, text_elements[i]["text"])
                        # print("Roman Numeral: ", text_elements[i-3:i+1])
                        return False
                k += 1
            return True
    return False

def detect_alphabetical_letter(start_index, text_elements):
    if start_index >= len(text_elements):
        return False

    start_y0 = text_elements[start_index]["y0"]
    i = start_index
    letter_detected = False

    text = ""
    while (i < len(text_elements) and is_same_line(text_elements[i]["y0"], start_y0) and text_elements[i]["text"] != "."):
        text += text_elements[i]["text"]
        i += 1
    
    if text.isalpha() and text.isupper():
        # print("text: ", text, "character after text: ", text_elements[i]["text"])
        letter_detected = True

    if letter_detected and (i < len(text_elements)) and text_elements[i]["text"] == ".":
        # print("Capitalized Alpha Letter Detected")
        return True
    return False

def check_no_lowercase_on_line(start_index, text_elements, current_y0):
    # print("Running Checking Lowercase Function")
    i = start_index
    while is_same_line(text_elements[i]["y0"], current_y0):
        if text_elements[i]["text"].islower():
            # print("lowercase text: ", text_elements[i]["text"])
            return False
        i += 1
    return True

def filter_ieee_headings(text_elements, common_font_size, common_fontname, headings):

    heading_type = ""
    heading_detected = False
    print("common font name: ", common_fontname)
    print("commmon font size: ", common_font_size)
    print("text elements length: ", len(text_elements))

    j = 0
    while j < len(text_elements):
        font_size = round(text_elements[j]["font_size"])
        font_name = text_elements[j]["fontname"]
        current_y0 = text_elements[j]["y0"] if j < len(text_elements) else None
        previous_y0 = text_elements[j-1]["y0"] if j > 0 else None
        temp_heading = ""
        heading_type = ""
        heading_detected = False

        if (is_same_line(text_elements[j]["y0"], previous_y0) == False) and (font_name != common_fontname):
            # print("Identified Possible Abstract Word")
            temp = ""
            for k in range(8):
                if (j + k) < len(text_elements):
                    temp += text_elements[j + k]["text"]
            if temp.strip().lower() == "abstract":
                print("\n---------------Starting!!!----------------\n")
                headings["main_headings"].append(temp.strip())
                break
        j += 1

    i = j
    while i < len(text_elements):
        font_size = round(text_elements[i]["font_size"])
        font_name = text_elements[i]["fontname"]
        current_y0 = text_elements[i]["y0"] if i < len(text_elements) else None
        previous_y0 = text_elements[i-1]["y0"] if i > 0 else None
        temp_heading = ""
        heading_type = ""
        heading_detected = False

        if (is_same_line(text_elements[i]["y0"], previous_y0) == False):
            temp = ""
            for k in range(10):
                if (i + k) < len(text_elements):
                    if text_elements[i+k]["text"].isupper():
                        # print("Reference elements: ", text_elements[i+k])
                        temp += text_elements[i + k]["text"]
                    else:
                        break
            if temp.strip().lower() == "references":
                headings["main_headings"].append(temp.strip())
                print("---------------Breaking!!!----------------")
                break
        
        # print("text element: ", text_elements[i]["text"])

        if font_size < common_font_size:
            i += 1
            continue

        if (is_same_line(current_y0, previous_y0) == False):
            if detect_roman_numeral(i, text_elements):
                # print("\nRoman Numeral Layer Passed\n")
                if check_no_lowercase_on_line(i, text_elements, current_y0): 
                    print("\nMain Heading Detected Baby\n")
                    heading_type = "main_headings"
                    heading_detected = True
                    j = i
                    while is_same_line(text_elements[j]["y0"], current_y0):
                        # print("text elements: ", text_elements[j]["text"])
                        temp_heading += text_elements[j]["text"]
                        j += 1
                    # print("temp heading: ", temp_heading)
                    i = j

            elif (font_name != common_fontname):

                if detect_alphabetical_letter(i, text_elements):
                    if check_no_normal_text_on_line(i, current_y0, text_elements, common_fontname):
                        print("\nSub Heading Detected Baby\n")
                        heading_detected = True
                        heading_type = "sub_headings"
                        j = i
                        while is_same_line(text_elements[j]["y0"], current_y0) and (font_name != common_fontname):
                            temp_heading += text_elements[j]["text"]
                            j += 1
                        # print("temp heading: ", temp_heading)
                        i = j
            
        if (heading_detected) and (is_same_line(text_elements[i]["y0"], previous_y0) == False):
            heading_detected = False
            print("temp heading: ", temp_heading)
            headings[heading_type].append(temp_heading)
            temp_heading = ""
            heading_type = "" 

        i += 1
    print("\n\n\nheadings: ", headings, "\n\n\n")
    return headings

def has_columns(text_elements, pdf_path):
    print("\nRunning has_columns function\n")
    radius = 10
    pages = list(extract_pages(pdf_path))  # Convert the generator to a list
    if isinstance(pages[0], LTPage):
        print("Page 1 is a pdf page object.")
        width = pages[0].x1 - pages[0].x0
        middle = width / 2
        print("\nwidth: ", width, "\n")
        for element in text_elements:
            if middle - radius < element["x0"] < middle + radius or middle - radius < element["x1"] < middle + radius:
                return False
    return True

def extract_font_sizes(text_elements):
    font_sizes = []
    for element in text_elements:
        if element["font_size"]:
            font_sizes.append(round(element["font_size"], 1))
    return font_sizes

def get_unique_font_sizes_and_most_common(font_sizes):
    unique_font_sizes = sorted(set(font_sizes))
    most_common_font_size = Counter(font_sizes).most_common(1)[0][0]
    return unique_font_sizes, most_common_font_size

def identify_key_font_sizes(unique_font_sizes, most_common_font_size):
    title_font_size = max(unique_font_sizes)
    main_heading_font_size = None
    sub_heading_font_size = None

    for size in reversed(unique_font_sizes):
        if size < title_font_size and size > most_common_font_size and main_heading_font_size is None:
            main_heading_font_size = size
        elif main_heading_font_size is not None and size < main_heading_font_size and size > most_common_font_size and sub_heading_font_size is None:
            sub_heading_font_size = size
            break

    return round(main_heading_font_size), round(sub_heading_font_size)

def filter_fontname_fontsize_headings(text_elements, main_heading_font_size, sub_heading_font_size, common_fontname, common_font_size, headings):
    
    heading_type = ""
    heading_detected = False
    print("common font name: ", common_fontname)
    print("commmon font size: ", common_font_size)
    print("text elements length: ", len(text_elements)) 

    j = 0
    while j < len(text_elements):
        font_size = round(text_elements[j]["font_size"])
        font_name = text_elements[j]["fontname"]
        current_y0 = text_elements[j]["y0"] if j < len(text_elements) else None
        previous_y0 = text_elements[j-1]["y0"] if j > 0 else None
        temp_heading = ""
        heading_type = ""
        heading_detected = False

        if (is_same_line(text_elements[j]["y0"], previous_y0) == False) and (font_name != common_fontname):
            temp = ""
            for k in range(8):
                if (j + k) < len(text_elements):
                    temp += text_elements[j + k]["text"]
            if temp.strip().lower() == "abstract":
                print("\n---------------Starting!!!----------------\n")
                headings["main_headings"].append(temp.strip())
                break
        j += 1

    i = j
    while i < len(text_elements):
        font_size = round(text_elements[i]["font_size"])
        font_name = text_elements[i]["fontname"]
        current_y0 = text_elements[i]["y0"] if i < len(text_elements) else None
        previous_y0 = text_elements[i-1]["y0"] if i > 0 else None
        temp_heading = ""
        heading_type = ""
        heading_detected = False

        if (is_same_line(text_elements[i]["y0"], previous_y0) == False) and (font_name != common_fontname):
            temp = ""
            for k in range(10):
                if (i + k) < len(text_elements):
                    temp += text_elements[i + k]["text"]
            if temp.strip().lower() == "references":
                headings["main_headings"].append(temp)
                print("---------------Breaking!!!----------------")
                break
        
        # print("text element: ", text_elements[i]["text"])

        if font_size < common_font_size:
            i += 1
            continue

        if (is_same_line(current_y0, previous_y0) == False) and (font_name != common_fontname) and (font_size == main_heading_font_size):
            if check_no_normal_text_on_line(i, current_y0, text_elements, common_fontname):
                heading_detected = True
                heading_type = "main_headings"
                j = i
                while is_same_line(text_elements[j]["y0"], current_y0):
                    # print("text elements: ", text_elements[j]["text"])
                    temp_heading += text_elements[j]["text"]
                    j += 1
                # print("temp heading: ", temp_heading)
                i = j
        
        elif ((is_same_line(current_y0, previous_y0) == False) and (font_name != common_fontname) and (font_size == sub_heading_font_size)):
            if check_no_normal_text_on_line(i, current_y0, text_elements, common_fontname):
                heading_detected = True
                heading_type = "sub_headings"
                j = i
                while is_same_line(text_elements[j]["y0"], current_y0):
                    # print("text elements: ", text_elements[j]["text"])
                    temp_heading += text_elements[j]["text"]
                    j += 1
                # print("temp heading: ", temp_heading)
                i = j 

        if (heading_detected) and (is_same_line(text_elements[i]["y0"], previous_y0) == False):
            heading_detected = False
            print("temp heading: ", temp_heading)
            headings[heading_type].append(temp_heading)
            temp_heading = ""
            heading_type = "" 

        i += 1
    print("\n\n\nheadings: ", headings, "\n\n\n")
    return headings
 
def filter_headings(text_elements, common_font_size, common_fontname, pdf_path):
    headings = {
        "main_headings": [],
        "sub_headings": [],
        "sub_sub_headings": []
    }

    punctuation_except_periods = string.punctuation.replace(".", "")
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    running_number_headings = False
    running_roman_headings = False
   
    if has_columns(text_elements, pdf_path):
        print("Has Columns")
    else:
         
        i = 0

        while i < len(text_elements):
            element = text_elements[i]
            font_size = round(element["font_size"])
            font_name = element["fontname"]
            char = element["text"]
            current_y0 = element["y0"]
            previous_y0 = text_elements[i-1]["y0"] if i > 0 else None
            no_title_exceptions = True

            if (is_same_line(current_y0, previous_y0) == False) and font_size >= common_font_size:
                if check_no_normal_text_on_line(i, current_y0, text_elements, common_fontname):
                    temp = ""
                    for k in range(10):
                        if (i + k) < len(text_elements):
                            temp += text_elements[i + k]["text"]
                    if temp.strip().lower() == "references":
                        print("---------------Breaking!!!----------------")
                        break

            if (is_same_line(current_y0, previous_y0) == False):
                if font_name != common_fontname and (char in digits) and font_size >= common_font_size:
                    if (text_elements[i+1]["text"] in punctuation_except_periods) == False:
                        if check_no_normal_text_on_line(i, current_y0, text_elements, common_fontname):

                            k = i+1
                            while k < i + 4:
                                print("text: ", text_elements[k]["text"])
                                if ((font_size <= common_font_size)) and (text_elements[k]["text"].isalpha() == False):
                                    # print("Num: ", text, text_elements[i]["text"])
                                    no_title_exceptions = False
                                k += 1
                            
                            print("\n\nboolean value: ", no_title_exceptions, "\n\n")
                            if (no_title_exceptions):
                                print("----------Identified NUMBER Pattern Sequence----------")
                                running_number_headings = True
                                print("+- 10 elements discovered: ", text_elements[i-10:i+10])
                                print("\nelement discovered: ", text_elements[i])
                                print("\n\ncurrent y0: ", current_y0, "compared with pervious y0: ", previous_y0, "\n\n")
                                # print("\n\nelement font: ", font_size, "compared to normal font size: ", common_font_size, "\n\n")
                                headings = filter_number_headings(text_elements, common_font_size, common_fontname, headings, digits)
                                # Skip the processed elements
                                break
            i += 1

    if (running_number_headings == False):
        if has_columns(text_elements, pdf_path):
            print("Has Columns")
        else:
            found_roman_numeral = False
            found_alphabetical_letter = False
            i = 0
            while i < len(text_elements):
                element = text_elements[i]
                current_y0 = element["y0"]
                previous_y0 = text_elements[i-1]["y0"] if i > 0 else None

                if (is_same_line(text_elements[i]["y0"], previous_y0) == False):
                    temp = ""
                    for k in range(10):
                        if (i + k) < len(text_elements):
                            if text_elements[i+k]["text"].isupper():
                                # print("Reference elements: ", text_elements[i+k])
                                temp += text_elements[i + k]["text"]
                            else:
                                break
                    if temp.strip().lower() == "references":
                        print("---------------Breaking!!!----------------")
                        break

                if (is_same_line(current_y0, previous_y0) == False):
                    if detect_roman_numeral(i, text_elements):
                            print("----------Identified ROMAN NUMERAL Pattern Sequence----------")
                            found_roman_numeral = True       
                    
                if (is_same_line(current_y0, previous_y0) == False):
                    # print("Detected change in line.")
                    if detect_alphabetical_letter(i, text_elements):
                            print("----------Identified ALPHABETICAL LETTER Pattern Sequence----------")
                            found_alphabetical_letter = True
                
                if (found_roman_numeral and found_alphabetical_letter):
                    print("----------Identified IEEE Pattern Sequence----------")
                    running_roman_headings = True 
                    headings = filter_ieee_headings(text_elements, common_font_size, common_fontname, headings)
                    break

                i += 1
    
    if (running_number_headings == False and running_roman_headings == False):
        print("----------Identified FONTNAME & FONTSIZE Pattern Sequence----------") 
        font_sizes = extract_font_sizes(text_elements)
        unique_font_sizes, most_common_font_size = get_unique_font_sizes_and_most_common(font_sizes)
        main_heading_font_size, sub_heading_font_size = identify_key_font_sizes(unique_font_sizes, most_common_font_size)
        print("\nmain heading font size: ", main_heading_font_size)
        print("sub heading font size: ", sub_heading_font_size, "\n")

        headings = filter_fontname_fontsize_headings(text_elements, main_heading_font_size, sub_heading_font_size, common_fontname, common_font_size, headings)

    return headings

def main():
    file_path = os.path.dirname(os.path.realpath(__file__))
    pdf_path = file_path + "/test1.pdf"
    text_elements = extract_text_with_attributes(pdf_path)

    common_font_size, common_fontname = determine_common_text_attributes(text_elements)
    headings = filter_headings(text_elements, common_font_size, common_fontname, pdf_path)

    print("\n\n\nheadings before decare: ", headings, "\n\n\n")
    headings_json = {"headings": headings}

    with open(file_path + "/headings.json", "w") as json_file:
        json.dump(headings_json, json_file, indent=4)

    print("Headings extracted and saved to headings.json")

if __name__ == "__main__":
    main()
