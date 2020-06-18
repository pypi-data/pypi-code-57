import io
from PIL import Image, ImageOps
import PyPDF2
from PyPDF2 import PdfFileReader
import base64
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from wllib2.pdf_lib import pdf_utils


def create_pdf_func_response(pdf_file, cog_serv_endpoint, cog_serv_key, max_pages):
    resp_dict = {}
    pdf_text, n_pages, n_pages_in_pdf = pdf_utils.get_text_from_pdfbytes_images(pdf_file, cog_serv_endpoint, cog_serv_key, max_pages = max_pages)
    resp_dict['PDFText'] = pdf_text
    resp_dict['NumberOfPDFPagesScanned'] = n_pages
    resp_dict['TotalPagesInPDF'] = n_pages_in_pdf
    return resp_dict

class PDFAzHandler():

    def __init__(self, app_env, input_args, input_file=None):
        self.env = app_env
        self.args = input_args
        self.file = input_file
        return 

    def get_binary_pdf_info(self):
        response_dict = {}
        pdf = PdfFileReader(io.BytesIO(self.file))
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()
        response_dict['information'] = information
        response_dict['number_of_pages'] = number_of_pages
        return response_dict

    def get_json_pdf_info(self):
        response_dict = {}
        pdf_file_base64 = self.args.get('PDFFile')
        pdf_file_name = self.args.get('PDFFileName')
        pdf_file = base64.b64decode(pdf_file_base64)
        pdf = PdfFileReader(io.BytesIO(pdf_file))
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()
        response_dict['FileName'] = pdf_file_name
        response_dict['information'] = information
        response_dict['number_of_pages'] = number_of_pages
        return response_dict

    def get_blob_pdf_info(self):
        response_dict = {}
        connect_str = self.env.get_parameter('AzStorageContainer')
        local_file_name = self.args.get('PDFFile')
        container_name = self.args.get('StorageSubDir')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
        fstream = blob_client.download_blob()
        pdf_file = fstream.readall()
        pdf = PdfFileReader(io.BytesIO(pdf_file))
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()
        response_dict['PDF'] = local_file_name
        response_dict['Blob'] = container_name
        response_dict['information'] = information
        response_dict['number_of_pages'] = number_of_pages
        return response_dict

    def get_pdffile_images_text(self):
        max_pages = -1
        max_pages_str = self.args.get('MaxPages')
        if max_pages_str is not None:
            max_pages = int(max_pages_str)
        cog_serv_endpoint = self.env.get_secret_value('ImgCogServicesEndpoint')
        cog_serv_key = self.env.get_secret_value('ImgCogServicesKey')
        return create_pdf_func_response(self.file, cog_serv_endpoint, cog_serv_key, max_pages)

    def get_pdfjson_images_text(self):
        max_pages = -1
        pdf_file_base64 = self.args.get('PDFFile')
        max_pages_str = self.args.get('MaxPages')
        if max_pages_str is not None:
            max_pages = int(max_pages_str)
        cog_serv_endpoint = self.env.get_secret_value('ImgCogServicesEndpoint')
        cog_serv_key = self.env.get_secret_value('ImgCogServicesKey')
        return create_pdf_func_response(base64.b64decode(pdf_file_base64),  cog_serv_endpoint, cog_serv_key, max_pages)

    def get_pdfblob_images_text(self):
        connect_str = self.env.get_parameter('AzStorageContainer')
        local_file_name = self.args.get('PDFFile')
        container_name = self.args.get('StorageSubDir')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
        fstream = blob_client.download_blob()
        pdf_file = fstream.readall()

        max_pages_str = self.args.get('MaxPages')
        if max_pages_str is not None:
            max_pages = int(max_pages_str)
        else:
            max_pages = -1

        cog_serv_endpoint = self.env.get_secret_value('ImgCogServicesEndpoint')
        cog_serv_key = self.env.get_secret_value('ImgCogServicesKey')

        return create_pdf_func_response(pdf_file, cog_serv_endpoint, cog_serv_key, max_pages)



