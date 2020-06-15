import io, os, shutil
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase
from model_bakery import baker
from ai_kit_file_management.settings import api_settings, DEFAULTS

UserModel = get_user_model()
PASSWORD = "testpassword"

MEDIA_ROOT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), settings.MEDIA_ROOT
)

FILE_DATA_1 = b"content of file 1"
FILE_DATA_2 = b"content of file 2"

FILE_PATH = settings.MEDIA_ROOT


def _file(data, format="text/plain", name=None):
    file = io.BytesIO(data)
    file.content_type = format
    file.name = name
    return file


upload_url = reverse("ai_kit_file_management:upload")
file_list_url = reverse("ai_kit_file_management:file-list")


class setting:
    """
    Used in a 'with' statement, to temporarily change the permission classes for file upload to default.
    """

    def __init__(self, setting, value):
        self.setting = setting
        self.value = value

    def __enter__(self):
        self.old = api_settings._settings[self.setting]
        api_settings._settings[self.setting] = self.value

    def __exit__(self, exc_type, exc_val, exc_tb):
        api_settings._settings[self.setting] = self.old


class FileAPITestCase(APITestCase):
    def setUp(self) -> None:
        # upload test files
        r1 = self.client.post(
            upload_url,
            {"file": _file(FILE_DATA_1, name="testfile_1.txt")},
            format="multipart",
        )
        self.file_1_name_on_disk = r1.data["file"]
        r2 = self.client.post(
            upload_url,
            {"file": _file(FILE_DATA_1, name="testfile_2.txt")},
            format="multipart",
        )
        self.file_2_name_on_disk = r2.data["file"]

    def tearDown(self) -> None:
        api_settings.FILE_MODEL.objects.all().delete()
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)

    def test_list(self):
        response = self.client.get(file_list_url)
        file_1_response = response.data[0]
        file_2_response = response.data[1]
        self.assertTrue(self.file_1_name_on_disk in file_1_response["file"])
        self.assertTrue(self.file_2_name_on_disk in file_2_response["file"])

    def test_retrieve(self):
        response = self.client.get(
            reverse("ai_kit_file_management:file-detail", args=[1])
        )
        self.assertTrue(self.file_1_name_on_disk in response.data["file"])

    @patch("ai_kit_file_management.models.File.objects.visible_for")
    def test_manager_used_in_list(self, visible_for):
        self.client.get(file_list_url)
        visible_for.assert_called()


class FileDownloadAPITestCase(APITestCase):
    def setUp(self) -> None:
        # upload test file
        response = self.client.post(
            upload_url,
            {"file": _file(FILE_DATA_1, name="testfile.txt")},
            format="multipart",
        )
        self.file_name = response.data["file"]
        self.download_url = reverse(
            "ai_kit_file_management:download", args=[*self.file_name.split(os.sep)]
        )

    def test_download_dev(self):
        response = self.client.get(self.download_url)
        self.assertTrue(response.filename, "testfile.txt")
        self.assertEqual(*response.streaming_content, FILE_DATA_1)

    def test_download_nginx(self):
        with setting("FILESERVER_BACKEND", "nginx"):
            response = self.client.get(self.download_url)
            self.assertTrue(response.filename, "testfile.txt")
            self.assertEqual(
                response._headers["x-accel-redirect"][1],
                os.path.join(FILE_PATH, self.file_name),
            )

    def test_download_xsendfile(self):
        with setting("FILESERVER_BACKEND", "x-sendfile"):
            response = self.client.get(self.download_url)
            self.assertTrue(response.filename, "testfile.txt")
            self.assertEqual(
                response._headers["x-sendfile"][1],
                os.path.join(FILE_PATH, self.file_name),
            )


class FileUploadAPITestCase(APITestCase):
    def setUp(self) -> None:
        # assure media folder is empty on start
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)

    def tearDown(self) -> None:
        # clean up again
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)

    def test_upload(self):
        response1 = self.client.post(
            upload_url, {"file": _file(FILE_DATA_1)}, format="multipart",
        )
        response2 = self.client.post(
            upload_url, {"file": _file(FILE_DATA_2)}, format="multipart",
        )
        # now there should be two file objects
        self.assertEqual(api_settings.FILE_MODEL.objects.count(), 2)

        # two media files with the correct content
        with open(os.path.join(MEDIA_ROOT, response1.data["file"]), "rb") as f:
            self.assertEqual(f.read(), FILE_DATA_1)
        with open(os.path.join(MEDIA_ROOT, response2.data["file"]), "rb") as f:
            self.assertEqual(f.read(), FILE_DATA_2)

        # ...and a created response
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

    def test_upload_filename_too_long_fail(self):
        response = self.client.post(
            upload_url,
            {"file": _file(FILE_DATA_1, name="foo" * 50)},
            format="multipart",
        )
        self.assertEqual(api_settings.FILE_MODEL.objects.count(), 0)
        self.assertEqual(str(response.data["file"][0]), "filename_too_long")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_forbidden_mime_type_fail(self):
        response = self.client.post(
            upload_url,
            {"file": _file(FILE_DATA_1, format="text/html")},
            format="multipart",
        )
        self.assertEqual(api_settings.FILE_MODEL.objects.count(), 0)
        self.assertEqual(str(response.data["file"][0]), "mime_type_not_allowed")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_file_too_large_fail(self):
        response = self.client.post(
            upload_url, {"file": _file(FILE_DATA_1 * 100)}, format="multipart",
        )
        self.assertEqual(api_settings.FILE_MODEL.objects.count(), 0)
        self.assertEqual(str(response.data["file"][0]), "filesize_too_large")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logged_in(self):
        with setting("PERMISSION_CLASSES", DEFAULTS["PERMISSION_CLASSES"]):
            user = baker.make(UserModel)
            user.set_password(PASSWORD)
            user.save()
            self.client.login(username=user.username, password=PASSWORD)
            response = self.client.post(
                upload_url, {"file": _file(FILE_DATA_1)}, format="multipart",
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(api_settings.FILE_MODEL.objects.count(), 1)
            self.assertEqual(api_settings.FILE_MODEL.objects.first().creator, user)

    def test_not_logged_in_fail(self):
        with setting("PERMISSION_CLASSES", DEFAULTS["PERMISSION_CLASSES"]):
            response = self.client.post(
                upload_url, {"file": _file(FILE_DATA_1)}, format="multipart",
            )
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(api_settings.FILE_MODEL.objects.count(), 0)
