from psu_upload.models.uploaded_file import UploadedFile
from psu_base.services import utility_service, email_service, date_service, auth_service, message_service
from psu_base.classes.Log import Log

log = Log()

# Base queries that can have further filtering applied to them by the calling app


def get_all_files():
    app_code = utility_service.get_app_code()
    return UploadedFile.objects.filter(app_code=app_code).exclude(status='D')


def get_user_files(username=None):
    if not username:
        username = auth_service.get_user().username
    app_code = utility_service.get_app_code()
    return UploadedFile.objects.filter(app_code=app_code, owner=username).exclude(status='D')
