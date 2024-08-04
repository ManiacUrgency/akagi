import os
import requests
import tempfile
import json
from collections import Counter
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal, LTPage, LTChar
import string


# List of Roman numerals
roman_numerals = [
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX",
    "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI", "XXVII", "XXVIII", "XXIX", "XXX"
]

def is_same_line(current_y0, previous_y0):
    if current_y0 is None or previous_y0 is None:
        print("Last line of text.")
    else:
        return abs(previous_y0 - current_y0) < 0.5
    
def count_digits_in_line(text_elements, start_index, common_fontname, digits):
    if start_index >= len(text_elements):
        return 0

    digit_count = 0
    i = start_index
    next_y0 = text_elements[i+1]["y0"] 

    # print("\n\ncurrent_y0: ", text_elements[i]["y0"])
    # print("next_y0: ", next_y0)
    # print("Line Changed (TF): ", is_same_line(text_elements[i]["y0"], next_y0))
    while i < len(text_elements) and is_same_line(text_elements[i]["y0"], next_y0) and text_elements[i]["fontname"] != common_fontname:
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

    # Write text elements to a file in pretty print
    with open("output_text_elements.txt", 'w') as f:
        for element in text_elements:
            f.write(f"{element}\n")

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

    sorted_font_sizes = sorted(font_sizes.items(), key=lambda item: item[1], reverse=True)
    common_font_size = round(sorted_font_sizes[0][0])
    second_common_font_size = round(sorted_font_sizes[1][0]) if len(sorted_font_sizes) > 1 else None

    common_fontname = max(font_names, key=font_names.get)

    return common_font_size, second_common_font_size, common_fontname

def check_no_normal_text_on_line(start_index, current_y0, text_elements, common_fontname):
    i = start_index
    while text_elements[i]["y0"] == current_y0:
        if text_elements[i]["fontname"] == common_fontname:
            return False
        i += 1
    return True

def filter_number_headings(text_elements, common_font_size, second_common_font_size, common_fontname, headings, digits):

    print("Running Filter Number Headings")
    temp_heading = ""
    heading_detected = False
    print("common font name: ", common_fontname)
    print("commmon font size: ", common_font_size)
    print("text elements length: ", len(text_elements))
    
    abstract_found = False 
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
                    print("\nAbstract Found\n")
                    headings.append(temp.strip())
                    abstract_found = True
                    print("\n---------------Starting!!!----------------\n")
                    break
        j += 1

    print("abstract_found value: ", abstract_found)
    if abstract_found == False:
        print("\n\nRunning No Abstract Finding Code")
        k = 0
        while k < len(text_elements):
            current_y0 = text_elements[k]["y0"]
            previous_y0 = text_elements[k-1]["y0"] if j > 0 else None

            if (is_same_line(current_y0, previous_y0) == False) and font_size == second_common_font_size:
                headings.append("Abstract")
                print("\nNo Abstract title\n")
                print("\n---------------Starting!!!----------------\n")
                break
            k += 1
        j = 0

    i = j
    previous_x1 = None
    while i < len(text_elements):
        font_size = round(text_elements[i]["font_size"])
        font_name = text_elements[i]["fontname"]
        char = text_elements[i]["text"]
        current_y0 = text_elements[i]["y0"]
        previous_y0 = text_elements[i-1]["y0"] if i > 0 else None
        num_digits = None
        
        if font_name != common_fontname and not is_same_line(current_y0, previous_y0) and font_size >= common_font_size:
            if check_no_normal_text_on_line(i, text_elements[i]["y0"], text_elements, common_fontname):
                temp = ""
                for k in range(10):
                    if (i + k) < len(text_elements):
                        temp += text_elements[i + k]["text"]
                if temp.strip().lower() == "references":
                    headings.append(temp.strip())
                    print("---------------Breaking!!!----------------")
                    break
        
        if font_size < common_font_size:
            i += 1
            continue

        if not is_same_line(current_y0, previous_y0) and font_name != common_fontname and char in digits:
            heading_detected = True
            num_digits = count_digits_in_line(text_elements, i, common_fontname, digits)
            # print("\nnum digits: ", num_digits, "\n")
            if num_digits == 1:
                if check_no_normal_text_on_line(i, current_y0, text_elements, common_fontname):
                    print("----------Digit 1 Activation----------")
                    
                    j = i
                    while j < len(text_elements) and text_elements[j]["fontname"] != common_fontname:
                        if previous_x1 is not None and text_elements[j]["x0"] > previous_x1 + 1:
                            temp_heading += " "
                        temp_heading += text_elements[j]["text"]
                        previous_x1 = text_elements[j]["x1"]
                        j += 1
                    i = j
            elif num_digits == 2:
                if check_no_normal_text_on_line(i, current_y0, text_elements, common_fontname):
                    print("----------Digit 2 Activation----------")
                    
                    j = i
                    while j < len(text_elements) and text_elements[j]["fontname"] != common_fontname:
                        if previous_x1 is not None and text_elements[j]["x0"] > previous_x1 + 1:
                            temp_heading += " "
                        temp_heading += text_elements[j]["text"]
                        previous_x1 = text_elements[j]["x1"]
                        j += 1
                    i = j
            elif num_digits == 3:
                print("----------Digit 3 Activation----------")
                
                j = i
                while j < len(text_elements) and text_elements[j]["fontname"] != common_fontname:
                    if previous_x1 is not None and text_elements[j]["x0"] > previous_x1 + 1:
                        temp_heading += " "
                    temp_heading += text_elements[j]["text"]
                    previous_x1 = text_elements[j]["x1"]
                    j += 1
                i = j

        # print("Same line? ", is_same_line(text_elements[i]["y0"], previous_y0))
        if heading_detected and i < len(text_elements) and not is_same_line(text_elements[i]["y0"], previous_y0) and len(temp_heading.strip()) > 0 and any(char.isalpha() for char in temp_heading):
            print("Adding Heading")
            
            heading_detected = False
            print("\ntemp heading: ", temp_heading)
            
            headings.append(temp_heading.strip())
            temp_heading = ""
        i += 1
    
    # print("\n\n\nHeadings: ", headings, "\n\n\n")
    
    return headings

