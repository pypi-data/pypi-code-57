"""
    aiocheck

    A python asyncio host health checker using native ping commands.

    Example:
    ```
    import aiocheck
    aiocheck.cli.main(['localhost'])
    ```

    :copyright: 2020 kruserr
    :license: MIT
"""

from aiocheck.Database import Database
from aiocheck.Host import Host
