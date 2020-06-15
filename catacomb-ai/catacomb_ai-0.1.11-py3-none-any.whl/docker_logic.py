import click
import os
from .common import common_config, CATACOMB_URL
from .static import DOCKERFILE, SERVER
import requests

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
    except:
        click.echo("Something went wrong! Ensure that your Pipfile and system.py are correctly specified and try again.")

    try:    
        os.remove("./Dockerfile")
        os.remove("./server.py") 
    except:
        click.echo("Something went wrong! Ensure your system includes all the necessary components and try again.")

    click.echo(f'🤖 Image {repository} built!\n')

def push():
    config = common_config()
    client = config["docker_client"]

    repository = config["docker_username"] + '/' + config["system_name"]

    # Try pushing image to registry
    try:
        click.echo("Pushing your image to the Docker Registry (this may take a while)...")
        for line in client.images.push(repository, stream=True, decode=True):
            click.echo(line)
    except:
        click.echo("Something went wrong! Ensure you have the correct permissions to push to {} and try again.".format(repository))

    # Try adding image to Catacomb servers
    try:
        r = requests.post('{}/api/upload/'.format(CATACOMB_URL), json={'image': repository, 'name': name})
        image = r.json()['image']
        click.echo("""\n🤖 We've pushed your system's image to: https://hub.docker.com/r/{}/.""".format(repository))
        click.echo('Almost done! Finalize and deploy your system at: {}/upload/image/{}/'.format(CATACOMB_URL, image))
    except Exception as error:
        print(repr(error))
        click.echo("Something went wrong! Double check your connection and try again.")
