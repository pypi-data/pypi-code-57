CLI_CONFIG = {"config": {"options": ["-c"],}, "cmd": {"positional": True,}}
CONFIG = {
    "config": {
        "default": "build.conf",
        "help": 'The location of the Bodger configuration file, this defaults to the local directory and a file called "bodger.conf."',
    },
    "cmd": {"default": "test", "help": "The command to execute when bodger is called",},
}
SUBCOMMANDS = {}
DYNE = {
    "bodger": ["bodger"],
}
