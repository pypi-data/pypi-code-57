import os
import click
import requests
import docker
import urllib.request

DEBUG = False
CATACOMB_URL = 'http://localhost:8000' if DEBUG else 'https://beta.catacomb.ai'

@click.command()
def cli():
    # Try getting Docker daemon instance
    try:
        client = docker.from_env()
    except:
        click.echo("Something went wrong! Ensure you have Docker installed and logged in locally.")

    # Prompt user for image metadata
    name = click.prompt("🤖 Image name", type=str)
    docker_username = click.prompt("🤖 Docker account username", type=str)
    repository = docker_username + '/' + name


    # Try cloning deployment files and building image
    click.echo("""\n🤖 Got it! Building your Docker image (this may take a while)...""")
    
    urllib.request.urlretrieve("https://raw.githubusercontent.com/catacomb-ai/examples/master/mnist_classifier/Dockerfile", "./Dockerfile")
    urllib.request.urlretrieve("https://raw.githubusercontent.com/catacomb-ai/examples/master/mnist_classifier/server.py", "./server.py")

    try:
        image = client.images.build(path='./', tag={repository})
    except:
        click.echo("Something went wrong! Ensure that your Pipfile and system.py are correctly specified and try again.")

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

    # Try performing system clean-up
    try:    
        os.remove("./Dockerfile")
        os.remove("./server.py") 
    except:
        click.echo("Something went wrong! Ensure your system includes all the necessary components and try again.")