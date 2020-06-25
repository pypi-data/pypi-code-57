__doc__ = """
A Python interface for reading and deleting emails

Functions: 
    readmail - read an email. 
    deletemail - internal function, not intended for user to use.

Classes:
    EmailAttachmentList - internal class, not intented for user to initialize. 
    EmailAttachment - internal class, not intended for user to initialize. 
    EmailMessage - internal class, not intended for user to initialize.
    EmailMessageList - internal class, not intended for user to initialize. 
"""

import sys
import email as _email
import imaplib
import pickle
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
COMMASPACE = ', '
import os
from os.path import basename
import ospy
from base64 import *
import emailpy.imgformats as imgfs

def readmail(email, pwd):
    """
    readmail(email, pwd) > EmailMessageList

    Arguments:
        str: email -  email to read messages from
        str: pwd -  email password

    Return Value:
        returns EmailMessageList object if email inbox not empty,
        and None if email inbox empty.

    Return Value Usage:
        value = readmail(email, pwd)
        value.messages > list of messages
        value[0] > message index 0
        value.uids > email uids
        email = value[0] > message index 0
        email.delete() > delete email
        email.body > email body
        email.subject > email subject
        email.html > email html
        email.sender > email sender
        email.recvers > email recvers
    """

    if email.endswith('@gmail.com'):
        host = 'smtp.gmail.com'
        port = 993
    elif email.endswith('@outlook.com'):
        host = 'smtp-mail.outlook.com'
        port = 993
    elif email.endswith('@hotmail.com'):
        host = 'smtp-mail.outlook.com'
        port = 993
    elif email.endswith('@yahoo.com'):
        host = 'smtp.mail.yahoo.com'
        port = 993
    elif email.endswith('@txt.att.net'):
        host = 'smtp.mail.att.net'
        port = 993
    elif email.endswith('@comcast.net'):
        host = 'smtp.comcast.net'
        port = 993
    elif email.endswith('@vtext.com'):
        host = 'smtp.verizon.net'
        port = 993

    conn = imaplib.IMAP4_SSL(host, port)
    conn.login(email, pwd)
    conn.select('INBOX', readonly = True)
    
    mail = []
    
    subs = []
    bodys = []
    froms = []
    htmls = []
    files = []
    dates = []

    tos = []

    uids = []

    bids = conn.search(None, 'ALL')[1][0].split()
    ids = [int(x) for x in bids]

    for x in range(len(ids)):
        msg = conn.fetch(bids[x], '(RFC822)')
        msg = _email.message_from_string(msg[1][0][1].decode())
        sub = msg['Subject']
        fr = msg['From']
        to = msg['To'].split(', ')
        date = msg['Date']
        text = None
        html = None
        file = []
        if msg.is_multipart():
            for y in msg.get_payload():
                if y.get_content_type() == 'text/plain':
                    text = y.get_payload()
                elif y.get_content_type() == 'text/html':
                    html = y.get_payload()
                else:
                    file.append({y.get_filename(): y.get_payload()})

        if not text:
            if html:
                if re.findall(r'<pre(.*)?>(.*)</pre>', html):
                    text = '\n'.join([x[1] for x in \
                                    re.findall(r'<pre(.*)?>(.*)</pre>', html)])

        subs.append(sub)
        bodys.append(str(text))
        froms.append(fr)
        htmls.append(str(html))
        tos.append(to)
        uids.append(ids[x])
        files.append(file)
        dates.append(date)
    

    for x in range(len(ids)):
        t = [email]
        
        for y in tos[x]:
            t.append(y)
            
        tos[x] = t

        mail.append((froms[x], (subs[x], bodys[x], htmls[x], files[x],
                                dates[x]), tos[x][0], uids[x]))

    for x in range(len(mail)):
        mail[x] = EmailMessage(mail[x], email, pwd)

    if not mail:
        return

    mail = EmailMessageList(mail)

    return mail

def deletemail(email, pwd, uid_s):
    if type(uid_s) == int or type(uid_s) == bytes:
        uid_s = [uid_s]
    else:
        pass

    for x in range(len(uid_s)):
        if type(uid_s[x]) == int:
            uid_s[x] = str(uid_s[x]).encode()
            
    conn = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    conn.login(email, pwd)
    conn.select('INBOX', readonly = False)

    for uid in uid_s:
        conn.store(uid, '+X-GM-LABELS', '\\Trash')
        
    conn.expunge()
    conn.close()
    conn.logout()


def get_from(msg):
    return msg[0]

def get_subject(msg):
    return msg[1][0]

def get_body(msg):
    return msg[1][1]

def get_html(msg):
    return msg[1][2]

def get_tos(msg):
    return msg[2]

def get_uid(msg):
    return msg[3]

def get_files(msg):
    files = []
    for x in msg[1][3]:
        files.append(list(x)[0])
    return files

def get_isa(msg):
    return bool(msg[1][3])

def get_date(msg):
    return msg[1][4]

def get_data(msg):
    data = []
    for x in msg[1][3]:
        if type(x[list(x)[0]]) == str:
            data.append(x[list(x)[0]])
    return data

class MIMEMultipart2(MIMEMultipart):
    def __repr__(self):
        return '<email.mime.multipart.MIMEMultipart Object>'

