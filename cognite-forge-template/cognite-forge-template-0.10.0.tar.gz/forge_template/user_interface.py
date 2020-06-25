from typing import Callable, Dict, List, Optional

import colorama
from click import confirm
from pyfiglet import Figlet
from termcolor import colored, cprint


class UserInterface:
    RETURN = "b"
    EXIT = "e"

    colorama.init()

    @staticmethod
    def print_title(title):
        cprint(Figlet(font="slant").renderText(title), "white")

    @staticmethod
    def print_failure(msg):
        cprint(msg, "red")

    @staticmethod
    def print_warning(msg):
        cprint(msg, "yellow")

    @staticmethod
    def print_ok(msg):
        cprint(msg, "green")

    @staticmethod
    def print_in_progress(msg):
        cprint(msg, "blue")

    def get_input(
        self,
        prompt: str,
        default: str = "",
        choices: Optional[List[str]] = None,
        validate: Optional[Callable[[str], bool]] = None,
    ) -> str:
        _prompt = self.format_prompt(prompt, choices, default)
        value = input(_prompt) or default
        if choices and value not in choices:
            self.print_failure("Must be one of {}".format(choices))
            return self.get_input(prompt, default, choices, validate)
        if validate and validate(value) is False:
            return self.get_input(prompt, default=default, choices=choices, validate=validate)
        return value

    def show_menu(self, prompt: str, options: Dict[str, Callable], is_top_level: bool = False) -> str:
        choice = ""
        while not (choice == self.EXIT or (choice == self.RETURN and not is_top_level)):
            choice = self.get_menu_selection(prompt, list(options.keys()), is_top_level=is_top_level)
            if not (choice == self.EXIT or (choice == self.RETURN and not is_top_level)):
                choice = options[choice]()
        return choice

    def get_menu_selection(self, prompt, choices: List[str], is_top_level: bool = False) -> str:
        print()
        for i, choice in enumerate(choices):
            print("[{}] {}".format(colored(str(i), "green"), choice))
        print()
        if not is_top_level:
            print("[{}] {}".format(colored(self.RETURN, "green"), "Back"))
        print("[{}] {}".format(colored(self.EXIT, "green"), "Exit"))
        print()
        choice = self.get_input(prompt)

        i_choices = [str(i) for i in range(len(choices))] + ([self.EXIT] if is_top_level else [self.RETURN, self.EXIT])
        while choice not in i_choices:
            self.print_failure("Must be one of {}".format(i_choices))
            choice = self.get_input(prompt)

        if choice in [self.EXIT, self.RETURN]:
            return choice
        return choices[int(choice)]

    def get_input_list_of_dicts(self, prompt: str, validators: Dict[str, Callable[[str], bool]], keys: List[str]):
        result = []
        while confirm(prompt, prompt_suffix="? ", show_default=True, default=False):
            values = {}
            for key in keys:
                values[key] = self.get_input(key.capitalize(), validate=validators[key])

            result.append(values)

        return result

    @staticmethod
    def format_prompt(prompt: str, choices: Optional[List[str]], default: str) -> str:
        _prompt = prompt
        if choices:
            _prompt += colored(" ({})".format("/".join(choices)), "blue")
        if default:
            _prompt += colored(" [{}]".format(default), "cyan")
        return _prompt + ": "
