__doc__ = """
A Python interface for sending emails

Functions:
    sendmail - send an email
    sendmailobj - send an EmailMessage object.
    forward - forward an email
"""

## get required modules ##

import copy # to duplicate emails for forwarding and sending
import smtplib # to send emails (Simple Mail Transfer Protocol)
import threading # to send emails in the background
from os.path import basename # to send email attachments
from email.mime.application import MIMEApplication # to send email attachments
from email.mime.multipart import MIMEMultipart # to create multipart emails
from email.mime.text import MIMEText # to add plaintext and html to emails
from email.utils import COMMASPACE, formatdate # COMMASPACE (", "), formatdate
# for getting date of email sending
from .read import EmailMessage2, EmailMessage # get EmailMessage and
# EmailMessage2 classes from emailpy.read module
from .gethostport import gethostport # to get host and port for sending emails

## Functions ##

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
        nofileattach[x] = open(x, 'rb').read() # create nofileattach dictionary

    # background function
    def _sendmail(fromemail, pwd, toemails, subject = '', body = '', \
                  html = None, attachments = None, nofileattach = None):
        # generate the email
        msg = MIMEMultipart('alternative') # create base multipart
        msg['From'] = fromemail # set fromemail
        msg['To'] = COMMASPACE.join(toemails) # set toemails
        msg['Date'] = formatdate(localtime = True) # set date using formatdate
        msg['Subject'] = subject # set subject

        # convert body text to html and add html to end. 
        html = '<pre style = "font-family: Calibri;">'+body+'</pre>'+html
        msg.attach(MIMEText(html, 'html')) # add html and body to email

        for file in nofileattach: # iter through attachments to add to email
            part = MIMEApplication(nofileattach[file], Name = basename(file))
            part['Content-Disposition'] = 'attachment; filename="%s"'\
                                          %basename(file)
            msg.attach(part) # add attachment to email

        host, port = gethostport(fromemail, 'smtp') # get host and port
    
        conn = smtplib.SMTP(host, port) # create connection
        conn.ehlo() # send ehlo message
        conn.starttls() # start tls encryption
        conn.login(fromemail, pwd) # login to email server. 
        conn.sendmail(fromemail, toemails, msg.as_string()) # send email
        conn.close() # close connection

        mail.sent = True # set mail.sent variable to True (set remotely)

    mail = EmailMessage2(fromemail, toemails, subject, body,
                         html, nofileattach) # create mail object

    _sendmail_thread = threading.Thread(target = _sendmail, args = (
        fromemail, pwd, toemails, subject, body, html, attachments,
        nofileattach
        )) # create background thread
    _sendmail_thread.daemon = True # set daemon to True (to run in the background)
    _sendmail_thread.start() # start the thread

    return mail # return mail object

def sendmailobj(mailobj, **kwargs):
    email = kwargs.get('email') or kwargs.get('fromemail') or mailobj.email
    pwd = kwargs.get('pwd') or mailobj.pwd
    recvers = kwargs.get('recvers') or kwargs.get('toemails') or \
              mailobj.recvers
    subject = kwargs.get('subject') or mailobj.subject
    body = kwargs.get('body') or mailobj.body
    html = kwargs.get('html') or mailobj.html
    attachments = kwargs.get('attachments') or []
    nofileattach = kwargs.get('nofileattach') or \
                   ({filename: filedata for filename in \
                    mailobj.attachments.file for filedata \
                    in mailobj.attachments.data} if mailobj.attachments else \
                                               {})
                                                
    return sendmail(email, pwd, recvers, subject, body, html,
                    attachments, nofileattach)

def forward(mailobj, toemails, **kwargs):
    email = kwargs.get('email') or kwargs.get('fromemail') or mailobj.email
    pwd = kwargs.get('pwd') or mailobj.pwd
    recvers = toemails
    subject = kwargs.get('subject') or mailobj.subject
    body = kwargs.get('body') or mailobj.body
    html = kwargs.get('html') or mailobj.html
    attachments = kwargs.get('attachments') or []
    nofileattach = kwargs.get('nofileattach') or \
                   ({filename: filedata for filename in \
                    mailobj.attachments.file for filedata \
                    in mailobj.attachments.data} if mailobj.attachments else \
                                               {})
    date = mailobj.date

    prefix = f'''
---------- Forwarded message ----------
From: {email}
Date: {date}
Subject: {subject}
To: {recvers}

'''
    nsubject = 'Fwd: '+subject
    nbody = prefix + body    
    
    emailobj = copy.deepcopy(mailobj)
    emailobj.msg = list(emailobj.msg)
    emailobj.msg[1] = list(emailobj.msg[1])
    emailobj.msg[1][0] = nsubject
    emailobj.msg[1][1] = nbody
    emailobj.msg[1] = tuple(emailobj.msg[1])
    emailobj.msg = tuple(emailobj.msg)
    
    return sendmailobj(emailobj)
