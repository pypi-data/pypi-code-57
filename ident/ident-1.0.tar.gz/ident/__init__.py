import os
import base64
import hashlib
import tempfile
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def sign(challenge_message):
    return os.popen(
        'echo "%s" | openssl rsautl -sign -inkey ~/.ssh/id_rsa | base64 -w 0 && echo -n ":" && cat ~/.ssh/id_rsa.pub | base64 -w 0' % (challenge_message,)
    ).read().rstrip()

def verify(challenge_response):
    try:
        sig, pub = challenge_response.split(':')

        pubkey = base64.b64decode(pub)
        key = serialization.load_ssh_public_key(pubkey, default_backend())
        pemkey = key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        rawkey = key.public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH
        )
        b64pubkey = str(rawkey, 'utf-8').split(' ')[-1]
        sha256 = hashlib.sha256()
        sha256.update(base64.b64decode(b64pubkey))
        b64fingerprint = base64.b64encode(sha256.digest())

        keyprint = {'fingerprint': b64fingerprint, 'pem': pemkey }


        f = tempfile.NamedTemporaryFile()
        challenge_recovered = None
        try:
            f.write(pemkey)
            f.seek(0)
            challenge_recovered = os.popen(
                'echo "%s" | base64 -d -w 0 | openssl rsautl -verify -inkey %s -pubin' % (sig, f.name)
            ).read().rstrip()
        finally:
            f.close()

        if challenge_recovered is not None:
            return {
                'success': True,
                'status': 'Verification successful.',
                'recovered_challenge_message': challenge_recovered,
                'key': keyprint,
            }
        else:
            return {
                'success': False,
                'status': 'Verification failed.',
                'recovered_challenge_message': challenge_recovered or 'UNKNOWN',
                'key': keyprint,
            }
    except Exception as e:
        return {
            'success': False,
            'status': 'Verification failed with error.',
            'error': repr(e),
            'recovered_challenge_message': 'UNKNOWN',
        }

