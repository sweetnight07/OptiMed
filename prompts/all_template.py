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
Please select the agent needed to fill out the report below:

You have a basic responding tool that is not needed:

{tools} or {tool_names}


Here are the agents names:
- NURSE: Responsible for filling out the 'patient_info' field and 'appointment_details' only after 'patient_info', 'diagnosis', 'recommendations' has been filled.
- DIAGNOSIS: Responsible for filling out the 'diagnosis' field.
- RECOMMENDATION: Responsible for filling out the 'recommendations' field.
- RECEPTION: Responsible for scheduling when all entries have been filled.

(END OF AGENT LIST)

Use the following format:
Current Report: {input}
Thought: Think about which agent should be called to complete their section.
Action: [agent_name]
Final Answer: [agent_name]

(END OF FORMAT)

Output the final answer
Before you begin here are some examples:

{examples}
(END OF EXAMPLES)



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
  - Format: [MM/DD/YYYY, HH:MM-HH:MM]

Begin! 
{agent_scratchpad}
"""

DIAGNOSIS_TEMPLATE = """
CONTEXT
Current Patient Report Status: {input}
Available Tools: {tools}

(END OF CONTEXT)

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
    - [A brief description on the patient diagnosis.]
    - UNKNOWN

Begin!
{agent_scratchpad}
"""

RECOMMENDATION_TEMPLATE = """
CONTEXT
Current Patient Report Status: 

{input}

(END OF CONTEXT)

You have access to the following tools:

{tools}

TASK STRUCTURE  
1. Review the current patient report and determine whether a treatment or diagnostic recommendation can be made.  
    - If no recommendation can be made, you may use the available tools to gather additional information.  
    - IMPORTANT: Each tool can only be used **twice**. If a specific tool has been used twice, it cannot be used again. However, other tools can still be utilized.  
    - Once a treatment or diagnostic recommendation is made, you may display the final answer.

RESPONSE FORMAT
Thought: [Analyze the current patient report and identify the next steps]
Reasoning: [Justify why the next step is appropriate]
Action: [Select a tool from {tool_names}]
Action Input: [Diagnosis Name]
  - Ensure you input only the condition name, not a full sentence.
Observation: [Assess the output from the tool]
... (This Thought/Reasoning/Action/Action Input/Observation cycle may repeat as needed until there is sufficient information or all tools have been used)

Final Thought: [Verify that a conclusion can be made]
Final Answer: [One of the following]
    - [A brief description of the recommended treatment or diagnostic test]
    - No Recommendations

NOTES:
**Limitation on Tools**: The **Search CDC Online** tool can only be used **twice**.

Begin!
{agent_scratchpad}
"""

RECEPTION_TEMPLATE = """
CONTEXT
Current Patient Report: {input}

(END OF CONTEXT)

You have access to the following tools:

{tools}

TASK
- Use the available tools to **schedule** the appointment.
- Confirm the booking and provide a **confirmation message** including:
   - Date and Time of the appointment.
   - Appointment Type (e.g., "ECG Scan").
   - Confirmation of appointment status** (e.g., "The appointment has been successfully booked.")

RESPONSE FORMAT
Thought: [Brief explanation of the next steps for scheduling]
Action: [Use one of the tools provided: {tool_names} to be used to schedule the appointment]
Action Input: [The requested input for that tool, you may decide at your own discretion]
Observation: [Result of the action (confirmation from the tool)]
Final Answer: [Confirmation message with date, time, patient name, and appointment type]

Begin!
{agent_scratchpad}
"""









