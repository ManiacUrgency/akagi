import json
from text_extractor import main as text_extractor_main

def extract_text_under_headings(json_file, text_file, output_file):
    # Step 1: Read the JSON file
    try:
        with open(json_file, "r") as f:
            data = json.load(f)
        print("JSON file read successfully.")
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return
    
    # Extracting required data from JSON
    try:
        paper_title = data.get("paper_title", "Unknown Title")
        authors = data.get("authors", [])
        publication_info = data.get("publication_info", "Unknown Info")
        publication_year = data.get("publication_year", "Unknown Year")
        url = data.get("url", "Unknown URL")
        headings = data.get("headings", [])
        print("Extracted required data from JSON.")
    except Exception as e:
        print(f"Error extracting data from JSON: {e}")
        return

    # Debugging: Print the loaded JSON data
    print("Loaded JSON data:", headings)
    try:
        text_extractor_main(url)
        print("\nCalled text_extractor\n")
    except:
        print("Failed to extract link!")
    # Step 2: Read the raw text file
    try:
        with open(text_file, "r") as f:
            raw_text = f.read()
        print("Raw text file read successfully.")
    except Exception as e:
        print(f"Error reading text file: {e}")
        return

    # Step 3: Initialize the extracted text for each heading
    extracted_data = [{"title": heading, "text": ""} for heading in headings]
    print("Initialized extracted data:", extracted_data)

    # Step 4: Extract text under each heading using string matching
    for i, heading in enumerate(extracted_data):
        title = heading["title"]
        start_pos = raw_text.find(title)
        if start_pos != -1:
            start_pos += len(title)
            if i + 1 < len(extracted_data):
                next_title = extracted_data[i + 1]["title"]
                end_pos = raw_text.find(next_title, start_pos)
                if end_pos == -1:
                    end_pos = len(raw_text)
            else:
                end_pos = len(raw_text)
            
            extracted_text = raw_text[start_pos:end_pos].strip()
            heading["text"] = extracted_text

            # Debugging: Print extracted text
            print(f"Extracted text for {title}: {extracted_text[:100]}...")
        else:
            print(f"Title '{title}' not found in raw text.")

    # Step 5: Write the output to a JSON file
    try:
        with open(output_file, "w") as f:
            json.dump({
                "paper_title": paper_title,
                "publication_info": publication_info,
                "authors": authors,
                "publication_year": publication_year,
                "url": url,
                "headings": extracted_data
            }, f, indent=4)
        print(f"JSON file created successfully: {output_file}")
    except Exception as e:
        print(f"Error writing JSON file: {e}")

def main():
    # Usage
    json_file = "headings.json"
    text_file = "raw_text.txt"
    output_file = "headings_with_text.json"
    extract_text_under_headings(json_file, text_file, output_file)

main()