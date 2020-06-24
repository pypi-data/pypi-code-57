from swap.common.logging import logger
from swap.api.sequences.step_codes import StepCode

class CommandStep:
    def __init__(self, command, pre_hook, post_hook):
        self.command = command
        self.pre_hook = pre_hook
        self.post_hook = post_hook

    def check_for_errors(self, output):
        if output == StepCode.NoServiceRequestsReceived:
            return False
        elif output == StepCode.NoServiceOffersReceived:
            return False
        else:
            return True

    def call(self, input):
        pre_hook_output = self.pre_hook.call(input)
        if self.check_for_errors(pre_hook_output) == False:
            return pre_hook_output
        command_output = self.command.call(pre_hook_output)
        if self.check_for_errors(command_output) == False:
            return command_output
        post_hook_output = self.post_hook.call(command_output)
        if self.check_for_errors(post_hook_output) == False:
            return post_hook_output

        return post_hook_output
