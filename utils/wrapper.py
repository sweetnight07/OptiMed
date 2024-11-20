from functools import wraps
from typing import Dict

def enforce_dict_input(func):
    @wraps(func)
    def wrapper(report, *args, **kwargs):
        # Ensure the report is a dictionary
        if not isinstance(report, dict):
            raise ValueError(f"Expected input to be a dictionary, but got {type(report)}")

        # Ensure it has the required keys and correct types
        expected_keys = ['patient_info', 'messages', 'diagnosis', 'recommendations', 'appointment_details']
        for key in expected_keys:
            if key not in report:
                raise ValueError(f"Missing expected key: '{key}' in the report dictionary.")
        
        # Check the types of the values
        if not isinstance(report['patient_info'], str):
            raise ValueError("Expected 'patient_info' to be a string.")
        
        if not isinstance(report['messages'], list):
            raise ValueError("Expected 'messages' to be a list of dictionaries.")
        
        if not isinstance(report['diagnosis'], str):
            raise ValueError("Expected 'diagnosis' to be a string.")
        
        if not isinstance(report['recommendations'], str):
            raise ValueError("Expected 'recommendations' to be a string.")
        
        if not isinstance(report['appointment_details'], str):
            raise ValueError("Expected 'appointment_details' to be a string.")

        # If everything checks out, call the original function
        return func(report, *args, **kwargs)
    
    return wrapper
