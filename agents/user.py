import os 

# go to workspace directory
from dotenv import load_dotenv
load_dotenv()
os.chdir(os.getenv('WORKSPACE_DIRECTORY'))

from agents.base_llm import OpenAILLMs


from prompts.all_system import USER_SYSTEM_PROMPT
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

        self.user = OpenAILLMs(system_prompt=USER_SYSTEM_PROMPT, template=USER_TEMPLATE, tools=self.user_tools, agent_role="User Interaction Agent")


    # call the llm after it builds the prompt
    def __call__(self, input):
       return self.user(input)
    
    # receives input from the users.
    def get_user_input(self, prompt: str) -> str:
        """Get input from user with the provided prompt"""
        return input(f"{prompt}\nYour response: ")
