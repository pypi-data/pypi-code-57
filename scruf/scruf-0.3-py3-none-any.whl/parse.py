import enum

from scruf import exception, test


class Parser:
    """
    Parser for parsing raw tests

    Attributes
    ----------
    indent : string
        The indentation to be used when parsing tests
    """

    def __init__(self, indent="    "):
        self.tokeniser = _Tokeniser(indent)
        self.fsm = _FSM(self.tokeniser)

        self._content_getter = {
            self.fsm.States.DESCRIPTION: self.tokeniser.get_description,
            self.fsm.States.SETUP_COMMAND: self.tokeniser.get_setup_command,
            self.fsm.States.TEST_COMMAND: self.tokeniser.get_test_command,
            self.fsm.States.CONTINUE: self.tokeniser.get_continue,
            self.fsm.States.RESULT: self.tokeniser.get_result,
        }

    def parse(self, lines):
        """Parse raw lines into `scruf.test.Test` objects

        Parameters
        ----------
        lines : list of str

        Returns
        -------
        list of `scruf.test.Test`

        Raises
        ------
        scruf.parse.ProgressionError
            If an invalid progression is found, e.g. the raw lines hold a description
            followed by a continuation line
        """

        prev_state = self.fsm.States.START
        tests = []
        test = self._new_test()

        for i, line in enumerate(lines):
            if self.tokeniser.is_comment(line) or self.tokeniser.is_empty(line):
                continue

            state = self.fsm.progress(prev_state, line)
            if state == self.fsm.States.START:
                tests.append(self._test_to_test_object(test))
                test = self._new_test()
                state = self.fsm.progress(state, line)

            if state is None:
                from_state = self.fsm.state_name(prev_state)
                expected_states = self.fsm.get_named_progressions(prev_state)
                raise ProgressionError(i, line, from_state, expected_states)
            # Preserve newlines for results
            if not state == self.fsm.States.RESULT:
                line = line.rstrip()

            test[state].append(self._content_getter[state](line))
            prev_state = state

        tests.append(self._test_to_test_object(test))
        return tests

    def _new_test(self):
        return dict((key, []) for key in self._content_getter)

    def _test_to_test_object(self, raw_test):
        command = " ".join(
            raw_test[self.fsm.States.TEST_COMMAND] + raw_test[self.fsm.States.CONTINUE]
        )
        description = " ".join(raw_test[self.fsm.States.DESCRIPTION])
        result_lines = raw_test[self.fsm.States.RESULT]
        setup_commands = raw_test[self.fsm.States.SETUP_COMMAND]
        return test.Test(
            command,
            setup_commands=setup_commands,
            description=description,
            result_lines=result_lines,
        )


class ProgressionError(exception.CramerError):
    """
    Exception for invalid progressions when parsing raw lines

    Attributes
    ----------
    line_num : int
    line_content : str
    from_state : str
        Human readable version of the state before the invalid line
    expected_states : list of str
        List of human readable version of the expected states given `from_state`

    """

    def __init__(self, line_num, line_content, from_state, expected_states):
        message = "Failed to parse line {}: {}\nExpected line of type: {}".format(
            line_num, line_content.rstrip(), " or ".join(expected_states),
        )
        super().__init__(message)

        self.line_num = line_num
        self.from_state = from_state
        self.expected_states = expected_states


class _Tokeniser:
    def __init__(self, indent):
        self.comment_character = "#"
        self.command_character = "$"
        self.continue_character = ">"
        self.indent = indent

        self.command_prefix = self.indent + self.command_character
        self.continue_prefix = self.indent + self.continue_character

        pass

    def is_test_command(self, line):
        return line.startswith(self.command_prefix)

    def is_setup_command(self, line):
        return line.startswith(self.command_character)

    def is_continue(self, line):
        return line.startswith(self.continue_prefix)

    def is_description(self, line):
        return (
            not line[0].isspace()
            and not self.is_comment(line)
            and not self.is_setup_command(line)
        )

    def is_comment(self, line):
        return line.startswith(self.comment_character)

    def is_empty(self, line):
        return not line or not line.startswith(self.indent) and line.isspace()

    def is_result(self, line):
        return (
            line.startswith(self.indent)
            and not self.is_test_command(line)
            and not self.is_continue(line)
        )

    def get_test_command(self, line):
        return line[len(self.command_prefix) :].strip()

    def get_setup_command(self, line):
        return line[len(self.command_character) :].strip()

    def get_continue(self, line):
        return line[len(self.continue_prefix) :].strip()

    def get_description(self, line):
        return line

    def get_result(self, line):
        return line[len(self.indent) :]


class _FSM:
    class States(enum.Enum):
        START = enum.auto()
        DESCRIPTION = enum.auto()
        SETUP_COMMAND = enum.auto()
        TEST_COMMAND = enum.auto()
        CONTINUE = enum.auto()
        RESULT = enum.auto()

    STATE_NAMES = {
        States.START: "start",
        States.DESCRIPTION: "description",
        States.SETUP_COMMAND: "setup_command",
        States.TEST_COMMAND: "test_command",
        States.CONTINUE: "continue",
        States.RESULT: "result",
    }

    def __init__(self, tokeniser):
        self.tokeniser = tokeniser

        self.progressions = {
            self.States.START: {
                self.States.DESCRIPTION: self.tokeniser.is_description,
                self.States.SETUP_COMMAND: self.tokeniser.is_setup_command,
                self.States.TEST_COMMAND: self.tokeniser.is_test_command,
            },
            self.States.DESCRIPTION: {
                self.States.DESCRIPTION: self.tokeniser.is_description,
                self.States.SETUP_COMMAND: self.tokeniser.is_setup_command,
                self.States.TEST_COMMAND: self.tokeniser.is_test_command,
            },
            self.States.SETUP_COMMAND: {
                self.States.SETUP_COMMAND: self.tokeniser.is_setup_command,
                self.States.TEST_COMMAND: self.tokeniser.is_test_command,
            },
            self.States.TEST_COMMAND: {
                self.States.CONTINUE: self.tokeniser.is_continue,
                self.States.RESULT: self.tokeniser.is_result,
                self.States.START: lambda line: self.tokeniser.is_description(line)
                or self.tokeniser.is_test_command(line)
                or self.tokeniser.is_setup_command(line),
            },
            self.States.CONTINUE: {
                self.States.CONTINUE: self.tokeniser.is_continue,
                self.States.RESULT: self.tokeniser.is_result,
                self.States.START: lambda line: self.tokeniser.is_description(line)
                or self.tokeniser.is_test_command(line),
            },
            self.States.RESULT: {
                self.States.RESULT: self.tokeniser.is_result,
                self.States.START: lambda line: self.tokeniser.is_description(line)
                or self.tokeniser.is_test_command(line),
            },
        }

    def progress(self, from_state, line):
        for to_state, condition in self.progressions[from_state].items():
            if condition(line):
                return to_state
        return None

    @classmethod
    def state_name(cls, state):
        return cls.STATE_NAMES[state]

    def get_named_progressions(self, state):
        progression_states = list(self.progressions[state].keys())

        # "Start" is just an internal state, so avoid presenting it
        if self.States.START in progression_states:
            del progression_states[progression_states.index(self.States.START)]
            progression_states += self.progressions[self.States.START].keys()
        return [self.state_name(s) for s in progression_states]
