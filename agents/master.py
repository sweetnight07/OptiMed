# initial set up and imports
import os 
os.chdir("c:\\Users\\jzou2\\Fall 2024-2025\\Project\\OptiMed")
from typing import TypedDict, List

from agents.base_llm import OpenAILLMs
from agents.diagnosis.diagnosis_coordinator import DiagnosticCoordinator
from agents.recommendation.recommender import RecommendationLLM
from agents.schedule.scheduler import SchedulerLLM

from prompts.master.master_prompt import MASTER_SYSTEM_PROMPT, master_prompt
from prompts.master.master_example import MASTER_EXAMPLE

from langchain.agents import Tool
from langgraph.graph import StateGraph, END

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

class MasterWorkflow:
    def __init__(self):
        # initialize master workflow tool and prompts
        # self.tools = [
        #     Tool(
        #         name="get_user_input",
        #         func=self.get_user_input,
        #         description="Prompts the user for input and returns their response to guide the workflow or decision-making process."
        #     )
        # ]
        self.master_prompt = master_prompt

        # inner level of the open ai
        self.master = OpenAILLMs(system_prompt=MASTER_SYSTEM_PROMPT)

        # level one
        self.recommender = RecommendationLLM()
        self.scheduler = SchedulerLLM()

        # the diagnositc coordinator is created withi nthe node so that the report can be passed along 
    
    def master_node(self, report: Report):
        """Coordinate and delegate the workflow from the patient information"""
        master_prompt = self.build_master_prompt(report, MASTER_EXAMPLE)
        master_message = self.master(master_prompt)

        return {"messages": [{"role": "main coordinator", "content": master_message}]}
        
    def diagnostic_coordinator_node(self, report: Report):
        """Diagnostic team collaboration node"""
        print("Diagnostic Coordinator Node Report:", report)  # Debugging line
        self.diagnostic_coordinator = DiagnosticCoordinator(report)
        comprehensive_diagnosis = self.diagnostic_coordinator(
            f"Coordinate among the three doctors: {report['patient_info']}"
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
        workflow.add_node("master_coordinator", self.master_node)
        
        # add level one nodes
        workflow.add_node("diagnostic_coordinator", self.diagnostic_coordinator_node)
        # add later
        # workflow.add_node("recommender", self.recommender_node)
        # workflow.add_node("scheduler", self.scheduler_node)
        
        # add level one branches
        workflow.add_edge("master_coordinator", "diagnostic_coordinator")
        # add later
        # workflow.add_edge("master", "recommender")
        # workflow.add_edge("master", "scheduler")
        
        # add end states
        # workflow.add_edge("scheduler", END) 

        # set entry point
        workflow.set_entry_point("master_coordinator")
        
        # compile the graph
        return workflow.compile()
    
    def __call__(self):
        patient_info = input("Hello, we are here to help you! Please provide your age, symptoms, and patient id if available")

        workflow = self.build_workflow()

        initial_report = {
            "patient_info": patient_info,
            "messages": [],
            "diagnosis": "",
            "recommendations": "",
            "appointment_details": ""
        }

        return workflow.invoke(initial_report)
    
    # format the prompt
    def build_master_prompt(self, form, examples) -> str:
        return self.master_prompt.format(
                            form = form,
                            examples = examples)

    # a tool to get human inputs
    # def get_user_input(self, prompt):
    #     """
    #     This function is called when the agent wants to ask a question.
    #     It uses the prompt generated by the LLM and gets the user's response.
    #     """
    #     user_input = input(f"{prompt} Please provide your response: ")
    #     if not user_input.strip():
    #         print("Input cannot be empty. Please try again.")
    #         return self.get_user_input(prompt)
    #     return user_input




        
