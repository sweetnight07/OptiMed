import os 

# go to workspace directory
from dotenv import load_dotenv
load_dotenv()
os.chdir(os.getenv('WORKSPACE_DIRECTORY'))

from typing import List 

from agents.base_llm import OpenAILLMs


from prompts.all_system import DIAGNOSIS_SYSTEM_PROMPT
from prompts.all_template import DIAGNOSIS_TEMPLATE
from prompts.all_examples import DIAGNOSIS_EXAMPLES

from langchain.agents import Tool

from utils.vector_database import PDFVectorDatabase
from utils.ddg_search_engine import DDGSearch

class DiagnosisLLM():
    def __init__(self):
        # set up the utils 
        self.vector_database = PDFVectorDatabase()
        self.vector_database.add_pdf_directory('data\diagnosis')
        self.vector_database.load_pdfs()
        self.vector_database.build_database()

        self.search_engine = DDGSearch()

        # self.web_scraper = 

        # set up diagnosis tools 
        self.diagnostic_tools = [
            Tool(
                name="search_database",
                func=self.search_database,
                description="Searchs up relevant information in the vector database."
            ),
            Tool(
                name="search_online",
                func=self.search_online,
                description="Search online for relevant information regarding the diagnosis"
            ),
            Tool(
                name="none_tool",
                func=self.none_tool,
                description="Does nothing. Serves as the 'None' tool."
            )
        ]

        self.diagnosis = OpenAILLMs(tools=self.diagnostic_tools, system_prompt=DIAGNOSIS_SYSTEM_PROMPT, template=DIAGNOSIS_TEMPLATE, agent_role="Diagnosis Agent")

    def search_database(self, query):
        """search through the vector database given a query"""
        documents = self.vector_database.search_with_metadata(query=query)
        content = self.parse_query(documents)
        return content
    
    # parse output from search database
    def parse_query(self, documents : List): 
        """extracts the content from the output query"""
        page_contents = [doc.page_content for doc in documents]
        return page_contents
    
    # search engine
    def search_online(self, query):
        """search online given a query"""
        search_result = self.search_engine.search(query)
        return search_result
    
    # define the 'none_tool' which does nothing
    def none_tool(self, *args, **kwargs):
        """A tool that does nothing and returns None."""
        return None

    # call the llm after it builds the prompt
    def __call__(self, report):
       return self.diagnosis(report, examples=DIAGNOSIS_EXAMPLES)
    


        