# coding: utf-8

"""
    Flywheel

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 12.1.0-rc.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import mimetypes, os.path

class FileSpec:
    def __init__(self, name, contents=None, content_type=None):
        self.name = name
        self.contents = contents
        self.content_type = content_type

    def to_file_tuple(self):
        if self.contents is None:
            if not self.name:
                raise RuntimeError('FileSpec is invalid, file or content is required!')
            # TODO: Switch to library that supports file streaming
            f = open(self.name, 'rb')
            filename = os.path.basename(f.name)
            filedata = f
        else:
            filename = self.name
            filedata = self.contents

        if self.content_type is None:
            mimetype = (mimetypes.guess_type(filename)[0] or 'application/octet-stream')
        else:
            mimetype = self.content_type

        return tuple([filename, filedata, mimetype])

