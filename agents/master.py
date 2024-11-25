# import other packages
import os 
from dotenv import load_dotenv
from typing import TypedDict, List, Annotated
from operator import add
import uuid

# import agents 
from agents.agent import MyAgent
from agents.nurse import NurseAgent
from agents.diagnosis import DiagnosisAgent
from agents.recommender import RecommendationAgent
from agents.receptionist import ReceptionAgent

# import the prompts
from prompts.all_system import MASTER_SYSTEM_PROMPT
from prompts.all_template import MASTER_TEMPLATE
from prompts.all_examples import MASTER_EXAMPLES

# import langchain packages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from langchain.agents import Tool


# import the default tool
from tools.tool import RespondTool

class Report(TypedDict):
    """
    defines the state for the multi-agent workflow
    includes messages, patient info, and workflow states
    """
    patient_info: str
    messages: Annotated[List[dict], add]
    diagnosis: str
    recommendations: str
    appointment_details: str

class MasterWorkflow:
    def __init__(self):
        """
        initializes the master agents its nodes
        """
        # set up the environment
        self._setup_environment()
        # initial report
        self.initial_report = {
            "patient_info" : '',
            "messages" : [],
            "diagnosis" : "",
            "recommendations" : "",
            "appointment_details" : ""
        }

        # create thred id 
        self.thread_id = str(uuid.uuid4())

        # current report 
        self.current_report = self.initial_report.copy()

        # sets up the masters tool 
        self.respond_tool = RespondTool()

        self.master_tools = [
            Tool(
                name=self.respond_tool.name,
                func=self.respond_tool._run,
                description=self.respond_tool.description
            )
        ]

        # initialize masters 
        self.master_agent = MyAgent(tools=self.master_tools, system_prompt=MASTER_SYSTEM_PROMPT, template=MASTER_TEMPLATE, agent_role="Master Agent")
        
        # define directory/directories for external data
        self.directory_path = 'data\diagnosis'
        # initializes other agents
        self.nurse_agent = NurseAgent()
        self.diagnosis_agent = DiagnosisAgent(directory_path=self.directory_path)
        self.recommendation_agent = RecommendationAgent()
        self.reception_agent = ReceptionAgent()

        # build the workflow
        self.build_workflow()

        # store the report and return it 
    
    def _setup_environment(self):
        """load environment variables and set workspace directory and optionally returns keys."""
        load_dotenv()
        workspace_directory = os.getenv('WORKSPACE_DIRECTORY')

        if not workspace_directory:
            raise ValueError("WORKSPACE_DIRECTORY not set in environment variables")
        
        os.chdir(workspace_directory)

    def master_node(self, report: Report):
        """
        constructs the master node and serves as the entry
        """
        # invokes the masters the input
        master_output = self.master_agent(report, examples=MASTER_EXAMPLES)

        # routing to keep track of the next agent
        report['messages'] = report['messages'] + [{
            "role": "master",
            "content": master_output
        }]

        # returns the report and passes it along
        return report
        
    def nurse_node(self, report: Report):
        """
        create the nurse node and invokes it
        """
        # queries the user
        nurse_output = self.nurse_agent(report) # has a template filled should pass in the report laters 
        
        # they take care of the appointment details and patient info
        if not report['patient_info']: 
            report['patient_info'] = nurse_output
        else:
            report['appointment_details'] = nurse_output

        # returns the the report and passes along
        return report
    
    def diagnosis_node(self, report: Report):
        """
        initialzies the diagnosis node and invokes it
        """
        # asks for a diagnosis 
        diagnosis_output = self.diagnosis_agent(report) 

        # writes a diagnosis 
        report['diagnosis'] = diagnosis_output

        # returns the the report and passes along
        return report

    def recommendation_node(self, report: Report):
        """
        initializes the recommendation node and invokes it
        """
        # asks for recommendation
        recommendation_output = self.recommendation_agent(report)

        # provide recommendation 
        report['recommendations'] = recommendation_output

        # returns the the report and passes along
        return report

    def reception_node(self, report: Report):
        """
        initializes the receptionist node and invokes it
        """
        reception_output = self.reception_agent(report)

        # sets up the appointment 
        report['messages'] = report['messages'] + [{
            "role": "reception",
            "content": reception_output
        }]

        # returns the the report and passes along to the master
        return report

    def build_workflow(self):
        """
        construct the workflow using the report
        """
        workflow = StateGraph(Report)

        # creates the node, and upon entering, it calls the node 
        workflow.add_node("master node", self.master_node)
        workflow.add_node("nurse node", self.nurse_node)
        workflow.add_node("diagnosis node", self.diagnosis_node)
        workflow.add_node("recommendation node", self.recommendation_node)
        workflow.add_node("reception node", self.reception_node)

        # entry point
        workflow.set_entry_point("master node")

        # routing logic
        def route_master(report: Report):
            """
            determine the next node based on master's output
            """
            
            last_master_message = report['messages'][-1]['content'] if report['messages'] else ""
            
            if "NURSE" in last_master_message.upper():
                return "nurse node"
            elif "DIAGNOSIS" in last_master_message.upper():
                  return "diagnosis node"
            elif "RECOMMENDATION" in last_master_message.upper():
                return "recommendation node"
            elif "RECEPTION" in last_master_message.upper():
                return "reception node"
            else:
                return "master node"

        # add conditional edges
        workflow.add_conditional_edges(
            "master node",
            route_master
        )

        # bidirectional information so it can return the report 
        workflow.add_edge("nurse node", "master node")
        workflow.add_edge("diagnosis node", "master node")
        workflow.add_edge("recommendation node", "master node")
        workflow.add_edge("reception node", END)
        
        # check points the report
        checkpointer = MemorySaver()

        # construct the workflow with the checkpoint at each return
        self.app = workflow.compile(checkpointer=checkpointer)

    def run(self):
        """
        run the workflow with a maximum number of iterations
        """
        report = self.initial_report.copy()

        # configs the thread for checkpointing
        config = {
            "configurable": {
                "thread_id": self.thread_id
            }
        }

        # the final result should be an report
        result = self.app.invoke(report, config=config)

        self.report = result
        return self.report
    
      
    def test_call(self, report: Report):
        """
        for testing purpose where we directly invoke the master
        """
        master_response = self.master_agent(str(report), examples=MASTER_EXAMPLES)
        return master_response


