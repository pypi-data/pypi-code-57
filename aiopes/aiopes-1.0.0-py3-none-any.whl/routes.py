class Routes:
    _route = "https://api.pacifices.cloud/v1/"

    server_base = "servers"
    server_validate = "servers/validate"
    server_get = "servers/{}"
    server_logs = "servers/{}/logs"
    server_player_history = "servers/{}/player-history"
    server_player_count = "servers/{}/player-count"
    server_version = "servers/{}/version"
    server_commad = "servers/{}/command"
    server_reset = "servers/{}/restart"
    server_update = "servers/{}/update"
    server_history = "servers/{}/history"

    locations = "locations"
    mapgroups = "mapgroups"
    mods = "mods"
    plugins = "plugins"
    tickrates = "tickrates"
    gamemodes = "gamemodes"
    files = "files"

    def format_routes(self):
        """
        Formats PES routes.
        """

        routes = [
            attr for attr in dir(Routes())
            if not callable(getattr(Routes(), attr))
            and not attr.startswith("__")
            and not attr.startswith("_")
        ]

        for route in routes:
            setattr(
                self,
                route,
                (
                    self._route
                    +
                    getattr(
                        self,
                        route
                    )
                )
            )


ROUTES = Routes()
ROUTES.format_routes()
