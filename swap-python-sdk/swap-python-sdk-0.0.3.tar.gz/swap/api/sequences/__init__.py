from swap.common.logging import logger
from swap.api.sequences.step_codes import StepCode

class CommandSequence:
    def __init__(self):
        self.current_index = 0
        self.index = {}
        self.steps = []

    def add_step(self, key, step):
        self.steps.append(step)
        self.index[key] = self.current_index
        self.current_index += 1

    def call(self, input):
        result = input

        for step in self.steps:
            result = step.call(result)

            if result == StepCode.NoServiceRequestsReceived:
                logger.info("No service requests received")
                return {"Result":"No service requests have been received, stopping workflow"}
            elif result == StepCode.NoServiceOffersReceived:
                logger.info("No service offers received")
                return {"Result":"No service offers have been received, stopping workflow"}

        return result