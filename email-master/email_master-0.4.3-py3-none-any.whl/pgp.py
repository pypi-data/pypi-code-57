from email_master.compat import base64_decode_to_bytes, base64_encode_bytes
from pgpy.constants import SymmetricKeyAlgorithm, HashAlgorithm
from pgpy.errors import PGPError
from email_master.parser import EmailMasterParser
from email.encoders import encode_7or8bit
from pgpy import PGPKey, PGPMessage, PGPSignature
import email
from email.mime.application import MIMEApplication
from email.utils import collapse_rfc2231_value
from email import message_from_string
import email_master.rfc3156 as rfc3156
from datetime import datetime
import copy
import tempfile
import re
import six
import random

if six.PY3:
    from io import StringIO
else:
    from cStringIO import StringIO


class PGPConfig(object):
    SIGNED = "Signed"
    SIGNED_AND_ENCRYPT = "Signed & Encrypted"
    ENCRYPTED = "Encrypted"
    NONE = "Cleartext"
    SIGNED_AND_VERIFIED = "Signed & Verified"
    SIGNED_AND_ENC_VERIFIED = "Signed & Verified & Encrypted"

    def __undefined_attr(self, attr_name):
        def attr(self):
            raise ValueError("Property '{}' not defined and cannot be accessed".format(attr_name))

        return property(attr)

    def __init__(self, pgp_action=None, pgp_private_b64="", pgp_public_b64="", pgp_password=""):
        self.pgp_action = pgp_action
        self.key_pw = pgp_password

        if pgp_action in (PGPConfig.SIGNED, PGPConfig.SIGNED_AND_ENCRYPT, PGPConfig.ENCRYPTED):
            if not pgp_private_b64 or not pgp_public_b64:
                raise ValueError("Must provice PGP private and public keys to sign/encrypt!")
        elif pgp_action == PGPConfig.NONE:
            pass
        elif pgp_action is not None:
            raise ValueError(
                "Invalid pgp_action '{}'! Must be None, PGPConfig.SIGNED PGPConfig.SIGNED_AND_ENCRYPT, or PGPConfig.ENCRYPT!".format(
                    pgp_action))

        self.priv_key, self.priv_keystore = self._key_from_b64(pgp_private_b64)
        self.pub_key, self.pub_keystore = self._key_from_b64(pgp_public_b64)

        if self.priv_key:
            try:
                with self.priv_key.unlock(self.key_pw):
                    pass
            except Exception as e:
                raise ValueError("Invalid privkey or password, key unlock failed! Error: '{}'".format(str(e)))
        else:
            setattr(PGPConfig, "priv_key", self.__undefined_attr("Private Key"))

        if not self.pub_key:
            setattr(PGPConfig, "pub_key", self.__undefined_attr("Public Key"))

    def _generate_bound(self):
        valid_chars = []
        valid_chars.extend(range(ord("A"), ord("Z")))  # A-Z
        valid_chars.extend(range(ord("a"), ord("z")))  # a-z
        valid_chars.extend(range(ord("0"), ord("9")))  # 0-9
        valid_chars = [chr(rr) for rr in valid_chars]  # Convert to chars
        if six.PY3:
            return "".join(random.choices(valid_chars, k=32))  # Sample 32 at random (py3 only)
        else:
            return "".join([random.choice(valid_chars) for _ in range(32)])  # py2 32 samples

    def _key_from_b64(self, data):
        if not data:
            return None, None

        f = tempfile.NamedTemporaryFile(suffix=b'')
        dd = base64_decode_to_bytes(data)
        f.write(dd)
        f.seek(0)
        key, keystore = PGPKey.from_file(f.name)
        f.close()
        return key, keystore

    def _find_pgp_sig(self, msg_obj):
        attachments = len(msg_obj.get_payload())
        for idx in range(attachments):
            try:
                pgp_blob = msg_obj.get_payload(idx).get_payload()
                pgp_blob = PGPSignature.from_blob(pgp_blob)
                msg_str = msg_obj.get_payload(0).as_string()  # Hard coded 0 for base payload to verify against
                msg_str_replaced = msg_str.replace("\n", "\r\n")  # Need to replace newlines with \r\n "sometimes"
                pgp_verify1 = self.pub_key.verify(msg_str, pgp_blob)  # Need to test both original and replaced string
                pgp_verify2 = self.pub_key.verify(msg_str_replaced, pgp_blob)  # Based on format
                verified = list(pgp_verify1.good_signatures)
                verified.extend(list(pgp_verify2.good_signatures))  # Merge verified (only one can be good)
                return verified
            except PGPError as e:
                continue  # Invalid signature
            except TypeError as e:
                continue  # Invalid body type
        return []  # Couldn't find an attachment with a valid signature

    def unlock(self, msg_as_string, parser_kwargs):
        mime_msg = CustomMIMEWrapper(msg_as_string)
        is_encrypted = mime_msg.is_encrypted()
        is_verified = False
        fingerprints = []
        message_type = PGPConfig.ENCRYPTED if is_encrypted else PGPConfig.NONE

        if is_encrypted:
            with self.priv_key.unlock(self.key_pw) as unlocked_key:
                decrypted = mime_msg.decrypt(unlocked_key)
                if not decrypted:
                    raise ValueError("No decrypted message returned from mime_msg.decrypt!")
                mime_msg = decrypted

        is_signed = mime_msg.is_signed()  # Wait until message is possibly decrypted

        if is_signed:
            message_type = PGPConfig.SIGNED
            if is_encrypted:
                message_type = PGPConfig.SIGNED_AND_ENCRYPT

            sigs = self._find_pgp_sig(mime_msg.msg)
            is_verified = len(sigs) > 0
            if is_verified:
                if is_encrypted:
                    message_type = PGPConfig.SIGNED_AND_ENC_VERIFIED
                else:
                    message_type = PGPConfig.SIGNED_AND_VERIFIED

            fingerprints = [str(sig.by.fingerprint) for sig in sigs]

        if len(mime_msg.msg._payload) == 2 and is_signed:
            mime_msg.msg._payload[0]._headers.extend(mime_msg.msg._headers)  # Copy outer headers into the inner message object
            mime_msg.msg._payload[0].preamble = mime_msg.msg.preamble  # Copy the preamble

            orig_msg = EmailMasterParser(base64_encode_bytes(str(mime_msg.msg.get_payload(0)).encode()), **parser_kwargs).parse()  # Orig message
            sig_msg = EmailMasterParser(base64_encode_bytes(str(mime_msg.msg.get_payload(1)).encode()), **parser_kwargs).parse()  # Signature
            merge_keys = ["attachments_sha1", "attachments_md5", "attachments_sha256", "attach_info", "attachments"]
            for k in merge_keys:
                if isinstance(orig_msg[k], list):
                    orig_msg[k].extend(sig_msg[k])
                else:
                    ks = orig_msg[k].split(",")
                    if ks == ['']:
                        ks = []
                    ks.append(sig_msg[k])
                    orig_msg[k] = ",".join(ks)

            email_data = orig_msg
        else:
            email_data = EmailMasterParser(base64_encode_bytes(str(mime_msg.msg).encode()), **parser_kwargs).parse()

        tw = 2

        email_data.update({
            "message_type": message_type,
            "is_verified": is_verified,
            "is_signed": is_signed,
            "is_encrypted": is_encrypted,
            "fingerprints": fingerprints
        })
        return email_data

    def _format_signed_payload(self, mime_message, payload, signed_payload, dt):
        bound = self._generate_bound()
        new_headers = list(filter(lambda x: x[0] != "Content-Type", email.message_from_string(payload)._headers))

        signed_payload = signed_payload.as_string().replace("\n", "\r\n")

        header_data = "\r\n".join(["{}: {}".format(b[0], b[1]) for b in new_headers])
        newmsg = header_data + \
                 "\r\nContent-Type: multipart/signed; micalg=pgp-sha256; " + \
                 "protocol=\"application/pgp-signature\";" + \
                 "boundary=\"{bound}\"\r\n--{bound}\r\n".format(bound=bound) + \
                 payload + \
                 "\r\n--{bound}\r\n".format(bound=bound) + \
                 signed_payload + \
                 "--{}--".format(bound)
        return newmsg

    def lock(self, mime_message):
        if self.pgp_action == PGPConfig.NONE:
            return str(mime_message.msg)
        elif self.pgp_action == PGPConfig.SIGNED:
            with self.priv_key.unlock(self.key_pw) as k:
                dt = datetime.utcnow()
                payload, signed_payload = mime_message.sign(k, hash=HashAlgorithm.SHA256)  # created=dt)
                return self._format_signed_payload(mime_message, payload, signed_payload, dt)
        elif self.pgp_action == PGPConfig.SIGNED_AND_ENCRYPT:
            with self.priv_key.unlock(self.key_pw) as k:
                mime = mime_message.sign_encrypt(k, list(self.pub_keystore.values()))
                return str(mime.msg)
        elif self.pgp_action == PGPConfig.ENCRYPTED:
            with self.priv_key.unlock(self.key_pw) as k:
                mime = mime_message.encrypt(k, list(self.pub_keystore.values()))
                return str(mime.msg)
        else:
            raise ValueError("Unknown PGPConfig option: {}".format(self.pgp_action))


