import json
import os

from gnews import GNews
import newspaper
import nltk
nltk.download('punkt_tab')
#For extracting original link from Google Redirect link
import re
import urllib.parse
from serpapi import GoogleSearch

# No longer used because GNews can't return the original URL
# We also try to use selenium to get the orignal URL from the google news URL
# but we cannot get through because of Google news server recognizes and blocks our client.
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

def get_articles_serp_api(query, api_key):
    params = {
        "engine": "google_news",
        "q": query,
        "api_key": api_key
    }
    print("Start search google news for query:", query)
    search = GoogleSearch(params)
    results = search.get_dict()
    print("Search completed")
    return results["news_results"]

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

def get_articles_data(json_file_path, articles, downloaded_articles):
    print("\n\n\nUsing Newspaper4k\n\n\n")

    articles_data = []

    flat_articles = []
    for art in articles:
        #print(json.dumps(art, indent=2))
        if 'stories' in art:
            for story in art['stories']:
                # return the value of story['title'] or the default value ''
                if not downloaded_articles.get(story['title'], ''):
                    flat_articles.append(story)
        else:
            if not downloaded_articles.get(art['title'], ''): 
                flat_articles.append(art)
    print("Number of articles to crawl: ", len(flat_articles))
    
    count = 0
    for art in flat_articles:
        url = art['link']
        print("\n========== Original URL: ", url)
        title = art.get('title', '')
        authors = art.get('authors', '')
        print("Title: ", title)
        print("Author: ", authors)

        try:
            if url in downloaded_articles and downloaded_articles[url].get('text',''):
                print(">>>>> Use existing article data. No need to crawl.")
                article_info = downloaded_articles[url] 
            else:
                print(">>>>> Crawl the article.")
                article = newspaper.article(url)
                article.download()
                article.parse()
                article.nlp()

                print("\nArticle: ", article)
                print("\nArticle Title: ", article.title)
                print("\nArticles authors: ", article.authors)
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
        except Exception as e:
            print(f"\nError processing article: {e}")
            # only use SERP crawled article's meta data
            article_info = {
                "title": title,
                "authors": authors,
                "text": "",
                "publish_date": "",
                "keywords": "",
                "summary": "",
                "url": url
            }             
        finally:
            # Append to the list of articles
            articles_data.append(article_info)
            with open(json_file_path, "w") as json_file:
                json.dump(articles_data, json_file, indent=4)
            json_file.close()
            count += 1
            print("Number of files saved: ", count)

    print("\nArticles saved to news_articles.json")

def main():
    serp_api_key = os.environ["SERP_API_KEY"]

    file_path = os.path.dirname(os.path.realpath(__file__))
    json_file_path = file_path + "/articles-output-data/news_articles.json"

    import shutil
    if os.path.exists(json_file_path):
        # Create a backup file with '.bak' suffix
        backup_file_path = json_file_path + ".bak"
        shutil.copy2(json_file_path, backup_file_path)
        print(f"Backup created: {backup_file_path}")

    with open(json_file_path, "r") as json_file:
        downloaded_articles = json.load(json_file)
    # Create a hashmap of downloaded articles keyed by title with text as value
    url_keyed_downloaded_articles = {article['url']: article for article in downloaded_articles}

    query = "opioid crisis"
    articles = get_articles_serp_api(query, serp_api_key)
    get_articles_data(json_file_path, articles, url_keyed_downloaded_articles)

main()