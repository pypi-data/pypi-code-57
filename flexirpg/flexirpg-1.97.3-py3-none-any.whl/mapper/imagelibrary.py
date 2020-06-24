# FlexiRPG -- Library of images identified by UUID.
#
# Copyright (C) 2017 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from uuid import UUID, uuid4

class ImageLibrary(object):
    def __init__(self, image_class):
        """Create an empty image library.

        """

        self.image_class = image_class
        self.providers = []
        self.images = {}

    def register_provider(self, provider):
        self.providers.append(provider)

    def unregister_provider(self, provider):
        assert provider in self.providers

        providers.remove(providers)

    def add(self, image):
        self.images[image.uuid] = image
        if not image.has_image():
            self._fetch(image)

    def get(self, uuid, size=None):
        """Get an images from the cache by its UUID.

        The image data will be requested but may not be immediately
        available (e.g., if it needs to be fetched from a client or
        server.).

        """

        assert type(uuid) == UUID

        if uuid in self.images:
            return self.images[uuid]
        new_image = self.image_class(uuid=uuid, size=size)
        self.add(new_image)
        return new_image

    def get_local(self, uuid):
        """Get an image from the library, iff it exists locally.

        If the image exists locally, the image data will be
        immediately available, otherwise None is returned.

        """
        if uuid in self.images:
            image = self.images[uuid]
            if image.has_image():
                return image
        else:
            image = self.image_class(uuid)
            if self._fetch_local(image):
                self.images[image.uuid] = image
                return image
        return None

    def _fetch(self, image):
        for provider in self.providers:
            if provider.fetch(image):
                return True
        return False

    def _fetch_local(self, image):
        for provider in self.providers:
            if provider.fetch_local(image):
                return True
        return False

    def get_from_file(self, path):
        f = open(path, "rb")
        data = f.read()
        f.close()

        image = self.image_class(uuid4())
        image.set_image(data)
        self.add(image)
        return image
