import random
import sys

import click

from engineerquiz.questions import QUESTIONS


QUIZ_LENGTH = 6


TRUE_ENDING = (
    "AHA! You tried to hack this, didn't you? No need for you to take this test; "
    "you must be a 999x engineer!"
)


@click.command()
def main():
    score = 0

    questions = random.sample(list(QUESTIONS.keys()), QUIZ_LENGTH)

    for question in questions:
        click.echo()
        click.secho(question, bold=True)

        # Question and options
        choices = QUESTIONS[question]
        ordered_choices = list(choices.keys())
        random.shuffle(ordered_choices)
        for i, choice in enumerate(ordered_choices):
            click.echo(f'{i}. {choice}')

        # Answer prompt
        answer = click.prompt(click.style('Enter a number', dim=True))

        try:
            answer = int(answer.strip())
        except ValueError:
            click.echo(TRUE_ENDING)
            sys.exit()

        if 0 <= answer <= len(choices) - 1:
            score += choices[ordered_choices[answer]]
        else:
            click.echo(TRUE_ENDING)
            sys.exit()

    click.echo()
    click.secho('=' * 80, dim=True)
    click.echo()
    click.echo(
        'Congratulations, you are a '
        + click.style(f' {score}x engineer ', bg='magenta', blink=True, bold=True)
        + '!'
    )
    click.echo()
    click.pause('')
    click.secho('Does that look like an arbitrary number?', dim=True)
    click.secho('Well, what did you expect from a random quiz from the internet?', dim=True)
    click.echo()
    click.pause('')
    click.secho("You're awesome and don't let anyone tell you otherwise.", dim=True)
