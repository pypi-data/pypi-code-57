import pandas as pd
from wllib2.db_lib import db_utils
import io
from PIL import Image
from PyPDF2 import PdfFileReader
import base64
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient


class AzTestHandler():

    def __init__(self, app_env, input_args, input_file=None):
        self.env = app_env
        self.args = input_args
        self.file = input_file
        return 

    def get_env_name(self):
        return f"This function is executing on the  {self.env.get_env_name()}!"

    def say_hello(self):
        name = self.args.get('Name')
        return f"Simon's Azure function says hello {name}!"

    def maths_numbers(self):
        a = self.args.get('a')
        b = self.args.get('b')
        sum_response = {}
        sum_response['Sum'] = int(a)+int(b)
        sum_response['Minus'] = int(a)-int(b)
        sum_response['Product'] = int(a)*int(b)
        sum_response['Divide'] = int(a)/int(b)
        return sum_response

    def get_simple_dataframe(self):
        raw_data = {'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'], 
                'last_name': ['Miller', 'Jacobson', 'Ali', 'Milner', 'Cooze'], 
                'age': [42, 52, 36, 24, 73], 
                'preTestScore': [4, 24, 31, 2, 3],
                'postTestScore': [25, 94, 57, 62, 70]}
        df = pd.DataFrame(raw_data, columns = ['first_name', 'last_name', 'age', 'preTestScore', 'postTestScore'])
        return df

    def analyse_pdf(self):
        response_dict = {}
        pdf = PdfFileReader(io.BytesIO(self.file))
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()
        response_dict['information'] = information
        response_dict['number_of_pages'] = number_of_pages
        return response_dict


    def image_converter(self):
        data = {}

        img64 = self.args.get('InputImg')
        new_img_format = self.args.get('NewImageFormat')
        new_img_name = self.args.get('NewImageName')

        imgbytes = base64.b64decode(img64)
        img = Image.open(io.BytesIO(imgbytes))

        imgbytes_new = image_to_byte_array(img,new_img_format)

        img64_new = base64.b64encode(imgbytes_new).decode("utf-8")

        data['fil'] = img64_new
        data['fnam'] = new_img_name
        data['height'] = img.height
        data['width'] = img.width
        return data

    def get_test_keyvault_value(self):
        response_dict = {}
        secret_key_name = self.args.get('SecretKeyName')
        key_val = self.env.get_secret_value(secret_key_name)
        response_dict[secret_key_name] = key_val
        return response_dict

    def test_dbquery(self):
        db = self.args.get('DB')
        sqlquery = self.args.get('QRY')
        sqldb = db_utils.SQLDBConn(self.env, db_name=db)
        if not sqlquery:
            sqlquery = f'select * from Test.TestTable'
        df = sqldb.fetch_sql_query(sqlquery)
        return df


def image_to_byte_array(image:Image, img_format):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=img_format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr
