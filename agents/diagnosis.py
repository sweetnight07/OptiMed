import os 

# go to workspace directory
from dotenv import load_dotenv
load_dotenv()
os.chdir(os.getenv('WORKSPACE_DIRECTORY'))

from agents.base_llm import OpenAILLMs


from prompts.all_system import DIAGNOSIS_SYSTEM_PROMPT
from prompts.all_template import DIAGNOSIS_TEMPLATE

from langchain.agents import Tool

mock_patient_info = """
John Doe, a 45-year-old male, reports experiencing persistent chest pain, shortness of breath, occasional dizziness, and fatigue for the past two weeks. His medical history includes hypertension diagnosed five years ago, managed with medication, and borderline high cholesterol with no current treatment. He has a family history of heart disease, as his father suffered a heart attack at age 50. He has no known allergies.
"""

class DiagnosisLLM():
    def __init__(self):
        # set up the utils 
        

        # set up diagnosis tools 
        self.diagnostic_tools = [
            Tool(
                name="search online",
                func=self.search_online,
                description="Prompts the user for input and returns their response."
            ),
            Tool(
                name="view database "
            )
        ]

        self.diagnosis = OpenAILLMs(system_prompt=DIAGNOSIS_SYSTEM_PROMPT, template=DIAGNOSIS_TEMPLATE, agent_role="Diagnosis Agent")

    def search_online(self, query):
        return

    # call the llm after it builds the prompt
    def __call__(self, report):
       return self.diagnosis(report)
    


        