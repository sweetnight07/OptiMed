import agent

class SpecialistLLM():
    def __init__(self, model_name):
        # create the tools
        # create the prompt 
        self.generalist = agent.OpenAILLMs(model_name)

    def __call__():
        return None