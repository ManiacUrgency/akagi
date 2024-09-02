import json
import os

from gnews import GNews
import newspaper
import nltk
nltk.download('punkt_tab')
#For extracting original link from Google Redirect link
import re
import urllib.parse

def get_articles(keyword):
    google_news = GNews()

    google_news.start_date = (2024, 8, 30)
    google_news.end_date = (2024, 8, 31)
    google_news.max_results = 2

    # Fetch news based on the specified query
    articles = google_news.get_news(keyword)
    print("Length of output list:", len(articles))

    print("\nArticles:\n", articles)

    return articles
    # Dump the result dictionary to a JSON-formatted string and print it
    # with open("news_articles.json", "w") as json_file:
    #     json.dump(articles, json_file, indent=4)  # `indent=4` for pretty printing

def extract_original_url(google_news_url):
    # Step 1: Decode the Google News URL
    decoded_url = urllib.parse.unquote(google_news_url)

    # Step 2: Use a regular expression to find the actual URL within the redirect link
    url_match = re.search(r'(https?://[^\s]+)', decoded_url)
    
    if url_match:
        # Step 3: Extract and clean up the original URL
        original_url = url_match.group(0).split('&')[0]  # Splitting to remove any trailing parameters
        return original_url
    else:
        return "Original URL not found."

def get_articles_data(json_file_path, articles):
    print("\n\n\nUsing Newspaper4k\n\n\n")

    articles_data = []

    for art in articles:
        google_redirect_url = art['url']
        print("url: ", google_redirect_url)
        url = extract_original_url(google_redirect_url)
        print("\nOriginal URL: ", url)
        article = newspaper.article(url)

        article.download()
        article.parse()
        article.nlp()
        print("\n\n\nArticle: ", article)
        print("\nArticle Title: \n", article.title)
        # Extract desired attributes
        article_info = {
            "title": article.title,
            "authors": article.authors,
            "text": article.text,
            "publish_date": str(article.publish_date),  # Convert to string to avoid JSON serialization issues
            "keywords": article.keywords,
            "summary": article.summary,
            "url": url
        }

        # Append to the list of articles
        articles_data.append(article_info)

    with open(json_file_path, "w") as json_file:
        json.dump(articles_data, json_file, indent=4)

    print("\nArticles saved to news_articles.json")

def main():
    file_path = os.path.dirname(os.path.realpath(__file__))
    json_file_path = file_path + "/articles-output-data/news_articles.json"

    keyword = "Opioid Crisis"
    articles = get_articles(keyword)
    get_articles_data(json_file_path, articles)

main()