from gnews_helper import *
from news_location_detector import *

import MySQLdb
import json
import time
import random

def process_relevance_and_location(db_connection, db_cursor):
    """
    Processes rows in the 'articles' table where 'is_relevant' is NULL.
    Calls extract_relevance_and_location on 'text' and updates the database.
    :param db_connection: Database connection to interact with the MySQL database.
    :param db_cursor: Database cursor to interact with the MySQL database.
    :return The number of rows processed successfully.
    """
    count = 0
    try:
        # SQL query to fetch rows where `is_relevant` is NULL
        sql_query = """
            SELECT id, text FROM articles
            WHERE text <> '' AND is_related IS NULL;
        """
        print(sql_query)
        db_cursor.execute(sql_query)
        rows = db_cursor.fetchall()

        print(f"{len(rows)} rows found in articles database table that need processing.") 
        for row in rows:
            article_id, text = row
            
            print(f"\n{article_id}: {text}")

            # Call the function to extract relevance and location
            result_json = extract_relevance_and_location(text)
            if result_json is None: 
                continue
            
            print(f"\nresult: \n{result_json}")
            # Update the database with the extracted `is_relevant` value
            update_sql = """
                UPDATE articles 
                SET is_related = %s, 
                    is_national = %s, 
                    city = %s, 
                    state = %s, 
                    location = %s
                WHERE id = %s;
            """
            # Construct the data tuple with appropriate fields from the JSON result
            data = (
                result_json.get('isRelated'),  # Map to `is_relevant` column
                result_json.get('isNational'),  # Map to `is_national` column
                result_json.get('city'),  # Map to `city` column
                result_json.get('state'),  # Map to `state` column
                json.dumps(result_json.get('location')),  # Convert list to JSON for `location` column
                article_id  # Map to the `id` column for identifying the row
            )

            # Execute the update statement
            db_cursor.execute(update_sql, data)
            db_connection.commit()
            
            count += 1 
            print(f"{count} row processed. Relevance & location updated successfully for id: {article_id}")

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
    logger = set_up_logging('gnews_location_ingestor', '/var/log/gnews/gnews_location_ingestor.log')
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
    count = process_relevance_and_location(db_connection, db_cursor)
    print(f"{count} rows in total processed.")

main()