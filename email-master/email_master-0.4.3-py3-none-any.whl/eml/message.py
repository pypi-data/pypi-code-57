from email_master.messages import EmailMasterMessage
from email_master.pgp import CustomMIMEWrapper, PGPConfig
from email_master.compat import base64_encode, to_unicode
from email_master.compat import MIMEMultipart, EmailMessage
from email.utils import make_msgid, formatdate
import mimetypes
import smtplib, ssl
import six

if six.PY2:
    from email.MIMEText import MIMEText
elif six.PY3:
    StringTypes = str
    unicode = to_unicode


class EMLMessage(EmailMasterMessage):
    def __init__(self, pgp_config=None):
        if six.PY3:
            super(EMLMessage, self).__init__(EmailMessage(), pgp_config)
        else:
            super(EMLMessage, self).__init__(MIMEMultipart(), pgp_config)

    def _get_to_addrs(self):
        return list(filter(lambda x: x, [self.message_obj["To"], self.message_obj["Cc"], self.message_obj["Bcc"]]))

    def test_conn(self, username, password, host, port, verify_conn=True):
        conn = smtplib.SMTP(host, port, timeout=5)
        conn.ehlo()
        if verify_conn:
            context = ssl.create_default_context()
        else:
            context = ssl._create_unverified_context()

        if six.PY3:
            conn.starttls(context=context)
        else:
            conn.starttls()
            conn.ehlo()
        if password != EmailMasterMessage.NO_PASSWORD:  # Don't log in if no password
            conn.login(username, password)

        conn.noop()  # test connection
        return conn

    def send(self, username, password, host, port, verify_conn=True, attach_hook=None):
        self.message_obj["Message-ID"] = make_msgid()
        self.message_obj["Date"] = formatdate()

        for attch in self._attachments.attachments:  # Add attachments before sending
            fn = attch.filename
            data = attch.raw_data

            ctype_and_encoding = mimetypes.guess_extension(fn)
            if ctype_and_encoding is not None and len(ctype_and_encoding) == 2:
                ctype, encoding = ctype_and_encoding
            else:
                ctype = None
                encoding = None

            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"
            maintype, subtype = ctype.split("/", 1)
            if six.PY3:
                if attach_hook:
                    attch_kwargs = attach_hook(attch)
                else:
                    attch_kwargs = {
                        "maintype": maintype,
                        "subtype": subtype,
                        "filename": fn
                    }
                self.message_obj.add_attachment(
                    data,
                    **attch_kwargs
                )
            else:
                attch_payload = MIMEText(base64_encode(data) + "\r\n", "base64")
                attch_payload.set_charset("utf-8")
                attch_payload.add_header("Content-Disposition", "attachment", filename=fn)
                attch_payload.add_header("Content-Transfer-Encoding", "base64")
                self.message_obj._payload[0].attach(attch_payload)

        signed_payload = self.pgp_config.lock(CustomMIMEWrapper(self.message_obj))
        conn = self.test_conn(username, password, host, port, verify_conn)
        conn.sendmail(self.message_obj["From"], self._get_to_addrs(), signed_payload)

    def get_summary(self):
        return {
            "message_type": str(self.pgp_config.pgp_action.to_ingest_type()),
            "sent_to": ",".join(self._get_to_addrs()),
            "num_attachments": len(self._attachments.attachments),
            "attach_filenames": ",".join([a.filename for a in self._attachments.attachments]),
            "attach_hashes_md5": ",".join([a.hash_md5 for a in self._attachments.attachments]),
            "attach_hashes_sha1": ",".join([a.hash_sha256 for a in self._attachments.attachments]),
            "attach_hashes_sha256": ",".join([a.hash_sha256 for a in self._attachments.attachments]),
            "subject": self.message_obj["Subject"]
        }
