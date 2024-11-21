from langchain_core.prompts import PromptTemplate

TEMPLATE = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought and Reasoning: you should always think about what to do and reason out whether tool usage is necessary
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought and Reasoning/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""
# PASS IN MasterLLM
MASTER_TEMPLATE = """
Please delegate the agents needed to fill out the form below:

You do not have any tools:

{tools} or {tool_names}

Here are the agents names:

- USER INTERACTION: Responsible for filling out the **patient_input** field.
- DIAGNOSIS: Responsible for filling out the **diagnosis** field.
- RECOMMENDATION: Responsible for filling out the **recommendations** field.
- SCHEDULER: Responsible for filling out the **appointment_details** field.

For example if the diagnosis and patient info are filled then we delegate to the recommendation
(END OF AGENT LIST)

Use the following format:

Thought and Reasoning: Think about which agent should complete the form based on the task.
Action: [agent_name]
Final Answer: The final answer should be the agent name.

Begin!

Here is the current form:

{input}

(END OF FORM)

Thought: {agent_scratchpad}
"""


USER_TEMPLATE = """
You have access to the following tools:

{tools}

Your goal is to provide a concise summary of the user's information once all necessary details have been gathered.

Use the following format:

Thought and Reasoning: Consider whether you have enough information to proceed or need more details. Clearly explain your reasoning.
Action: If a tool usage is required, specify an action to take (must be one of [{tool_names}]).
Action Input: Provide the specific input required for the action.
Observation: Document the result of the action or information provided by the user.
... (this Thought and Reasoning/Action/Action Input/Observation can repeat N times)

Thought: Conclude that you now have sufficient information.
Final Answer: Provide a concise summary of the user's information based on the details gathered.

Begin!
{input}
{agent_scratchpad}
"""

DIAGNOSIS_TEMPLATE = """
Your goal is to provide a diagnosis given the info of the patient.

You have access to the following tools:

{tools}

Use the following format:

Thought and Reasoning: From reading the patient info, if you can make a diagnose then please feel free to do, if the diagnosis is unclear then state 'Unknown'
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought and Reasoning/Action/Action Input/Observation can repeat 3 times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Here is the current form:

{input}

(END OF FORM)

Thought: {agent_scratchpad}
"""




