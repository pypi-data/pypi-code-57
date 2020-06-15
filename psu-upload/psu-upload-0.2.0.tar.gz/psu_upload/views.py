from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from psu_base.classes.Log import Log
from psu_base.services import utility_service, message_service, auth_service
from psu_base.decorators import require_authority, require_authentication
from psu_base.classes.DynamicRole import DynamicRole
from psu_upload.models.uploaded_file import UploadedFile

from psu_upload.services import upload_service
import os


log = Log()

# ToDo: Error Handling/Messages


@require_authentication()
def index(request):
    """
    Menu of ...
    """
    log.trace()

    uploaded_files = UploadedFile.objects.all()

    return render(
        request, 'upload_sample.html',
        {'uploaded_files': uploaded_files}
    )


@require_authentication()
def upload_file(request):
    """
    Upload a file and store it in S3
    """
    log.trace()

    if request.method == 'POST':
        ufs = upload_service.upload_files(request, 'uploaded_file', 'test-', 'Tests')

    return redirect('upload:sample')


