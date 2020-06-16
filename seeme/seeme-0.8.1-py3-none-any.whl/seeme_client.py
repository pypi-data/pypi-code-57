import os
import json
import requests
import http
from requests_toolbelt.multipart.encoder import MultipartEncoder

REGISTER_ENDPOINT = 'register'
LOGIN_ENDPOINT = 'login'
MODELS_ENDPOINT = 'models'
TRAINING_REQUESTS_ENDPOINT = 'trainingrequests'
INFERENCE_ENDPOINT = 'inferences'
DETECTION_ENDPOINT = 'detections'
DATASETS_ENDPOINT = 'datasets'
NLP_CLASSIFICATION_ENDPOINT = 'nlpclassification'
APPLICATIONS_ENDPOINT = 'applications'

ID = "ID"

class Client():
  def __init__(self, username:str=None, apikey:str=None, backend:str="https://api.seeme.ai/api/v1/"):
    self.backend = backend
    self.headers = {}
    self.update_auth_header(username, apikey)
    self.endpoints = {
      REGISTER_ENDPOINT: self.crud_endpoint(REGISTER_ENDPOINT),
      LOGIN_ENDPOINT: self.crud_endpoint(LOGIN_ENDPOINT),
      MODELS_ENDPOINT: self.crud_endpoint(MODELS_ENDPOINT),
      TRAINING_REQUESTS_ENDPOINT: self.crud_endpoint(TRAINING_REQUESTS_ENDPOINT),
      INFERENCE_ENDPOINT: self.crud_endpoint(INFERENCE_ENDPOINT),
      DETECTION_ENDPOINT: self.crud_endpoint(DETECTION_ENDPOINT),
      NLP_CLASSIFICATION_ENDPOINT: self.crud_endpoint(NLP_CLASSIFICATION_ENDPOINT),
      DATASETS_ENDPOINT: self.crud_endpoint(DATASETS_ENDPOINT),
      APPLICATIONS_ENDPOINT: self.crud_endpoint(APPLICATIONS_ENDPOINT)
    }
    self.applications = []

  # -- Login / Registration --

  def register(self, username:str, email:str, password:str, firstname:str, name:str):
    register_api = self.endpoints[REGISTER_ENDPOINT]
    register_data = {
      'username': username,
      'email': email,
      'password': password,
      'firstname': firstname,
      'name': name,
    }

    r = requests.post(register_api, data=json.dumps(register_data), headers=self.headers)

    assert r.status_code == http.HTTPStatus.BAD_REQUEST
    
    registered_user = r.json()

    if "message" in registered_user:
      raise ValueError(registered_user["message"])
    
    return registered_user

  def login(self, username:str, password:str):
    login_api = self.endpoints[LOGIN_ENDPOINT]
    login_data = {
      'username': username,
      'password': password
    }
    
    logged_in = self.api_post(login_api, login_data)

    self.update_auth_header(logged_in["username"], logged_in["apikey"])

    applications_api = self.endpoints[APPLICATIONS_ENDPOINT]
    self.applications =  self.api_get(applications_api)
      
  def logout(self):
    self.update_auth_header("", "")
    
  # -- CRUD models --

  def get_models(self):
    self.requires_login()

    model_api = self.endpoints[MODELS_ENDPOINT]

    return self.api_get(model_api)

  def create_model(self, name:str, classes:str, description:str=""):
    self.requires_login()

    model_api = self.endpoints[MODELS_ENDPOINT]
    model_data = {
      'name': name,
      'classes': classes,
      'description': description
    }

    return self.api_post(model_api, model_data)

  def create_full_model(self, model):
    self.requires_login()

    model_api = self.endpoints[MODELS_ENDPOINT]

    return self.api_post(model_api, model)
  
  def get_application_id(self, base_framework="pytorch", framework="fastai", base_framework_version="1.5.0", framework_version="1.0.61", application="image_classification"):
    for f in self.applications:
      if f["base_framework"] == base_framework \
        and f["framework"] == framework \
        and f["base_framework_version"] == base_framework_version \
        and f["framework_version"] == framework_version \
        and f["application"] == application:
          return f["ID"]
      
    raise NotImplementedError()

  def get_model(self, model_id:str):
    self.requires_login()

    model_api = self.endpoints[MODELS_ENDPOINT] + "/" + model_id

    return self.api_get(model_api)

  def update_model(self, model):
    self.requires_login()

    assert model
    assert model[ID]
    model_api = self.endpoints[MODELS_ENDPOINT] + "/" + model[ID]
    return self.api_put(model_api, model)

  def delete_model(self, id:str):
    self.requires_login()
    delete_api = self.endpoints[MODELS_ENDPOINT] + "/" + id

    return self.api_delete(delete_api)

  def upload_model(self, model_id:str, folder:str="data", filename:str="export.pkl"):
    return self.upload(model_id, folder, filename, 'application/octet-stream')
  
  def upload_logo(self, model_id:str, folder:str="data", filename:str="logo.jpg"):
    if filename.endswith("jpg"):
      content_type="image/jpg"
    elif filename.endswith("jpeg"):
      content_type="image/jpeg"
    elif filename.endswith("png"):
      content_type="image/png"

    return self.upload(model_id, folder, filename,  content_type)
  
  def get_logo(self, model):
    logo_endpoint = self.endpoints[MODELS_ENDPOINT] + "/" + model["ID"] + "/download/logo"
    return self.api_download(logo_endpoint, model["logo"])

  def get_mlmodel(self, model):
    mlmodel_endpoint = self.endpoints[MODELS_ENDPOINT] + "/" + model["ID"] + "/download/mlmodel"
    return self.api_download(mlmodel_endpoint, model["ID"]+".mlmodel")

  def upload(self, model_id:str, folder:str, filename:str, content_type:str):
    self.requires_login()

    model_upload_api = self.endpoints[MODELS_ENDPOINT] + "/" + model_id  + "/upload"

    data = MultipartEncoder(
                fields={
                    'file': (filename, open(folder + "/" + filename, 'rb'), content_type)}
                       )

    content_headers = self.headers

    content_headers['Content-Type'] = data.content_type

    return self.api_upload(model_upload_api, data=data, headers=content_headers)

  def upload_detection_model(self, model_id:str, folder:str="data", filename:str="export.pkl"):
    self.requires_login()

    model_upload_api = self.endpoints[MODELS_ENDPOINT] + "/" + model_id  + "/upload"

    data = MultipartEncoder(
                fields={
                    'file': ('filename', open(folder + "/" + filename, 'rb'), 'application/octet-stream')}
                       )

    content_headers = self.headers

    content_headers['Content-Type'] = data.content_type

    return self.api_upload(model_upload_api, data=data, headers=content_headers)

  # -- CRUD requests --

  def get_training_requests(self):
    self.requires_login()

    training_requests_api = self.endpoints[TRAINING_REQUESTS_ENDPOINT]

    return self.api_get(training_requests_api)
  
  def create_training_request(self, name:str, classes:str, description:str=""):
    self.requires_login()

    req_api = self.endpoints[TRAINING_REQUESTS_ENDPOINT]
    req_data = {
      'name': name,
      'classes': classes,
      'description': description
    }

    return self.api_post(req_api, req_data)

  def update_training_request(self, training_request):
    self.requires_login()

    assert training_request
    assert training_request[ID]
    training_request_api = self.endpoints[TRAINING_REQUESTS_ENDPOINT] + "/" + training_request[ID]
    return self.api_put(training_request_api, training_request)

  def delete_training_request(self, id:str):
    self.requires_login()
    delete_api = self.endpoints[TRAINING_REQUESTS_ENDPOINT] + "/" + id

    return self.api_delete(delete_api)

  # -- CRUD Inference --

  def inference(self, model_id:str, file:str):
    self.requires_login()

    inference_api = self.endpoints[INFERENCE_ENDPOINT] + "/" + model_id

    data = MultipartEncoder(
                fields={
                    'file': ('filename', open(file, 'rb'), 'application/octet-stream')}
                       )

    content_headers = self.headers

    content_headers['Content-Type'] = data.content_type

    return self.api_upload(inference_api, data=data, headers=content_headers)
  
  def update_inference(self, inference):
    self.requires_login()

    inference_api = self.endpoints[INFERENCE_ENDPOINT] + "/" + inference["ID"]

    return self.api_put(inference_api, inference)

  # -- CRUD Detection --

  def detect(self, model_id:str, file:str):
    self.requires_login()

    detection_api = self.endpoints[DETECTION_ENDPOINT] + "/" + model_id

    data = MultipartEncoder(
                fields={
                    'file': (os.path.basename(file), open(file, 'rb'), 'application/octet-stream')}
                       )

    content_headers = self.headers

    content_headers['Content-Type'] = data.content_type

    return self.api_upload(detection_api, data=data, headers=content_headers)

  # -- CRUD Nlp Classification

  def nlpclassification(self, model_id:str, input_text:str):
    self.requires_login()

    nlp_api = self.endpoints[NLP_CLASSIFICATION_ENDPOINT] + "/" + model_id

    req_data = {
      'input_text': input_text
    }

    return self.api_post(nlp_api, req_data)

  # -- CRUD applicationS --
  def get_applications(self):
    self.requires_login()

    application_api = self.endpoints[APPLICATIONS_ENDPOINT]

    return self.api_get(application_api)
  
  def create_application(self, application):
    self.requires_login()

    application_api = self.endpoints[APPLICATIONS_ENDPOINT]

    return self.api_post(application_api, application)

  # -- CRUD DATASETS --

  def get_datasets(self):
    self.requires_login()

    dataset_api = self.endpoints[DATASETS_ENDPOINT]

    return self.api_get(dataset_api)

  def create_dataset(self, name:str, description:str=""):
    self.requires_login()

    dataset_api = self.endpoints[DATASETS_ENDPOINT]
    dataset_data = {
      'name': name,
      'description': description
    }

    return self.api_post(dataset_api, dataset_data)

  def get_dataset(self, dataset_id:str):
    self.requires_login()

    dataset_api = self.endpoints[DATASETS_ENDPOINT] + "/" + dataset_id

    return self.api_get(dataset_api)

  def update_dataset(self, dataset):
    self.requires_login()

    assert dataset
    assert dataset[ID]
    dataset_api = self.endpoints[DATASETS_ENDPOINT] + "/" + dataset[ID]
    return self.api_put(dataset_api, dataset)

  def delete_dataset(self, id:str):
    self.requires_login()
    dataset_api = self.endpoints[DATASETS_ENDPOINT] + "/" + id

    return self.api_delete(dataset_api)


  # Convenience methods

  def get_apikey(self):
    return self.apikey

  # Helpers

  def requires_login(self):
    if not self.is_logged_in():
      raise Exception("You need to be logged in for this.")

  def update_auth_header(self, username:str=None, apikey:str=None):
    if username == None or apikey == None:
      return

    self.apikey = apikey
    
    self.headers = {
      "Authorization": f"{username}:{apikey}"
    }
  
  def is_logged_in(self):
    if "Authorization" in self.headers:
      return True

    return False

  def crud_endpoint(self, endpoint:str):
    return f"{self.backend}{endpoint}"

  ## CRUD API methods

  def api_get(self, api:str):
    r = requests.get(api, headers=self.headers)

    return r.json()

  def api_post(self, api:str, data):
    data = json.dumps(data)

    r = requests.post(api, data=data, headers=self.headers)
    
    return r.json()
  
  def api_upload(self, api:str, data, headers):
    r = requests.post(api, data=data, headers=headers)
    
    return r.json()
  
  def api_put(self, api:str, data):
    data = json.dumps(data)

    r = requests.put(api, data=data, headers=self.headers)

    return r.json()
  
  def api_delete(self, api:str):
    r = requests.delete(api, headers=self.headers)

    return r.json()

  def api_download(self, api:str, filename:str):
    r = requests.get(api, allow_redirects=True, headers=self.headers)

    open(filename, "wb").write(r.content)