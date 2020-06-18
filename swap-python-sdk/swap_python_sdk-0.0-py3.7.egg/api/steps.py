class CommandStep:
    def __init__(self, command, pre_hook, post_hook):
        self.command = command
        self.pre_hook = pre_hook
        self.post_hook = post_hook

    def call(self, input):
        pre_hook_output = self.pre_hook.call(input)
        command_output = self.command.call(pre_hook_output)
        post_hook_output = self.post_hook.call(command_output)

        return post_hook_output
