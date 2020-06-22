#import os
import io
#import sys
#import struct
from PIL import Image, ImageOps
#import sys, time, requests, traceback
import PyPDF2
from PyPDF2 import PdfFileReader
#import base64
#from collections import namedtuple
import warnings
#import json

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from wllib2.img_lib import img_utils

#PdfImage = namedtuple('PdfImage', ['data', 'format','image_name'])

warnings.filterwarnings("ignore")

img_modes = {'/DeviceRGB': 'RGB', '/DefaultRGB': 'RGB',
             '/DeviceCMYK': 'CMYK', '/DefaultCMYK': 'CMYK',
             '/DeviceGray': 'L', '/DefaultGray': 'L',
             '/Indexed': 'P'}


def extract_image_objects_from_pdf_page(xObject):
    image_obj_list = []
    xobj_res_xobj_obj = None
    
    if xObject:
        xobj_res = xObject.get('/Resources')
        if xobj_res:
            xobj_res_xobj = xobj_res.get('/XObject')
            if xobj_res_xobj:
                xobj_res_xobj_obj = xobj_res_xobj.getObject()

    #xObject = xObject['/Resources']['/XObject'].getObject()

    if xobj_res_xobj_obj:
        for obj in xobj_res_xobj_obj:
            # xObj_this_obj = xObject.get(obj)
            xObj_this_obj = xobj_res_xobj_obj[obj]

            subtype_is_image = False
            if xObj_this_obj:
                if xObj_this_obj.get('/Subtype') == '/Image':
                    subtype_is_image = True

            if subtype_is_image:
                size = (xObj_this_obj.get('/Width'), xObj_this_obj.get('/Height'))
                data = xObj_this_obj._data
                xobj_obj = xObj_this_obj
                color_space = xobj_obj.get('/ColorSpace')
                if '/FlateDecode' in xobj_obj.get('/Filter'):
                    if isinstance(color_space, PyPDF2.generic.ArrayObject) and color_space[0] == '/Indexed':
                        color_space, _, _, _ = [v.getObject() for v in color_space] 
                    mode = img_modes[color_space]
                    data = xObj_this_obj.getData() 
                    img = Image.frombytes(mode, size, data)
                    if color_space == '/Indexed':
                        img.putpalette(lookup.getData())
                        img = img.convert('RGB')
                    imgByteArr = io.BytesIO()
                    img.save(imgByteArr,format='PNG')
                    if img.width > img.height:
                        img = img.rotate(90, expand=True)
                    image_obj_list.append(img)                
                elif '/DCTDecode' in xobj_obj.get('/Filter') or '/JPXDecode' in xobj_obj.get('/Filter'):
                    img = Image.open(io.BytesIO(data))
                    if img.width > img.height:
                        img = img.rotate(90, expand=True)
                    image_obj_list.append(img)
                elif '/CCITTFaxDecode' in xobj_obj.get('/Filter'):
                    decode_params = xObj_this_obj.get('/DecodeParms')
                    if decode_params.get('/K') == -1:
                        CCITT_group = 4
                    else:
                        CCITT_group = 3
                    data = xObj_this_obj._data 
                    img_size = len(data)
                    tiff_header = img_utils.tiff_header_for_CCITT(size[0], size[1], img_size, CCITT_group)
                    img = Image.open(io.BytesIO(tiff_header + data))

                    if img.width > img.height:
                        img = img.rotate(90, expand=True)
                    
                    image_obj_list.append(img)
            else:
                image_obj_list += extract_image_objects_from_pdf_page(xObj_this_obj)
    
    return image_obj_list

def get_pdf_images_from_pypdf2(py_pdf2_file, max_pages):
    pdf_file_image_list = []
    for p in range(max_pages):
        page_image_list = extract_image_objects_from_pdf_page(py_pdf2_file.getPage(p))
        for img in page_image_list:
            pdf_file_image_list.append(img)
    return pdf_file_image_list


def get_text_from_pdfbytes_images(pdf_bytes, cog_serv_endpoint, cog_serv_key, max_pages = -1):
    wholetext = ''
    number_of_pages_in_pdf = 0

    py_pdf2_file = PyPDF2.PdfFileReader(io.BytesIO(pdf_bytes))
    number_of_pages_in_pdf = py_pdf2_file.getNumPages()

    if max_pages == -1:
        max_pages = number_of_pages_in_pdf
    else:
        max_pages if max_pages > number_of_pages_in_pdf else number_of_pages_in_pdf
    
    pdf_page_images = get_pdf_images_from_pypdf2(py_pdf2_file, max_pages)

    if len(pdf_page_images):
        az_ocr = img_utils.AzureImageOCR(endpoint=cog_serv_endpoint, key=cog_serv_key)
        for page_img in pdf_page_images:
            wholetext += az_ocr.get_image_text(page_img)

    return wholetext, len(pdf_page_images), number_of_pages_in_pdf



