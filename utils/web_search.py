from duckduckgo_search import DDGS
import re
from typing import Dict, List, Union

def search_company(company_name: str) -> Dict[str, Union[str, List[str]]]:
    """
    Search for company information using DuckDuckGo.
    Returns a dictionary with company name, phone numbers, and emails.
    """
    # Search query to specifically look for contact information
    query = f"{company_name} company contact information phone email"
    
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
        
        return {
            "company_name": company_name,
            "phone_numbers": list(phone_numbers) if phone_numbers else ["Not found"],
            "emails": list(emails) if emails else ["Not found"],
            "source": "Web Search"
        }
        
    except Exception as e:
        return {
            "company_name": company_name,
            "phone_numbers": ["Error occurred"],
            "emails": ["Error occurred"],
            "source": "Web Search",
            "error": str(e)
        } 