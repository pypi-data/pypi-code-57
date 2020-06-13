import logging
import subprocess
import time

import rich


def do_test(args):
    logging.debug(args)

    from .._utils import get_adb_exe

    times: int = 0
    console = rich.console.Console()

    for _ in range(args.times):
        times += 1

        console.rule("epoch: {}".format(str(times)))
        console.print("[gold1][b]launching app")
        out = subprocess.Popen([get_adb_exe(), "shell", "am", "start", "-n",
                                "puzzle.blockpuzzle.cube.relax/com.meevii.unity.GameMainActivity"],
                               stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        stderr = out.stderr.read().decode("utf-8")
        stdout = out.stdout.read().decode("utf-8")

        if len(stderr) > 0:
            logging.warning(stderr)

        if len(stdout) > 0:
            console.print("[medium_spring_green]{}".format(stdout))

        wait_time = 30
        if args.interval:
            wait_time = args.interval

        from rich.progress import Progress
        with Progress() as progress:
            task1 = progress.add_task("[yellow]waiting app", total=wait_time * 10)
            for i in range(0, wait_time * 10):
                progress.update(task1, advance=1)
                time.sleep(0.1)

        console.print("[gold1][b]stopping app")
        out = subprocess.Popen([get_adb_exe(), "shell", "am", "force-stop", "puzzle.blockpuzzle.cube.relax"],
                               stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        stderr = out.stderr.read().decode("utf-8")
        stdout = out.stdout.read().decode("utf-8")

        if len(stderr) > 0:
            logging.warning(stderr)

        if len(stdout) > 0:
            console.print("[medium_spring_green]{}".format(stdout))

