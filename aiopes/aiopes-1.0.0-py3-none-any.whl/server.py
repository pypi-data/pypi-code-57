from .wrapped_requests import AWR
from .routes import ROUTES

from .models.server import ServerModel
from .models.logs import LogsModel
from .models.players import PlayersHistoryModel
from .models.version import VersionModel
from .models.history import HistoryModel


class Server:
    def __init__(self, server_id):
        self.server_id = server_id

    async def create(self, **kwargs):
        """ https://api.pacifices.cloud/docs.html#servers-servers-post
                Creates a new server.
        """

        data = await AWR(
            ROUTES.server_base,
            json=kwargs
        ).post()

        self.server_id = data["result"]["id"]

    async def get(self):
        """ https://api.pacifices.cloud/docs.html#servers-server-actions-get
                Retrieve a server’s information.
        """

        data = await AWR(
            ROUTES.server_get.format(
                self.server_id
            )
        ).get()

        return ServerModel(data["result"]["server"])

    async def delete(self):
        """ https://api.pacifices.cloud/docs.html#servers-server-actions-delete
                Destroy a server.
        """

        await AWR(
            ROUTES.server_get.format(
                self.server_id
            )
        ).delete(json=False)

    async def settings(self, **kwargs):
        """ https://api.pacifices.cloud/docs.html#servers-server-actions-put
                Change a server’s settings. Also performs an update on the
                server to ensure the server settings are applied.
        """

        await AWR(
            ROUTES.server_get.format(
                self.server_id
            ),
            json=kwargs
        ).put(json=False)

    async def logs(self):
        """ https://api.pacifices.cloud/docs.html#servers-server-logs-get
                Retrieve a server’s logs.
                    - json, should we return a dict or data.
        """

        data = await AWR(
            ROUTES.server_logs.format(
                self.server_id
            )
        ).get()

        for log in data["result"]["logs"].values():
            yield LogsModel(log)

    async def player_history(self):
        """ https://api.pacifices.cloud/docs.html#servers-server-player-history-get
                Get a history of the player count on the server.
        """

        data = await AWR(
            ROUTES.server_player_history.format(
                self.server_id
            )
        ).get()

        for player in data["result"]:
            yield PlayersHistoryModel(player)

    async def player_count(self):
        """ https://api.pacifices.cloud/docs.html#servers-server-player-count-get
                Get the current count of players in the server.
        """

        data = await AWR(
            ROUTES.server_player_count.format(
                self.server_id
            )
        ).get()

        return data["result"]["players"]

    async def version(self):
        """ https://api.pacifices.cloud/docs.html#servers-server-version-get
                Get the current server version and
                whether the server is up-to-date.
        """

        data = await AWR(
            ROUTES.server_version.format(
                self.server_id
            )
        ).get()

        return VersionModel(data)

    async def command(self, command: str):
        """ https://api.pacifices.cloud/docs.html#servers-server-command-post
                Send a command to a server.

                command: str
                    console command.
        """

        await AWR(
            ROUTES.server_commad.format(
                self.server_id
            ),
            json={
                "command": command,
            }
        ).post(json=False)

    async def restart(self):
        """ https://api.pacifices.cloud/docs.html#servers-server-restart-post
                Restart a server.
        """

        await AWR(
            ROUTES.server_reset.format(
                self.server_id
            )
        ).post(json=False)

    async def update(self):
        """ https://api.pacifices.cloud/docs.html#servers-server-update-post
                Update a server.
        """

        await AWR(
            ROUTES.server_update.format(
                self.server_id
            )
        ).post(json=False)

    async def history(self):
        """ https://api.pacifices.cloud/docs.html#servers-server-history-get
                Retrieve a server’s history.
        """

        data = await AWR(
            ROUTES.server_history.format(
                self.server_id
            )
        ).get()

        for history in data["result"]:
            yield HistoryModel(history)
