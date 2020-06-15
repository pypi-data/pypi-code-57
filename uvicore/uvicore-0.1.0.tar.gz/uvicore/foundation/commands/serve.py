import os
import typer
import uvicorn
from uvicore import config

from subprocess import Popen


cli = typer.Typer()

@cli.command()
def serve():
    """Unicorn dev server (reload and logs)
    """
    # Uvicorn dev server info
    appname = config('app.server.app')
    host = config('app.server.host')
    port = config('app.server.port')
    autoreload = config('app.server.reload')
    access_log = config('app.server.access_log')

    # Run Uvicorn server
    uvicorn.run(appname, host=host, port=port, reload=autoreload, access_log=access_log)
