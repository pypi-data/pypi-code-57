from .wrapped_requests import AWR
from .routes import ROUTES


class Validate:
    async def create(self, **kwargs):
        """
        https://api.pacifices.cloud/docs.html#servers-server-payload-validation-post
                Validate's a payload.
        """

        return (
                await AWR(
                        ROUTES.server_validate,
                        json=kwargs
                ).post()
            )["result"]["valid"]

    async def settings(self, **kwargs):
        """ https://api.pacifices.cloud/docs.html#servers-server-payload-validation-put
                Validate a payload used to update a server’s settings.
        """

        return (
                await AWR(
                        ROUTES.server_validate,
                        json=kwargs
                ).put()
            )["result"]["valid"]
