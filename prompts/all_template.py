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

MASTER_TEMPLATE = """
Please delegate the agents needed to fill out the report below:

You do not have any tools:

{tools} or {tool_names}

Here are the agents names:

- NURSE: Responsible for filling out the 'patient_info' field.
- DIAGNOSIS: Responsible for filling out the 'diagnosis' field.
- RECOMMENDATION: Responsible for filling out the 'recommendations' field.
- SCHEDULE: Responsible for filling out the 'appointment_details' field.

(END OF AGENT LIST)

Use the following format:
Current Report: {input}
Thought: Think about which agent should complete the report based on the task.
Action: [agent_name]
Final Answer: The final answer should be the agent name.

Begin!

{agent_scratchpad}
"""

NURSE_TEMPLATE = """
CONTEXT
Current Patient Report Status: {input}
Available Tools: {tools}

(END OF CONTEXT)

TASK STRUCTURE
1. Review current report status to identify missing information.
2. Gather 'patient_info' if missing (this includes collecting symptoms, age, and medical history).
3. If both 'patient_info' and 'recommendations' are already filled, then proceed to gather 'appointment_details'.

EXAMPLES

{examples}

(END OF EXAMPLES)


RESPONSE FORMAT
Thought: [Analysis of the current report and next steps]
Reasoning: [Justification for chosen action]
Action: [Selected tool from {tool_names}]
Action Input: [Specific query or command]
Observation: [The users input for the query]
... (this Reasoning/Action/Action Input/Observation can repeat N times until there is sufficient information)

Final Thought: [Verify That You Have Done The Appropiate Step]
Final Answer: [One of the following]
  - [A concise summary of the patient report written in a sentence or paragraph]
  - Appointmet details [Format: Date: MM/DD/YYYY, Time: HH:MM-HH:MM]

Begin! 
{agent_scratchpad}
"""

DIAGNOSIS_TEMPLATE = """
CONTEXT
Current Patient Report Status: {input}
Available Tools: {tools}

TASK STRUCTURE 
1. Review current report status and identify whether a clear diagnosis could be made.
    - If a disgnosis can not be made then you may the tools provided.
    - IMPORTANT: If a specifc tool has already been used then you may not use it again, but you can use other tools if you would like 
    - If a diangosis can be made then you may display the final answer

EXAMPLES

{examples}

(END OF EXAMPLES)

RESPONSE FORMAT
Thought: [Analysis of the current report and next steps]
Reasoning: [Justification for the chosen action and whether this tool has already been used]
Action: [Selected tool from {tool_names}]
Action Input: [Specific input into the tools]
Observation: [Assess the output from the tool]
... (this Thought/Reasoning/Action/Action Input/Observation can repeat N times until there is sufficient information or when you have used all of the tools at your disposal)

Final Thought: [Verify That You Can Make Conclusion]
Final Answer: [One of the following]
    - [A brief description on fhe patient diagnosis.]
    - UNKNOWN

Begin!
{agent_scratchpad}
"""




