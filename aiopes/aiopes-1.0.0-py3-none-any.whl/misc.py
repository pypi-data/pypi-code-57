class Misc(object):
    async def locations(self):
        """ https://api.pacifices.cloud/docs.html#locations-locations-get
                Get all available locations where you can deploy a server.
        """
        
        return await self._get(url=self.ROUTES["locations"])

    async def mapgroups(self):
        """ https://api.pacifices.cloud/docs.html#mapgroups
                Get all available mapgroups.
        """
        
        return await self._get(url=self.ROUTES["mapgroups"])

    async def mods(self):
        """ https://api.pacifices.cloud/docs.html#mods-mods-get
                Get all available mods.
        """
        
        return await self._get(url=self.ROUTES["mods"])

    async def plugins(self):
        """ https://api.pacifices.cloud/docs.html#plugins
                Get all available plugins.
        """
        
        return await self._get(url=self.ROUTES["plugins"])

    async def tickrates(self):
        """ https://api.pacifices.cloud/docs.html#tickrates-tickrates-get
                Get all available tickrates.
        """
        
        return await self._get(url=self.ROUTES["tickrates"])

    async def gamemodes(self):
        """ https://api.pacifices.cloud/docs.html#gamemodes-gamemodes-get
                Get all available gamemodes.
        """
        
        return await self._get(url=self.ROUTES["gamemodes"])

    async def files(self):
        """ https://api.pacifices.cloud/docs.html#files
                Get all available files.
        """
        
        return await self._get(url=self.ROUTES["files"])