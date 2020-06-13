import random

from app.check import check


def generate(bits):
    return "".join([random.choice("10") for i in range(bits)])


def generate_problems(bits, num_problems):
    return [generate(bits) for i in range(num_problems)]


def generate_answers(problems):
    return [check(problem) for problem in problems]
