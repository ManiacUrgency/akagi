from gnews_helper import *

import MySQLdb
import csv

def export_query_to_csv(db_connection, cursor, query, output_file):
    """
    Executes a query and exports the result to a CSV file.
    
    :param db_connection: The database connection object.
    :param cursor: The cursor to exectue query.
    :param query: The SQL query to execute.
    :param output_file: The path to the CSV file to write.
    """
    try:
        cursor.execute(query)

        # Fetch all rows from the query result
        rows = cursor.fetchall()

        # Get column names from the cursor description
        column_names = [desc[0] for desc in cursor.description]

        # Open the output file for writing
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Write the header row
            writer.writerow(column_names)
            
            # Write data rows
            writer.writerows(rows)

        print(f"Data successfully exported to {output_file}")
    except MySQLdb.Error as err:
        print(f"Error: {err}")

db_connection, db_cursor = init_db()

# Output CSV file path
query = """
SELECT id, publish_date, state, site, title, url 
FROM articles WHERE text <> '' AND is_related = 1 AND is_national = 0 AND state is not NULL AND state <> '' AND publish_date >= '2021-11-01' ORDER BY publish_date asc;
"""
output_file = "articles_local_news_2021-11-01-2024-11-27.csv"
export_query_to_csv(db_connection, db_cursor, query,  output_file)

# SQL query to execute
query = """
SELECT id, publish_date, site, title, url 
FROM articles WHERE text <> '' AND is_related = 1 AND is_national = 1 AND publish_date >= '2021-11-01' ORDER BY publish_date asc;
"""
output_file = "articles_national_news_2021-11-01-2024-11-27.csv"

# Export the query result to CSV
export_query_to_csv(db_connection, db_cursor, query,  output_file)

close_db(db_connection, db_cursor)