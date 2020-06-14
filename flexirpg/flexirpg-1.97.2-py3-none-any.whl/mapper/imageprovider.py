# FlexiRPG -- Provide image data from files or the network.
#
# Copyright (C) 2017 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
import os.path
from uuid import UUID

import orpg.dirpath

class ImageProvider(object):
    """Base class image providers.

    Image provides supply the image data (in PNG or JPG format) given
    a UUID.

    See @ImageProviderCache and @ImageProviderNetwork.

    """

    def __init__(self):
        pass

    def fetch(self, image):
        """Asynchronously fetch image data.

        Calls image.set_image() when it is available.

        Returns True if the fetch is being attempted, False if the
        provider cannot supply the image.

        The image library will call each registered image provider in
        turn, until one return True.

        """
        return False

    def fetch_local(self, image):
        """Synchronously fetch the image data.
        """
        return False

class ImageProviderCache(ImageProvider):
    """Provides images from a local filesystem cache.

    Images are cached in ~/.flexirpg/images/<uuid>.{png|jpg}"""

    def __init__(self):
        self.images_dir = os.path.join(orpg.dirpath.dir_struct["user"], "images")

    def fetch(self, image):
        # Try all supported file extensions.
        for ext in ("png", "jpg"):
            path = os.path.join(self.images_dir, "{}.{}".format(image.uuid, ext))
            if os.path.exists(path):
                with open(path, "rb") as f:
                    data = f.read()
                image.set_image(data)
                return True
        return False

    def fetch_local(self, image):
        return self.fetch(image)

class ImageProviderClient(ImageProvider):
    """Provide images by querying the server.

    Clients send an IMAGEFETCH message, and the server responds with
    IMAGEDATA.

    Clients should have an ImageProviderCache, to cache images locally
    to reduces the number of IMAGEFETCH messages.

    See @ImageProviderServer.

    """
    def __init__(self, connection, image_library):
        ImageProvider.__init__(self)

        self.connection = connection
        self.image_library = image_library

        connection.add_msg_handler("imagedata", self.on_imagedata)
        connection.add_msg_handler("imagequery", self.on_imagequery)
        connection.add_msg_handler("imagefetch", self.on_imagefetch)

    def fetch(self, image):
        if not self.connection.is_connected():
            return False
        self.connection.outbox.put("<imagefetch id='%s' uuid='%s'/>"
                                   % (self.connection.id, image.uuid))
        return True

    def on_imagedata(self, id, msg, xml_dom):
        uuid = UUID(xml_dom.getAttribute("uuid"))
        image = self.image_library.get(uuid)
        if not image.has_image():
            image.set_image_from_base64(xml_dom.getAttribute("data"))

    def on_imagequery(self, id, msg, xml_dom):
        uuid = UUID(xml_dom.getAttribute("uuid"))
        image = self.image_library.get_local(uuid)
        if image:
            self.connection.outbox.put("<imageinfo id='%s' uuid='%s'/>"
                                       % (self.connection.id, image.uuid))

    def on_imagefetch(self, id, msg, xml_dom):
        uuid = UUID(xml_dom.getAttribute("uuid"))
        image = self.image_library.get_local(uuid)
        if image:
            self.connection.outbox.put("<imagedata uuid='%s' data='%s'/>"
                                       % (uuid, image.base64()))


class ImageProviderServer(ImageProvider):
    """Provide images by requesting it from clients.

    The server broadcasts a IMAGEQUERY message to all connected
    clients. Clients respond with IMAGEINFO messages if the have the
    image data (they do not respond if they do not have the data).
    The server sends an IMAGEFETCH message to the first client that
    responds.  The client sends the data back in an IMAGEDATA message.

    The server should have an ImageProviderCache, to cache images
    locally to avoid having to repeatedly send requests.

    """

    def __init__(self, server):
        self.server = server
        self.queried = {}

        self.server.addsvrcmd("imagefetch", self.on_imagefetch)
        self.server.addsvrcmd("imageinfo", self.on_imageinfo)
        self.server.addsvrcmd("imagedata", self.on_imagedata)

    def fetch(self, image):
        imagequery = "<imagequery uuid='%s'/>" % image.uuid
        self.server.send_to_all("0", imagequery)
        self.queried[image.uuid] = image
        return True

    def on_imagefetch(self, xml_dom, data):
        id = xml_dom.getAttribute("id")
        uuid = UUID(xml_dom.getAttribute("uuid"))

        image = self.server.image_library.get(uuid)
        if image.has_image():
            self.send_imagedata(id, image)
        else:
            image.add_requester(self, id)

    def on_imageinfo(self, xml_dom, data):
        id = xml_dom.getAttribute("id")
        uuid = UUID(xml_dom.getAttribute("uuid"))

        image = self.queried.pop(uuid, None)
        if image:
            imagefetch = "<imagefetch uuid='%s'/>" % image.uuid
            self.server.players[id].outbox.put(imagefetch)

    def on_imagedata(self, xml_dom, data):
        uuid = UUID(xml_dom.getAttribute("uuid"))
        data = xml_dom.getAttribute("data")

        image = self.server.image_library.get(uuid)
        if not image.has_image():
            image.set_image_from_base64(data)

    def send_imagedata(self, id, image):
        imagedata = "<imagedata uuid='%s' data='%s'/>" % (image.uuid, image.base64())
        self.server.players[id].outbox.put(imagedata)
