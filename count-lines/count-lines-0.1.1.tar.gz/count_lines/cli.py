
import click
import clipboard_util
from input_util import I


@click.command()
@click.option('--clipboard', '-c', is_flag=True, default=False)
def cli(clipboard):

    if not clipboard:
        print("Not implemented")
        raise click.Abort()

    clipoard_content = clipboard_util.paste()
    lines_count = I(clipoard_content).line_count_with_text
    print(lines_count)
