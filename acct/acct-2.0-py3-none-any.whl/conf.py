CLI_CONFIG = {
    "acct_file": {"positional": True,},
    "acct_key": {"os": "ACCT_FILE_KEY",},
}
CONFIG = {
    "acct_file": {
        "default": None,
        "help": "The file to encrypt, a new file will be created.",
    },
    "acct_key": {
        "default": None,
        "help": "The key to encrypt the file with, if no key is passed a key will be generated and displayed on after the encrypted file is created",
    },
    "acct_profile": {"default": "default", "help": "The default profile to use",},
}
SUBCOMMANDS = {}
DYNE = {
    "acct": ["acct"],
}
