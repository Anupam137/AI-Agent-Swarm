from company_data_agency.custom_agent import CustomAgent
from company_data_agency.web_search_agent.tools.web_search_tool import WebSearchTool
from typing import List, Dict

class WebSearchAgent(CustomAgent):
    def __init__(self):
        super().__init__(
            name="WebSearchAgent",
            description="Agent responsible for searching company information on the web using DuckDuckGo.",
            instructions="company_data_agency/web_search_agent/instructions.md",
            tools=[],  # Initialize with empty tools list
            temperature=0.5,
            model="mixtral-8x7b-32768"
        )
        
    async def process_message(self, message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """Process a message and update tool with the company name before processing."""
        # Extract company name from the message
        
        company_name = message.strip()
        
        # Create a new tool instance with the current company name
        web_search_tool = WebSearchTool(company_name=company_name)
        
        # Update tools list
        self.tools = [web_search_tool]
        
        # Process the message using the parent class method
        return await super().process_message(message, conversation_history) 
