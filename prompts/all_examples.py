NURSE_EXAMPLE = """
Example 1:

Current Form: 

{'patient_info': '', 'messages': [], 'diagnosis': '', 'recommendations': '', 'appointment_details': ''}

Thought: The current patient form status indicates that there is no patient info or information gathered yet. I need to start by collecting the user's symptoms, age, and medical history before proceeding to any appointment details.
Reasoning: Gathering the user's symptoms, age, and medical history is essential for understanding their health condition and determining the appropriate next steps. Once I have this information, I can then ask about setting an appointment if needed.
Action: get_user_input
Action Input: "Could you please describe your symptoms?" 
Observation: [Waiting for user response] "I have severe joint pain, especially in my knees and wrists, that has been progressively worsening over the past month."

Thought: The user has severe joint pain that has been progressively worsening for the past month. Now, I need to gather their age to complete the necessary information for the patient info.
Reasoning: Collecting the user's age is crucial to assess the severity of the symptoms and to consider age-related conditions.
Action: get_user_input
Action Input: "Thank you for sharing your symptoms. Could you please tell me your age?" 
Observation: [Waiting for user response] "I am 60 years old."

Thought: The user is 60 years old and has reported severe joint pain. Now, I need to gather their medical history to complete the necessary information for patient info.
Reasoning: Understanding the user's medical history is vital for identifying any pre-existing conditions or risk factors that may be related to their current symptoms.
Action: get_user_input
Action Input: "Thank you for your age. Could you please provide me with your medical history, including any past illnesses, surgeries, or ongoing treatments?" 
Observation: [Waiting for user response] "My medical history includes osteoarthritis in my knees, diabetes type 2, and a history of depression, for which I am currently taking medication."

Final Thought: I have gathered enough patient information and I will not query on recommednation because it is outside of scope so I will just return the output.
Final Answer: The user is a 60-year-old female named Mary Johnson who is experiencing severe joint pain, especially in her knees and wrists, that has been progressively worsening over the past month. She also reports occasional swelling in her hands and difficulty with mobility, particularly in the morning. Her medical history includes osteoarthritis in her knees, diabetes type 2, and a history of depression, for which she is currently taking medication.

Example 2:

Current Form:

{
  'patient_input': "The user is a 50-year-old male named David Clark who has been experiencing frequent headaches, especially in the mornings, accompanied by blurred vision and nausea for the past two weeks. He mentions that the pain intensifies after prolonged periods of screen use at work. He also has a family history of migraines and hypertension.",
  'messages': [],
  'diagnosis': "The patient is likely experiencing migraines with possible ocular involvement. Given the family history of migraines and the nature of the symptoms, it’s important to rule out any underlying conditions such as increased intracranial pressure or vision issues.",
  'recommendations': "The patient is advised to reduce screen time and take regular breaks, use proper ergonomics, and stay hydrated. An eye examination is recommended to assess for any vision-related causes. A follow-up MRI or CT scan of the brain may be needed to rule out other neurological conditions if symptoms persist. A referral to a neurologist for further evaluation of possible migraine management options is also recommended.",
  'appointment_details': ""
}

Thought: The current patient form status indicates that the patient info and the recommendation both have been filled.
Reasoning: Both fields have been filled, which is required in order to query the user if they would like to set up an appointment.
Action: get_user_input
Action Input: "Based on your patient form, would you like to schedule an appointment?" 
Observation: [Waiting for user response] "Yes."

Thought: The user has indicated they want to schedule an appointment, but I do not have information on when to schedule.
Reasoning: In order to set an appointment, knowing the specific time is important.
Action: get_user_input
Action Input: "Great! In order to schedule an appointment, can you please provide the Date (MM/DD/YYYY) and Time (HH:MM-HH:MM)?" 
Observation: [Waiting for user response] "Let's do May 17, 2024 from 9:30 am to 10:30 am."

Final Thought: I have collected enough information to schedule the appointment.
Final Answer: MRI and/or CT Scans [Date: 05/17/2024, Time: 09:30-10:30]

Example 3:

Current Form:

{'patient_info': '', 'messages': [], 'diagnosis': '', 'recommendations': '', 'appointment_details': ''}

Thought: The current patient form status indicates that there is no patient info or information gathered yet. I need to start by collecting the user's symptoms, age, and medical history before proceeding to any appointment details.
Reasoning: Gathering the user's symptoms, age, and medical history is essential for understanding their health condition and determining the appropriate next steps. Once I have this information, I can then ask about setting an appointment if needed.
Action: get_user_input
Action Input: "Could you please describe your symptoms?" 
Observation: [Waiting for user response] "I am a 45-year-old male, reports experiencing persistent chest pain, shortness of breath, occasional dizziness, and fatigue for the past two weeks. My medical history includes hypertension diagnosed five years ago, managed with medication, and borderline high cholesterol with no current treatment. I have family history of heart disease, as his father suffered a heart attack at age 50. He has no known allergies."

Final Thoguht: The user has provided enough neccessar information such as the their symptoms, their age, and their medical history. In addition, the 'recommendation' field is not filled so I will not ask for scheduling an appointment. Therefore I will now provide the patient info
Final Answer: The user is a 45-year-old male experiencing persistent chest pain, shortness of breath, occasional dizziness, and fatigue for the past two weeks. His medical history includes hypertension diagnosed five years ago, managed with medication, and borderline high cholesterol with no current treatment. He has a family history of heart disease, as his father suffered a heart attack at age 50. He has no known allergies.
"""