class EmailAttachmentList:
    def __init__(self, file, data):
        self.file = file
        self.data = data
        self.mode = 'wb'

    def __getitem__(self, key):
        return imgfs.get(EmailAttachment(self.file[key], self.data[key]))

    def __repr__(self):
        return '<EmailAttachmentList Object filenames='+\
               COMMASPACE.join(['"'+x+'"' for x in self.file])+'>'

    def __iter__(self):
        return iter([imgfs.get(EmailAttachment(file, data)) for file in self.file \
                     for data in self.data])

    def __len__(self):
        return len(self.file)

class EmailAttachmentList2(EmailAttachmentList):
    def __getitem__(self, key):
        return EmailAttachment2(self.file[key], self.data[key])

    def __iter__(self):
        return iter([EmailAttachment2(file, data) for file in self.file \
                     for data in self.data])

class EmailAttachment:
    def __init__(self, file, data):
        self.file = file
        try:
            self.data = b64decode(data)
        except:
            self.data = b''.join([bytes(data[x]) for x in range(len(data))])

        self.mode = 'wb'
        self.path = os.path.join(os.environ['HOME'], \
                                           'Downloads', self.file)

    def download(self):
        return open(self.path, self.mode).write(self.data)

    def show(self):
        if 'win' in sys.platform:
            return ospy.startfile(self.path)
        return os.system('open '+self.path)

    def __repr__(self):
        return '<EmailAttachment Object filename="'+self.file+'">'

class EmailAttachment2(EmailAttachment):
    def __init__(self, file, data):
        self.file = file
        try:
            self.data = data.decode()
        except:
            self.data = data
        self.mode = 'wb'
        self.path = os.path.join(os.environ['HOME'], \
                                 'Downloads', self.file)

class EmailMessage:
    def __init__(self, message, email, pwd):
        self.msg = message
        self.eml = MIMEMultipart2()
        self.eml['Subject'] = self.subject
        self.eml['From'] = get_from(self.msg)
        self.eml['To'] = COMMASPACE.join(self.recvers)
        self.eml.attach(MIMEText(self.body, 'plain'))
        self.eml.attach(MIMEText(self.html, 'html'))
        if self.is_attachment:
            for x in self.attachments:
                part = MIMEApplication(str(x.data[0]), Name = basename(x.file))
                part['Content-Disposition'] = 'attachment; filename=\
"%s"'%basename(x.file)
                self.eml.attach(part)
        
        self.email = email
        self.pwd = pwd
        self.location = os.path.join(os.environ['HOME'], 'Downloads')
        self.name = self.subject
        self.name = ''.join(re.findall(r'[^\/:*?<>|\r\n.]', self.name)) + '.eml'

    @property
    def sender(self):
        if type(get_from(self.msg)) == str:
            return [get_from(self.msg)]
        return get_from(self.msg)

    @property
    def subject(self):
        return get_subject(self.msg)

    @property
    def body(self):
        return get_body(self.msg)

    @property
    def html(self):
        return get_html(self.msg)

    @property
    def recvers(self):
        if type(get_tos(self.msg)) == str:
            return [get_tos(self.msg)]
        return get_tos(self.msg)

    @property
    def uid(self):
        return get_uid(self.msg)

    @property
    def files(self):
        return [x for x in get_files(self.msg) if x]

    @property
    def is_attachment(self):
        return get_isa(self.msg)

    @property
    def date(self):
        return get_date(self.msg)

    @property
    def data(self):
        return [x for x in get_data(self.msg) if x]

    @property
    def attachments(self):
        if self.is_attachment:
            return EmailAttachmentList(self.files, self.data)

    def save(self):
        open(os.path.join(self.location, self.name), \
             'w').write(str(self.eml))

    def delete(self):
        deletemail(self.email, self.pwd, self.uid)

    def __repr__(self):
        return '<EmailMessage Object UID = '+str(self.uid)+'>'

class EmailMessage2:
    def __init__(self, send, recv, subject, body, html, filedata):
        self.sender = send
        self.recvers = recv
        self.subject = subject
        self.body = body
        self.html = html
        self.files = list(filedata)
        self.sent = False
        self.attachments = EmailAttachmentList2(list(filedata.keys()), \
                                               list(filedata.values()))
        self.is_attachment = bool(filedata)
        
        self.eml = MIMEMultipart2()
        self.eml['Subject'] = self.subject
        self.eml['From'] = self.sender
        self.eml['To'] = COMMASPACE.join(self.recvers)
        self.eml.attach(MIMEText(self.body, 'plain'))
        self.eml.attach(MIMEText(self.html, 'html'))
        if self.is_attachment:
            for x in self.attachments:
                part = MIMEApplication(x.data, Name = basename(x.file))
                part['Content-Disposition'] = 'attachment; filename=\
"%s"'%basename(x.file)
                self.eml.attach(part)
        
        self.location = os.path.join(os.environ['HOME'], 'Downloads')
        self.name = self.subject+'.eml'

    def save(self):
        open(os.path.join(self.location, self.name), \
             'w').write(str(self.eml))

    def __repr__(self):
        return '<EmailMessage Object>'

class EmailMessageList:
    def __init__(self, messages):
        self.messages = messages
        self.uids = [x.uid for x in self.messages]
        self.suids = [str(x) for x in self.uids]
        self.juids = ', '.join(self.suids) or 'None'

    def __getitem__(self, key):
        return self.messages[key]

    def __repr__(self):
        return '<EmailMessageList Object UIDs = '+self.juids+'>'

    def __iter__(self):
        return iter(self.messages)

    def __len__(self):
        return len(self.messages)
