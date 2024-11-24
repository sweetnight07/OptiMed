import os 

# go to workspace directory
from dotenv import load_dotenv
load_dotenv()
os.chdir(os.getenv('WORKSPACE_DIRECTORY'))

from typing import List 

from agents.base_llm import OpenAILLMs


from prompts.all_system import RECOMMENDATION_SYSTEM_PROMPT
from prompts.all_template import RECOMMENDATION_TEMPLATE

from langchain.agents import Tool

from utils.cdc_web_scraper import CDCWebScraper

class RecommendationLLM():
    def __init__(self):
        # collect the tools
        self.recommendation_tools = [
            Tool(
                name="search_cdc_online",
                func=self.search_cdc,
                description="searches the CDC for more information"
            )
        ]

        self.recommender = OpenAILLMs(tools=self.recommendation_tools, system_prompt=RECOMMENDATION_SYSTEM_PROMPT, template=RECOMMENDATION_TEMPLATE, agent_role="Recommendation Agent")

    # call the llm after it builds the prompt
    def __call__(self, report):
       return self.recommender(report)
    
    # format the prompt
    def search_cdc(self, query):
        """Input Parameters: the query"""
        webscraper = CDCWebScraper()

        try:
            webscraper.update_and_extract_search_url(query)
            webscraper.select_source()  # Select the first source result
            output = webscraper.extract_content_from_source()  # Extract content from the source page
        except Exception as e:
            output = f"Error occurred: {str(e)}"
        finally:
            webscraper.close()

        return output