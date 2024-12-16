from agency_swarm.tools import BaseTool
from pydantic import Field
from tabulate import tabulate

class DataPresenterTool(BaseTool):
    """
    A tool that combines and presents company information from different sources in a table format.
    """
    web_data: dict = Field(
        ..., description="Company data from web search"
    )
    db_data: dict = Field(
        ..., description="Company data from database"
    )

    def run(self):
        """
        Combines and presents the data in a nice table format
        """
        try:
            # Prepare the data for tabulation
            table_data = []
            
            # Add web search data
            for phone, email in zip(
                self.web_data.get('phone_numbers', ['Not found']),
                self.web_data.get('emails', ['Not found'])
            ):
                table_data.append([
                    self.web_data.get('company_name', 'N/A'),
                    phone,
                    email,
                    'Web Search'
                ])
            
            # Add database data
            for phone, email in zip(
                self.db_data.get('phone_numbers', ['Not found']),
                self.db_data.get('emails', ['Not found'])
            ):
                table_data.append([
                    self.db_data.get('company_name', 'N/A'),
                    phone,
                    email,
                    'Database'
                ])
            
            # Create the table
            headers = ['Company Name', 'Phone Number', 'Email', 'Source']
            table = tabulate(table_data, headers=headers, tablefmt='grid')
            
            return table
            
        except Exception as e:
            return f"Error presenting data: {str(e)}"

if __name__ == "__main__":
    web_data = {
        "company_name": "Example Corp",
        "phone_numbers": ["123-456-7890"],
        "emails": ["contact@example.com"],
        "source": "Web Search"
    }
    db_data = {
        "company_name": "Example Corp",
        "phone_numbers": ["987-654-3210"],
        "emails": ["info@example.com"],
        "source": "Database"
    }
    tool = DataPresenterTool(web_data=web_data, db_data=db_data)
    print(tool.run()) 