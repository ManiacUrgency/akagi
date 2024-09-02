import os

import json
import requests
from bs4 import BeautifulSoup

def load_json(json_file_path):
    """Load JSON data from a file."""
    with open(json_file_path, 'r') as file:
        return json.load(file)

def scrape_article(url):
    """Scrape the main content of a news article from a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.content, 'html.parser')

        # Attempt to extract the main content; adjust selectors as needed
        # This part may need customization based on the structure of the article
        paragraphs = soup.find_all('p')
        article_content = ' '.join([p.get_text() for p in paragraphs])

        return article_content if article_content else "Content not found or unable to scrape."
    except Exception as e:
        return f"Error scraping {url}: {e}"

def main():
    # Load the JSON file with news articles
    file_path = os.path.dirname(os.path.realpath(__file__))
    json_file_path = file_path + '/news_articles.json'
    articles = load_json(json_file_path)

    # Iterate over each article in the JSON
    for article in articles:
        title = article.get('title', 'No Title')
        url = article.get('url', '')

        print(f"\nTitle: {title}")
        print(f"URL: {url}")

        # Scrape and print the article content
        if url:
            content = scrape_article(url)
            print(f"Content:\n{content}")
        else:
            print("No URL found for this article.")

if __name__ == "__main__":
    main()
