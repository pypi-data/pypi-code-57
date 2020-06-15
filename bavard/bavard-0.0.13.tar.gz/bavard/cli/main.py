import click

from bavard.cli.qa import qa
from bavard.cli.text_summarization import text_summarization
from bavard.cli.chatbots import chatbots


@click.group()
def cli():
    pass


cli.add_command(qa)
cli.add_command(text_summarization)
cli.add_command(chatbots)


def main():
    cli()


if __name__ == '__main__':
    cli()
