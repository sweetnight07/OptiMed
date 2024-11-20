# import relevant packages 
import os
from typing import List, Optional, Callable
from dotenv import load_dotenv

# import LangChain packages 
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.schema import SystemMessage

# class for OpenAILLMs
class OpenAILLMs:
    def __init__(self, 
                 tools: Optional[List[Tool]]=None, 
                 model_name: str ='gpt-4o-mini', 
                 agent_type: str ='ZERO_SHOT_REACT_DESCRIPTION', 
                 system_prompt: Optional[str]=None,
                 temperature: float = 0.3,
                 max_tokens: Optional[int] = None,
                 agent_role: str ='Unspecified Agent'):
        
        # extract the api key (in __init__()) to ensure it is updated when changed
        load_dotenv()
        self.openai_key = os.getenv('OPENAI_API_KEY')

        # check if the key was loaded successfully
        if self.openai_key:
            print("openAI API Key loaded successfully.")
        else:
            print("failed to load OpenAI API Key.")

        # initialize llm
        self.llm = ChatOpenAI(api_key = self.openai_key, 
                              model=model_name, 
                              temperature=temperature,
                              max_tokens=max_tokens,)

        # intialize tools, system prompts, agent role
        self.tools = tools or [self._create_default_tool()]
        self.system_prompt = system_prompt or "You are a helpful assistant."
        self.agent_role = agent_role

        try: 
            # intialize the agent
            self.agent = initialize_agent(
                tools=self.tools,
                llm=self.llm,   
                agent_type=agent_type,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations= 10 # each agent can only talk twice 
            )
        except Exception as e:
            print(f"error in initializing agent:", {e})
            self.agent = None

    # invokes the llm
    def __call__(self, prompt: str):
        """"""
        messages = [
            SystemMessage(content=self.system_prompt),  
            {"role": "user", "content": prompt} 
        ]
        result = self.agent(messages)
        return self.agent_role, result["output"]
    
    # create a generic default tool
    def _create_default_tool(self) -> Tool:
        """Create a more sophisticated default tool"""
        def default_tool_func(input_str: str) -> str:
            return f"Processed generic input: {input_str}"
        
        return Tool(
            name="DefaultTool",
            func=default_tool_func,
            description="A generic tool for processing inputs when no specific tools are provided"
        )