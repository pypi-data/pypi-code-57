import os
import io
import sys
import struct
from PIL import Image, ImageOps
import sys, time, requests, traceback
import PyPDF2
from PyPDF2 import PdfFileReader
import json

'''
import os
import io
import sys
import struct
from PIL import Image, ImageOps
import sys, time, requests, traceback
import PyPDF2
from PyPDF2 import PdfFileReader
import base64
from collections import namedtuple
import warnings
import json

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

warnings.filterwarnings("ignore")

PdfImage = namedtuple('PdfImage', ['data', 'format','image_name'])


'''
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

'''
def convert_gray(img, preprocessing):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if preprocessing == 'thresh':
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    elif preprocessing == 'blur':
        gray = cv2.medianBlur(gray, 3)
    return gray
'''

def tiff_header_for_CCITT(width, height, img_size, CCITT_group=4):
    # http://www.fileformat.info/format/tiff/corion.htm
    fields = 8
    tiff_header_struct = '<' + '2s' + 'H' + 'L' + 'H' + 'HHLL' * fields + 'L'
    return struct.pack(tiff_header_struct,
                       b'II',  # Byte order indication: Little indian
                       42,  # Version number (always 42)
                       8,  # Offset to first IFD
                       fields,  # Number of tags in IFD
                       256, 4, 1, width,  # ImageWidth, LONG, 1, width
                       257, 4, 1, height,  # ImageLength, LONG, 1, lenght
                       258, 3, 1, 1,  # BitsPerSample, SHORT, 1, 1
                       259, 3, 1, CCITT_group,  # Compression, SHORT, 1, 4 = CCITT Group 4 fax encoding
                       262, 3, 1, 0,  # Threshholding, SHORT, 1, 0 = WhiteIsZero
                       # StripOffsets, LONG, 1, len of header
                       273, 4, 1, struct.calcsize(tiff_header_struct),
                       278, 4, 1, height,  # RowsPerStrip, LONG, 1, length
                       279, 4, 1, img_size,  # StripByteCounts, LONG, 1, size of image
                       0  # last IFD
                       )


def image_to_byte_array(img:Image, img_format):
    imgByteArrIOStream = io.BytesIO()
    img.save(imgByteArrIOStream, format=img_format)
    imgBytes = imgByteArrIOStream.getvalue()
    return imgBytes


class AzureImageOCR():
    def __init__(self, endpoint=None, key=None):
        if endpoint is not None:
            self.endpoint = endpoint
        if key is not None:
            self.key = key
        self.client = ComputerVisionClient(self.endpoint, CognitiveServicesCredentials(self.key))
        return
        
    def get_image_text(self, img, preprocess='blur'):
        '''Performing OCR using Azure Cognitive API. 
        See https://docs.microsoft.com/en-gb/azure/cognitive-services/computer-vision/quickstarts/python-hand-text?tabs=version-3
        
        :params image: image binary 
        :returns extracted_text: string of the recognized text
        '''
        image_bytes = image_to_byte_array(img, 'JPEG')
        text_recognition_url = self.endpoint +  "/vision/v3.0-preview/read/analyze"
        headers = {'Ocp-Apim-Subscription-Key': self.key, 'Content-Type': 'application/octet-stream'}
        params = {'language': 'en'}
        response = requests.post(text_recognition_url, headers=headers, params=params, data=image_bytes)
        response.raise_for_status()
        
        # Hold the URL used to retreive the recognized text
        operation_url = response.headers['Operation-Location']

        # Poll to wait for completion
        analysis = {}
        poll = True
        while (poll):
            response_final = requests.get(operation_url, headers=headers)
            analysis = response_final.json()
            time.sleep(1)
            if ('analyzeResult' in analysis):
                poll = False
            if ('status' in analysis and analysis['status'] == 'failed'):
                poll = False
        
        # Extract the recognized text
        extracted_text = ''
        if ('analyzeResult' in analysis):
            text = [x['text'] for x in analysis['analyzeResult']['readResults'][0]['lines']]
            extracted_text = ' '.join(x for x in text)

        # Extract the word bounding box and text
        return extracted_text

