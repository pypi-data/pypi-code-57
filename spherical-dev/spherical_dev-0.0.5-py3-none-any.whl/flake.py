import invoke


@invoke.task
def flake(ctx):
    ctx.run('flake8 tests/ src/ tasks.py --max-line-length=127')
