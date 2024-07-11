import os
import csv
from bs4 import BeautifulSoup

google_pages_dir = "google-pages/xai_pages"
output_file = "responsible_ai_research_papers/xai_extracted_data.csv"

# Initialize counters and a set for unique entries
count = 0
pdf_count = 0
unique_entries = set()

# Open the CSV file for writing
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write the header row
    csvwriter.writerow(['Name', 'Authors', 'Publication Info', 'Year', 'URL'])

    # Loop through the HTML files and extract data
    for i in range(1, 51):
        file_path = os.path.join(google_pages_dir, f"p{i}.html")
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            elements = soup.select('.gs_r.gs_or.gs_scl')
            for element in elements:
                name = element.select_one('.gs_rt a').text
                try:
                    url = element.select_one('.gs_ctg2').parent['href']
                except:
                    url = ''
                try:
                    authors_info = element.select_one('.gs_a').text
                    authors_part, publication_info_part = authors_info.split(' - ', 1)
                    publication_info1, year = publication_info_part.rsplit(', ', 1)
                    year, publication_info2 = year.split(' -', 1)
                    publication_info = publication_info1 + " -" + publication_info2
                except:
                    authors_part = 'Unknown'
                    publication_info = 'Unknown'
                    year = 'Unknown'

                # Create a tuple of the extracted data
                entry = (name, authors_part, publication_info, year, url)

                # Check if the entry is unique
                if entry not in unique_entries:
                    unique_entries.add(entry)
                    csvwriter.writerow(entry)
                    count += 1
                    if url != '':
                        pdf_count += 1

# Uncomment the following lines if you want to print the totals
# print("\nTotal: ", count)
# print("Total PDF: ", pdf_count)
