CLI_CONFIG = {}
CONFIG = {
    "vultr_timeout": {
        "dyne": "idem",
        "group": "Idem Vultr",
        "default": None,
        "help": "timeout for vultr cloud commnads",
        "type": int,
        "os": "IDEM_VULTR_TIMEOUT",
    },
    "vultr_check_interval": {
        "dyne": "idem",
        "group": "Idem Vultr",
        "default": 15,
        "help": "When creating/changing an instance, check for it's every X seconds",
        "type": int,
        "os": "IDEM_VULTR_CHECK_INTERVAL",
    },
    "vultr_rate_limit": {
        "dyne": "idem",
        "group": "Idem Vultr",
        "default": 3,
        "help": "The number of calls that can be made to the vultr api per second",
        "type": int,
        "os": "IDEM_VULTR_CHECK_INTERVAL",
    },
}
SUBCOMMANDS = {}
DYNE = {
    "acct": ["acct"],
    "exec": ["exec"],
    "states": ["states"],
}
