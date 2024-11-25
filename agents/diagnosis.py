# import other packages
import os 
from dotenv import load_dotenv

# import langcahin packages 
from langchain.agents import Tool

# import my file
from agents.agent import MyAgent

from prompts.all_system import DIAGNOSIS_SYSTEM_PROMPT
from prompts.all_template import DIAGNOSIS_TEMPLATE
from prompts.all_examples import DIAGNOSIS_EXAMPLES

from tools.tool import SearchDatabaseTool
from tools.tool import SearchOnlineTool

class DiagnosisAgent():
    def __init__(self, directory_path: str):
        """
        initializes the diagnosis agent
        """
        # set up the environment
        self._setup_environment()

        # set up directory path
        self.directory_path = directory_path

        # collect tools
        self.search_database_tool = SearchDatabaseTool(self.directory_path)
        self.search_online_tool = SearchOnlineTool()

        # set up diagnosis tools 
        self.diagnostic_tools = [
            Tool(
                name=self.search_database_tool.name,
                func=self.search_database_tool._run,
                description=self.search_database_tool.description
            ),
            Tool(
                name=self.search_online_tool.name,
                func=self.search_online_tool._run,
                description=self.search_online_tool.description
            ),
        ]

        # create the diagnosis agent
        self.diagnosis = MyAgent(tools=self.diagnostic_tools,
                                  system_prompt=DIAGNOSIS_SYSTEM_PROMPT, 
                                  template=DIAGNOSIS_TEMPLATE, 
                                  agent_role="Diagnosis Agent")

    def _setup_environment(self):
        """load environment variables and set workspace directory and optionally returns keys."""
        load_dotenv()
        workspace_directory = os.getenv('WORKSPACE_DIRECTORY')

        if not workspace_directory:
            raise ValueError("WORKSPACE_DIRECTORY not set in environment variables")
        
        os.chdir(workspace_directory)

    def __call__(self, report):
       return self.diagnosis(report, examples=DIAGNOSIS_EXAMPLES)
    


        