def is_roman_numeral(text):
    return text in roman_numerals
    
def detect_roman_numeral(start_index, text_elements):
    # print("start index: ", start_index)
    i = start_index
    current_y0 = text_elements[i]["y0"]
    next_y0 = text_elements[i+1]["y0"]
    text = ""

    while i < len(text_elements) and is_same_line(current_y0, next_y0) and text_elements[i]["text"].isupper() and text_elements[i]["text"] != ".":
        text += text_elements[i]["text"]
        i += 1

    if is_roman_numeral(text):
        if text_elements[i]["text"] == ".":
            print("Roman numeral debugging: ", end = "")

            h = i-50
            while h < i:
                print("\n", text_elements[h], end = "")
                h += 1
            
            # print(text, "\n", text_elements[i-1]["text"], end = "")
            print(text_elements[i], end = "")
            z = i+1
            while z < i + 50:
                print("\n", text_elements[z], end = "")
                z += 1
            
            k = i+1
            while is_same_line(text_elements[k]["y0"], text_elements[k-1]["y0"]):
                # print("text: ", text_elements[k]["text"])
                
                if (text_elements[k]["text"] not in string.punctuation) and (text_elements[k]["text"] != " "):
                    if (text_elements[k]["text"].isupper() == False) and (text_elements[k]["text"].isalpha() == False):
                        print("Roman Numeral: ", text, "and character that is an exception: ", text_elements[k]["text"])
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
    while i < len(text_elements) and is_same_line(text_elements[i]["y0"], start_y0) and text_elements[i]["text"] != ".":
        text += text_elements[i]["text"]
        i += 1
    
    if text.isalpha() and text.isupper():
        # print("text: ", text, "character after text: ", text_elements[i]["text"])
        letter_detected = True

    if letter_detected and i < len(text_elements) and text_elements[i]["text"] == ".":
        # print("Capitalized Alpha Letter Detected")
        return True
    return False

def check_no_lowercase_on_line(start_index, text_elements, current_y0):
    # print("Running Checking Lowercase Function")
    # 
    i = start_index
    while is_same_line(text_elements[i]["y0"], current_y0):
        if text_elements[i]["text"] != string.punctuation:
            if text_elements[i]["text"].islower():
                print("lowercase text: ", text_elements[i]["text"])
                
                return False
        i += 1
    return True

