CLI_CONFIG = {
    "grains": {
        "positional": True,
        "nargs": "*",
        "default": [],
        "help": "Print the named grains",
        "type": str,
    },
    "output": {"options": ["-o", "--output"], "source": "rend"},
    "timeout": {"options": ["-t", "--timeout"]},
}

CONFIG = {
    "timeout": {
        "help": "The maximum time to wait for grains to be collected",
        "type": int,
        "default": None,
        "os": "GRAINS_TIMEOUT",
    }
}

DYNE = {
    "grains": ["grains"],
}
