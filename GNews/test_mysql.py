import sys
import MySQLdb 

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


def insert_row(db_connection, db_cursor):
    try:
        # Example SQL query to insert a row
        sql_query = """
            INSERT INTO test (
                id,
                title,
                number
            ) VALUES (
                UUID(),
                %s, 
                %s  
            );
        """ 
        # Data to insert into the table
        data = ('value1', 123)
        
        # Execute the query
        db_cursor.execute(sql_query, data)
        
        # Commit the transaction
        db_connection.commit()
        
        print("Row inserted successfully")
        
    except MySQLdb.Error as err:
        print(f"Error inserting row: {err}")
        db_connection.rollback()  # Rollback in case of an error

def close_db(db_connection, db_cursor):
    # Close the cursor and connection after use
    db_cursor.close()
    db_connection.close()

def main():
    db_connection, db_cursor = init_db()
    insert_row(db_connection, db_cursor)
    close_db(db_connection, db_cursor)    

main()