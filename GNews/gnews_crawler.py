import hashlib
import sys
import json
import csv
from datetime import datetime
import time
import random

from gnews_util import GNews
from googlenewsdecoder import new_decoderv1
import MySQLdb 
import logging
from datetime import datetime, timedelta

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
    print(f">>>>> Query with Site: {site_name}")
    news_articles = news_client.get_news(query_with_site)

    print(f"Found {len(news_articles)} article(s)")
    #print(json.dumps(news_articles, indent=4, ensure_ascii=False)) 

    total_sleep_time_so_far = 0
    TOTAL_SLEEP_TIME_TO_TRIGGER_ADDITIONAL_SLEEP = 45

    total_count = len(news_articles)
    count_found_in_db = 0
    count_fetched = 0
    count_inserted_not_fetched = 0 
    for article in news_articles:
        #print("article: ", article)
        article_url = decode_url(article['url'])

        if article_url is not None and article_url != '' and is_in_articles(db_cursor, article_url):
            count_found_in_db += 1
            print(f">>> Do NOT fetch article. It's already in database. url: {article_url}")
        else:
            print(f">>> Fetching article: \"{article['title']}\" at {article_url}")
            full_article = news_client.get_full_article(article_url)
            if full_article:
                count_fetched += 1
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
                #print("\nArticle Info:")
                #print(json.dumps(article_info, indent=4, ensure_ascii=False))

                print(f"Fetched. Inserting article on publish date: {article_info['publish_date']}")
                insert_article(db_connection, db_cursor, article_info)

                # Add random delay between requests
                interval = random.uniform(5, 10)
                print(f"Sleep for {interval} second(s)...")
                time.sleep(interval)
                total_sleep_time_so_far += interval
                if total_sleep_time_so_far >= TOTAL_SLEEP_TIME_TO_TRIGGER_ADDITIONAL_SLEEP:
                    # Sleep an extra number of seconds 
                    interval = random.uniform(5, 10)
                    print(f"Slept for at least 45 seconds total. Sleep for additional {interval} second(s)...")
                    time.sleep(interval)
                    total_sleep_time_so_far = 0
            else:
                count_inserted_not_fetched += 1
                if article['published date'] is not None:
                    parsed_date = datetime.strptime(article['published date'], "%a, %d %b %Y %H:%M:%S %Z")
                    publish_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    publish_date = None
                # Set a few attributes, so we can re-crawl later by checking if text field is NULL
                article_info = {
                    "title": article['title'],
                    "author": None,
                    "text": None,
                    "publish_date": publish_date,
                    "keywords": None,
                    "summary": None,
                    "site": site_name,
                    "site_url": site_url,
                    "url": article_url
                } 
                print(json.dumps(article_info, indent=4, ensure_ascii=False)) 
                print(f"Failed to fetch article at url: {article_url}. Inserting article on Publish date: {publish_date}")
                insert_article(db_connection, db_cursor, article_info)

    print(f">>>>> Done with site:{site_name}")    
    print(f"total:{total_count}, fetched:{count_fetched}, found in db:{count_found_in_db}, inserted not fetched:{count_inserted_not_fetched}")
    return (total_count, count_fetched, count_found_in_db, count_inserted_not_fetched)

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
                url,
                hashed_url
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
            json.dumps(article['author']) if article['author'] else '[]',
            article['text'],
            article['publish_date'],
            json.dumps(article['keywords']) if article['keywords'] else '[]',
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
        
        print(f"Row inserted successfully")
        
    except MySQLdb.Error as err:
        print(f"Error inserting row: {err}")
        db_connection.rollback()  # Rollback in case of an error


def is_in_articles(db_cursor, article_url):
    try:
        sql_query = """
            SELECT count(*) FROM articles 
            WHERE hashed_url = %s;
        """
        data = (md5(article_url), ) # need a comma to pass as tuple
        db_cursor.execute(sql_query, data)
        result = db_cursor.fetchone()
        if result[0] == 0: # should be either 0 or 1
            return False
        else:
            return True
    except MySQLdb.Error as err:
        print(f"Error select count from articles: {err}") 
        return True  # Conservative approach: assume article exists to avoid duplicates

def close_db(db_connection, db_cursor):
    # Close the cursor and connection after use
    db_cursor.close()
    db_connection.close()

def set_up_logging():
    logger = logging.getLogger('gnews_crawler')
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('/var/log/gnews/gnews_crawler.log')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logger.addHandler(file_handler)
    return logger

def main():
    # set up logging and redirect all print to the log file (beside to the terminal)
    logger = set_up_logging()
    logger.info("Logging initialized")
    # Redirect print to the custom logger
    class PrintToLog:
        def __init__(self, logger):
            self.logger = logger

        def write(self, message):
            if message.strip():  # Avoid logging empty lines
                self.logger.info(message.strip())

        def flush(self):  # Required to handle stdout flushing
            pass

    sys.stdout = PrintToLog(logger)
    sys.stderr = PrintToLog(logger)  # Redirect error messages as well
    
    db_connection, db_cursor = init_db()

    sites_file = "top50_news_sites.csv" 
    # Open the CSV file and read the list of news sites
    with open(sites_file, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = list(csv.reader(file))  # Load CSV data

    query = "Opioid Crisis"

    first_date = datetime(2023, 11, 1)
    last_date = datetime(2024, 11, 27)

    step = timedelta(days=5)
    step_four_days = timedelta(days=4)
    current_date = first_date

    total_count = 0
    count_fetched = 0
    count_found_in_db = 0
    count_inserted_not_fetched = 0
    while current_date <= last_date:
        total_count_date = 0
        count_fetched_date = 0
        count_found_in_db_date = 0 
        count_inserted_not_fetched_date = 0
        start_date = current_date
        end_date = current_date + step_four_days
        #print(f"Start Date: {start_date.strftime('%Y-%m-%d')}, End Date: {end_date.strftime('%Y-%m-%d')}")
        current_date += step

        print(f">>>>>>>>>> Crawl articles for query \"{query}\", from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

        for row in csv_reader:
            #row[0] = 'The Hill'
            #row[1] = 'https://thehill.com'
            total_count_r, count_fetched_r, count_found_in_db_r, count_inserted_not_fetched_r = fetch_articles_for_site(
                row[0], row[1], query, start_date, end_date, db_connection, db_cursor
            )
            total_count_date += total_count_r
            count_fetched_date += count_fetched_r
            count_found_in_db_date += count_found_in_db_r
            count_inserted_not_fetched_date += count_inserted_not_fetched_r
            #break

        print(f">>>>>>>>>> Done with dates from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        print(f"total:{total_count_date}, fetched:{count_fetched_date}, found in db:{count_found_in_db_date}, inserted not fetched:{count_inserted_not_fetched_date}")
        interval = random.uniform(10, 20)
        print(f"Sleep for {interval} second(s)...")
        #time.sleep(interval)

    print(f">>>>>>>>>>>>>>> Finished fetch all articls from {first_date.strftime('%Y-%m-%d')}, End Date: {last_date.strftime('%Y-%m-%d')}")
    print(f"total:{total_count}, fetched:{count_fetched}, found in db:{count_found_in_db}, inserted not fetched:{count_inserted_not_fetched}")

main()
