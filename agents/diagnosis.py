import os 
os.chdir("c:\\Users\\jzou2\\Fall 2024-2025\\Project\\OptiMed")

from agents.base_llm import OpenAILLMs


from prompts.all_system_message import DIAGNOSIS_SYSTEM_PROMPT
from prompts.all_template import DIAGNOSIS_TEMPLATE

from langchain.agents import Tool


class DiagnosisLLM():
    def __init__(self):
        # get users 
        # self.diagnostic_tools = [
        #     Tool(
        #         name="get_user_input",
        #         func=self.get_user_input,
        #         description="Prompts the user for input and returns their response."
        #     )
        # ]

        self.diagnosis = OpenAILLMs(system_prompt=DIAGNOSIS_SYSTEM_PROMPT, agent_role="Diagnosis Agent")


    # call the llm after it builds the prompt
    def __call__(self, report):
       
       full_input = f"""{DIAGNOSIS_TEMPLATE}
       
Current Report:
{str(report)}
(END OF FORM)
"""

       return self.diagnosis(full_input)


        