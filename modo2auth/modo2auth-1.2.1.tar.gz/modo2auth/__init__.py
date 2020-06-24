import hmac
import hashlib
import time
import base64


def replaceBase64Chars(string):
    return string.replace("=", "").replace("+", "-").replace("/", "_")


def base64encodestring(message):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = replaceBase64Chars(base64_bytes.decode('ascii'))
    return base64_message


def createSignature(key, header, payload):
    message = "{}.{}".format(header, payload)
    message_bytes = message.encode('ascii')
    key_bytes = key.encode('ascii')
    signature = base64.b64encode(hmac.new(
        key_bytes, message_bytes, digestmod=hashlib.sha256).digest(), '-_'.encode('ascii'))
    signature = signature.decode('ascii')
    signature = replaceBase64Chars(signature)
    return signature.rstrip("=")


class Sign(object):
    def __init__(self, api_id, secret, api_uri, header='Authorization'):
        self.secret = secret
        self.api_id = api_id
        self.api_uri = api_uri
        self.header = header
        self.debug = False
        self.header_plain = '{"alg":"HS256","typ":"JWT"}'

    def __call__(self, request):
        # Get the body of the request so we can hash it
        body = request.body
        if not isinstance(body, bytes):   # Python 3
            if isinstance(body, str):
                body = body.encode('latin1')  # standard encoding for HTTP
            else:
                # for http get, we will have no body, so just make it an empty string
                body = "".encode('latin1')

        header = base64encodestring(self.header_plain)

        # Hash our body payload
        body_hash = hashlib.sha256(body).hexdigest()
        # get the current time
        iat_time = int(time.time())

        # put it all together and encode it (base64)
        payload_plain = '{"iat":'+str(iat_time)+',"api_identifier":"'+self.api_id + \
            '","api_uri":"'+self.api_uri+'","body_hash":"'+body_hash+'"}'
        payload = base64encodestring(payload_plain)

        # create the signature
        signature = createSignature(self.secret, header, payload)

        # create our auth token
        modo_auth_token = 'MODO2 {}.{}.{}'.format(header, payload, signature)

        if (self.debug == True):
            print('Body Hash: ' + body_hash)
            print('Signature: ' + signature)
            print('Token: ' + modo_auth_token)

        request.headers[self.header] = modo_auth_token
        return request
