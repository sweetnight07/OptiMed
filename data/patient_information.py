import json

mock_patient_database = {
  "12345": {
    "medical_history": {
      "conditions": ["hypertension", "type 2 diabetes"],
      "medications": ["lisinopril", "metformin"],
      "allergies": ["penicillin"],
      "previous_visits": [
        {
          "date": "2023-12-15",
          "reason": "routine checkup",
          "findings": "blood pressure elevated (140/90)",
          "treatment": "adjusted lisinopril dosage"
        },
        {
          "date": "2023-08-20",
          "reason": "chest pain",
          "findings": "non-cardiac chest pain, likely musculoskeletal",
          "treatment": "prescribed NSAIDs"
        }
      ],
      "lab_results": [
        {
          "date": "2023-12-15",
          "type": "HbA1c",
          "value": "6.8%",
          "reference": "4.0-5.6%"
        },
        {
          "date": "2023-12-15",
          "type": "Lipid Panel",
          "value": "LDL: 130mg/dL",
          "reference": "<100mg/dL"
        }
      ]
    }
  },
  "67890": {
    "medical_history": {
      "conditions": ["atrial fibrillation", "osteoarthritis"],
      "medications": ["warfarin", "metoprolol"],
      "allergies": ["sulfa drugs"],
      "previous_visits": [
        {
          "date": "2024-01-10",
          "reason": "irregular heartbeat",
          "findings": "AFib with RVR",
          "treatment": "adjusted metoprolol dosage"
        }
      ],
      "lab_results": [
        {
          "date": "2024-01-10",
          "type": "INR",
          "value": "2.5",
          "reference": "2.0-3.0"
        }
      ]
    }
  }
}

