# initial set up and imports
import os 
from typing import TypedDict, List

from agents.base_llm import OpenAILLMs
from agents.diagnosis.generalist import GeneralistLLM
from agents.diagnosis.cardiologist import CardiologistLLM
from agents.diagnosis.neurologist import NeurologistLLM
from agents.diagnosis.diagnosis_coordinator import DiagnosticCoordinator
from agents.recommendation.recommender import RecommendationLLM
from agents.schedule.scheduler import SchedulerLLM

from prompts.master.master_prompt import MASTER_PROMPT
from prompts.master.master_example import MASTER_EXAMPLE

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

os.chdir("c:\\Users\\jzou2\\Fall 2024-2025\\Project\\OptiMed")

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

class MasterLLM:
    def __init__(self):
        # Initialize Agents 
        self.master = OpenAILLMs(system_prompt=MASTER_PROMPT)

        self.diagnostic_coordinator = DiagnosticCoordinator()
        self.diagnostic_team = {
            'generalist': GeneralistLLM(),
            'neurologist' : NeurologistLLM(),
            'cardiologist' : CardiologistLLM()
        }

        self.recommender = RecommendationLLM()
        self.scheduler = SchedulerLLM()
    
    # create a master node
    def master_node(self, report: Report):
        """Coordinate initial patient information distribution"""

        patient_info = report['patient_info']
        coordinated_message = self.master(
            f"Coordinate diagnostic process for patient with info: {patient_info}"
        )
        return {"messages": [{"role": "coordinator", "content": coordinated_message}]}
    
    def diagnostic_coordinator_node(self, report: Report):
        """Diagnostic team collaboration node"""
        diagnostic_inputs = [
            self.diagnostic_team['generalist'](f"Generalist assessment: {report['patient_info']}"),
            self.diagnostic_team['neurologist'](f"Neurological assessment: {report['patient_info']}"),
            self.diagnostic_team['cardiologist'](f"Cardiovascular assessment: {report['patient_info']}")
        ]
        
        comprehensive_diagnosis = self.diagnostic_coordinator(
            f"Synthesize diagnoses: {diagnostic_inputs}"
        )
        
        return {"diagnosis": comprehensive_diagnosis}
    
    def recommender_node(self, report: Report):
        """Generate medical recommendations"""
        recommendations = self.recommender(
            f"Provide recommendations based on diagnosis: {report['diagnosis']}"
        )
        return {"recommendations": recommendations}

    def scheduler_node(self, report: Report):
        """Handle appointment scheduling"""
        appointment_options = self.scheduler(
            f"Generate appointment options for: {report['recommendations']}"
        )
        return {"appointment_details": appointment_options}
    
    def build_workflow(self):
        """Construct the workflow graph"""
        workflow = StateGraph(Report)
        
        # add master note
        workflow.add_node("master", self.master_node)
        
        # add level one nodes
        workflow.add_node("diagnostic_coordinator", self.diagnostic_coordinator_node)
        workflow.add_node("recommender", self.recommender_node)
        workflow.add_node("scheduler", self.scheduler_node)
        
        # add level one branches
        workflow.add_edge("master", "diagnostic_coordinator")
        workflow.add_edge("master", "recommender")
        workflow.add_edge("master", "scheduler")
        
        # add end states
        workflow.add_edge("recommender", END) 
        workflow.add_edge("scheduler", END) 

        # set entry point
        workflow.set_entry_point("master")
        
        # compile the graph
        return workflow.compile()
    
    def __call__(self, patient_info: str):
        workflow = self.build_workflow()
        initial_report = {
            "patient_info": patient_info,
            "messages": [],
            "diagnosis": "",
            "recommendations": "",
            "appointment_details": ""
        }

        return workflow.invoke(initial_report)


        
