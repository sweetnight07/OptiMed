import os 

# go to workspace directory
from dotenv import load_dotenv
load_dotenv()
os.chdir(os.getenv('WORKSPACE_DIRECTORY'))

from typing import List 

from agents.base_llm import OpenAILLMs
from tools import CDCSearchTool
from prompts.all_system import RECOMMENDATION_SYSTEM_PROMPT
from prompts.all_template import RECOMMENDATION_TEMPLATE

from langchain.agents import Tool

class RecommendationLLM():
    def __init__(self):
        # collect the tools
        self.cdc_tool = CDCSearchTool()

        self.recommendation_tools = [
            Tool(
                name=self.cdc_tool.name,
                func=self.cdc_tool._run,
                description=self.cdc_tool.description
            )
        ]
        
        self.recommender = OpenAILLMs(
            tools=self.recommendation_tools,
            system_prompt=RECOMMENDATION_SYSTEM_PROMPT, 
            template=RECOMMENDATION_TEMPLATE, 
            agent_role="Recommendation Agent")

    # call the llm after it builds the prompt
    def __call__(self, report):
       return self.recommender(report)
