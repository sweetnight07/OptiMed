# import other packages
import os 
from dotenv import load_dotenv

# import langchain packages
from langchain.agents import Tool

# import my file
from agents.agent import MyAgent

from prompts.all_system import NURSE_SYSTEM_PROMPT
from prompts.all_template import NURSE_TEMPLATE
from prompts.all_examples import NURSE_EXAMPLES

from tools.tool import UserInputTool

class NurseAgent():
    def __init__(self):
        """
        intializes the nurse agent
        """
        # set up environemnt
        self._setup_environment()

        # collect tools
        self.user_input_tool = UserInputTool()

        # set up the nurse tools
        self.nurse_tools = [
            Tool(
                name=self.user_input_tool.name,
                func=self.user_input_tool._run,
                description=self.user_input_tool.description
            )
        ]

        # create the nurse agent
        self.nurse = MyAgent(tools=self.nurse_tools, 
                                   system_prompt=NURSE_SYSTEM_PROMPT, 
                                   template=NURSE_TEMPLATE, 
                                   agent_role="Nurse Agent")

    def _setup_environment(self):
        """load environment variables and set workspace directory and optionally returns keys."""
        load_dotenv()
        workspace_directory = os.getenv('WORKSPACE_DIRECTORY')

        if not workspace_directory:
            raise ValueError("WORKSPACE_DIRECTORY not set in environment variables")
        
        os.chdir(workspace_directory)

    def __call__(self, report):
        """ invoke the agent with the prompt with optional examples depending on template"""
        return self.nurse(report, examples=NURSE_EXAMPLES)
    
