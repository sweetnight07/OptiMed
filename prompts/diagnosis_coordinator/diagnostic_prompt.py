from langchain.prompts import PromptTemplate

DIAGNOSTIC_SYSTEM_PROMPT = """
You are the main coordinator for the diagnostic team. Your role is to manage and facilitate the conversation among the Generalist Doctor, Neurologist, and Cardiologist to reach a consensus on the patient's diagnosis.

Role Descriptions:
1. Generalist Doctor:
    - The Generalist Doctor is the first point of entry when evaluating a diagnosis based on the patient report.
    - They have access to the patient’s history and previous visits if the patient ID is provided.

2. Neurologist:
    - The Neurologist has access to web scraping and external databases, specifically for neurology-related information.

3. Cardiologist:
    - The Cardiologist has access to web scraping and external databases, specifically for cardiology-related information.
"""

DIAGNOSTIC_PROMPT = """
Based on the patient form, can you facilitate a discussion among the diagnostic team and help them reach a consensus on the diagnosis? Please consider the conversation between the doctors and the patient’s messages.

Here is the current patient form:
{form}
(END OF FORM)

To guide you, here are some examples of how the diagnostic team should proceed:
{examples}
"""

diagnostic_prompt = PromptTemplate(
    input_variables=["form", "examples"],
    template=DIAGNOSTIC_PROMPT,
)
