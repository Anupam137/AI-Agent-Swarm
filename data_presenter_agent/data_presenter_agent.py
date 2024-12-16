from company_data_agency.custom_agent import CustomAgent
from company_data_agency.data_presenter_agent.tools.data_presenter_tool import DataPresenterTool
from typing import List, Dict

class DataPresenterAgent(CustomAgent):
    def __init__(self):
        super().__init__(
            name="DataPresenterAgent",
            description="Agent responsible for combining and presenting company information in a table format.",
            instructions="company_data_agency/data_presenter_agent/instructions.md",
            tools=[],  # Initialize with empty tools list
            temperature=0.5,
            model="mixtral-8x7b-32768"
        )
        
    async def process_message(self, message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """Process a message and update tool with the data before processing."""
        # Try to extract data from the message
        # The message should be in the format of a dictionary string containing web_data and db_data
        try:
            # Simple string to dict conversion - in production you'd want more robust parsing
            data = eval(message)
            web_data = data.get('web_data', {})
            db_data = data.get('db_data', {})
            
            # Create a new tool instance with the current data
            presenter_tool = DataPresenterTool(web_data=web_data, db_data=db_data)
            
            # Update tools list
            self.tools = [presenter_tool]
            
            # Process the message using the parent class method
            return await super().process_message("Please present the company data in a table format", conversation_history)
            
        except Exception as e:
            print(f"Error processing data in DataPresenterAgent: {str(e)}")
            return f"Error processing data: {str(e)}" 