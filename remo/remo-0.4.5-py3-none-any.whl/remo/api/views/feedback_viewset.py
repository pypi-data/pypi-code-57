import os
import re
import sys
import json
import platform

from django.conf import settings
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from remo_app.remo.api.serializers import FeedbackSerializer
from remo_app.remo.models import Feedback
from sendgrid import SendGridAPIClient, HtmlContent, Mail, Attachment, FileContent, FileName, FileType, Disposition

from remo_app import __version__


class FeedbackViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = FeedbackSerializer
    img_rxp = re.compile(r'^data:(image/(\w+));base64,')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        self.send_email(serializer.data)

    def get_attachment(self, data):
        img = data.get('screenshot')
        if not img:
            return

        match = self.img_rxp.match(img)
        if match:
            base64_prefix = match.group()
            file_type, file_extension = match.groups()
            if file_type not in settings.IMAGE_MIME_TYPES:
                print('ERROR: Failed to send feedback attachment, not supported file type:', file_type)
                return None

            img = img[len(base64_prefix):]
            return Attachment(
                file_content=FileContent(img),
                file_name=FileName('Screenshot.{}'.format(file_extension)),
                file_type=FileType(file_type),
                disposition=Disposition('attachment')
            )

    def get_message(self, user, data):
        user_fullname = f'{user.first_name} {user.last_name}'
        text = json.loads(data['text'])
        html_text = f"""
<html>
    <body>
        <h5>Feedback from user</h5>
        <div>
            <p><b>Name:</b> {user_fullname} </p>
            <p><b>Email:</b> {user.email} </p>
            <p><b>Page:</b> {data['page_url']} </p>
            <p><b>Type:</b> {text['type']} </p>
            <p><b>System info:</b>
                    Remo: {__version__},
                    Python: {platform.python_version()}, exe: {sys.executable},
                    OS: {platform.platform()}
                    Use conda: {bool(os.getenv('CONDA_PREFIX'))}
            </p>
            <p><b>Message:</b> {text['message']} </p>
        </div>
    </body>
</html>
"""
        return Mail(
            from_email='noreply@remo.ai',
            to_emails=settings.EMAIL_LIST,
            subject=f'Remo feedback from {user_fullname}',
            html_content=HtmlContent(html_text),
        )

    def send_email(self, data):
        user = self.request.user
        message = self.get_message(user, data)
        attachment = self.get_attachment(data)
        if attachment:
            message.attachment = attachment

        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            sg.send(message)
        except Exception as err:
            print('ERROR: Send feedback failed:', err)


class Feedbacks(GenericAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        key = request.query_params.get('access-key')
        if key != settings.FEEDBACKS_ACCESS_KEY:
            return Response(status=403)

        queryset = Feedback.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
