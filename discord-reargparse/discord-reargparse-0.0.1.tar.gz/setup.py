# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discord_reargparse']

package_data = \
{'': ['*']}

install_requires = \
['discord.py>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'discord-reargparse',
    'version': '0.0.1',
    'description': 'RegEx based argument parsing for commands in discord.py',
    'long_description': 'discord_reargparse\n==================\n\nProvides support for RegEx based argument parsing in commands for the\n[discord.py](https://github.com/Rapptz/discord.py/) library.\n\n```python\nparam_converter = RegExArgConverter(\n    r"^(\\S+[\\ \\S]*?)(?:\\ -c(\\d+))?(\\ -n)?$",\n    # OR re.compile(r"^(\\S+[\\ \\S]*?)(?:\\ -c(\\d+))?(\\ -n)?$"),\n    \n    string = Parameter(\n        default="hello!",\n    ),\n    count = Parameter(\n        int,\n        default=2,\n    ),\n    new_line = Parameter(\n        lambda x: bool(x),\n    )\n)\n\n# ...\n\n@bot.command()\nasync def repeat(ctx, *, params:param_converter=param_converter.defaults):\n    string = params["string"]\n    count = params["count"]\n    sep = "\\n" if params.get("new_line", False) else " "\n    \n    await ctx.send(sep.join([string]*count))\n\n@repeat.error\nasync def repeat_error(ctx, error):\n    if isinstance(error, NotMatchedWithPattern):\n        await ctx.send(\n            "{0} not matched with pattern r\'{1}\'".format(\n                repr(error.argstr), error.pattern.pattern,\n            )\n        )\n```\n\nOn your discord server, the commands can be invoked like this:\n\n```\n!repeat\n\n> hello! hello!\n\n!repeat Hi -c3 -n\n\n> Hi\n> Hi\n> Hi\n\n!repeat hello\nworld\n\n    → will raise a NotMatchedWithPattern exception\n```\n\n\nInstallation\n------------\n\nInstallation is available via pip:\n\n```\npip install discord_reargparse\n```\n\n\nDocumentation\n-------------\n\nInitialize an `RegExArgConverter` as in the example above, annotate a\nkeyword-only function argument in your command with the instance and,\noptionally, set its default value by using the `.defaults` attribute.\nSetting a default value can be omitted for non-optional regex groups.\n\nIt will raise a `NotMatchedWithPattern` exception if not matched\nwith given regex pattern.\n\nInside the command, you can access the arguments as a dict.\n\n\ncommand\'s usage\n---------------\n\nThe usage string of repeat command is displayed like.\n```\n!help repeat\n\n> repeat [params=Args(r\'^(\\S+[\\ \\S]*?)(?:\\ -c(\\d+))?(\\ -n)?$\' => [string=hello!] [count=2] <new_line>)]\n```\n\nYou might also want to set the `usage` parameter of the `command()` function\ndecorator to display a alternative usage string, especially when using the\n`RegExArgConverter.defaults` attribute.\n',
    'author': 'nkpro2000sr',
    'author_email': 'srnaveen2k@yahoo.com',
    'maintainer': 'nkpro2000sr',
    'maintainer_email': 'srnaveen2k@yahoo.com',
    'url': 'https://github.com/nkpro2000sr/discord-reargparse',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
