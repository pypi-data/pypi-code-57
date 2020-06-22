import io
from PIL import Image, ImageOps
import base64
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from wllib2.img_lib import img_utils

class ImgAzHandler():

    def __init__(self, app_env, input_args, input_file=None):
        self.env = app_env
        self.args = input_args
        self.file = input_file
        return 

    def get_image_text(self):
        cog_serv_endpoint = self.env.get_secret_value('ImgCogServicesEndpoint')
        cog_serv_key = self.env.get_secret_value('ImgCogServicesKey')
        az_img_ocr = img_utils.AzureImageOCR(endpoint=cog_serv_endpoint, key=cog_serv_key)
        img = Image.open(io.BytesIO(self.file))
        return az_img_ocr.get_image_text(img)



