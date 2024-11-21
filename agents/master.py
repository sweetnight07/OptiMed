# initial set up and imports
import os 
os.chdir("c:\\Users\\jzou2\\Fall 2024-2025\\Project\\OptiMed")
from typing import TypedDict, List, Annotated
from operator import add
import uuid

from agents.base_llm import OpenAILLMs
from agents.user_interaction.user_inputter import UserLLM


from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

from agents.diagnosis.diagnosis_coordinator import DiagnosticCoordinator
from agents.recommendation.recommender import RecommendationLLM
from agents.schedule.scheduler import SchedulerLLM

from prompts.all_system_message import MASTER_SYSTEM_PROMPT
from prompts.all_template import MASTER_TEMPLATE

from langchain.agents import Tool

class Report(TypedDict):
    """
    Defines the state for the multi-agent workflow
    Includes messages, patient input, and workflow states
    """
    patient_input: str
    messages: Annotated[List[dict], add]
    diagnosis: str
    recommendations: str
    appointment_details: str

class MasterWorkflow:
    def __init__(self):
        # initial report
        self.initial_report = {
            "patient_input" : "",
            "messages" : [],
            "diagnosis" : "",
            "recommendations" : "",
            "appointment_details" : ""
        }
        # create thred id 
        self.thread_id = str(uuid.uuid4())

        # current report 
        self.current_report = self.initial_report.copy()

        # initialize llm agents
        self.master = OpenAILLMs(system_prompt=MASTER_SYSTEM_PROMPT, agent_role="Main Orchestrator")
        self.user_inputter = UserLLM()

        # build the workflow
        self.build_workflow()

    # testing purposes        
    def test_call(self):
        # Construct the full input by combining the master template, current report, and prompt
        full_input = f"""{MASTER_TEMPLATE}

Current Report:
{str(self.current_report)}
(END OF FORM)

"""
        master_response = self.master(full_input)
        return master_response
    
    # this node is the entry so it is invoked there   
    def master_node(self, report: Report):
        # Construct the full input by combining the master template, current report, and prompt
        full_input = f"""{MASTER_TEMPLATE}
Here Is The Current Report:
{str(report)}
(END OF FORM)
"""
        # Add a message from the master
        report['messages'].append({
            "role": "master", 
            "content": "Analyzing patient information"
        })

        self.master(full_input)
        # return the thingy
        return report
        
    # only have access to the patent 
    def user_node(self, report: Report):
        # gets the summary 
        user_input = self.user_inputter() # has a template filled should pass in the report laters 
        
        # the summary is now the patient info hypothetically 
        report['patient_input'] = user_input

        report['messages'].append({
            "role": "user", 
            "content": user_input
        })

        return report


    def build_workflow(self):
        """ Construct the workflow using"""
        workflow = StateGraph(Report)

        workflow.add_node("master", self.master_node)
        workflow.add_node("user", self.user_node)

        workflow.set_entry_point("master")

        # bidirectional information will go to users 
        workflow.add_edge("master", "user")
        workflow.add_edge("user", "master")

        checkpointer = MemorySaver()

        # # routing logic
        # def route_master(report: Report):
        #     """Determine the next node"""
        #     last_master_message = report['messages'][-1]['content'] if report['message'] else ""

        #     if "user" in last_master_message.lower():
        #         return "user"
        
        # # add the conditional edges
        # workflow.add_conditional_edges(
        #     "master",
        #     route_master
        # )

        checkpointer = MemorySaver()

        self.app = workflow.compile(checkpointer=checkpointer)

    def run(self, max_iterations = 5):
        """
        Run the workflow with a maximum number of iterations
        """
        report = self.initial_report.copy()
        # update report

        # has config
        config = {
            "configurable": {
                "thread_id": self.thread_id
            }
        }
        
        result = self.app.invoke(report, config=config)

        report = result
        return report


