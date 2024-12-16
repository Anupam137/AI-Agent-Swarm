from agency_swarm.tools import BaseTool
from pydantic import Field
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseSearchTool(BaseTool):
    """
    A tool that searches for company information in a MySQL database.
    """
    company_name: str = Field(
        ..., description="The name of the company to search for in the database"
    )

    def run(self):
        """
        Searches for company information in the MySQL database.
        """
        print(f"\nSearching database for company: {self.company_name}")
        
        try:
            # Connect to MySQL database
            print("Connecting to database...")
            print(f"Host: {os.getenv('MYSQL_HOST')}")
            print(f"User: {os.getenv('MYSQL_USER')}")
            print(f"Database: {os.getenv('MYSQL_DATABASE')}")
            
            connection = mysql.connector.connect(
                host=os.getenv('MYSQL_HOST'),
                user=os.getenv('MYSQL_USER'),
                password=os.getenv('MYSQL_PASSWORD'),
                database=os.getenv('MYSQL_DATABASE')
            )
            
            print("Database connection successful!")
            cursor = connection.cursor(dictionary=True)
            
            try:
                # First, let's see what tables we have
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print("\nAvailable tables:", tables)
                
                # Search in the test table
                query = """
                    SELECT Company_Name, Phone_Number 
                    FROM test 
                    WHERE Company_Name LIKE %s
                """
                print(f"\nExecuting query: {query} with parameter: %{self.company_name}%")
                
                cursor.execute(query, (f"%{self.company_name}%",))
                result = cursor.fetchone()
                
                print(f"Query result: {result}")
                
                if result:
                    return {
                        "company_name": result['Company_Name'],
                        "phone_numbers": [result['Phone_Number']] if result['Phone_Number'] else ["Not found"],
                        "emails": ["Not available"],  # Email is not in the table
                        "source": "Database"
                    }
                else:
                    print(f"No results found for company: {self.company_name}")
                    return {
                        "company_name": self.company_name,
                        "phone_numbers": ["Not available in db"],
                        "emails": ["Not available"],
                        "source": "Database"
                    }
            
            except mysql.connector.Error as e:
                print(f"Database query error: {str(e)}")
                return {
                    "company_name": self.company_name,
                    "phone_numbers": ["Database query failed"],
                    "emails": ["Not available"],
                    "source": "Database",
                    "error": f"Query Error: {str(e)}"
                }
            
            finally:
                cursor.close()
                connection.close()
                print("Database connection closed.")
                
        except mysql.connector.Error as e:
            print(f"Database connection error: {str(e)}")
            return {
                "company_name": self.company_name,
                "phone_numbers": ["Database connection failed"],
                "emails": ["Not available"],
                "source": "Database",
                "error": f"Connection Error: {str(e)}"
            }
        except Exception as e:
            print(f"General error: {str(e)}")
            return {
                "company_name": self.company_name,
                "phone_numbers": ["Database error"],
                "emails": ["Not available"],
                "source": "Database",
                "error": f"General Error: {str(e)}"
            }

if __name__ == "__main__":
    # Test the tool
    tool = DatabaseSearchTool(company_name="Tesla")
    result = tool.run()
    print("\nTest result:", result) 