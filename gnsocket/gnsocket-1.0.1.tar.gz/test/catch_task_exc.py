import asyncio
from tasktools.taskloop import coromask, renew, simple_fargs
import functools
from termcolor import colored, cprint

"""
A test example to raise an exceptio throw an asyncio task
"""

def gprint(text):
    msg = colored(text, 'green', attrs=['reverse', 'blink'])
    print(msg)

def bprint(text):
    msg = colored(text, 'blue', attrs=['reverse', 'blink'])
    print(msg)

def rprint(text):
    msg = colored(text, 'red', attrs=['reverse', 'blink'])
    print(msg)

if __name__ == "__main__":
    mode = 'server'
    print("Entrando a loop")
    loop = asyncio.get_event_loop()

    async def div0(n):
        try:
            print(n)
            n/0
        except:
            raise Exception()

    def div0_task():
        try:
            args=[10]
            task=loop.create_task(
                coromask(
                    div0,
                    args,
                    simple_fargs)
            )
            task.add_done_callback(
                functools.partial(
                    renew,
                    task,
                    div0,
                    simple_fargs)
            )
        except Exception as exec:
            raise exec

    try:
        div0_task()
        loop.run_forever()
    except:
        raise Exception()
    loop.close()
