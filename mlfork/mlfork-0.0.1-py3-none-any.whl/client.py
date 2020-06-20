import requests
import os
import zipfile
import random
import string
import shutil
from mlfork.auth import AuthRequests

API_DOMAIN = 'api.mlfork.com'

class Client:

    def __init__(self, api_domain=API_DOMAIN,
                 api_key_id=None, api_secret=None):
        self.domain = api_domain
        self.key_id = api_key_id
        self.secret = api_secret
        self.auth = AuthRequests(self.domain, self.key_id, self.secret)


    def get_model(self, model_id):
        return True


    def push_model(self, model, model_id=None):
        tmpname = ''.join(random.choices(string.ascii_letters, k=10))

        if os.path.isfile(model):
            zipf = zipfile.ZipFile(tmpname+'.zip', 'w', zipfile.ZIP_DEFLATED)
            zipf.write(model)
            zipf.close()
        elif os.path.isdir(model):
            zipf = zipfile.ZipFile(tmpname+'.zip', 'w', zipfile.ZIP_DEFLATED)
            for root, dirs, files in os.walk(model):
                for file in files:
                    zipf.write(os.path.join(root, file))
            zipf.close()
        else:
            raise Exception("Path does not exist: "+model)

        path = "/model"
        if model_id is not None:
            path += "/"+model_id
        model_opts = {'source':'TensorFlow', 'public':True}
        r = self.auth.post(path, data=model_opts)
        if r.status_code not in [200, 201]:
            os.remove(tmpname+'.zip')
            raise Exception("Server returned %d"%r.status_code)
        rsp = r.json()
        putUrl = rsp['url']
        if model_id is None:
            model_id = rsp['name']
        with open(tmpname+'.zip', 'rb') as zf:
            r = requests.put(putUrl, data=zf.read())
            print(r.text)
        os.remove(tmpname+'.zip')
        return model_id
