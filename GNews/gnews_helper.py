import MySQLdb 
import sys
import logging

def set_up_logging(name, filepath):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(filepath)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logger.addHandler(file_handler)
    return logger

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

def close_db(db_connection, db_cursor):
    # Close the cursor and connection after use
    db_cursor.close()
    db_connection.close()