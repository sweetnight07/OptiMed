MASTER_EXAMPLE = """
Master Agent: "Hello, we are here to assist you. Please provide your symptoms, age, and patient ID if available."

Human Input: "Chest pain or discomfort, shortness of breath, nausea or vomiting, dizziness, and fatigue."

Master Agent: Action: Delegate to Diagnosis Team.

Diagnosis Coordinator: Takes symptoms and patient information.

Diagnosis Coordinator: Action: Delegate the information to the Generalist.

Generalist: Takes input from the patient.

Generalist Action: Search patient history.

Generalist Action: Refer to Cardiologist.

Cardiologist: Takes input from the patient.

Cardiologist Action: Searches the database and conducts a symptom analysis based on the information provided.

... (Converse among agents as needed)

Diagnosis Coordinator: Action: Delegate to Recommender Agent.

Recommender: Takes the diagnosis provided by the Diagnosis Team.

Recommender Action: Use tools for recommendation system to suggest appropriate next steps.

Recommender: "Based on the diagnosis, we suggest an ECG."

Diagnosis Coordinator: "The diagnosis has concluded that the symptoms are indicative of a heart attack. The Recommender has suggested an ECG. Would you like to book an appointment?"

Human Input: "Yes, I would like to schedule an appointment."

Diagnosis Coordinator: "Please provide your preferred time."

Human Input: "Let's do this Friday from 12:30 PM to 1:00 PM."

Diagnosis Coordinator: Action: Delegate to Scheduler Agent.

Scheduler Agent: Accesses the calendar API and delegates the task of scheduling the appointment in the patient's Google Calendar.
"""
