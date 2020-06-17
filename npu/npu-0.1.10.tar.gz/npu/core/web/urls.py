import os

BASE_URL = "https://api.neuro-ai.co.uk/"

if "BASE_URL" in os.environ:
    BASE_URL = os.environ["BASE_URL"]

COMPILE_URL = BASE_URL + "UploadModel"
RETRIEVE_MODEL_URL = BASE_URL + "RetrieveModel"
UPLOAD_DATA_URL = BASE_URL + "UploadData"
PREDICT_URL = BASE_URL + "Predict"
TRAIN_URL = BASE_URL + "Train"
HASH_URL = BASE_URL + "Hash"
TOKEN_URL = BASE_URL + "Token"
EXPORT_URL = BASE_URL + "Export"
TASK_STATUS_URL = BASE_URL + "status/"
