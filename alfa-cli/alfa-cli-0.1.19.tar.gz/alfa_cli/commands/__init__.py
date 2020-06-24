from alfa_cli.commands.alfa import alfa
from alfa_cli.commands import configure, secrets, algorithm, resource

alfa.add_command(configure.configure)
alfa.add_command(algorithm.algorithm)
alfa.add_command(secrets.secrets)
alfa.add_command(resource.resource)