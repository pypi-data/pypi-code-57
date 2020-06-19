from typing import List

import psutil
import socket
from multiprocessing import Process
import requests
import typer


def is_remo_server_running(config):
    try:
        resp = requests.get('{}/version'.format(config.get_host_address())).json()
        return resp.get('app') == 'remo'
    except Exception:
        pass
    return False


def try_to_terminate_another_remo_app(config):
    if not is_remo_server_running(config):
        return False

    msg = f'Another instance of remo-app is running on port {config.port}, do you want to stop it and start a new one?'
    if not typer.confirm(msg, default=True):
        return False

    terminate_remo(config)

    if not is_port_in_use(config.port):
        return True

    typer.echo(f'Failed to terminate the remo-app, port {config.port} still in use')
    return False


def list_and_confirm_kill_remo(config):
    processes = None
    if is_remo_server_running(config):
        processes = list_remo_processes(config)

    if not processes:
        typer.echo('No other remo processes found.')
        return

    typer.echo('This will kill the following processes:\n'
               'PID\tStatus\t  Name')
    for p in processes:
        try:
            info = p.as_dict(attrs=['pid', 'name', 'status'])
            typer.echo('{}\t{}\t  {}'.format(info['pid'], info['status'], info['name']))
        except Exception as err:
            typer.echo(err)

    if typer.confirm('\nDo you want to continue?', default=True):
        terminate_processes(processes)


def kill_background_process(*processes):
    for process in processes:
        if isinstance(process, Process) and process.is_alive():
            process.terminate()

    typer.echo('\nRemo was stopped.')


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', int(port))) == 0


def terminate_remo(config):
    processes = list_remo_processes(config)
    terminate_processes(processes)


def find_processes(name="", starts_with=""):
    processes = []
    for proc in psutil.process_iter():
        try:
            info = proc.as_dict(attrs=['pid', 'name'])
            if info and info['name']:
                process_name = info['name'].lower()
                if name and name == process_name:
                    processes.append(proc)
                elif starts_with and process_name.startswith(starts_with):
                    processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return processes


def terminate_electron_app():
    processes = find_processes(starts_with='remo')
    terminate_processes(processes)


def terminate_processes(processes: List[psutil.Process]):
    for p in processes:
        terminate_process(p)


def terminate_process(p: psutil.Process):
    typer.echo(f'Terminating process: {p}')
    try:
        p.terminate()
        p.wait(2)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, psutil.TimeoutExpired) as err:
        typer.echo(f'ERROR: {err}')


def list_remo_electron_processes():
    return find_processes(starts_with='remo')


def list_remo_app_processes(config):
    port = int(config.port)
    processes = []
    try:
        for p in find_processes(starts_with='python'):
            connections = p.connections("inet4")
            if len(connections):
                conn = connections[0]
                if config.is_local_server():
                    if conn.laddr and conn.laddr.port == port:
                        processes.append(p)
                else:
                    if conn.raddr and conn.raddr.port == port:
                        processes.append(p)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

    return processes


def list_remo_processes(config):
    return list_remo_electron_processes() + list_remo_app_processes(config)
