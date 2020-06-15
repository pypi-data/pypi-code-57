import click


class AliasedGroup(click.Group):
    """Support command aliases"""

    # Map of aliased commands
    aliases = {}

    def get_command(self, ctx, cmd_name):
        cmd = super().get_command(ctx, cmd_name)
        if cmd is not None:
            return cmd
        if cmd_name in self.aliases:
            return super().get_command(ctx, self.aliases[cmd_name])
        ctx.fail("Unknown command: {0}".format(cmd_name))

    def command(self, *args, alias=None, **kwargs):
        aliases = alias or []
        if not aliases:
            return super().command(*args, **kwargs)

        if not isinstance(aliases, list):
            aliases = [aliases]
        original_decorator = super().command(*args, cls=AliasedCommand, **kwargs)

        def decorator(f):
            cmd = original_decorator(f)
            cmd.aliases = aliases
            for name in aliases:
                self.aliases[name] = cmd.name
            return cmd

        return decorator


class AliasedCommand(click.Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aliases = []

    def get_short_help_str(self, *args, **kwargs):
        short_help = super().get_short_help_str(*args, **kwargs)
        if not self.aliases:
            return short_help
        alias_list = ", ".join(self.aliases)
        alias_suffix = f" (alias: {alias_list})"
        if short_help.endswith("."):
            short_help = short_help[:-1]
            alias_suffix += "."
        return short_help + alias_suffix
