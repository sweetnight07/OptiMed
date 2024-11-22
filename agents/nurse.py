import os 

# go to workspace directory
from dotenv import load_dotenv
load_dotenv()
os.chdir(os.getenv('WORKSPACE_DIRECTORY'))

from agents.base_llm import OpenAILLMs


from prompts.all_system import NURSE_SYSTEM_PROMPT
from prompts.all_template import NURSE_TEMPLATE
from prompts.all_examples import NURSE_EXAMPLE

from langchain.agents import Tool

class NurseLLM():
    def __init__(self):
        # get users 

        self.nurse_tools = [
            Tool(
                name="get_user_input",
                func=self.get_user_input,
                description="Prompts the user for input and returns their response."
            )
        ]

        self.user = OpenAILLMs(system_prompt=NURSE_SYSTEM_PROMPT, template=NURSE_TEMPLATE, tools=self.nurse_tools, agent_role="Nurse Agent")


    # call the llm after it builds the prompt
    def __call__(self, input):
       return self.user(input, NURSE_EXAMPLE)
    
    # receives input from the users.
    def get_user_input(self, prompt: str) -> str:
        """Get input from user with the provided prompt"""
        return input(f"{prompt}\nYour response: ")
