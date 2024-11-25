# import other packages
import os
from typing import List, Optional
from dotenv import load_dotenv
    
# import langchain packages
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor, Tool

# import my file
from prompts.all_system import DEFAULT_SYSTEM_MESSAGE
from prompts.all_template import TEMPLATE


class MyAgent:
    def __init__(self, 
                 tools: Optional[List[Tool]] = None, 
                 model_name: str = 'gpt-4o-mini', 
                 system_prompt: Optional[str] = None,
                 template: Optional[str] = None,
                 temperature: float = 0.3,
                 agent_role: str = 'Default Agent',
                 max_iterations = 6):
        """
        initailzes a customizable agent
        
        1. Base ReAct agent: Custom tools, uses default template and system prompt
        2. Custom ReAct agent: Custom tools, uses custom template and system prompt
        3. Basic LLM: No tools, uses default system prompt
        4. Custom LLM: No tools, uses custom default system prompt 
        """
        # get the key
        self.openai_key = self._setup_environment_and_extract_keys()

        # create llm
        self.llm = self._initialize_llm(model_name=model_name, temperature=temperature)

        # intialize the prompts 
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_MESSAGE # defines custom or default prompts
        self.template_prompt = template or TEMPLATE 
        self.agent_role = agent_role
        self.max_iterations = max_iterations
        
        # initialize agents
        self.tools = tools

        if self.tools:
            # if tools provided, create ReAct agent with custom prompt
            self.prompt = self._create_prompt()
            self.agent = self._create_react_agent()
            self.agent_executor = self._create_agent_executor()
        else:
            # otherwise use direct llm
            self.prompt = self._create_prompt()
    
    def _setup_environment_and_extract_keys(self):
        """load environment variables and set workspace directory and optionally returns keys."""
        load_dotenv()
        workspace_directory = os.getenv('WORKSPACE_DIRECTORY')

        if not workspace_directory:
            raise ValueError("WORKSPACE_DIRECTORY not set in environment variables")
        
        os.chdir(workspace_directory)

        # extract the open ai
        openai_key = os.getenv('OPENAI_API_KEY')
        if not openai_key:
            raise ValueError("OpenAI API Key not found in environment variables")
        return openai_key
    

    def _initialize_llm(self, model_name: str, temperature: float) -> ChatOpenAI:
        """initialize the llm"""
        return ChatOpenAI(
            api_key=self.openai_key,
            model=model_name,
            temperature=temperature
        )

    def _create_prompt(self): 
        """creates prompt that the agent will used"""
        if self.tools:
            return ChatPromptTemplate.from_messages([
                SystemMessage(content=self.system_prompt),
                # note, might add some chat history
                HumanMessagePromptTemplate.from_template(
                    template=self.template_prompt)
            ])

    def _create_chat_messages(self, input: str):
        """creates the message list for direct LLM chat"""
        messages = [
            SystemMessage(content=self.system_prompt)
        ]

        messages.append(HumanMessage(content=str(input)))
        return messages

    def _create_react_agent(self):
        """creates a ReAct agent will the template and model it will using"""
        # create react automatically assumes input variable [tools, tool_name, agent_scratchpad] 
        return create_react_agent(
                    tools=self.tools,
                    llm=self.llm,
                    prompt=self.prompt
                )
    
    def _create_agent_executor(self):
        """creates an agent executor, which starts the chain"""
        return AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=self.max_iterations
        )
    
    def __call__(self, input: str = "", examples: str = ""):
        """
        invoke the LLM with the user prompt with optional examples depending on template
        """
        print(self.agent_role)
        invoke_args = {"input": input}
        
        # optional
        if examples:
            invoke_args["examples"] = examples

        # use ReAct or regular
        if self.tools:
            # use agent executor if tools are available
            result = self.agent_executor.invoke(invoke_args)
            return result["output"]
        else:
            # direct LLM usage if no tools
            messages = self._create_chat_messages(input) 
            response = self.llm.invoke(messages)
            return response.content
    


