MASTER_EXAMPLES = """
EXAMPLE 1:
Current Report:
{
    'patient_info': '',
    'messages': [],
    'diagnosis': '',
    'recommendations': '',
    'appointment_details': '',
}
Thought: The 'patient_info' is empty and needs to be filled. The NURSE is responsible for filling it out
Action: NURSE
Final Answer: NURSE

EXAMPLE 2:
Current Report:
{
    'patient_info': 'Sarah Johnson, 58-year-old female, presents with irregular heartbeat, heart palpitations, extreme fatigue, and shortness of breath during routine activities. Reports occasional dizziness and anxiety. History of thyroid disease.',
    'messages': [],
    'diagnosis': 'Primary diagnosis suggests Atrial Fibrillation (AFib) based on irregular heart rhythm and associated symptoms. Thyroid condition may be a contributing factor. Requires ECG confirmation and possible Holter monitoring.',
    'recommendations': 'Immediate ECG monitoring, blood tests including thyroid function, and possible anticoagulation therapy assessment. Follow-up with cardiac electrophysiologist recommended.',
    'appointment_details': '',
}
Thought: The 'patient_info', 'diagnosis', 'recommendations' has been filled. The 'appointment_details' is empty. The NURSE is responsible for filling out the 'appointment_details.'
Action: NURSE
Final Answer: NURSE

EXAMPLE 3:
Current Report:
{
    'patient_info': 'Linda Chang, 44-year-old female with progressive dyspnea on exertion, fatigue, and occasional chest pressure. History of systemic lupus erythematosus. Reports ankle swelling and dry cough.',
    'messages': [],
    'diagnosis': '',
    'recommendations': '',
    'appointment_details': '',
}
Thought: The 'patient_info' has been filled, and now we need to diagnose the patient. I will pass this to the DIAGNOSIS.
Action: DIAGNOSIS
Final Answer: DIAGNOSIS

EXAMPLE 4:
Current Report:
{
    'patient_info': 'Margaret Wilson, 72-year-old female with progressive shortness of breath, decreased exercise tolerance, and heart murmur noted on physical exam. Reports occasional chest pressure and dizziness when standing quickly.',
    'messages': [],
    'diagnosis': 'Suspected severe Aortic Stenosis based on characteristic murmur and symptoms. Age and symptom progression suggest calcific aortic valve disease.',
    'recommendations': '',
    'appointment_details': '',
}
Thought: The 'patient_info', 'diagnosis' field has been filled. Given this information we need to suggest next steps after the diagnosis. I will pass this to the RECOMMENDATION.
Action: RECOMMENDATION
Final Answer: RECOMMENDATION

EXAMPLE 5:
Current Report:
{
    'patient_info': 'Margaret Wilson, 72-year-old female with progressive shortness of breath, decreased exercise tolerance, and heart murmur noted on physical exam. Reports occasional chest pressure and dizziness when standing quickly.',
    'messages': [],
    'diagnosis': 'Suspected severe Aortic Stenosis based on characteristic murmur and symptoms. Age and symptom progression suggest calcific aortic valve disease.',
    'recommendations': 'Urgent echocardiogram for valve assessment, carotid ultrasound, and cardiac catheterization if indicated. Evaluation for possible TAVR procedure.',
    'appointment_details': '01/05/2025, 11:00-12:00',
}
Thought: The 'patient_info', 'diagnosis', 'recommendations', 'appointment_details' has been filled. An appointment needs to be schedule. I will pass this to the RECEPTION.
Action: RECEPTION
Final Answer: RECEPTION
"""

