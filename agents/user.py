import os 
os.chdir("c:\\Users\\jzou2\\Fall 2024-2025\\Project\\OptiMed")

from agents.base_llm import OpenAILLMs


from prompts.all_system_message import USER_SYSTEM_PROMPT
from prompts.all_template import USER_TEMPLATE

from langchain.agents import Tool

class UserLLM():
    def __init__(self):
        # get users 

        self.user_tools = [
            Tool(
                name="get_user_input",
                func=self.get_user_input,
                description="Prompts the user for input and returns their response."
            )
        ]

        self.user = OpenAILLMs(system_prompt=USER_SYSTEM_PROMPT, tools=self.user_tools, agent_role="User Interaction Agent")


    # call the llm after it builds the prompt
    def __call__(self):
       
       full_input = f"""{USER_TEMPLATE}"""

       return self.user(full_input)
    
    # receives input from the users.
    def get_user_input(self, prompt: str) -> str:
        """Get input from user with the provided prompt"""
        return input(f"{prompt}\nYour response: ")