def filter_ieee_headings(text_elements, common_font_size, common_fontname, headings):

    heading_detected = False
    
    j = 0
    while j < len(text_elements):
        font_size = round(text_elements[j]["font_size"])
        font_name = text_elements[j]["fontname"]
        current_y0 = text_elements[j]["y0"] if j < len(text_elements) else None
        previous_y0 = text_elements[j-1]["y0"] if j > 0 else None
        temp_heading = ""
        heading_detected = False

        if not is_same_line(text_elements[j]["y0"], previous_y0) and font_name != common_fontname:
            # print("Identified Possible Abstract Word")
            temp = ""
            for k in range(8):
                if (j + k) < len(text_elements):
                    temp += text_elements[j + k]["text"]
            if temp.strip().lower() == "abstract":
                print("\n---------------Starting!!!----------------\n")
                
                headings.append(temp.strip())
                break
        j += 1

    i = j
    previous_x1 = None
    while i < len(text_elements):
        font_size = round(text_elements[i]["font_size"])
        font_name = text_elements[i]["fontname"]
        current_y0 = text_elements[i]["y0"] if i < len(text_elements) else None
        previous_y0 = text_elements[i-1]["y0"] if i > 0 else None
        temp_heading = ""
        heading_detected = False

        if not is_same_line(current_y0, previous_y0):
            temp = ""
            for k in range(10):
                if (i + k) < len(text_elements):
                    if text_elements[i+k]["text"].isupper():
                        # print("Reference elements: ", text_elements[i+k])
                        temp += text_elements[i + k]["text"]
                    else:
                        break
            if temp.strip().lower() == "references":
                headings.append(temp.strip())
                print("---------------Breaking!!!----------------")
                
                break
        
        # print("text element: ", text_elements[i]["text"])

        if font_size < common_font_size:
            i += 1
            continue

        if not is_same_line(current_y0, previous_y0):
            if detect_roman_numeral(i, text_elements):
                print("\nMain Heading Detected Baby\n")
                
                heading_detected = True
                j = i
                while is_same_line(text_elements[j]["y0"], current_y0):
                    if previous_x1 is not None and text_elements[j]["x0"] > previous_x1 + 1:
                        temp_heading += " "
                    temp_heading += text_elements[j]["text"]
                    previous_x1 = text_elements[j]["x1"]
                    j += 1
                i = j

            elif font_name != common_fontname:

                if detect_alphabetical_letter(i, text_elements):
                    if check_no_normal_text_on_line(i, current_y0, text_elements, common_fontname):
                        print("\nSub Heading Detected Baby\n")
                        
                        heading_detected = True
                        j = i
                        while is_same_line(text_elements[j]["y0"], current_y0) and font_name != common_fontname:
                            if previous_x1 is not None and text_elements[j]["x0"] > previous_x1 + 1:
                                temp_heading += " "
                            temp_heading += text_elements[j]["text"]
                            previous_x1 = text_elements[j]["x1"]
                            j += 1
                        # print("temp heading: ", temp_heading)
                        
                        i = j

        if heading_detected and i < len(text_elements) and not is_same_line(text_elements[i]["y0"], previous_y0) and len(temp_heading.strip()) > 0 and any(char.isalpha() for char in temp_heading):   
            heading_detected = False
            print("\nAdding Heading\n")
            print("temp heading: ", temp_heading)
            
            headings.append(temp_heading.strip())
            temp_heading = ""

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
    
    heading_detected = False
    
    j = 0
    while j < len(text_elements):
        font_size = round(text_elements[j]["font_size"])
        font_name = text_elements[j]["fontname"]
        current_y0 = text_elements[j]["y0"] if j < len(text_elements) else None
        previous_y0 = text_elements[j-1]["y0"] if j > 0 else None
        temp_heading = ""
        heading_detected = False

        if not is_same_line(text_elements[j]["y0"], previous_y0) and font_name != common_fontname:
            temp = ""
            for k in range(8):
                if (j + k) < len(text_elements):
                    temp += text_elements[j + k]["text"]
            if temp.strip().lower() == "abstract":
                print("\n---------------Starting!!!----------------\n")
                
                headings.append(temp.strip())
                break
        j += 1

    print("Common font name: ", common_fontname)
    i = j
    previous_x1 = None
    while i < len(text_elements):
        font_size = round(text_elements[i]["font_size"])
        font_name = text_elements[i]["fontname"]
        current_y0 = text_elements[i]["y0"] if i < len(text_elements) else None
        previous_y0 = text_elements[i-1]["y0"] if i > 0 else None
        temp_heading = ""
        heading_detected = False

        if not is_same_line(current_y0, previous_y0):
            temp = ""
            for k in range(10):
                if (i + k) < len(text_elements):
                    temp += text_elements[i + k]["text"]
            if temp.strip().lower() == "references":
                headings.append(temp)
                print("---------------Breaking!!!----------------")
                
                break

        if font_size < common_font_size:
            # with open("temp_log.txt", "a") as file:
            #     file.write("\ntext skipped: " + text_elements[i-1]["text"] + "(" + text_elements[i]["text"] + ")" + text_elements[i+1]["text"] + text_elements[i+2]["text"] + text_elements[i+3]["text"] + "  text font size: " + str(text_elements[i]["font_size"]) + " common font size: " + str(common_font_size))
            i += 1
            continue

        if (is_same_line(current_y0, previous_y0) == False) and font_name != common_fontname and font_size == main_heading_font_size:
            if check_no_normal_text_on_line(i, current_y0, text_elements, common_fontname):
                # with open("temp_log.txt", "a") as file:
                #     file.write("\n\nMain heading text: " + text_elements[i]["text"])

                heading_detected = True
                j = i
                while is_same_line(text_elements[j]["y0"], current_y0):
                    if previous_x1 is not None and text_elements[j]["x0"] > previous_x1 + 1:
                        temp_heading += " "
                    temp_heading += text_elements[j]["text"]
                    previous_x1 = text_elements[j]["x1"]
                    j += 1
                
                print("Main Heading: ", temp_heading, "and font size: ", font_size)
                i = j - 1
        
        if (is_same_line(current_y0, previous_y0) == False) and font_name != common_fontname and font_size == sub_heading_font_size:
            # print("font name: ", font_name)
            # with open("temp_log.txt", "a") as file:
            #     file.write("\nsubheading text: " + text_elements[i-3]["text"] + text_elements[i-2]["text"] + text_elements[i-1]["text"] + "(" + text_elements[i]["text"] + ")" + text_elements[i+1]["text"] + text_elements[i+2]["text"] + text_elements[i+3]["text"] + "   current y0: " + str(current_y0) + "  previous y0: " + str(previous_y0) + "    fontname: " + font_name + "    common font name: " + common_fontname + "    font size: " + str(font_size) + "    common font size: " + str(common_font_size))
            #     file.write("\nsubheading text " + str(i-1) + ": " + "(" + text_elements[i-1]["text"] + ")" + "   current y0: " + str(text_elements[i-1]["y0"]) + "  previous y0: " + str(text_elements[i-2]["y0"]) + "    fontname: " + text_elements[i-1]["fontname"] + "    common font name: " + common_fontname + "    font size: " + str(text_elements[i-1]["font_size"]) + "    common font size: " + str(common_font_size))

            if check_no_normal_text_on_line(i, current_y0, text_elements, common_fontname):
                heading_detected = True
                j = i
                while is_same_line(text_elements[j]["y0"], current_y0):
                    if previous_x1 is not None and text_elements[j]["x0"] > previous_x1 + 1:
                        temp_heading += " "
                    temp_heading += text_elements[j]["text"]
                    previous_x1 = text_elements[j]["x1"]
                    j += 1
                
                print("Sub Heading: ", temp_heading, "and font size: ", font_size)
                i = j - 1

        if heading_detected and i < len(text_elements) and not is_same_line(text_elements[i]["y0"], previous_y0) and len(temp_heading.strip()) > 0 and any(char.isalpha() for char in temp_heading):
            heading_detected = False
            # print("temp heading: ", temp_heading)
            
            headings.append(temp_heading.strip())
            temp_heading = ""

        # if i == 6973:
        #     print("\n\n\nThis is the text at index 6973: ", text_elements[i]["text"], "\n\n\n")
        i += 1
    print("\n\n\nheadings: ", headings, "\n\n\n")
    
    
    return headings

def filter_headings(text_elements, common_font_size, second_common_font_size, common_fontname, pdf_path):
    headings = []

    punctuation_except_periods = string.punctuation.replace(".", "")
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    running_number_headings = False
    running_roman_headings = False
   
    if has_columns(text_elements, pdf_path):
        print("Has Columns")
        
    else:
        print("***Running Number Filter Headings***") 
        i = 0

        while i < len(text_elements):
            element = text_elements[i]
            font_size = round(element["font_size"])
            font_name = element["fontname"]
            char = element["text"]
            current_y0 = element["y0"]
            previous_y0 = text_elements[i-1]["y0"] if i > 0 else None
            no_title_exceptions = True

            if not is_same_line(current_y0, previous_y0) and font_size >= common_font_size:
                if check_no_normal_text_on_line(i, current_y0, text_elements, common_fontname):
                    temp = ""
                    for k in range(10):
                        if (i + k) < len(text_elements):
                            temp += text_elements[i + k]["text"]
                    if temp.strip().lower() == "references":
                        print("---------------NUMBER Breaking!!!----------------")
                        break

            if not is_same_line(current_y0, previous_y0):
                # print("\n Level 1 Passed\n")
                if font_name != common_fontname and char in digits and font_size >= common_font_size:
                    # print("\n Level 2 Passed\n")
                    if text_elements[i+1]["text"] not in punctuation_except_periods:
                        # print("\n Level 3 Passed\n")
                        if check_no_normal_text_on_line(i, current_y0, text_elements, common_fontname):
                            print("\n Level 4 Passed\n")

                            k = i+1
                            while k < i + 6:
                                print("text: ", text_elements[k]["text"])
                                # print("is alphabetical letter: ", text_elements[k]["text"].isalpha() == False)
                                if text_elements[k]["text"] != "." and (font_size < common_font_size or not text_elements[k]["text"].isalpha()):
                                    # print("Num: ", text, text_elements[i]["text"])
                                    no_title_exceptions = False
                                k += 1
                            
                            print("\n\nboolean value: ", no_title_exceptions, "\n\n")
                            if no_title_exceptions:
                                print("----------Identified NUMBER Pattern Sequence----------")
                                running_number_headings = True
                                print("+- 10 elements discovered: ", text_elements[i-10:i+10])
                                print("\nelement discovered: ", text_elements[i])
                                print("\n\ncurrent y0: ", current_y0, "compared with pervious y0: ", previous_y0, "\n\n")
                                # print("\n\nelement font: ", font_size, "compared to normal font size: ", common_font_size, "\n\n")
                                
                                headings = filter_number_headings(text_elements, common_font_size, second_common_font_size, common_fontname, headings, digits)
                                # Skip the processed elements
                                break
            i += 1

    if not running_number_headings:
        if has_columns(text_elements, pdf_path):
            print("Has Columns")
        else:
            print("***Running IEEE Filter Headings***")
            found_roman_numeral = False
            found_alphabetical_letter = False
            i = 0
            while i < len(text_elements):
                element = text_elements[i]
                current_y0 = element["y0"]
                previous_y0 = text_elements[i-1]["y0"] if i > 0 else None

                if not is_same_line(text_elements[i]["y0"], previous_y0):
                    temp = ""
                    for k in range(10):
                        if (i + k) < len(text_elements):
                            if text_elements[i+k]["text"].isupper() or font_name != common_fontname:
                                # print("Reference elements: ", text_elements[i+k])
                                temp += text_elements[i + k]["text"]
                            else:
                                break
                    if temp.strip().lower() == "references":
                        print("\nREFERENCES DETECTED\n")
                        print("---------------IEEE Breaking!!!----------------")
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
                
                if found_roman_numeral and found_alphabetical_letter:
                    print("----------Identified IEEE Pattern Sequence----------")
                    running_roman_headings = True 
                    headings = filter_ieee_headings(text_elements, common_font_size, common_fontname, headings)
                    break

                i += 1
    
    if not running_number_headings and not running_roman_headings:
        print("----------Identified FONTNAME & FONTSIZE Pattern Sequence----------") 
        font_sizes = extract_font_sizes(text_elements)
        unique_font_sizes, most_common_font_size = get_unique_font_sizes_and_most_common(font_sizes)
        main_heading_font_size, sub_heading_font_size = identify_key_font_sizes(unique_font_sizes, most_common_font_size)
        
        print("\nmain heading font size: ", main_heading_font_size)
        print("sub heading font size: ", sub_heading_font_size, "\n")

        headings = filter_fontname_fontsize_headings(text_elements, main_heading_font_size, sub_heading_font_size, common_fontname, common_font_size, headings)

    return headings

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

