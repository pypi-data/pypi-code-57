import docker
import click
import os
import yaml

DEBUG = False
CATACOMB_URL = 'http://localhost:8000' if DEBUG else 'https://beta.catacomb.ai'

def common_config():
    config = get_config()
    try:
        config["docker_client"] = docker.from_env()
    except:
        click.echo("Something went wrong! Ensure you have Docker installed and logged in locally.")
        os.exit(1)

    return config

def get_config():
    config = {}
    if not os.path.exists(".catacomb.yaml"):
        open(".catacomb.yaml", "a").close()
    else:
        with open(".catacomb.yaml", "r") as stream:
            found_config = yaml.safe_load(stream)
            if found_config != None:
                config = found_config
    
    saved_config = config.copy()

    if not "system_name" in config:
        if "CATACOMB_SYSTEM_NAME" in os.environ:
            config["system_name"] = os.environ["CATACOMB_SYSTEM_NAME"]
        else:
            config["system_name"] = click.prompt("🤖 Image name", type=str)
    if not "docker_username" in config:
        if "DOCKER_USERNAME" in os.environ:
            config["docker_username"] = os.environ["DOCKER_USERNAME"]
        else:
            config["docker_username"] = click.prompt("🤖 Docker hub username", type=str)

    if saved_config != config:
        with open(".catacomb.yaml", "w") as config_file:
            config_file.write(yaml.safe_dump(config))

    return config