import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Create and return a database connection using environment variables."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE')
        )
        return connection
    except mysql.connector.Error as e:
        raise Exception(f"Database connection failed: {str(e)}")

def execute_query(query: str, params: tuple = None):
    """Execute a database query and return the results."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        results = cursor.fetchall()
        return results
    
    except mysql.connector.Error as e:
        raise Exception(f"Query execution failed: {str(e)}")
    
    finally:
        cursor.close()
        connection.close() 