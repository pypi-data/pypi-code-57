import os

from django.conf import settings
from remo_app.remo import utils
from remo_app.remo.services.uploads import UploadSessionStatus


class FileStore:
    def __init__(self, session: UploadSessionStatus):
        self.session = session

    def report_error(self, filename: str, error: str):
        self.session.append_file_error(filename, error)

    def report_file_uploaded(self, file, file_type):
        arg_name = {
            'image': 'image_file_size',
            'annotation': 'annotation_file_size',
            'archive': 'archive_file_size'
        }
        kwargs = {
            arg_name[file_type]: file.size
        }
        self.session.uploaded(**kwargs)

    def save_files(self, files):
        utils.make_dir(self.session.dir_path())
        for file in files:
            self.save_file(file, self.session.dir_path())

    def save_file(self, file, dir_path):
        file_type = self.guess_file_type(file)
        if not self.is_valid_file(file, file_type):
            return

        file_path = os.path.join(dir_path, file.name)
        with open(file_path, "wb") as output:
            for chunk in file.chunks():
                output.write(chunk)

        self.report_file_uploaded(file, file_type)

    def is_valid_file(self, file, file_type):
        return self.is_valid_file_size(file) and self.is_valid_file_type(file, file_type)

    def is_valid_file_size(self, file):
        if file.size > settings.MAX_FILE_SIZE:
            self.report_error(file.name,
                           f'File size {utils.human_size(file.size)} exceed max file size for upload')
            return False
        return True

    def guess_file_type(self, file):
        _, extension = os.path.splitext(file.name)
        extension = extension.lower()
        mime = utils.guess_mime(file)

        if mime in settings.IMAGE_MIME_TYPES and extension in settings.IMAGE_FILE_EXTENSIONS:
            return 'image'
        if mime in settings.ANNOTATION_MIME_TYPES and extension in settings.ANNOTATION_FILE_EXTENSIONS:
            return 'annotation'
        if mime in settings.ARCHIVE_MIME_TYPES and extension in settings.ARCHIVE_FILE_EXTENSIONS:
            return 'archive'
        return None

    def is_valid_file_type(self, file, file_type):
        if not file_type:
            self.report_error(file.name, f'File content type not supported')
            return False
        return True
