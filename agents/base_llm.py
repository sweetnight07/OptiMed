# import relevant packages
import os
from typing import List, Optional
from dotenv import load_dotenv

# import LangChain packages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, create_react_agent, AgentExecutor

from prompts.all_system_message import DEFAULT_SYSTEM_MESSAGE
from prompts.all_template import TEMPLATE

class OpenAILLMs:
    def __init__(self, 
                 tools: Optional[List[Tool]] = None, 
                 model_name: str = 'gpt-4o-mini', 
                 system_prompt: Optional[str] = None,
                 template: Optional[str] = None,
                 temperature: float = 0.3,
                 agent_role: str = 'Default Agent'):

        # Load environment variables
        load_dotenv()
        self.openai_key = os.getenv('OPENAI_API_KEY')

        if not self.openai_key:
            raise ValueError("OpenAI API Key not found in environment variables")

        # Initialize LLM
        self.llm = ChatOpenAI(
            api_key=self.openai_key,
            model=model_name,
            temperature=temperature
        )

        # Initialize tools and prompts
        self.tools = tools or [self._create_default_tool()]
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_MESSAGE
        self.template = template or TEMPLATE
        self.agent_role = agent_role

        # Set up the ChatPromptTemplate with the TEMPLATE
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=self.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", self.template)
        ])

        print(self.prompt)
        
        # Create the agent
        self.agent = create_react_agent(
            tools=self.tools,
            llm=self.llm,
            prompt=self.prompt
        )

        # Create the agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )

    def __call__(self, input: str):
        """
        Invoke the LLM with the user prompt.
        """
        # Use the agent executor to process the input
        # Prepare input with chat history
        input_dict = {
            "input": input,
            "chat_history": []
        }

        # Use the agent executor to process the input
        result = self.agent_executor.invoke(input_dict)
        return self.agent_role, result["output"]
    
    def _create_default_tool(self) -> Tool:
        """Create a tool for generic responses."""

        def default_tool_func(input_str: str) -> str:
            return f"Response: {input_str}"
        
        return Tool(
            name="respond_tool",
            func=default_tool_func,
            description="A tool to respond to general queries or statements."
        )


