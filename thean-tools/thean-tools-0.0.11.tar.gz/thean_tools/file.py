import base64


def get_file_binary(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def get_file_base64(filePath):
    b64 = base64.b64encode(get_file_binary(filePath))
    return str(b64, 'utf-8')
