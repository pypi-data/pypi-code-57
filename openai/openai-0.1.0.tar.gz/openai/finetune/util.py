from termcolor import colored
import openai
from contextlib import contextmanager
import time


def ask_user_bool(question):
    while True:
        answer = input(question + " [y/n] ")
        if answer == "y":
            return True
        elif answer == "n":
            return False


def exit_if_no(question):
    ok = ask_user_bool(colored(question, color="magenta", attrs={"bold"}))
    if not ok:
        print(colored("Exiting", color="red"))
        exit(1)
