from heading_extractor import main as heading_extractor_main
from extract_text_under_headings import main as extract_text_under_headings_main 
from index_and_embed_research_papers import main as index_and_embed_research_papers_main

import csv
import logging

valid_pdf_paths = []
num_errors = 0
successes = 0
csv_file_path = "responsible_ai_research_papers/extracted_data.csv"

# Initialize logging
logging.basicConfig(filename='process.log', level=logging.DEBUG)

with open(csv_file_path, 'r') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # Skip the header row
    for i, row in enumerate(reader, start=2):  # Start counting from 2 to account for the header row
        if len(row) < 5:
            print(f"Skipping line {i}: Invalid format {row}")
            logging.error("Skipping line %d: Invalid format %s", i, row)
            continue
        
        title = row[0].strip() if len(row) > 0 else "Unknown"
        authors = row[1].strip() if len(row) > 1 else "Unknown"
        publication_info = row[2].strip() if len(row) > 2 else "Unknown"
        publication_year = row[3].strip() if len(row) > 3 else "Unknown"
        url = row[4].strip() if len(row) > 4 else "Unknown"

        print("\n\n\n---------------New Paper---------------")
        print(f"Title: {title}")
        print(f"URL: {url}")
        logging.debug("\n\n\n---------------New Paper---------------")
        logging.debug("Title: %s", title)
        logging.debug("URL: %s", url)
        
        try:
            heading_extractor_main(title, authors, publication_info, publication_year, url)
            extract_text_under_headings_main()
            index_and_embed_research_papers_main()

            successes += 1
        except Exception as e:
            num_errors += 1
            print("\n\n\n**********ERROR**********")
            print(f"Title: {title}")
            print(f"URL: {url}")
            print(f"Error: {e}")
            print("\n\n\n")
            logging.error("\n\n\n**********ERROR**********")
            logging.error("Title: %s", title)
            logging.error("URL: %s", url)
            logging.error("Error: %s", e)

print("\n\nNumber of total papers extracted: ", successes)
print("Number of total errors: ", num_errors, "\n\n")
logging.debug("\n\nNumber of total papers extracted: %s", successes)
logging.debug("Number of total errors: %s\n\n", num_errors)
