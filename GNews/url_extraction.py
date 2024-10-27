import json
import csv
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from gnews_util import GNews
from googlenewsdecoder import new_decoderv1


def decode_url(source_url):
    try:
        decoded_url = new_decoderv1(source_url)
        if decoded_url.get("status"):
            # print("Decoded URL:", decoded_url["decoded_url"])
            return decoded_url["decoded_url"]
        else:
            print("Error:", decoded_url["message"])
    except Exception as e:
        print(f"Error occurred: {e}")

def fetch_articles_for_site(site_name, site_url, query, start_date, end_date):
    news_client = GNews(
        language="en", 
        country="US",
        start_date=start_date,  # Start date
        end_date=end_date       # End date
    )

    # Fetch news articles for the current site
    query_with_site = query + "%20" + site_name
    print("Query with Site: ", query_with_site)
    news_articles = news_client.get_news(query_with_site)
    articles_data = []

    for article in news_articles:
        article_url = decode_url(article['url'])
        full_article = news_client.get_full_article(article_url)
        if full_article:
            # Collect the article's details
            article_info = {
                "title": full_article.title,
                "author": full_article.authors,
                "text": full_article.text,
                "publish_date": full_article.publish_date.isoformat() if full_article.publish_date is not None else None,
                "keywords": full_article.keywords,
                "summary": full_article.summary,
                "site": site_name,
                "site_url": site_url,
                "url": article_url
            }
            articles_data.append(article_info)
        else:
            print(f"Failed to extract article from {article_url}")
    return articles_data

def main():
    output_json_file = "extracted_articles.json"
    sites_file = "top50_news_sites.csv" 
    query = "Opioid Crisis"
    articles_data = []
    start_date = (2024, 10, 8)
    end_date = (2024, 10, 15)

    # Open the CSV file and read the list of news sites
    with open(sites_file, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = list(csv.reader(file))  # Load CSV data

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(fetch_articles_for_site, row[0], row[1], query, start_date, end_date)
            for row in csv_reader
        ]

        for future in as_completed(futures):
            try:
                articles_data.extend(future.result())  # Append the results
            except Exception as exc:
                print(f"Generated an exception: {exc}")

    # Save the extracted data into a JSON file
    with open(output_json_file, 'w', encoding='utf-8') as json_file:
        json.dump(articles_data, json_file, ensure_ascii=False, indent=4)

    print("Articles have been successfully extracted and stored in 'extracted_articles.json'")

main()
