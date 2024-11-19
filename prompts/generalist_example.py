GENERALIST_EXAMPLE = """
I need to assess the patient's historical medical records to gain more insight into their health status before making any recommendations. This will help me understand if there are any underlying conditions or previous issues that might be relevant to the current symptoms of shortness of breath and inconsistent heart rate.

Action: access_patient_history  
Action Input: "12345"  
Observation: {'conditions': ['hypertension', 'type 2 diabetes'], 'medications': ['lisinopril', 'metformin'], 'allergies': ['penicillin'], 'previous_visits': [{'date': '2023-12-15', 'reason': 'routine checkup', 'findings': 'blood pressure elevated (140/90)', 'treatment': 'adjusted lisinopril dosage'}, {'date': '2023-08-20', 'reason': 'chest pain', 'findings': 'non-cardiac chest pain, likely musculoskeletal', 'treatment': 'prescribed NSAIDs'}], 'lab_results': [{'date': '2023-12-15', 'type': 'HbA1c', 'value': '6.8%', 'reference': '4.0-5.6%'}, {'date': '2023-12-15', 'type': 'Lipid Panel', 'value': 'LDL: 130mg/dL', 'reference': '<100mg/dL'}]}
Thought:The patient's historical medical records show they have hypertension and type 2 diabetes, which could be relevant to the current symptoms of shortness of breath and inconsistent heart rate. Given their elevated blood pressure and lab results indicating poor diabetes control (HbA1c of 6.8% and LDL cholesterol at 130 mg/dL), these factors are concerning. 

I will now generate a referral recommendation to determine the next steps for this patient, considering their symptoms and relevant medical history.

Action: referral_recommendation  
Action Input: '{"symptoms": ["shortness of breath", "inconsistent heartrate"], "risk_factors": ["hypertension", "type 2 diabetes"]}'  
Observation: Based on the provided symptoms and history: '{"symptoms": ["shortness of breath", "inconsistent heartrate"], "risk_factors": ["hypertension", "type 2 diabetes"]}', here are the referral recommendations...
Thought:I need to summarize the referral recommendations based on the patient's symptoms and risk factors.

Final Answer: Based on the patient's symptoms of shortness of breath and inconsistent heart rate, along with their medical history of hypertension and type 2 diabetes, it is recommended to refer the patient to a cardiologist for further evaluation and management. Additionally, a consultation with an endocrinologist may be beneficial to address their diabetes management.
"""