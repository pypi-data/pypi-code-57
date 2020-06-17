""" Adds support for a shortcut file with some of the most common CLI
attributes. """


def shortcut_file(args):
    """ Read the current folder to see if there is a .evc_manager file
     with authentication options. If file is not found or has a permission
     error, just ignore and return args.

     If a specific argument was provided via CLI, it takes precedence."""

    try:
        source_file = args.shortcut_file if args.shortcut_file else ".evc_manager"
        with open(source_file, 'r') as stream:
            lines = stream.readlines()

        auth_options = dict()
        for line in lines:
            auth_options[line.split("=")[0]] = line.split("=")[1].split("\n")[0]

    except (OSError, FileNotFoundError):
        return args

    if not (args.oess_url or args.kytos_url):

        if "url" in auth_options and "backend" in auth_options:
            if auth_options['backend'] == 'oess':
                args.oess_url = auth_options["url"]
            elif auth_options["backend"] == "kytos":
                args.kytos_url = auth_options["url"]

    if not args.user and "user" in auth_options:
        args.user = auth_options["user"]

    if not args.password and "password" in auth_options:
        args.password = auth_options["password"]

    if not args.tenant and "tenant" in auth_options:
        args.tenant = auth_options["tenant"]

    return args
