import click
from click import ClickException

from app.config import BEGIN_ANSWERS_TOKEN
from app.generate import generate_answers, generate_problems
from app.pdf import make_pdf


@click.command()
@click.argument("bits", type=click.INT)
@click.argument("num-problems", type=click.INT)
@click.option("--pdf", default=False, is_flag=True)
@click.option("--silent", default=False, is_flag=True)
@click.option("--include-answers", default=True, is_flag=True)
@click.option("--output-filepath")
@click.option("--num-columns", default=4)
@click.option("--font-size", default=12)
def main(
    bits: int,
    num_problems: int,
    pdf: bool = False,
    silent: bool = False,
    include_answers: bool = True,
    output_filepath: str = None,
    num_columns: int = 4,
    font_size: int = 12,
) -> None:

    validate_args(pdf, silent, output_filepath)

    answers, problems = make_problems_and_answers(bits, num_problems)

    if bits > 12:
        num_columns = 3

    if pdf:
        silent = True
        make_pdf(
            problems=problems,
            answers=answers,
            output_path=output_filepath or "problems.pdf",
            include_answers=include_answers,
            num_columns=num_columns,
            font_size=font_size,
        )

    if not silent:
        if include_answers:
            click.echo(BEGIN_ANSWERS_TOKEN.join((problems, answers)))
        else:
            click.echo(problems)


def validate_args(pdf, silent, output_filepath):
    if pdf and silent:
        raise ClickException(
            "please specify either `pdf` or `silent`, not both (otherwise there "
            "won't be any outcome of running the app!"
        )

    if pdf and output_filepath and not output_filepath.endswith("pdf"):
        raise ClickException("Please include an output filepath ending in '.pdf'")


def make_problems_and_answers(bits, num_problems):
    problems = generate_problems(bits, num_problems)
    answers = generate_answers(problems)
    problems_string = "\n\n".join(problems)
    answers_string = "\n\n".join(
        [f"{problem} | {answer} " for problem, answer in zip(problems, answers)]
    )
    return answers_string, problems_string
