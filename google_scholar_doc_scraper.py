import os
from bs4 import BeautifulSoup

google_pages_dir = "google-pages"
count = 0
pdf_count = 0
for i in range(1, 16):
    file_path = os.path.join(google_pages_dir, f"p{i}.html")
    #print("\n\nParsing file ", i)
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        elements = soup.select('.gs_r.gs_or.gs_scl')
        for element in elements:
            name = element.select_one('.gs_rt a:link').text
            try:
                url = element.select_one('.gs_ctg2').parent['href']
            except:
                url = ''
            count += 1
            if url != '':
                pdf_count += 1
            line = f'"{name}",{url}'
            print(line)
# print("\nTotal: ", count)
# print("Total PDF: ", pdf_count)