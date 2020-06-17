import paramiko
import enum
import os
import progress.bar as progress
from loguru import logger
import pyzipper
import glob


class Client:
    class Status(enum.Enum):
        DISCONNECTED = enum.auto()
        CONNECTED = enum.auto()

    def __init__(self):
        self._hostname = 'wockets.ccs.neu.edu'
        self._username = 'wockets'
        self._password = 'mobilehealth6'
        self._status = Client.Status.DISCONNECTED
        self._data_folder = '/srv/'
        self._studies = ['MICROT', 'LML']
        self._client = None

    def connect(self):
        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._client.connect(hostname=self._hostname,
                             username=self._username, password=self._password)
        self._status = Client.Status.CONNECTED
        logger.info('Connected to the server')

    def validate_study_name(self, study_name):
        if study_name not in self._studies:
            logger.error('Study name is not supported: {}', study_name)
            return False
        return True

    def get_participants(self, project):
        assert self._status == Client.Status.CONNECTED
        stdin, stdout, stderr = self._client.exec_command(
            'ls ' + os.path.join(self._data_folder, project))
        participants = [l.strip() for l in stdout.readlines()]
        return participants

    def find_participants(self, project, keyword):
        participants = self.get_participants(project)
        pids = list(filter(lambda pid: keyword in pid, participants))
        return pids

    def download_all(self, project, to, pwd=None):
        folder = os.path.join(self._data_folder, project)
        self._download(folder, to)
        if pwd is None:
            return
        else:
            failed_files = self._decrypt(to, pwd)
            logger.error("Failed to decrypt these files: ")
            for f, e in failed_files:
                logger.error('{}, {}', f, e)

    def download_by_participant(self, project, pid, to, pwd=None):
        folder = self._data_folder + project + '/' + pid
        to = os.path.join(to, pid)
        self._download(folder, to)
        if pwd is None:
            return
        else:
            failed_files = self._decrypt(to, pwd)
            logger.error("Failed to decrypt these files: ")
            for f, e in failed_files:
                logger.error('{}, {}', f, e)

    def _decrypt_file(self, f, to, pwd):
        ref = None
        try:
            ref = pyzipper.AESZipFile(
                f, mode='r', compression=pyzipper.ZIP_DEFLATED)
            os.makedirs(to, exist_ok=True)
            try:
                ref.extractall(to)
            except RuntimeError as e:
                ref.extractall(to, pwd=pwd)
            except Exception as e:
                ref.extractall(to, pwd=pwd)
            ref.close()
            if os.path.dirname(f) != to:
                failed_files = self._decrypt(to, pwd, progress_bar=False)
                if failed_files is not None:
                    return failed_files
                else:
                    return None
            else:
                return None
        except Exception as e:
            if ref is not None:
                ref.close()
            if e is not None:
                return f, e
            else:
                return f, ""

    def _decrypt(self, folder, pwd, progress_bar=True):
        local_files = glob.glob(os.path.join(
            folder, '**', '*.zip'), recursive=True)
        n = len(local_files)
        if progress_bar:
            bar = progress.ChargingBar(
                'Decrypting files', max=n, suffix='%(index)d/%(max)d (%(elapsed_td)s - %(eta_td)s)')
        failed_files = []
        for f in local_files:
            if os.path.basename(f).count('.') > 1:
                to = os.path.dirname(f)
            else:
                to = os.path.join(os.path.dirname(
                    f), os.path.basename(f).split('.')[0])
            result = self._decrypt_file(f, to, pwd)
            if result is not None:
                if type(result) is list:
                    failed_files += result
                else:
                    failed_files.append(result)
            else:
                os.remove(f)
                # create an empty file as a marker indicating that this zip file has been decrypted.
                with open(f + '.done', 'w'):
                    pass
            if progress_bar:
                bar.next()
        if progress_bar:
            bar.finish()
        if len(failed_files) == 0:
            return None
        return failed_files

    def _download(self, folder, to):
        assert self._status == Client.Status.CONNECTED

        ftp_client = self._client.open_sftp()
        stdin, stdout, stderr = self._client.exec_command(
            'find ' + folder + ' -type f')
        files = [l.strip() for l in stdout.readlines()]
        n = len(files)
        bar = progress.ChargingBar(
            'Downloading files', max=n, suffix='%(index)d/%(max)d (%(elapsed_td)s - %(eta_td)s)')
        for f in files:
            local = f.replace(folder, to)
            if os.path.exists(local) or os.path.exists(local + '.done'):
                bar.next()
                continue
            os.makedirs(os.path.dirname(local), exist_ok=True)
            ftp_client.get(f, local)
            bar.next()
        bar.finish()

    @staticmethod
    def extract_participant_list(filepath):
        with open(filepath, mode='r') as f:
            pids = f.readlines()
        pids = list(map(lambda pid: pid.strip('\n'), pids))
        return pids


if __name__ == "__main__":
    client = Client()
    client.connect()
    # client.find_participants('MICROT', 'usc')
    client.download_by_participant(
        'MICROT', 'smeltingexerciserstabilize@timestudy_com', 'D:/Datasets/MICROT')
