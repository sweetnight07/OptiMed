# import relevant packages 
import os
from dotenv import load_dotenv

# import LangChain packages 
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.schema import SystemMessage

# extract the api key
load_dotenv()
openai_key = os.getenv('OPENAI_API_KEY')

# class for OpenAILLMs
class OpenAILLMs:
    def __init__(self, tools=None, model_name='gpt-4o-mini', agent_type='ZERO_SHOT_REACT_DESCRIPTION', system_prompt=None):
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
        
        # set the system prompt
        self.system_prompt = system_prompt or "You are a helpful assistant."
        
        # parameters need agents 
        if not self.tools:
            self.tools = [Tool(
                name="DefaultTool",
                func=default_tool(),
                description="A default tool that processes input"
            )]

        # intialize the agent
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent_type=self.agent_type,
            verbose=True,
            handle_parsing_errors=True
        )

    # invokes the llm
    def __call__(self, prompt: str):
        """"""
        messages = [
            SystemMessage(content=self.system_prompt),  
            {"role": "user", "content": prompt} 
        ]
        result = self.agent(messages)
        return result["output"]
        

# default tool that does nothing
def default_tool():
    """A default tool that processes input and returns a response."""
    def _default_tool(input_str: str) -> str:
        return f"Processed input: {input_str}"
    return _default_tool