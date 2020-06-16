CLI_CONFIG = {
    "grains": {
        "positional": True,
        "nargs": "*",
        "default": [],
        "help": "Print the named grains",
        "type": str,
    },
    "output": {"options": ["-o", "--output"], "source": "rend"},
}

CONFIG = {}

DYNE = {
    "grains": ["grains"],
}
