import os
from dotenv import load_dotenv
from groq import Groq
from typing import List, Dict, Any, Optional

load_dotenv()

class CustomAgent:
    def __init__(
        self,
        name: str,
        description: str,
        instructions: str,
        tools: List[Any] = None,
        model: str = "mixtral-8x7b-32768",
        temperature: float = 0.5,
        max_tokens: int = 4000
    ):
        self.name = name
        self.description = description
        self.instructions = self._load_instructions(instructions)
        self.tools = tools or []
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))

    def _load_instructions(self, instructions_path: str) -> str:
        """Load instructions from a markdown file."""
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
            print(f"Warning: Could not find instructions file at {full_path}")
            return "No instructions available."

    def _create_system_prompt(self) -> str:
        """Create a concise system prompt."""
        prompt = f"You are {self.name}. {self.description}\n\n"
        prompt += "Available tools:\n"
        for tool in self.tools:
            prompt += f"- {tool.__class__.__name__}\n"
        return prompt

    async def process_message(self, message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """Process a message and return a response."""
        print(f"\n{self.name} processing message: {message}")
        
        system_prompt = self._create_system_prompt()
        
        # Prepare the messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add only the most recent conversation history if provided
        if conversation_history:
            # Only keep the last 2 messages to reduce context size
            messages.extend(conversation_history[-2:])
        
        # Add the current message
        messages.append({"role": "user", "content": message})
        
        print(f"\nSending request to Groq API...")
        try:
            # Get response from Groq
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            response = chat_completion.choices[0].message.content
            print(f"\nGroq API response: {response}")
            
            # Check if the response contains a tool call
            if any(tool.__class__.__name__.lower() in response.lower() for tool in self.tools):
                print("\nTool call detected in response")
                # Execute the appropriate tool
                for tool in self.tools:
                    tool_name = tool.__class__.__name__.lower()
                    if tool_name in response.lower():
                        print(f"\nExecuting tool: {tool_name}")
                        try:
                            tool_result = tool.run()
                            print(f"\nTool execution result: {tool_result}")
                            return str(tool_result)  # Ensure result is a string
                        except Exception as e:
                            error_msg = f"Error executing tool {tool_name}: {str(e)}"
                            print(f"\n{error_msg}")
                            return error_msg
            
            return response
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"\n{error_msg}")
            return error_msg

    def add_tool(self, tool: Any) -> None:
        """Add a tool to the agent."""
        self.tools.append(tool)

    def get_tools(self) -> List[Any]:
        """Get the list of available tools."""
        return self.tools