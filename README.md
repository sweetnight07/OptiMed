#### Specific Use Case
Caridiology and Neurology 



#### Steps To Implementation
Implementation Steps:

1. Set Up Environment, Import Relevant Packages, Plan MultiAgentSystem Goals and Tools

2. Create Base LLM Class

3. Create The Diagnosis Agent
3a. General Practioner
3b. Specialist

Key Features: Multiple Agents Conversing and Reflection/Reasoning

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



#### Some Problems You Might Run Into
- incorrect API key provided: three reasons: invalid key from the source, created api key may take a while to be active, the key is not reflective of the current key from the .env (consider restarting environment)

- parsing error: you can add handle_parsing_errors=True which allows the agent to handle any parsing issues

-  the jupyter notebook test might not be updated due to failed cache, consider restarting the kernel

- tool does not support sync invocation : ensure that each tool returns a callable function rather than a None or String for synced invocation

- 


#### Resources

- Initialize Agents: https://api.python.langchain.com/en/latest/agents/langchain.agents.agent_types.AgentType.html#langchain.agents.agent_types.AgentType

    - AgentType: https://api.python.langchain.com/en/latest/agents/langchain.agents.initialize.initialize_agent.html

    - AgentExecutor: https://api.python.langchain.com/en/latest/agents/langchain.agents.agent.AgentExecutor.html#langchain.agents.agent.AgentExecutor

- Tools
