# initial set up and imports
import os 

# go to workspace directory
from dotenv import load_dotenv
load_dotenv()
os.chdir(os.getenv('WORKSPACE_DIRECTORY'))

from typing import TypedDict, List, Annotated
from operator import add
import uuid

from agents.base_llm import OpenAILLMs
from agents.nurse import NurseLLM
from agents.diagnosis import DiagnosisLLM


from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END

# from agents.diagnosis import DiagnosisLLM
# from agents.recommender import RecommendationLLM
# from agents.scheduler import SchedulerLLM

from prompts.all_system import MASTER_SYSTEM_PROMPT
from prompts.all_template import MASTER_TEMPLATE

from langchain.agents import Tool

class Report(TypedDict):
    """
    Defines the state for the multi-agent workflow
    Includes messages, patient info, and workflow states
    """
    patient_info: str
    messages: Annotated[List[dict], add]
    diagnosis: str
    recommendations: str
    appointment_details: str

class MasterWorkflow:
    def __init__(self):
        # initial report
        self.initial_report = {
            "patient_info" : "",
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
        self.master_agent = OpenAILLMs(system_prompt=MASTER_SYSTEM_PROMPT, template=MASTER_TEMPLATE, agent_role="Master Agent")
        self.nurse_agent = NurseLLM()
        self.diagnosis_agent = DiagnosisLLM()

        # build the workflow
        self.build_workflow()
    
    # this node is the entry so it is invoked there   
    def master_node(self, report: Report):
        # Construct the full input by combining the master template, current report, and prompt
        # Add a message from the master

        output = self.master_agent(report)

        # routing purposes 
        report['messages'].append({
            "role": "master", 
            "content": output
        })
        # return the thingy
        return report
        
    # only have access to the patent 
    def nurse_node(self, report: Report):
        # gets the summary 
        nurse_input = self.nurse_agent(report) # has a template filled should pass in the report laters 
        
        # the summary is now the patient info hypothetically 
        report['patient_info'] = nurse_input

        report['messages'].append({
            "role": "nurse", 
            "content": nurse_input
        })

        return report
    
    def diagnosis_node(self, report: Report):
        diagnosis_output = self.diagnosis_agent(report) # need

        report['diagnosis'] = diagnosis_output

        report['messages'].append({
            "role": "diagnosis", 
            "content": diagnosis_output
        })

        return report
        
    def build_workflow(self):
        """ Construct the workflow using"""
        workflow = StateGraph(Report)

        workflow.add_node("master node", self.master_node)
        workflow.add_node("nurse node", self.nurse_node)
        workflow.add_node("diagnosis node", self.diagnosis_node)

        workflow.set_entry_point("master node")

        # Routing logic
        def route_master(report: Report):
            """Determine the next node based on master's output"""
            last_master_message = report['messages'][-1]['content'] if report['messages'] else ""
            
            if "NURSE" in last_master_message.upper():
                return "nurse node"
            elif "DIAGNOSIS" in last_master_message.upper():
                  return "diagnosis node"
            else:
                return "master node"  # Stay in master node if no clear routing

        # Add conditional edges
        workflow.add_conditional_edges(
            "master node",
            route_master
        )

        # bidirectional information will go to users 
        workflow.add_edge("nurse node", "master node")
        workflow.add_edge("diagnosis node", "master node")

        checkpointer = MemorySaver()

        self.app = workflow.compile(checkpointer=checkpointer)

    def run(self):
        """
        Run the workflow with a maximum number of iterations
        """
        report = self.initial_report.copy()
        # has config
        config = {
            "configurable": {
                "thread_id": self.thread_id
            }
        }
        
        result = self.app.invoke(report, config=config)

        report = result
        return report
    
    # for testing purpose
        # testing purposes        
    def test_call(self, report: Report):
        # Construct the full input by combining the master template, current report, and prompt

        master_response = self.master_agent(str(report))
        return master_response

    def test_run(self, report: Report):
        """
        Run the workflow with a maximum number of iterations
        """
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


