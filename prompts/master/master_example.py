MASTER_EXAMPLE = """
You got this!!

"""
# Observation: "i am 50 years old, and my patient id is 12345 and i have shortness of breath and chest pain" 

# Thought: I need to gather more information from the user to fill out the initial form and proceed with the healthcare workflow. The patient has provided some symptoms, but I need to confirm the details and possibly ask follow-up questions to ensure the diagnosis team has enough information.

# Action: get_user_input  
# Action Input: "Could you please provide more details about your symptoms? For example, when did the shortness of breath and chest pain start? Have you experienced any other symptoms such as dizziness, nausea, or fatigue?"  
# Observation: "i started having chest pain 2 days and i get sharp pain occasionally, maybe a little diziness as well"
# Thought: The user has now provided additional information about their symptoms, indicating that the chest pain started two days ago, is sharp, and they have experienced some dizziness. This information is crucial for the Diagnosis Team to analyze the situation effectively.

# Action: Delegate to Diagnostic Coordinator
# Observation: "the diagnositic team has concluded that the "