### Here Are Some Note Worthy Features
1. Reasoning Capabilities 
2. Multi-Agent Conversing and Facilitation (LangGraph)
3. Search Capabilities 
4. Vector Similarity Search (FAISS)
4. Hugging Face Integration (Recommendation System Agent)
5. Google Calendar Planning (Scheduler Agent)



### Specific Use Case
Caridiology and Neurology 

### Steps To Implementation
Implementation Steps:

1. Set Up Environment, Import Relevant Packages, Plan MultiAgentSystem Goals and Tools

2. Create Base LLM Class

3. Create The Diagnosis Agent
3a. General Practioner
3b. Specialist

4. Create Coordinator Agent (MAS Converse)
4a. conversation_management: structures the dialogue flow
4b. consensus_builder: synthesizes opinions and facilitates agreement

5. Generalist Agent
5a. patient_history_access:
5b. intial_assessment
5c. referal_recommendation

. Specialist (Cardiologist) Tools
7a. medical_search
7



### Some Problems You Might Run Into
- incorrect API key provided: three reasons: invalid key from the source, created api key may take a while to be active, the key is not reflective of the current key from the .env (consider restarting environment)

- parsing error: you can add handle_parsing_errors=True which allows the agent to handle any parsing issues

- the jupyter notebook test might not be updated due to failed cache, consider restarting the kernel

- tool does not support sync invocation : ensure that each tool returns a callable function rather than a None or String for synced invocation

- invalid reducer signature for StateGraph: ensure that the State is in the appropiate type

- self.report is not actually the report dict type itself, but an instance so make sure to re initialized when passed in 

- user_input: the master agent had access to the user_input tool but in this case it is too complicated 

- DEPRECIATION CRYYY

- HAHHAAHHAHAHAHA HAAHAHAHAH the output cell was empty but if you copy it there was acutal reasoning bruhhhhh



#### PROBELMS FOR THE SAKE OF SIMPLICITY WE WILL NOT IMPLEMENT A DIAGNOSIS TEAM

CODE TOP BUT PROMPT ENGINEER BOTTOM UP




- IT is chronolgoical system but finetung laters 


#### Resources

- Initialize Agents: https://api.python.langchain.com/en/latest/agents/langchain.agents.agent_types.AgentType.html#langchain.agents.agent_types.AgentType

    - AgentType: https://api.python.langchain.com/en/latest/agents/langchain.agents.initialize.initialize_agent.html

    - AgentExecutor: https://api.python.langchain.com/en/latest/agents/langchain.agents.agent.AgentExecutor.html#langchain.agents.agent.AgentExecutor

- Tools
    - https://python.langchain.com/docs/how_to/custom_tools/

- Graphs 
    - https://langchain-ai.github.io/langgraph/concepts/low_level/#threads

# Thoguht Process 

- create a generic llm for better coding practice (give it the chance to create reasoning or regular agent)


- start from the top bottom approach, start from the master node and handling its work flow first


If there is uncertainty or they require further collaboration, a Secondary Coordinator Agent might be used to facilitate communication between specialists.

- use a agentstate to keep track of hte state of hte report



- ideally we add everythign to the prioir ddatabase

- only thing different about each agent is there tools and the agent type 


- Incorporates some use of knowledge graphs 

