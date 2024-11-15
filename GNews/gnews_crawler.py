import hashlib
import sys
import json
import csv
from datetime import datetime
import time
import random
#from concurrent.futures import ThreadPoolExecutor, as_completed

from gnews_util import GNews
from googlenewsdecoder import new_decoderv1
import MySQLdb 

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

def fetch_articles_for_site(site_name, site_url, query, start_date, end_date, db_connection, db_cursor):
    news_client = GNews(
        language="en", 
        country="US",
        start_date=start_date,  
        end_date=end_date      
    )

    # Fetch news articles for the current site
    query_with_site = query + "%20" + site_name
    print("Query with Site: ", query_with_site)
    news_articles = news_client.get_news(query_with_site)

    print("\nnews_articles:")
    print(json.dumps(news_articles, indent=4, ensure_ascii=False)) 

    articles_data = []

    total_sleep_time_so_far = 0
    TOTAL_SLEEP_TIME_TO_TRIGGER_ADDITIONAL_SLEEP = 45

    count = 0 
    for article in news_articles:
        article_url = decode_url(article['url'])

    

        print("\n>>> Fetching url: ", article_url)
        full_article = news_client.get_full_article(article_url)
        if full_article:
            # Collect the article's details
            article_info = {
                "title": full_article.title,
                "author": full_article.authors,
                "text": full_article.text,
                "publish_date": full_article.publish_date.strftime("%Y-%m-%d %H:%M:%S") if full_article.publish_date is not None else None,
                "keywords": full_article.keywords,
                "summary": full_article.summary,
                "site": site_name,
                "site_url": site_url,
                "url": article_url
            }
            print("\nArticle Info:")
            print(json.dumps(article_info, indent=4, ensure_ascii=False))

            insert_article(db_cursor, db_connection, article_info)

            if count > 1: 
                sys.exit(0)
            count += 1

            # Add random delay between requests
            interval = random.uniform(5, 10)
            total_sleep_time_so_far += interval
            print(f"Sleep for {interval} second(s)...")
            time.sleep(interval)

            if total_sleep_time_so_far >= TOTAL_SLEEP_TIME_TO_TRIGGER_ADDITIONAL_SLEEP:
                # Sleep an extra number of seconds 
                interval = random.uniform(5, 10)
                print(f"Slept for at least 45 seconds total. Sleep for additional {interval} second(s)...")
                time.sleep(interval)
                total_sleep_time_so_far = 0
        else:
            print(f"Failed to extract article from {article_url}")
            sys.exit(0)
    return articles_data

def md5(url):
    return hashlib.md5(url.encode('utf-8')).hexdigest()

def init_db(): 
    # Connect to MySQL database
    try:
        db_connection = MySQLdb.connect(
            host="localhost",
            user="lodge", 
            password="rabig!2109",
            database="gnews"
        )
        print("Successfully connected to MySQL database")
        db_cursor = db_connection.cursor()
    except MySQLdb.connector.Error as err:
        print(f"Error connecting to MySQL database: {err}")
        sys.exit(1)
    return db_connection, db_cursor

def insert_article(db_connection, db_cursor, article):
    try:
        # Example SQL query to insert a row
        sql_query = """
            INSERT INTO articles (
                id,
                title,
                author,
                text,
                publish_date,
                keywords,
                summary,
                site,
                site_url,
                url
            ) VALUES (
                UUID(),
                %s,  -- title
                %s,  -- author (JSON string)
                %s,  -- text
                %s,  -- publish_date
                %s,  -- keywords (JSON string)
                %s,  -- summary
                %s,  -- site
                %s,  -- site_url
                %s,   -- url
                %s  -- hashed_url
            );
        """ 
        # Data to insert into the table
        data = (
            article['title'],
            article['author'],
            article['text'],
            article['publish_date'],
            article['keywords'],
            article['summary'],
            article['site'],
            article['site_url'], 
            article['url'],
            md5(article['url'])
        )
        
        # Execute the query
        db_cursor.execute(sql_query, data)
        
        # Commit the transaction
        db_connection.commit()
        
        print("Row inserted successfully")
        
    except MySQLdb.Error as err:
        print(f"Error inserting row: {err}")
        db_connection.rollback()  # Rollback in case of an error


def is_not_in_articles(db_connection, db_cursor, article):
    sql_query = """
        SELECT count(*) FROM articles 
        WHERE hashed_url = %s;
    """
    data = (md5(article['url']))
    db_cursor.execute(sql_query, data)
    result = db_cursor.fetchone()
    if result[0] == 1:
        return True
    else:
        return False


def close_db(db_connection, db_cursor):
    # Close the cursor and connection after use
    db_cursor.close()
    db_connection.close()

def main():
    sites_file = "top50_news_sites.csv" 
    query = "Opioid Crisis"
    articles_data = []
    start_date = (2024, 10, 8)
    end_date = (2024, 10, 10)

    db_connection, db_cursor = init_db()

    # Open the CSV file and read the list of news sites
    with open(sites_file, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = list(csv.reader(file))  # Load CSV data

    for row in csv_reader:
        fetch_articles_for_site(row[0], row[1], query, start_date, end_date, db_connection, db_cursor)

    # Notes: we should not use parallel processing. This will send too many requests at a burst
    # causing Google to throttle and block us. 
    # 
    # # Use ThreadPoolExecutor for parallel processing
    # with ThreadPoolExecutor(max_workers=10) as executor:
    #     futures = [
    #         executor.submit(fetch_articles_for_site, row[0], row[1], query, start_date, end_date)
    #         for row in csv_reader
    #     ]

    #     for future in as_completed(futures):
    #         try:
    #             articles_data.extend(future.result())  # Append the results
    #         except Exception as exc:
    #             print(f"Generated an exception: {exc}")

    print("Articles have been processed'")

main()

# We will save for each news site two files for each month .... save it to a folder 
# it needs tom make into run at any time, never repeat any work, also incremental getting more articles.
# 
