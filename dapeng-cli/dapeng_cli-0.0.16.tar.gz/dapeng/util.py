import os
import logging
import datetime
from ftplib import FTP
from base64 import b64decode
import click

SER_HOST = "c21iLXN3bGFiLmNuLXN6aDAyLm54cC5jb20="
CRED = ('bWN1eHByZXNzbw==', 'bWN1X254cF8yMDIw')

LOGGER = logging.getLogger(__name__)

def upload_file(boardname, filepath):
    filename = os.path.basename(filepath)
    home_dir = 'sdk_binary'

    host = b64decode(SER_HOST)
    user = b64decode(CRED[0])
    pwd = b64decode(CRED[1])

    ftp = FTP(host)
    ftp.login(user, pwd)
    ftp.cwd('./')

    LOGGER.info("Upload <%s> to file server: %s.", filename, host)
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M')
    filename = os.path.basename(filepath)
    remote_dir = home_dir + '/' + timestamp + "/" + boardname
    remotefile = remote_dir + "/" + filename

    for fodlername in remote_dir.split('/'):
        if not fodlername:
            continue
        if fodlername not in ftp.nlst():
            ftp.mkd(fodlername)
        ftp.cwd(fodlername)

    filesize = os.path.getsize(filepath)
    with open(filepath, 'rb') as fileobj:
        with click.progressbar(length=filesize, label="progress") as bar:
            ftp.storbinary(
                'STOR %s' % filename,
                fileobj,
                1024,
                callback=lambda sent: bar.update(len(sent)))
    ftp.close()

    return "ftp://{user}:{pwd}@{host}/{path}".format(
        user=user,
        pwd=pwd,
        host=host,
        path=remotefile)
