# import other packages
import os 
from dotenv import load_dotenv

# import langchain packages
from langchain.agents import Tool

# import my file
from agents.agent import MyAgent

from prompts.all_system import RECEPTION_SYSTEM_PROMPT
from prompts.all_template import RECEPTION_TEMPLATE

from tools.tool import ParseAppointmentTool
from tools.tool import ScheduleAppointmentTool

class ReceptionAgent():
    def __init__(self):
        """
        initialzies the reception agent
        """
        # set up environment
        self._setup_environment()

        # collect the tools
        self.parse_appointment_tool = ParseAppointmentTool()
        self.schedule_appointment_tool = ScheduleAppointmentTool()

        # set up the reception tools
        self.reception_tools = [
            Tool(
                name=self.parse_appointment_tool.name,
                func=self.parse_appointment_tool._run,
                description=self.parse_appointment_tool.description
            ),
            Tool(
                name=self.schedule_appointment_tool.name,
                func=self.schedule_appointment_tool._run,
                description=self.schedule_appointment_tool.description
            )
        ]

        self.reception = MyAgent(tools=self.reception_tools,
                                 system_prompt=RECEPTION_SYSTEM_PROMPT,
                                 template=RECEPTION_TEMPLATE,
                                 agent_role="Reception Agent")

    def _setup_environment(self):
        """load environment variables and set workspace directory and optionally returns keys."""
        load_dotenv()
        workspace_directory = os.getenv('WORKSPACE_DIRECTORY')

        if not workspace_directory:
            raise ValueError("WORKSPACE_DIRECTORY not set in environment variables")
        
        os.chdir(workspace_directory)

    # call the llm after it builds the prompt
    def __call__(self, report):
        return self.reception(report)
