from .bitcoin import Bitcoin
import os
import subprocess
from datetime import datetime
import shutil

ROOT_DIR = os.path.dirname(os.path.abspath("omg"))
PKG_DIR = os.path.dirname(os.path.abspath(__file__))


class OMG(object):

    def __init__(self, signing_key):
        self.template_path = os.path.join(PKG_DIR, "templates")
        self.public_path = os.path.join(ROOT_DIR, "public")
        self.unsigned_path = os.path.join(self.public_path, "unsigned")
        self.signed_path = os.path.join(self.public_path, "signed")
        self.signing_key = signing_key

    def create_directory(self, path):
        try:
            os.makedirs(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)

    def make_dynamic_text(self):
        date = datetime.now().strftime('%Y-%m-%d')
        blockhash = Bitcoin.latest_block_hash()
        text = '\nToday is {}.\nLatest bitcoin block hash:\n{}'.format(
                                                                    date,
                                                                    blockhash)
        return text

    def get_public_key_block(self):
        file = os.path.join(self.signed_path, "pgp.txt.asc")

        if not os.path.isfile(file):
            cmd = 'gpg --yes --armor --export {} > {}'.format(self.signing_key,
                                                              file)
            p = subprocess.Popen("exec " + cmd,
                                 stdout=subprocess.PIPE,
                                 shell=True)
            p.stdout.close()

    def create_template_files(self):
        if not os.path.isdir(self.template_path):
            self.create_directory(self.template_path)

            master_templates = os.path.join(PKG_DIR, "templates")
            for filename in os.listdir(master_templates):
                if filename.endswith(".tpl"):
                    file = os.path.join(self.template_path, filename)
                    shutil.copy(os.path.join(master_templates, filename), file)

    def make_text_files(self):
        if not os.path.isdir(self.unsigned_path):
            self.create_directory(self.unsigned_path)

        for filename in os.listdir(self.template_path):

            if filename.endswith(".tpl"):
                file = os.path.join(self.unsigned_path,
                                    filename.split(".")[0] + ".txt")

                text = self.make_dynamic_text()
                shutil.copy(os.path.join(self.template_path, filename), file)
                with open(file, "a") as f:
                    f.write(text)

    def sign_text(self):
        if not os.path.isdir(self.signed_path):
            self.create_directory(self.signed_path)

        for filename in os.listdir(self.unsigned_path):
            if filename.endswith(".txt"):
                file = os.path.join(self.unsigned_path, filename)
                file_output = os.path.join(self.signed_path,
                                           filename.split(".")[0] + ".txt.asc")

                cmd = 'gpg --yes --clearsign --default-key {} --output {} {}'.format(self.signing_key, file_output, file)

                p = subprocess.Popen("exec " + cmd,
                                     stdout=subprocess.PIPE,
                                     shell=True)
                p.stdout.close()

    def sign(self):
        self.make_text_files()
        self.sign_text()
        self.get_public_key_block()
