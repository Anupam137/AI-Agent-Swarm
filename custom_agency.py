import os
import asyncio
from typing import List, Dict, Any, Optional
from .custom_agent import CustomAgent

class CustomAgency:
    def __init__(
        self,
        agents: List[CustomAgent],
        communication_flows: List[List[CustomAgent]],
        shared_instructions: Optional[str] = None
    ):
        self.agents = agents
        self.communication_flows = communication_flows
        self.shared_instructions = self._load_shared_instructions(shared_instructions) if shared_instructions else ""

    def _load_shared_instructions(self, instructions_path: str) -> str:
        """Load shared instructions from a markdown file."""
        # Get the absolute path of the current file
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Remove any leading ./ from the instructions path
        if instructions_path.startswith('./'):
            instructions_path = instructions_path[2:]
        
        # Combine the paths
        full_path = os.path.join(current_dir, instructions_path)
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Warning: Could not find shared instructions file at {full_path}")
            return "No shared instructions available."

    def _can_communicate(self, sender: CustomAgent, receiver: CustomAgent) -> bool:
        """Check if two agents can communicate based on communication flows."""
        return any(flow[0] == sender and flow[1] == receiver for flow in self.communication_flows)

    async def process_message(self, message: str) -> str:
        """Process a message through the agency's agents."""
        try:
            # First, get results from web search and database agents
            web_result = await self.agents[0].process_message(message)  # Web search agent
            db_result = await self.agents[1].process_message(message)   # Database agent
            
            # Prepare data for the presenter agent
            data = {
                'web_data': eval(web_result) if isinstance(web_result, str) else web_result,
                'db_data': eval(db_result) if isinstance(db_result, str) else db_result
            }
            
            # Send combined data to presenter agent
            final_result = await self.agents[2].process_message(str(data))  # Presenter agent
            return final_result
            
        except Exception as e:
            return f"Error processing request: {str(e)}"

    def run_sync(self, message: str) -> str:
        """Run the agency synchronously."""
        return asyncio.run(self.process_message(message)) 