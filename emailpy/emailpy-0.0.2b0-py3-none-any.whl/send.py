__doc__ = """
A Python interface for sending emails

Functions:
    sendmail - send an email
"""

import smtplib
import threading
from os.path import basename
from email import message_from_string
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from .read import EmailMessage2

def sendmail(fromemail, pwd, toemails, subject = '', body = '', html = None, \
             attachments = None, nofileattach = None):
    """
    sendmail(fromemail, pwd, toemails, subject = '', body = '', html = None,
             attachments = None) > send an email

    Arguments:
        str: fromemail - email to send from
        str: pwd - email password
        list, str: toemails - email(s) to send to
        str: subject - email subject
        str: body - email body
        str: html - html code of email after body. (optional)
        list, str: attachments - list of string filename attachments or single string \
        filename attachment
        dict: nofileattach - attachments without file ({filename: filedata})
    """
    if type(toemails) == str:
        toemails = [toemails]
    if type(attachments) == str:
        attachments = [attachments]
    if not html:
        html = ''

    attachments = attachments or []
    nofileattach = nofileattach or {}
    
    for x in attachments:
        nofileattach[x] = open(x, 'rb').read()

    def _sendmail(fromemail, pwd, toemails, subject = '', body = '', \
                  html = None, attachments = None, nofileattach = None):
        msg = MIMEMultipart('alternative')
        msg['From'] = fromemail
        msg['To'] = COMMASPACE.join(toemails)
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = subject

        html = '<pre style = "font-family: Calibri;">'+body+'</pre>'+html
        msg.attach(MIMEText(html, 'html'))

        for file in nofileattach:
            part = MIMEApplication(nofileattach[file], Name = basename(file))
            part['Content-Disposition'] = 'attachment; filename="%s"'\
                                          %basename(file)
            msg.attach(part)

        if fromemail.endswith('@gmail.com'):
            host = 'smtp.gmail.com'
            port = 587
        elif fromemail.endswith('@outlook.com'):
            host = 'smtp-mail.outlook.com'
            port = 587
        elif fromemail.endswith('@hotmail.com'):
            host = 'smtp-mail.outlook.com'
            port = 587
        elif fromemail.endswith('@yahoo.com'):
            host = 'smtp.mail.yahoo.com'
            port = 587
        elif fromemail.endswith('@txt.att.net'):
            host = 'smtp.mail.att.net'
            port = 465
        elif fromemail.endswith('@comcast.net'):
            host = 'smtp.comcast.net'
            port = 587
        elif fromemail.endswith('@vtext.com'):
            host = 'smtp.verizon.net'
            port = 465
    
        conn = smtplib.SMTP(host, port)
        conn.ehlo()
        conn.starttls()
        conn.login(fromemail, pwd)
        conn.sendmail(fromemail, toemails, msg.as_string())
        conn.close()

        mail.sent = True

    mail = EmailMessage2(fromemail, toemails, subject, body,
                         html, nofileattach)

    _sendmail_thread = threading.Thread(target = _sendmail, args = (
        fromemail, pwd, toemails, subject, body, html, attachments,
        nofileattach
        ))
    _sendmail_thread.daemon = True
    _sendmail_thread.start()

    return mail

def sendmailobj(mailobj, **kwargs):
    email = kwargs.get('email') or kwargs.get('fromemail') or mailobj.email
    pwd = kwargs.get('pwd') or mailobj.pwd
    recvers = kwargs.get('recvers') or kwargs.get('toemails') or \
              mailobj.recvers
    subject = kwargs.get('subject') or mailobj.subject
    body = kwargs.get('body') or mailobj.body
    html = kwargs.get('html') or html
    attachments = kwargs.get('attachments') or []
    nofileattach = kwargs.get('nofileattach') or \
                   {filename: filedata for filename in \
                    mailobj.attachments.file for filedata \
                    in mailobj.attachments.data}
    
    return sendmail(email, pwd, recvers, subject, body, html,
                    attachments, nofileattach)
