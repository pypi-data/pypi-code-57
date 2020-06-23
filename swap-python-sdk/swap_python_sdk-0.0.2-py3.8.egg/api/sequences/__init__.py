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

        return result
