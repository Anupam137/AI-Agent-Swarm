from company_data_agency.custom_agent import CustomAgent
from company_data_agency.database_agent.tools.database_search_tool import DatabaseSearchTool
from typing import List, Dict

class DatabaseAgent(CustomAgent):
    def __init__(self):
        super().__init__(
            name="DatabaseAgent",
            description="Agent responsible for searching company information in the MySQL database.",
            instructions="company_data_agency/database_agent/instructions.md",
            tools=[],  # Initialize with empty tools list
            temperature=0.5,
            model="mixtral-8x7b-32768"
        )
        
    async def process_message(self, message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """Process a message and update tool with the company name before processing."""
        # Extract company name from the message
        # This is a simple implementation - you might want to make it more sophisticated
        company_name = message.strip()
        
        # Create a new tool instance with the current company name
        db_search_tool = DatabaseSearchTool(company_name=company_name)
        
        # Update tools list
        self.tools = [db_search_tool]
        
        # Process the message using the parent class method
        return await super().process_message(message, conversation_history) 