NURSE_EXAMPLES = """
EXAMPLE 1:
Current Patient Report Status:
{
  'patient_input': "The user is a 50-year-old male named David Clark who has been experiencing frequent headaches, especially in the mornings, accompanied by blurred vision and nausea for the past two weeks. He mentions that the pain intensifies after prolonged periods of screen use at work. He also has a family history of migraines and hypertension.",
  'messages': [],
  'diagnosis': "The patient is likely experiencing migraines with possible ocular involvement. Given the family history of migraines and the nature of the symptoms, it’s important to rule out any underlying conditions such as increased intracranial pressure or vision issues.",
  'recommendations': "The patient is advised to reduce screen time and take regular breaks, use proper ergonomics, and stay hydrated. An eye examination is recommended to assess for any vision-related causes. A follow-up MRI or CT scan of the brain may be needed to rule out other neurological conditions if symptoms persist. A referral to a neurologist for further evaluation of possible migraine management options is also recommended.",
  'appointment_details': ""
}

Thought: The current patient form status indicates that the patient info and the recommendation both have been filled.
Reasoning: Both fields have been filled, which is required in order to query the user if they would like to set up an appointment.
Action: user_input
Action Input: "Based on your patient form, would you like to schedule an appointment?" 
Observation: [Waiting for user response] "Yes."

Thought: The user has indicated they want to schedule an appointment, but I do not have information on when to schedule.
Reasoning: In order to set an appointment, knowing the specific time is important.
Action: user_input
Action Input: "Great! In order to schedule an appointment, can you please provide the Date (MM/DD/YYYY) and Time (HH:MM-HH:MM)?" 
Observation: [Waiting for user response] "Let's do May 17, 2024 from 9:30 am to 10:30 am."

Final Thought: I have collected enough information to schedule the appointment.
Final Answer: Date: 05/17/2024, 09:30-10:30


EXAMPLE 2:
Current Patient Report Status: {'patient_info': '', 'messages': [], 'diagnosis': '', 'recommendations': '', 'appointment_details': ''}

Thought: The current patient form status indicates that there is no patient info or information gathered yet. I need to start by collecting the user's symptoms, age, and medical history before proceeding to any appointment details.
Reasoning: Gathering the user's symptoms, age, and medical history is essential for understanding their health condition and determining the appropriate next steps. Once I have this information, I can then ask about setting an appointment if needed.
Action: user_input
Action Input: "Could you please describe your symptoms?" 
Observation: [Waiting for user response] "I have severe joint pain, especially in my knees and wrists, that has been progressively worsening over the past month."

Thought: The user has severe joint pain that has been progressively worsening for the past month. Now, I need to gather their age to complete the necessary information for the patient info.
Reasoning: Collecting the user's age is crucial to assess the severity of the symptoms and to consider age-related conditions.
Action: user_input
Action Input: "Thank you for sharing your symptoms. Could you please tell me your age?" 
Observation: [Waiting for user response] "I am 60 years old."

Thought: The user is 60 years old and has reported severe joint pain. Now, I need to gather their medical history to complete the necessary information for patient info.
Reasoning: Understanding the user's medical history is vital for identifying any pre-existing conditions or risk factors that may be related to their current symptoms.
Action: user_input
Action Input: "Thank you for your age. Could you please provide me with your medical history, including any past illnesses, surgeries, or ongoing treatments?" 
Observation: [Waiting for user response] "My medical history includes osteoarthritis in my knees, diabetes type 2, and a history of depression, for which I am currently taking medication."

Final Thought: I have gathered enough patient information and I will not query on recommednation because it is outside of scope so I will just return the output.
Final Answer: The user is a 60-year-old female named Mary Johnson who is experiencing severe joint pain, especially in her knees and wrists, that has been progressively worsening over the past month. She also reports occasional swelling in her hands and difficulty with mobility, particularly in the morning. Her medical history includes osteoarthritis in her knees, diabetes type 2, and a history of depression, for which she is currently taking medication.

EXAMPLE 3:
Current Patient Report Status: {'patient_info': '', 'messages': [], 'diagnosis': '', 'recommendations': '', 'appointment_details': ''}

Thought: The current patient form status indicates that there is no patient info or information gathered yet. I need to start by collecting the user's symptoms, age, and medical history before proceeding to any appointment details.
Reasoning: Gathering the user's symptoms, age, and medical history is essential for understanding their health condition and determining the appropriate next steps. Once I have this information, I can then ask about setting an appointment if needed.
Action: user_input
Action Input: "Could you please describe your symptoms?" 
Observation: [Waiting for user response] "I am a 45-year-old male, reports experiencing persistent chest pain, shortness of breath, occasional dizziness, and fatigue for the past two weeks. My medical history includes hypertension diagnosed five years ago, managed with medication, and borderline high cholesterol with no current treatment. I have family history of heart disease, as his father suffered a heart attack at age 50. He has no known allergies."

Final Thoguht: The user has provided enough neccessar information such as the their symptoms, their age, and their medical history. In addition, the 'recommendation' field is not filled so I will not ask for scheduling an appointment. Therefore I will now provide the patient info
Final Answer: The user is a 45-year-old male experiencing persistent chest pain, shortness of breath, occasional dizziness, and fatigue for the past two weeks. His medical history includes hypertension diagnosed five years ago, managed with medication, and borderline high cholesterol with no current treatment. He has a family history of heart disease, as his father suffered a heart attack at age 50. He has no known allergies.
"""

