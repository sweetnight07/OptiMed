# initial set up and imports
import os 
os.chdir("c:\\Users\\jzou2\\Fall 2024-2025\\Project\\OptiMed")
from typing import TypedDict, List

from agents.base_llm import OpenAILLMs

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

from agents.diagnosis.diagnosis_coordinator import DiagnosticCoordinator
from agents.recommendation.recommender import RecommendationLLM
from agents.schedule.scheduler import SchedulerLLM

from prompts.all_system_message import MASTER_SYSTEM_PROMPT
from prompts.all_template import MASTER_TEMPLATE

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

        # create the system and promt pt for master
        # self.master_prompt = master_prompt
        # self.user_prompt = user_prompt
        # format the template
        self.current_report = {
            "patient_info" : "",
            "messages" : [],
            "diagnosis" : "",
            "recommendation" : "",
            "appointment_details" : ""
        }

        # self.template = master_template.format(form=initial_report) # this works 

        self.master = OpenAILLMs(system_prompt=MASTER_SYSTEM_PROMPT, agent_role="Main Orchestrator")
        
        # Set up the ChatPromptTemplate with the TEMPLATE

        # self.user_interaction = OpenAILLMs(system_prompt=USER_SYSTEM_PROMPT)

        # level one
        # self.recommender = RecommendationLLM()
        # self.scheduler = SchedulerLLM()
        # self.diagnostic_coordinator = DiagnosticCoordinator()

    def __call__(self, prompt: str = None):
        # Construct the full input by combining the master template, current report, and prompt
        full_input = f"""{MASTER_TEMPLATE}

Current Report:
{str(self.current_report)}
(END OF FORM)

User Prompt:
{prompt or ''}
"""
        return self.master(full_input)

    # def master_node(self, report: Report):
    #     """Coordinate and delegate the workflow based on structured prompt response"""
    #     master_prompt = self.build_master_prompt(report, MASTER_EXAMPLE)
    #     master_message = self.master(master_prompt)
        
    #     # Extract the next agent from the response
    #     next_agent = None
    #     if "NEXT AGENT:" in master_message:
    #         next_agent = master_message.split("NEXT AGENT:")[1].split("\n")[0].strip()
        
    #     return {
    #         "messages": [{"role": "main coordinator", "content": master_message}],
    #         "next_agent": next_agent.lower() if next_agent else "diagnosis_team"  # default fallback
    #     }
        
    # def user_interaction_node(self, report: Report): 
    #     """May ask for more information or confirmation"""
    #     current_info = report["patient_info"]
    #     # build the prompt for the user when we do need to invoke this 
    #     user_prompt = self.build_user_prompt(current_info)

    #     additional_info = self.user_interaction(user_prompt)

    #     if additional_info:
    #         report["patient_info"] += f" {additional_info}"
        
    #     # Return the updated report with new patient information
    #     print(report)
    #     return report

    #     # get additional
    # def diagnostic_coordinator_node(self, report: Report):
    #     """Diagnostic team collaboration node"""
    #     # Create a new workflow instance for diagnostics
    #     diagnostic_workflow = self.diagnostic_coordinator.build_diagnostic_workflow()
        
    #     # Initialize the diagnostic report with current state
    #     diagnostic_report = {
    #         "patient_info": report["patient_info"],
    #         "messages": report["messages"],
    #         "diagnosis": "",
    #         "recommendations": "",
    #         "appointment_details": ""
    #     }
        
    #     # Run the diagnostic workflow
    #     diagnostic_result = diagnostic_workflow.invoke(diagnostic_report)
        
    #     # Merge the diagnostic results back into the main report
    #     merged_messages = report["messages"] + diagnostic_result["messages"]

    #     print(merged_messages)
        
    #     return {
    #         "messages": merged_messages,
    #         "diagnosis": diagnostic_result.get("diagnosis", "")
    #     }

    # def recommender_node(self, report: Report):
    #     """Generate medical recommendations"""
    #     recommendations = self.recommender(
    #         f"Provide recommendations based on diagnosis: {report['diagnosis']}"
    #     )
    #     return {"recommendations": recommendations}

    # def scheduler_node(self, report: Report):
    #     """Handle appointment scheduling"""
    #     appointment_options = self.scheduler(
    #         f"Generate appointment options for: {report['recommendations']}"
    #     )
    #     return {"appointment_details": appointment_options}
    
    # def build_workflow(self):
    #     """Construct the workflow graph"""
    #     workflow = StateGraph(Report)
        
    #     # Add nodes
    #     workflow.add_node("master_coordinator", self.master_node)
    #     workflow.add_node("diagnostic_coordinator", self.diagnostic_coordinator_node)
    #     workflow.add_node("recommender", self.recommender_node)
    #     workflow.add_node("scheduler", self.scheduler_node)
    #     workflow.add_node("user_interaction", self.user_interaction_node)
        
    #     # Add edges
    #     workflow.add_edge("master_coordinator", "diagnostic_coordinator")
    #     workflow.add_edge("master_coordinator", "recommender")
    #     workflow.add_edge("master_coordinator", "scheduler")
    #     workflow.add_edge("master_coordinator", "user_interaction")
    #     workflow.add_edge("scheduler", END)

    #     def route_to_agent(state):
    #         agent_mapping = {
    #             "user_interaction": "user_interaction",
    #             "diagnosis_team": "diagnostic_coordinator",
    #             "recommendation": "recommender",
    #             "scheduler": "scheduler"
    #         }
    #         return agent_mapping.get(state.get("next_agent", "diagnosis_team"))
        
    #     # Add edges
    #     workflow.add_conditional_edges(
    #         "master_coordinator",
    #         route_to_agent,
    #         {
    #             "user_interaction": "master_coordinator",  # Return to master after gathering info
    #             "diagnostic_coordinator": "master_coordinator",
    #             "recommender": "master_coordinator",
    #             "scheduler": END
    #         }
    #     )
        
    #     workflow.set_entry_point("master_coordinator")
    #     return workflow.compile()
    
    # def __call__(self):
    #     workflow = self.build_workflow()

    #     initial_report = {
    #         "patient_info": "",
    #         "messages": [],
    #         "diagnosis": "",
    #         "recommendations": "",
    #         "appointment_details": ""
    #     }

    #     return workflow.invoke(initial_report)
    
    # # format the prompt
    # def build_master_prompt(self, form, examples) -> str:
    #     return self.master_prompt.format(
    #                         form = form,
    #                         examples = examples)
    
    # # format the prompt
    # def build_user_prompt(self, form) -> str:
    #     return self.user_prompt.format(
    #                         form = form)
    
    # def get_user_input(self, prompt: str) -> str:
    #     """Get input from user with the provided prompt"""
    #     return input(f"{prompt}\nYour response: ")




        
