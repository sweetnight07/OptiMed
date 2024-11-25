# import other packages
import os 
from dotenv import load_dotenv

# import langchina packages
from langchain.agents import Tool

# import my file
from agents.agent import MyAgent

from prompts.all_system import RECOMMENDATION_SYSTEM_PROMPT
from prompts.all_template import RECOMMENDATION_TEMPLATE

from tools.tool import CDCSearchTool

class RecommendationAgent():
    def __init__(self):
        """
        initializes the recommender agent
        """
        # set up the environment
        self._setup_environment()

        # collect the tools
        self.cdc_tool = CDCSearchTool()

        # set up recommendation tools
        self.recommendation_tools = [
            Tool(
                name=self.cdc_tool.name,
                func=self.cdc_tool,
                description=self.cdc_tool.description
            )
        ]
        
        # create the recommedation agent
        self.recommender = MyAgent(
            tools=self.recommendation_tools,
            system_prompt=RECOMMENDATION_SYSTEM_PROMPT, 
            template=RECOMMENDATION_TEMPLATE, 
            agent_role="Recommendation Agent")

    def _setup_environment(self):
        """load environment variables and set workspace directory and optionally returns keys."""
        load_dotenv()
        workspace_directory = os.getenv('WORKSPACE_DIRECTORY')

        if not workspace_directory:
            raise ValueError("WORKSPACE_DIRECTORY not set in environment variables")
        
        os.chdir(workspace_directory)

    def __call__(self, report):
       return self.recommender(report)
