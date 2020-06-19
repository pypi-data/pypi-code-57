import logging
import os
from multiprocessing import Process
import atexit

from .config import Config
from .killer import is_port_in_use, try_to_terminate_another_remo_app, kill_background_process, terminate_electron_app
from .log import Log


def delayed_browse(config, debug=False):
    if config.viewer == 'electron':
        from .viewer.electron import browse
    else:
        from .viewer.browser import browse

    url = build_url(config)
    browse(url, debug)


def build_url(config, initial_page='datasets'):
    page = initial_page.strip('/')
    return '{}/{}/'.format(config.get_host_address(), page)


def run_server(config, debug=False, background_job=None, with_browser=True):
    debug = debug or config.debug
    if debug:
        os.environ['DJANGO_DEBUG'] = 'True'
    from remo_app.config.standalone.wsgi import application

    if config.is_local_server() and is_port_in_use(config.port):
        Log.error(f'Failed to start remo-app, port {config.port} already in use.')

        ok = try_to_terminate_another_remo_app(config)
        if not ok:
            Log.msg(f'You can change default port in config file: {Config.path()}')
            return
    else:
        terminate_electron_app()

    if config.is_local_server():
        if with_browser:
            ui_process = Process(target=delayed_browse, args=(config, debug), daemon=True)
            ui_process.start()

            # background_job_process = Process(target=background_job)
            # background_job_process.start()
            # atexit.register(kill_process, ui_process, background_job_process)

            atexit.register(kill_background_process, ui_process)

        start_server(application, config.port)

    else:
        Log.msg(f'Remo is running on remote server: {config.get_host_address()}')
        if with_browser:
            delayed_browse(config, debug)


def start_server(application, port: str = Config.default_port):
    from waitress import serve

    logging.basicConfig()
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.ERROR)

    Log.msg(f'Serving on http://localhost:{port}')
    serve(application, _quiet=True, port=port, threads=3)
