from gnews_helper import *
from publish_date_detector import *

import MySQLdb
from datetime import datetime
import time
import random

def process_publish_date(db_connection, db_cursor, sql_query):
    """
    Processes rows in the 'articles' table where 'publish_date' is NULL or empty.
    Calls get_clean_text from the 'url' to get clean text, and calls extract_publish_date on clean_text
    and updates the database with the publish_date
    :param db_connection: Database connection to interact with the MySQL database.
    :param db_cursor: Database cursor to interact with the MySQL database.
    :return The number of rows processed successfully.
    """
    count = 0
    try:
        print(sql_query)
        db_cursor.execute(sql_query)
        rows = db_cursor.fetchall()

        print(f"{len(rows)} rows found in articles database table that need processing.") 
        for row in rows:
            article_id, url = row
            
            print(f"\n{article_id}: {url}")

            clean_text = get_clean_text(url)
            if clean_text is None:
                continue
            else:
                publish_date_str = extract_publish_date(clean_text)
                if publish_date_str is None: 
                    continue
                publish_date = datetime.strptime(publish_date_str, '%Y-%m-%d')

                # Update the database with the extracted `is_relevant` value
                update_sql = """
                    UPDATE articles 
                    SET publish_date = %s 
                    WHERE id = %s;
                """
                # Construct the data tuple with appropriate fields 
                data = (
                    publish_date, 
                    article_id  # Map to the `id` column for identifying the row
                )

                # Execute the update statement
                db_cursor.execute(update_sql, data)
                db_connection.commit()
            
            count += 1 
            print(f"{count} row processed. Publish date updated successfully for id: {article_id}")

            if count % 10 == 0:
                interval = int(random.uniform(3, 5))
                print(f"Sleep {interval} second(s)...")
                time.sleep(interval)
        return count
    except MySQLdb.Error as err:
        print(f"Error processing relevance and location: {err}")
        db_connection.rollback() 
        return count

def main():
    # set up logging and redirect all print to the log file (beside to the terminal)
    logger = set_up_logging('gnews_publish_date_ingestor', '/var/log/gnews/gnews_publish_date_ingestor.log')
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

    # SQL query to fetch rows where publish date is NULL for the local news 
    sql_query = """
        SELECT id, url FROM articles
        WHERE text <> '' AND is_related = 1 AND is_national = 0 AND state is not NULL AND state <> '' AND publish_date is NULL;
    """

    # SQL for national news    
    sql_query = """
        SELECT id, url FROM articles
        WHERE text <> '' AND is_related = 1 AND is_national = 1 AND publish_date is NULL;
    """

    count = process_publish_date(db_connection, db_cursor, sql_query)
    print(f"{count} rows in total processed.")

main()