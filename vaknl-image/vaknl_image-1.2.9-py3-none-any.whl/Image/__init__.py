__author__ = "Wytze Bruinsma"

import os
import re
import requests
from PIL import Image
from dataclasses import dataclass
from io import BytesIO
from vaknl_gcp.Storage import StorageClient


@dataclass
class Acco:
    @dataclass
    class Image:
        url: str  # original url
        bucket_url: str = None  # bucket url
        width: int = None  # pixel with
        height: int = None  # pixel height
        bytes_size: int = None  # bytes size of image
        labels: list = None  # labels of the image
        descriptions: list = None  # descriptions of the image

    giataid: str
    source: str  # provider of the data
    images: list
    timestamp: str = None  # timestamp updated

    def __post_init__(self):
        if isinstance(self.giataid, int):
            self.giataid = str(self.giataid)

        if self.images:
            if not isinstance(self.images[0], Acco.Image):
                self.images = [Acco.Image(**image) for image in self.images]

    def basic_task(self):
        """
        Tasks are limited to 100KB
        So this is the bare minimum we need for a basic task
        :return:
        """
        return {
            'giataid': self.giataid,
            'source': self.source,
            'images': [{'url': image.url, 'descriptions': image.descriptions} for image in self.images]
        }


class ImageClient(object):

    def __init__(self, project_id):
        self.project_id = project_id
        self.storage_client = StorageClient(project_id=project_id)

    @staticmethod
    def get_image(image_url, auth=None, headers=None):
        for i in range(3):  # try 3 times if necessary
            try:
                response = requests.get(image_url, headers=headers, auth=auth)
                if response.status_code <= 204:
                    data = response.content
                    with Image.open(BytesIO(data)).convert('RGB') as img:
                        # convert to webp
                        with BytesIO() as bytes:
                            img.save(bytes, format='webp')
                            with Image.open(bytes) as web_img:
                                file_name = ''.join(os.path.basename(image_url).split('.')[0]) + '.webp'
                                width, height = web_img.size
                                size = web_img.tell()
                                return file_name, width, height, size, data
            except Exception as e:
                print(e)
        return None, None, None, None, None

    def upload_image_to_storage(self, id, bucket_name, image_url, auth=None):
        file_name, width, heigth, byte_size, image = self.get_image(image_url, auth)
        if image:
            bucket = self.storage_client.get_bucket(f'{bucket_name}-{self.project_id}')
            blob = bucket.blob(f"{id}/{file_name}")
            new_image_url = self.storage_client.upload_from_string(blob, image)
            return width, heigth, byte_size, new_image_url
        else:
            return None, None, None, None, None
