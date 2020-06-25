def gethostport(email, mode):
    if mode == 'smtp':
        fromemail = email
        
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

    elif mode == 'imap':
        if email.endswith('@gmail.com'):
            host = 'imap.gmail.com'
            port = 993
        elif email.endswith('@outlook.com'):
            host = 'imap-mail.outlook.com'
            port = 993
        elif email.endswith('@hotmail.com'):
            host = 'imap-mail.outlook.com'
            port = 993
        elif email.endswith('@yahoo.com'):
            host = 'imap.mail.yahoo.com'
            port = 993
        elif email.endswith('@txt.att.net'):
            host = 'imap.mail.att.net'
            port = 993
        elif email.endswith('@comcast.net'):
            host = 'imap.comcast.net'
            port = 993
        elif email.endswith('@vtext.com'):
            host = 'incoming.verizon.net'
            port = 993

    return host, port
