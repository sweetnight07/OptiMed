import os 
os.chdir("c:\\Users\\jzou2\\Fall 2024-2025\\Project\\OptiMed")

from agents.base_llm import OpenAILLMs
import data.patient_information as data
from langchain.agents import Tool
from prompts.generalist.generalist_prompt import generalist_prompt
from prompts.generalist.generalist_example import GENERALIST_EXAMPLE

class NeurologistLLM():
    def __init__(self):
        # collect the tools
        self.tools = [
            Tool(
                name="access_patient_history",
                func=self.access_patient_history,
                description="Access and analyze patient's historical medical records. Input should be a patient ID string."
            ),
            Tool(
                name="referral_recommendation",
                func=self.make_referral_recommendation,
                description="Generate specialist referrals based on patient assessment. Input should be a JSON string containing symptoms and risk factors."
            )
        ]

        # create the prompt for the call
        self.generalist_prompt = generalist_prompt

        self.generalist = OpenAILLMs(self.tools, agent_role='Neurologist')

    # call the llm after it builds the prompt
    def __call__(self, patient_id: str, symptoms: str):
        prompt = self.build_generalist_prompt(patient_id, symptoms,  GENERALIST_EXAMPLE)
        return self.generalist(prompt)

    # format the prompt
    def build_generalist_prompt(self, patient_id, symptoms, examples) -> str:
        return self.generalist_prompt.format(
                            patient_id = patient_id,
                            symptoms = symptoms, 
                            examples = examples)
    
    # create the tools
    def access_patient_history(self, patient_id) -> str:
        """Access patient history from the mock database."""
        if patient_id in data.mock_patient_database:
            return str(data.mock_patient_database[patient_id]["medical_history"])
        return "No patient history found."

    # make referral system
    def make_referral_recommendation(self, input_str) -> str:
        """Analyze symptoms and make referral recommendations for either a cardiologist or neruologist."""
        return f"Based on the provided symptoms and history: {input_str}, here are the referral recommendations..."