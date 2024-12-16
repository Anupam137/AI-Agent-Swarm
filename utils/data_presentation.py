from tabulate import tabulate
from typing import Dict, Any

def format_company_data(web_data: Dict[str, Any], db_data: Dict[str, Any]) -> str:
    """
    Format company data from web and database sources into a nice table.
    """
    try:
        # Prepare the data for tabulation
        table_data = []
        
        # Add web search data
        for phone, email in zip(
            web_data.get('phone_numbers', ['Not found']),
            web_data.get('emails', ['Not found'])
        ):
            table_data.append([
                web_data.get('company_name', 'N/A'),
                phone,
                email,
                'Web Search'
            ])
        
        # Add database data
        for phone, email in zip(
            db_data.get('phone_numbers', ['Not found']),
            db_data.get('emails', ['Not found'])
        ):
            table_data.append([
                db_data.get('company_name', 'N/A'),
                phone,
                email,
                'Database'
            ])
        
        # Create the table
        headers = ['Company Name', 'Phone Number', 'Email', 'Source']
        return tabulate(table_data, headers=headers, tablefmt='grid')
        
    except Exception as e:
        return f"Error formatting data: {str(e)}" 