import click
import os
from .common import common_config, CATACOMB_URL
from .static import DOCKERFILE, SERVER
import requests
from functools import partial
import signal

@click.command()
def build():
    config = common_config()
    client = config["docker_client"]

    repository = config["docker_username"] + '/' + config["system_name"]

    # Try cloning deployment files and building image
    click.echo("🤖 Building your Docker image (this may take a while so you might wanna grab some coffee ☕)...")

    with open('./Dockerfile', 'w') as f:
        f.write(DOCKERFILE)
    with open('./server.py', 'w') as f:
        f.write(SERVER)

    try:
        image = client.images.build(path='./', tag={repository})
    except Exception as error:
        print(repr(error))
        click.echo("Something went wrong! Ensure that your Pipfile and system.py are correctly specified and try again.")
        return

    try:
        os.remove("./Dockerfile")
        os.remove("./server.py") 
    except Exception as error:
        print(repr(error))
        click.echo("Something went wrong! Ensure your system includes all the necessary components and try again.")
        return

    click.echo(f'🤖 Image {repository} built!\n')

@click.command()
def push():
    config = common_config()
    client = config["docker_client"]

    repository = config["docker_username"] + '/' + config["system_name"]

    # Try pushing image to registry
    try:
        click.echo("Pushing your image to the Docker Registry (this may take a while)...")
        for line in client.images.push(repository, stream=True, decode=True):
            click.echo(line)
    except Exception as error:
        print(repr(error))
        click.echo("Something went wrong! Ensure you have the correct permissions to push to {} and try again.".format(repository))
        return

    # Try adding image to Catacomb servers
    try:
        r = requests.post(f'{CATACOMB_URL}/api/upload/', json={'image': repository, 'name': config["system_name"]})
        image = r.json()['image']
        click.echo(f"🤖 We've pushed your system's image to: https://hub.docker.com/r/{repository}/.\n")
        click.echo(f'Almost done! Finalize and deploy your system at: {CATACOMB_URL}/upload/image/{image}/')
    except Exception as error:
        print(repr(error))
        click.echo("Something went wrong! Double check your connection and try again.")

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

def signal_handler(client, container_name, signum, frame):
    click.echo("Stopping container")
    cont = client.containers.get(container_name)
    cont.stop()
    exit(0)
