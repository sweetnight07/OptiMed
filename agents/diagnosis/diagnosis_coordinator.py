import os 
os.chdir("c:\\Users\\jzou2\\Fall 2024-2025\\Project\\OptiMed")
from typing import TypedDict, List

from agents.base_llm import OpenAILLMs
from agents.diagnosis.cardiologist import CardiologistLLM
from agents.diagnosis.generalist import GeneralistLLM
from agents.diagnosis.neurologist import NeurologistLLM

from prompts.diagnosis_coordinator.diagnostic_prompt import DIAGNOSTIC_SYSTEM_PROMPT, diagnostic_prompt
from prompts.diagnosis_coordinator.diagnostic_example import DIAGNOSTIC_EXAMPLE

from langchain.agents import Tool
from langgraph.graph import StateGraph, END

from utils.wrapper import enforce_dict_input
class Report(TypedDict):
    """
    Defines the state for the multi-agent workflow
    Includes messages, patient info, and workflow states
    """
    patient_info: str
    messages: List[dict]
    diagnosis: str
    recommendations: str
    appointment_details: str

class DiagnosticCoordinator:
    def __init__(self, report : Report):
        # get the tools
        self.tools = [
            Tool(
                name="conclude_diagnosis",
                func=self.conclude_diagnosis,
                description="The input must be a dictionary consisting the patient info and messages from the diagnosis team. After the conversation among diagnostics concludes, form a final diagnosis"
            )
        ]

        # create the actual diagnosis coordinator
        self.diagnostic_coordinator = OpenAILLMs(self.tools, agent_role='Diagnosis Coordinator')
        self.diagnostic_coordinator_prompt = diagnostic_prompt
        
        self.report: Report = {
            'patient_info': report.get('patient_info', ''),
            'messages': report.get('messages', []),
            'diagnosis': report.get('diagnosis', ''),
            'recommendations': report.get('recommendations', ''),
            'appointment_details': report.get('appointment_details', '')
        }

        # create the agents 
        self.cardiologist = CardiologistLLM()
        self.generalist = GeneralistLLM()
        self.neurologist = NeurologistLLM()
        
    def diagnostic_node(self, report: Report):
        """Coordinate and delegate the workflow of the diagnostic team"""
        print("in diagnostic node")
        diagnostic_prompt = self.build_diagnostic_prompt(report, DIAGNOSTIC_EXAMPLE)
        diagnostic_message = self.diagnostic_coordinator(diagnostic_prompt)

        return {
            "messages": [{"role": "diagnostic coordinator", "content": diagnostic_message}],
            "diagnosis": ""  # Placeholder for final diagnosis
        }
    
    def generalist_node(self, report: Report):
        """Generalist consultation node"""
        generalist_input = self.generalist(
            f"Provide general assessment based on: {report['patient_info']}"
        )
        return {
            "messages": [{"role": "generalist", "content": generalist_input}]
        }
    
    def cardiologist_node(self, report: Report):
        """Cardiologist consultation node"""
        cardiologist_input = self.cardiologist(
            f"Provide cardiac assessment based on: {report['patient_info']}"
        )
        return {
            "messages": [{"role": "cardiologist", "content": cardiologist_input}]
        }
    
    def neurologist_node(self, report: Report):
        """Neurologist consultation node"""
        neurologist_input = self.neurologist(
            f"Provide neurological assessment based on: {report['patient_info']}"
        )
        return {
            "messages": [{"role": "neurologist", "content": neurologist_input}]
        }
    
    def build_diagnostic_workflow(self):
        """Construct the subgraph for the diagnostic team"""
        workflow = StateGraph(Report)

        # diagnostic team master node
        workflow.add_node("diagnostic_coordinator", self.diagnostic_node)
        workflow.add_node("generalist", self.generalist_node)
        workflow.add_node("cardiologist", self.cardiologist_node)
        workflow.add_node("neurologist", self.neurologist_node)

        # add the edges now 
        workflow.add_edge("diagnostic_coordinator", "generalist")
        workflow.add_edge("diagnostic_coordinator", "cardiologist")
        workflow.add_edge("diagnostic_coordinator", "neurologist")

        workflow.set_entry_point("diagnostic_coordinator")

        return workflow.compile()
    

    def __call__(self):
        # Now we initialize the workflow
        workflow = self.build_diagnostic_workflow()

        # Ensure the report is in the correct format
        print(f"Report Type: {type(self.report)}")

        # Extract the necessary fields to pass into the workflow
        report_input = {
            "patient_info": self.report.get('patient_info', ''),
            "messages": self.report.get('messages', []),
            "diagnosis": self.report.get('diagnosis', ''),
            "recommendations": self.report.get('recommendations', ''),
            "appointment_details": self.report.get('appointment_details', ''),
        }

        # Print the report input to debug the content
        print(f"Report input passed to workflow: {report_input}")

        # Invoke the workflow with the prepared input
        try:
            result = workflow.invoke(report_input)
            return result
        except Exception as e:
            print(f"Error invoking workflow: {e}")
            return None



    # format the prompt
    def build_diagnostic_prompt(self, report, examples) -> str:
        return self.diagnostic_coordinator_prompt.format(
                            form= report,
                            examples = examples)
    
    @enforce_dict_input
    def conclude_diagnosis(self, report: Report):
        """
        Compile final diagnosis from collected messages.
        Ensures the report stays consistent as a dictionary.
        """
        print(f"Type of report: {type(report)}")

        messages = report.get('messages', [])
        final_diagnosis = {"diagnosis": " ".join(msg.get('content', '') for msg in messages)}
        return final_diagnosis