def main(paper_title, authors, publication_info, publication_year, pdf_url):
    file_path = os.path.dirname(os.path.realpath(__file__))
    pdf_path = download_pdf(pdf_url)
    text_elements = extract_text_with_attributes(pdf_path)

    common_font_size, second_common_font_size, common_fontname = determine_common_text_attributes(text_elements)
    headings = filter_headings(text_elements, common_font_size, second_common_font_size, common_fontname, pdf_path)

    print("\n\n\nheadings before decare: ", headings, "\n\n\n")
    headings_json = {
        "paper_title": paper_title,
        "authors": authors,
        "publication_info": publication_info,
        "publication_year": str(publication_year),
        "url": pdf_url,
        "headings": headings
    }

    with open(file_path + "/headings.json", "w") as json_file:
        json.dump(headings_json, json_file, indent=4)

    print("Headings extracted and saved to headings.json")
    os.remove(pdf_path)
    print(f"Temporary PDF file removed: {pdf_path}")

# main("Intrinsic Action Tendency Consistency for Cooperative Multi-Agent Reinforcement Learning", "https://arxiv.org/pdf/2406.18152")
# main("A Decentralized Approach towards Responsible AIin Social Ecosystems", "https://ojs.aaai.org/index.php/ICWSM/article/download/19274/19046")
# main("Resolving Ethics Trade-offs in Implementing Responsible AI", "https://arxiv.org/pdf/2401.08103")
# main("Towards Socially Responsible AI: Cognitive Bias-Aware Multi-Objective Learning", "https://arxiv.org/pdf/2005.06618")
# main("A Scoping Study of Evaluation Practices for Responsible AI Tools: Steps Towards Effectiveness Evaluations", "https://arxiv.org/pdf/2401.17486")
# main("Using Explainable AI for EEG-based Reduced Montage Neonatal Seizure Detection","Dinuka Sandun Udayantha, Kavindu Weerasinghe, Nima Wickramasinghe1, Akila Abeyratne1, Kithmin Wickremasinghe2, Jithangi Wanigasinghe3, Anjula De Silva1, and Chamira Edussooriya", "Information fusion, 2020 - Elsevier", 2019, "https://arxiv.org/pdf/2406.16908")
# main("Responsible AI: Portraits with Intelligent Bibliometrics", "https://arxiv.org/pdf/2405.02846")
# main("Explainable Artificial Intelligence (XAI): Concepts, taxonomies, opportunities and challenges toward responsible AI", "AB Arrieta, N Díaz-Rodríguez, J Del Ser, A Bennetot…","Information fusion, 2020 - Elsevier", 2019, "https://arxiv.org/pdf/1910.10045")
main("Human Simulacra", "Authors", "Publications", 2023, "https://arxiv.org/pdf/2304.03442")
# import csv
# import 

