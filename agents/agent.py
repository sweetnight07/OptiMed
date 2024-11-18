# import relevant packages 
import os
from dotenv import load_dotenv

# import LangChain packages 
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, initialize_agent, AgentType

# extract the api key
load_dotenv()
openai_key = os.getenv('OPENAI_API_KEY')

class OpenAILLMs:
    def __init__(self, tools=None, model_name='gpt-4o-mini', agent_type='ZERO_SHOT_REACT_DESCRIPTION'):
        # check if the key was loaded successfully
        if openai_key:
            print("openAI API Key loaded successfully.")
        else:
            print("failed to load OpenAI API Key.")

        # initialize llm
        self.tools = tools or []
        self.model_name = model_name
        self.llm = ChatOpenAI(api_key = openai_key, model=model_name, temperature=0.7) # might change teh temperature to debug
        self.agent_type = agent_type
        
        # parameters need agents 
        if not self.tools:
            self.tools = [Tool(
                name="DefaultTool",
                func=default_tool(),
                description="A tool that does nothing"
            )]

        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent_type=self.agent_type,
            verbose=True
        )

    def __call__(self, prompt: str):
        # call the agent and return the result
        return self.agent.run(prompt)
        

# default tool that does nothing
def default_tool():
    return None