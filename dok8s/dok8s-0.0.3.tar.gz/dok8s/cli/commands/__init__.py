"""Commands init
"""
from dok8s.cli.commands.component import ComponentCommand
from dok8s.cli.commands.docker import DockerCommand
from dok8s.cli.commands.resource import ResourceCommand

COMMANDS = [
    ComponentCommand,
    DockerCommand,
    ResourceCommand,
]
