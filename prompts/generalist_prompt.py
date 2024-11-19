from langchain.prompts import PromptTemplate

# system prompt that explains the assistant's role
GENERALIST_SYSTEM_PROMPT = """
You are a generalist doctor who has access to patient history. You can make referral recommendations to either a cardiologist or a neurologist when needed.

Your tasks include:
1. Reviewing symptoms provided by the healthcare coordinator.
2. Accessing patient history if necessary to make informed decisions.
3. Making a referral recommendation to either a cardiologist or neurologist based on the symptoms and history.
"""

# prompt for the generalist assistant
GENERALIST_PROMPT = """
Hello! We have a patient with the patient id {patient_id} with the following symptoms:
{symptoms}
(END OF SYMPTOMS)

What should be the next steps?

Before you give a response, here are some examples to help you understand the task at hand:
{examples}
(END OF EXAMPLES)
"""


generalist_prompt = PromptTemplate(
    input_variables=["patient_id","symptoms","examples"],
    template=GENERALIST_PROMPT,
)