# valid_pdf_paths = []
# num_errors = 0
# successes = 0
# csv_file_path = "responsible_ai_research_papers/extracted_data.csv"

# # Initialize 
# 
# with open(csv_file_path, 'r') as csvfile:
#     reader = csv.reader(csvfile)
#     header = next(reader)  # Skip the header row
#     for i, row in enumerate(reader, start=2):  # Start counting from 2 to account for the header row
#         if len(row) < 5:
#             print(f"Skipping line {i}: Invalid format {row}")
#             
#             continue
        
#         title = row[0].strip() if len(row) > 0 else "Unknown"
#         authors = row[1].strip() if len(row) > 1 else "Unknown"
#         publication_info = row[2].strip() if len(row) > 2 else "Unknown"
#         publication_year = row[3].strip() if len(row) > 3 else "Unknown"
#         url = row[4].strip() if len(row) > 4 else "Unknown"

#         print("\n\n\n---------------New Paper---------------")
#         print(f"Title: {title}")
#         print(f"URL: {url}")
#         
#         try:
#             main(title, authors, publication_info, publication_year, url)
#             successes += 1
#         except Exception as e:
#             num_errors += 1
#             print("\n\n\n**********ERROR**********")
#             print(f"Title: {title}")
#             print(f"URL: {url}")
#             print(f"Error: {e}")
#             print("\n\n\n")
#             
# print("\n\nNumber of total papers extracted: ", successes)
# print("Number of total errors: ", num_errors, "\n\n")
# 
# 