DIAGNOSIS_EXAMPLES = """
EXAMPLE 1: 

Thought: The patient report includes symptoms of chest pain radiating to the left arm, shortness of breath, and a history of hypertension. These signs strongly indicate a possible acute coronary syndrome (ACS), and the provided details seem sufficient to make a diagnosis without using the tool.
Reasoning: The combination of classic symptoms and history points to ACS, and no further search is needed to confirm this likely diagnosis.
Action:
Action Input: 
Observation: None

Final Thought: The information provided is sufficient to make a diagnosis.
Final Answer: The patient most likely has Acute Coronary Syndrome. Immediate intervention recommended.

EXAMPLE 2:

Thought: The patient report mentions palpitations, fatigue, and dizziness. The patient also has a history of hypothyroidism, but no specific data regarding rhythm irregularities is provided. I need to use the database to check potential cardiology-related causes for these symptoms.
Reasoning: The symptoms are suggestive of arrhythmias or other cardiac issues, but confirmation is needed. This tool has not yet been used.
Action: search_database
Action Input: palpitations, fatigue, dizziness, and history of hypothyroidism.
Observation: [Output of the tool used]

Thought: Based on the database results and the patient’s symptoms, a diagnosis can be made.
Reasoning: The symptoms and database results align with atrial fibrillation as the most likely diagnosis. However, I will do further investigation using search_engine
Action: search_engine
Action Input: atrial fibrillation symptoms and palpitations, fatigue, dizziness, and history of hypothyroidism
Observation: [Output of the tool used]

Final Thought: Through search_engine, it appears that the it further provides evidence that the patient most likely has atrial fibrillation.
Final Answer: The patient most likely has Atrial Fibrillation. Would suggest follow up for recommendation

EXAMPLE 3:

Thought: The patient report describes non-specific symptoms such as mild chest discomfort and occasional lightheadedness, but no significant medical history is included. The symptoms are too vague to conclude. I will use the database to search for possible cardiology-related conditions.
Reasoning: The symptoms are ambiguous, and the database may help identify potential underlying cardiac conditions. This tool has not yet been used.
Action: search_database
Action Input: mild chest discomfort, occasional lightheadedness, no significant history.
Observation: The database lists potential causes such as anxiety, atypical angina, and mitral valve prolapse but provides no conclusive condition due to the lack of specific details.

Thought: Even with the database output, the information remains insufficient to determine a clear diagnosis.
Reasoning: Additional tests or detailed history (e.g., ECG, stress test, family history) would be required to narrow down the possibilities.
Action:
Action Input:
Observation: None

Final Thought: The information is insufficient for a diagnosis.
Final Answer: UNKNOWN
"""

RECOMMENDATION_EXAMPLES = """
"""