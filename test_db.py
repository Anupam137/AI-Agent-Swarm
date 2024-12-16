import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

try:
    print("Database Connection Settings:")
    print(f"Host: {os.getenv('MYSQL_HOST')}")
    print(f"User: {os.getenv('MYSQL_USER')}")
    print(f"Database: {os.getenv('MYSQL_DATABASE')}")
    
    # Connect to MySQL database
    connection = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )
    
    print("\nConnection successful!")
    
    cursor = connection.cursor(dictionary=True)
    
    # Show all tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("\nTables in database:")
    for table in tables:
        table_name = list(table.values())[0]
        print(f"- {table_name}")
        
        # Show structure of each table
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        print("  Columns:")
        for column in columns:
            print(f"  - {column['Field']} ({column['Type']})")
        
        # Show sample data
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
        samples = cursor.fetchall()
        print("  Sample data:")
        for sample in samples:
            print(f"  - {sample}")
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print("\nError:", str(e)) 