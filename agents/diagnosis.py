import os 

# go to workspace directory
from dotenv import load_dotenv
load_dotenv()
os.chdir(os.getenv('WORKSPACE_DIRECTORY'))

from typing import List 

from agents.base_llm import OpenAILLMs


from prompts.all_system import DIAGNOSIS_SYSTEM_PROMPT
from prompts.all_template import DIAGNOSIS_TEMPLATE

from langchain.agents import Tool

from utils.vector_database import PDFVectorDatabase

class DiagnosisLLM():
    def __init__(self):
        # set up the utils 
        self.vector_database = PDFVectorDatabase()
        self.vector_database.add_pdf_directory('data\diagnosis')
        self.vector_database.load_pdfs()
        self.vector_database.build_database()

        # set up diagnosis tools 
        self.diagnostic_tools = [
            Tool(
                name="search database",
                func=self.search_database,
                description="Takes in a query and extracts relevant information from the database."
            ),
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

    # call the llm after it builds the prompt
    def __call__(self, report):
       return self.diagnosis(report)
    


        