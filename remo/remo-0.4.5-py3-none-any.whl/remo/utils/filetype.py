import os

import filetype

extension_to_mime = {
    '.json': 'application/json',
    '.xml': 'text/xml',
    '.csv': 'text/csv'
}


def file_ext(name):
    return os.path.splitext(name)[1]


def guess_mime(file):
    mime = filetype.guess_mime(file)
    if mime:
        return mime

    if type(file) is str:
        name = file
    else:
        name = file.name  # when file uploads
    extension = file_ext(name)
    return extension_to_mime.get(extension)
