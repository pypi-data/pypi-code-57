class Test:
    """
    A runable test

    Attributes
    ----------
    command : string
        The command the test is to compare against
    description : string
    result_lines : list of strings
         The expected result of the command
    """

    def __init__(self, command, setup_commands=None, description="", result_lines=None):
        self.command = command
        self.description = description
        self.result_lines = [] if result_lines is None else result_lines
        self.setup_commands = [] if setup_commands is None else setup_commands
