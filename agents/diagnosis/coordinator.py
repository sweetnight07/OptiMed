import agent

# start initializing all of the agents
from diagnosis import generalist
from diagnosis import internist
from diagnosis import specialist

class CoordinatorAgent:
    def __init__(self, model_name="gpt-4o-mini"):
        # create the instances 
        self.generalist = generalist.GeneralistLLM(model_name)
        self.internist = internist.InternistLLM(model_name)
        self.specialist = specialist.SpecialistLLM(model_name)

        # initialize the coordinator tools 

    def __call