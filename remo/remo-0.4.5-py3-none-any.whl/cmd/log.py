import typer


class Log:
    @staticmethod
    def exit_msg(msg: str):
        Log.msg(msg)
        raise typer.Exit()

    @staticmethod
    def exit_warn(msg: str):
        Log.exit(msg, status='WARNING')

    @staticmethod
    def exit(msg: str, status='ERROR'):
        Log.error(msg, status=status)
        raise typer.Exit()

    @staticmethod
    def run_again(msg: str):
        Log.exit(f"""{msg}
and then run again `python -m remo_app init`
""")

    @staticmethod
    def installation_aborted(msg: str = ''):
        Log.exit(f"""{msg}
Installation aborted.
""")

    @staticmethod
    def warn(msg: str):
        Log.error(msg, status='WARNING')

    @staticmethod
    def error(msg: str, status='ERROR'):
        Log.msg(f'{status}: {msg}')

    @staticmethod
    def msg(msg: str):
        typer.echo(msg)


    @staticmethod
    def stage(msg: str, marker='[-]', separator='\n{}\n'.format('-' * 50)):
        Log.msg(f'{separator}{marker} {msg}')
