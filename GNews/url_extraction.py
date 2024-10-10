import json
from gnews_util import GNews
from googlenewsdecoder import new_decoderv1
from datetime import datetime

def decode_url(source_url):
    try:
        decoded_url = new_decoderv1(source_url)
        if decoded_url.get("status"):
            print("Decoded URL:", decoded_url["decoded_url"])
            return decoded_url["decoded_url"]
        else:
            print("Error:", decoded_url["message"])
    except Exception as e:
        print(f"Error occurred: {e}")

def main():
    # Initialize GNews client
    news_client = GNews(
        language="en", 
        country="US", 
        start_date=datetime(2024, 10, 8, 14, 30, 0),  # October 8th, 2024 at 14:30:00 (2:30 PM)
        end_date=datetime(2024, 10, 9, 16, 45, 30)    # October 9th, 2024 at 16:45:30 (4:45:30 PM)
    )
    # Fetch top news articles
    news_articles = news_client.get_news('Opioid Crisis')

    # List to store articles with details
    articles_data = []

    # Loop through the first few articles (you can limit or modify this)
    for article in news_articles:  
        # print("\n\n\nArticle:\n", article)
        # print("\nArticle URL: ", article['url'], "\n")
        article_url = decode_url(article['url'])
        
        # Get the full article content using the utility's get_full_article() method
        full_article = news_client.get_full_article(article_url)
        
        if full_article:
            # Parse the article's title, author, and text
            article_info = {
                "title": full_article.title,
                "author": full_article.authors,  # Authors are usually returned as a list
                "text": full_article.text,
                "publish_date": full_article.publish_date,
            }
            
            # Append to the list
            articles_data.append(article_info)
        else:
            print(f"Failed to extract article from {article_url}")

    # Save the extracted data into a JSON file
    with open('extracted_articles.json', 'w', encoding='utf-8') as json_file:
        json.dump(articles_data, json_file, ensure_ascii=False, indent=4)

    print("Articles have been successfully extracted and stored in 'extracted_articles.json'")

main()

# import json
# import time
# from datetime import datetime, timedelta

# from gnews_util import GNews
# from googlenewsdecoder import new_decoderv1

# def decode_url(source_url):
#     print("*Decoding URL...*")
#     try:
#         decoded_url = new_decoderv1(source_url)
#         if decoded_url.get("status"):
#             print("Decoded URL:", decoded_url["decoded_url"])
#             return decoded_url["decoded_url"]
#         else:
#             print("Error:", decoded_url["message"])
#             return None
#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return None

# def generate_intervals(year, month, start_day, end_day):
#     intervals = []
#     # Define the peak hours (hours in 24-hour format)
#     peak_hours = [
#         (6, 8),    # Early Morning (6 AM to 8 AM)
#         (8, 10),   # Morning (8 AM to 10 AM)
#         (10, 12),  # Late Morning (10 AM to 12 PM)
#         (12, 14),  # Midday (12 PM to 2 PM)
#         (14, 16),  # Afternoon (2 PM to 4 PM)
#         (16, 18),  # Late Afternoon (4 PM to 6 PM)
#         (18, 20),  # Evening (6 PM to 8 PM)
#         (20, 22),  # Night (8 PM to 10 PM)
#         (22, 24),  # Late Night (10 PM to 12 AM)
#         (0, 6)     # Early Morning (12 AM to 6 AM)
#     ]
    
#     # Generate intervals for each day in the date range
#     for day in range(start_day, end_day + 1):
#         for start_hour, end_hour in peak_hours:
#             # Handle the case where end_hour is 24 or more (next day)
#             start_time = datetime(year, month, day, start_hour)
#             if end_hour >= 24:
#                 end_time = datetime(year, month, day, 23, 59, 59)  # Set to end of day
#             else:
#                 end_time = datetime(year, month, day, end_hour)
#             intervals.append((start_time, end_time))
#     return intervals

# def main():
#     # Initialize GNews client with max_results set to 100
#     news_client = GNews(language="en", country="US", max_results=100)
    
#     # Define your query
#     query = 'Opioid Crisis'
#     year = 2023  # Use the current or past year
#     month = 10
#     start_day = 8
#     end_day = 9

#     # Generate time intervals during peak publication hours
#     intervals = generate_intervals(year, month, start_day, end_day)

#     # List to store articles with details
#     articles_data = []

#     # Set to track URLs of articles to avoid duplicates
#     seen_urls = set()

#     # Loop over each interval
#     for start_time, end_time in intervals:
#         print(f"\nTime Interval: {start_time} to {end_time}\n")

#         # Set the date range for the current interval
#         news_client.start_date = start_time
#         news_client.end_date = end_time

#         # Fetch news articles for the current interval
#         news_articles = news_client.get_news(query)
#         print(f"Number of articles found: {len(news_articles)}")

#         # Check if articles were found
#         if not news_articles:
#             print("No articles found for this interval.")
#             continue

#         # Loop through the articles
#         for article in news_articles:
#             print("Processing article...")
#             article_url = article['url']
#             print("Current URL: ", article_url)
#             # Check for duplicates
#             if article_url in seen_urls:
#                 continue  # Skip if we've already seen this URL
#             seen_urls.add(article_url)

#             # Decode the article URL
#             decoded_url = decode_url(article_url)
#             if not decoded_url:
#                 continue  # Skip if decoding failed

#             # Get the full article content
#             full_article = news_client.get_full_article(decoded_url)

#             if full_article:
#                 # Parse the article's title, author, and text
#                 article_info = {
#                     "title": full_article.title,
#                     "author": full_article.authors,  # Authors are usually returned as a list
#                     "text": full_article.text
#                 }

#                 # Append to the list
#                 articles_data.append(article_info)

#                 # Break if we've collected 1000 articles
#                 if len(articles_data) >= 1000:
#                     break
#             else:
#                 print(f"Failed to extract article from {decoded_url}")

#         # Break the outer loop if we've collected 1000 articles
#         if len(articles_data) >= 1000:
#             break

#         # Sleep to avoid rate limiting
#         time.sleep(1)  # Adjust the duration as needed

#     # Save the extracted data into a JSON file
#     with open(f'extracted_articles_{year}_{month}_{start_day}_to_{end_day}.json', 'w', encoding='utf-8') as json_file:
#         json.dump(articles_data, json_file, ensure_ascii=False, indent=4)

#     print(f"Articles have been successfully extracted and stored in 'extracted_articles_{year}_{month}_{start_day}_to_{end_day}.json'")

# main()