class CustomMIMEWrapper(object):
    """PGP/MIME (RFC1847 + RFC3156) compliant wrapper."""
    _signature_subtype = 'pgp-signature'
    _encryption_subtype = 'pgp-encrypted'
    _keys_subtype = 'pgp-keys'
    _signed_type = 'application/' + _signature_subtype
    _encrypted_type = 'application/' + _encryption_subtype
    _keys_type = 'application/' + _keys_subtype
    _signed_multipart = 'multipart/signed'
    _encrypted_multipart = 'multipart/encrypted'
    _signature_preamble = \
        'This is an OpenPGP/MIME signed message (RFC 4880 and 3156)'
    _encryption_preamble = \
        'This is an OpenPGP/MIME encrypted message (RFC 4880 and 3156)'

    def __init__(self, msg):
        self.msg = msg

    def get_payload(self):
        yield self.msg.as_string()

    def _is_mime(self):
        is_multipart = self.msg.is_multipart()
        payloads = len(self.msg.get_payload()) if self.msg.get_payload() else 0
        return is_multipart and payloads == 2

    def _micalg(self, hash_algo):
        algs = {
            HashAlgorithm.MD5: 'md5',
            HashAlgorithm.SHA1: 'sha1',
            HashAlgorithm.RIPEMD160: 'ripemd160',
            HashAlgorithm.SHA256: 'sha256',
            HashAlgorithm.SHA384: 'sha384',
            HashAlgorithm.SHA512: 'sha512',
            HashAlgorithm.SHA224: 'sha224'
        }
        return 'pgp-' + algs[hash_algo]

    def openpgp_mangle_for_signature(self, msg):
        """Return a message suitable for signing.
        Encodes multipart message parts in msg as base64, then renders the
        message to string enforcing the right newline conventions. The
        returned value is suitable for signing according to RFC 3156.
        The incoming message is modified in-place.
        """
        rfc3156.encode_base64_rec(msg)
        fp = StringIO()
        g = rfc3156.RFC3156CompliantGenerator(
            fp, mangle_from_=False, maxheaderlen=76)

        g.flatten(msg)

        s = re.sub('\r?\n', '\r\n', fp.getvalue())
        if msg.is_multipart():
            if not s.endswith('\r\n'):
                s += '\r\n'
        return s

    def _wrap_signed(self, msg, signature):
        self.msg.set_payload([])
        self.msg.attach(msg)
        self.msg.set_type(CustomMIMEWrapper._signed_multipart)
        self.msg.set_param('micalg', self._micalg(signature.hash_algorithm))
        self.msg.set_param('protocol', CustomMIMEWrapper._signed_type)
        self.msg.preamble = CustomMIMEWrapper._signature_preamble
        second_part = MIMEApplication(_data=str(signature),
                                      _subtype=CustomMIMEWrapper._signature_subtype,
                                      _encoder=encode_7or8bit,
                                      name='signature.asc')
        second_part.add_header('Content-Description', 'OpenPGP digital signature')
        second_part.add_header('Content-Disposition', 'attachment', filename='signature.asc')
        self.msg.attach(second_part)
        return second_part

    def get_encrypted(self):
        try:
            msg = PGPMessage.from_blob(self.msg.get_payload(1).get_payload())
        except:
            return
        yield msg

    @staticmethod
    def copy_headers(from_msg, to_msg, overwrite=False):
        for key, value in from_msg.items():
            if overwrite:
                del to_msg[key]
            if key not in to_msg:
                to_msg[key] = value
        if to_msg.get_unixfrom() is None or overwrite:
            to_msg.set_unixfrom(from_msg.get_unixfrom())
        if (hasattr(from_msg, 'original_size')
                and (getattr(to_msg, 'original_size', None) is None
                     or overwrite)):
            to_msg.original_size = from_msg.original_size

    def decrypt(self, key):
        pmsg = next(iter(self.get_encrypted()))
        decrypted = key.decrypt(pmsg)

        dmsg = decrypted.message
        if isinstance(dmsg, bytearray):
            dmsg = dmsg.decode(decrypted.charset or 'utf-8')

        out = message_from_string(dmsg)
        if decrypted.is_signed:
            signature = next(iter(decrypted.signatures))
            self._wrap_signed(out, signature)
        else:
            self.msg.set_payload(out.get_payload())
            self.copy_headers(out, self.msg, True)
        return self

    def sign(self, key, **kwargs):
        payload = self.openpgp_mangle_for_signature(self.msg)

        signature = key.sign(payload, **kwargs)
        original_msg = copy.deepcopy(self.msg)
        return payload, self._wrap_signed(original_msg, signature)

    def _wrap_encrypted(self, payload):
        self.msg.set_payload([])
        self.msg.set_type(CustomMIMEWrapper._encrypted_multipart)
        self.msg.set_param('protocol', CustomMIMEWrapper._encrypted_type)
        self.msg.preamble = CustomMIMEWrapper._encryption_preamble
        first_part = MIMEApplication(_data='Version: 1',
                                     _subtype=CustomMIMEWrapper._encryption_subtype,
                                     _encoder=encode_7or8bit)
        first_part.add_header('Content-Description',
                              'PGP/MIME version identification')
        self.msg.attach(first_part)
        second_part = MIMEApplication(_data=str(payload),
                                      _subtype='octet-stream',
                                      _encoder=encode_7or8bit,
                                      name='encrypted.asc')
        second_part.add_header('Content-Description',
                               'OpenPGP encrypted message')
        second_part.add_header('Content-Disposition', 'inline',
                               filename='encrypted.asc')
        self.msg.attach(second_part)

    def _encrypt(self, pmsg, keys, cipher, **kwargs):
        emsg = copy.copy(pmsg)
        if len(keys) == 1:
            emsg = keys[0].encrypt(emsg, cipher=cipher, **kwargs)
        else:
            session_key = cipher.gen_key()
            for key in keys:
                emsg = key.encrypt(emsg, cipher=cipher,
                                   sessionkey=session_key,
                                   **kwargs)
            del session_key
        return emsg

    def encrypt(self, key, keys, **kwargs):
        hash = kwargs.get("hash", None)
        if not kwargs.get("cipher"):
            kwargs["cipher"] = SymmetricKeyAlgorithm.AES256

        if len(keys) == 0:
            raise ValueError('At least one key necessary.')

        payload = next(iter(self.get_payload()))
        pmsg = PGPMessage.new(payload)
        pmsg = self._encrypt(pmsg, keys, **kwargs)
        self._wrap_encrypted(pmsg)
        return self

    def sign_encrypt(self, key, keys, **kwargs):
        hash = kwargs.get("hash", None)

        if not kwargs.get("cipher"):
            kwargs["cipher"] = SymmetricKeyAlgorithm.AES256

        if len(keys) == 0:
            raise ValueError('At least one key necessary.')

        payload = next(iter(self.get_payload()))
        pmsg = PGPMessage.new(payload)
        pmsg |= key.sign(pmsg, hash=hash)
        pmsg = self._encrypt(pmsg, keys, **kwargs)
        self._wrap_encrypted(pmsg)
        return self

    def is_signed(self):
        if not self._is_mime():
            return False

        return collapse_rfc2231_value(self.msg.get_payload(1).get_content_type()) == CustomMIMEWrapper._signed_type and \
               self.msg.get_content_subtype() == "signed"

    def is_encrypted(self):
        if not self._is_mime():
            return False
        first_part = self.msg.get_payload(0).as_string()
        first_type = self.msg.get_payload(0).get_content_type()
        second_type = self.msg.get_payload(1).get_content_type()
        content_subtype = self.msg.get_content_subtype()
        protocol_param = collapse_rfc2231_value(self.msg.get_param('protocol', ''))
        return ('Version: 1' in first_part and
                first_type == CustomMIMEWrapper._encrypted_type and
                second_type == 'application/octet-stream' and
                content_subtype == 'encrypted' and
                protocol_param == CustomMIMEWrapper._encrypted_type)
