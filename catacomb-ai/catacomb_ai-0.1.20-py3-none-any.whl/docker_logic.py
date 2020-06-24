import click
import os
from .common import common_config, CATACOMB_URL
from .static import DOCKERFILE, SERVER
import requests
from functools import partial
import signal
import subprocess
import shutil

@click.command()
def build():
    config = common_config()
    client = config["docker_client"]

    repository = config["docker_username"] + '/' + config["system_name"]

    # Try cloning deployment files and building image
    click.echo("🤖 Building your Docker image (this may take a while so you might wanna grab some coffee ☕)...")

    os.makedirs("./catacomb-out", exist_ok=True)
    with open('./catacomb-out/Dockerfile', 'w') as f:
        f.write(DOCKERFILE)
    with open('./catacomb-out/server.py', 'w') as f:
        f.write(SERVER)

    try:
        os.environ["DOCKER_BUILDKIT"] = "1"
        process = subprocess.Popen(['docker', 'build', '.', '-t', repository, '-f', 'catacomb-out/Dockerfile'], 
                           universal_newlines=True)
        ret_code = None
        while ret_code is None:
            ret_code = process.poll()

        if ret_code != 0:
            raise Exception(f"Failed to build image. See above for errors.")
    except Exception as error:
        print(repr(error))
        click.echo("Something went wrong! Some artifacts might be left over in ./catacomb-out")
        exit(1)

    try:
        shutil.rmtree("./catacomb-out")
    except Exception as error:
        print(repr(error))
        click.echo("Something went wrong! Ensure your system includes all the necessary components and try again.")
        exit(1)

    click.echo(f'🤖 Image {repository} built!\n')

@click.command()
def push():
    config = common_config()
    client = config["docker_client"]

    login_if_required(client)

    repository = config["docker_username"] + '/' + config["system_name"]

    # Try pushing image to registry
    try:
        click.echo("Pushing your image to the Docker Registry (this may take a while)...")
        process = subprocess.Popen(['docker', 'push', repository], 
                           universal_newlines=True)
        ret_code = None
        while ret_code is None:
            ret_code = process.poll()

        if ret_code != 0:
            raise Exception(f"Failed to push image. see above for errors.")
    except Exception as error:
        print(repr(error))
        click.echo("Something went wrong! Ensure you have the correct permissions to push to {} and try again.".format(repository))
        exit(1)

    # Try adding image to Catacomb servers
    try:
        r = requests.post(f'{CATACOMB_URL}/api/upload/', json={'image': repository, 'name': config["system_name"]})
        image = r.json()['image']
        click.echo(f"🤖 We've pushed your system's image to: https://hub.docker.com/r/{repository}/.\n")
        click.echo(f'Almost done! Finalize and deploy your system at: {CATACOMB_URL}/upload/image/{image}/')
    except Exception as error:
        print(repr(error))
        click.echo("Something went wrong! Double check your connection and try again.")
        exit(1)

@click.command()
@click.option('--detach', default=False)
@click.option('--remove', default=True)
@click.option('--port', default=8080)
def start(detach, remove, port):
    config = common_config()
    client = config["docker_client"]

    repository = config["docker_username"] + '/' + config["system_name"]
    container_name = f'{config["docker_username"]}-{config["system_name"]}-test'

    ports = {
        f'8080/tcp': ('127.0.0.1', port)
    }
    env = ["PORT=8080"]

    try:
        click.echo(f'🤖 Image {repository} now running. Press Ctrl+C to stop it.')
        signal.signal(signal.SIGINT, partial(signal_handler, client, container_name))
        container = client.containers.run(repository, detach=True, auto_remove=remove,
            ports=ports, name=container_name, environment=env)
        if not detach:
            for line in container.logs(stream=True):
                click.echo(line, nl=False)
    except Exception as error:
        print(repr(error))
        click.echo("Something went wrong! Ensure you've run `catacomb build`.",)
        exit(1)

def login_if_required(client):
    if "DOCKER_USERNAME" in os.environ and "DOCKER_PASSWORD" in os.environ:
        client.login(
            username=os.environ["DOCKER_USERNAME"],
            password=os.environ["DOCKER_PASSWORD"],
            registry=os.getenv("DOCKER_REPO", default="docker.io")
        )

def signal_handler(client, container_name, signum, frame):
    click.echo("Stopping container")
    cont = client.containers.get(container_name)
    cont.stop()
    exit(0)
