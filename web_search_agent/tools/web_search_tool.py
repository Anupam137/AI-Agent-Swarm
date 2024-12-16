from agency_swarm.tools import BaseTool
from pydantic import Field
from duckduckgo_search import DDGS
import re

class WebSearchTool(BaseTool):
    """
    A tool that searches for company information using DuckDuckGo search engine.
    It specifically looks for company contact information like phone numbers and email addresses.
    """
    company_name: str = Field(
        ..., description="The name of the company to search for"
    )

    def run(self):
        """
        Performs a DuckDuckGo search for the company and extracts contact information.
        """
        # Search query to specifically look for contact information
        query = f"{self.company_name} company contact information phone email"
        
        try:
            # Perform the search
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))
            
            # Initialize variables to store found information
            phone_numbers = set()
            emails = set()
            
            # Regular expressions for phone numbers and emails
            phone_pattern = r'\b(?:\+?1[-.]?)?\s*(?:\([0-9]{3}\)|[0-9]{3})[-.]?\s*[0-9]{3}[-.]?\s*[0-9]{4}\b'
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            
            # Process each search result
            for result in results:
                # Search in both title and body
                text = f"{result['title']} {result['body']}"
                
                # Find phone numbers
                phones = re.findall(phone_pattern, text)
                phone_numbers.update(phones)
                
                # Find emails
                emails_found = re.findall(email_pattern, text)
                emails.update(emails_found)
            
            # Format the results
            result_dict = {
                "company_name": self.company_name,
                "phone_numbers": list(phone_numbers) if phone_numbers else ["Not found"],
                "emails": list(emails) if emails else ["Not found"],
                "source": "Web Search"
            }
            
            return result_dict
            
        except Exception as e:
            return {
                "company_name": self.company_name,
                "phone_numbers": ["Error occurred"],
                "emails": ["Error occurred"],
                "source": "Web Search",
                "error": str(e)
            }

if __name__ == "__main__":
    tool = WebSearchTool(company_name="Example Corp")
    print(tool.run()) 