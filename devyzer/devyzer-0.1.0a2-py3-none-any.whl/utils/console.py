from devyzer.utils import cli
from devyzer.utils.cli import wrap_with_color, bcolors


def print_bot_output(message, color=cli.bcolors.OKBLUE):
    """
     print outputs of bot
    :param message: message
    :param color: color of message
    :return:
    """
    text = message.get("text")
    if text is not None:
        cli.print_with_color(f'{wrap_with_color("> ", bcolors.OKGREEN)} {text.strip()}', color)

    quick_replies = message.get("quick_replies")
    if quick_replies is not None:
        for quick_reply in quick_replies:
            # questionary.rawselect(
            #     message.get("text"),
            #     qmark="Devyzer    -> ",
            #     choices=[quick_reply.get("title") for quick_reply in quick_replies],
            #     style=Style([('qmark', '#cce200'),
            #                  ('qmark', 'fg:#cce200'),  # token in front of the question
            #                  ('question', 'bold'),  # question text
            #                  ('answer', 'fg:#FFFFFF bold'),  # submitted answer text behind the question
            #                  ])
            # ).ask()

            cli.print_with_color(f' {quick_reply.get("title").strip()}', bcolors.OKBLUE)
