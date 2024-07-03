import os
import csv
from bs4 import BeautifulSoup

google_pages_dir = "google-pages"
output_file = "extracted_data.csv"

# Initialize counters
count = 0
pdf_count = 0

# Open the CSV file for writing
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write the header row
    csvwriter.writerow(['Name', 'Authors', 'Publication Info', 'Year', 'URL'])

    # Loop through the HTML files and extract data
    for i in range(1, 16):
        file_path = os.path.join(google_pages_dir, f"p{i}.html")
        #print("\n\nParsing file ", i)
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
                    year, publication_info2= year.split(' -', 1)
                    publication_info = publication_info1 + " -" + publication_info2
                except:
                    authors_part = 'Unknown'
                    publication_info = 'Unknown'
                    year = 'Unknown'

                count += 1
                if url != '':
                    pdf_count += 1
                # Write the extracted data to the CSV file
                csvwriter.writerow([name, authors_part, publication_info, year, url])

# Uncomment the following lines if you want to print the totals
# print("\nTotal: ", count)
# print("Total PDF: ", pdf_count)
