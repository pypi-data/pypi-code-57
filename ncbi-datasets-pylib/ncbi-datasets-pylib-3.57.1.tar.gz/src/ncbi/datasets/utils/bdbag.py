import collections
from contextlib import contextmanager
import json
import logging
import os
import zipfile
import tempfile
from bdbag import bdbag_api


logger = logging.getLogger()


class BdBag():
    ''' BdBag is a wrapper to present a simplified interface to the dbbag api:
    https://github.com/fair-research/bdbag/blob/master/doc/api.md#archive_bag
    '''

    # tuple with fields required for remote-file manifiest
    RemoteFile = collections.namedtuple(
        'RemoteFile', 'url filename length md5')

    def __init__(self, package_name):
        ''' Create a temp directory for building the bag and create a directory
        inside of that called 'package_name'
        '''
        self.tmp_package_dir = tempfile.TemporaryDirectory()
        self.package_dir = os.path.join(
            self.tmp_package_dir.name, package_name)
        self.archived_file = ''
        os.mkdir(self.package_dir)

    def __del__(self):
        self.tmp_package_dir.cleanup()

    def get_package_dir(self):
        return self.package_dir

    def get_archived_file(self):
        return self.archived_file

    def get_file_path(self, file_name):
        return os.path.join(self.package_dir, file_name)

    @contextmanager
    def get_filehandle_for(self, file_name):
        filename = self.get_file_path(file_name)
        with open(filename, 'w', newline='\r\n') as fh:
            yield fh

    def create_bag(self, remote_files=None, resolve_bag=True, readme_file=""):
        self.make_bag(remote_files)
        if remote_files and resolve_bag:
            self.resolve_bag()
        return self.archive_bag(readme_file)

    def make_bag(self, remote_files=None):
        ''' Perform all steps to create and archive the bag including
        writing the remote files manifest (if provided) as json.

        Args:
            remote_files (list of FtpFile namedtuples) All the files that will be
                written to fetch.txt as remote files
        '''
        remote_manifest_f = None
        algs = ['md5']
        if remote_files:
            remote_manifest_f = tempfile.NamedTemporaryFile(
                mode="w", delete=False)
            print(
                json.dumps([ftp_file._asdict() for ftp_file in remote_files]),
                file=remote_manifest_f
            )
            remote_manifest_f.close()
            bdbag_api.make_bag(
                self.package_dir,
                algs=algs,
                remote_file_manifest=remote_manifest_f.name,
            )
        else:
            bdbag_api.make_bag(
                self.package_dir,
                algs=algs,
            )

        if remote_manifest_f:
            os.remove(remote_manifest_f.name)

    def resolve_bag(self):
        bdbag_api.resolve_fetch(self.package_dir)

    def archive_bag(self, readme_file=""):
        ''' Validate and archive (via zip) the contents of the bdbag adding, optionally,
        a readme file in the top-level directory. This functionality is essentially
        the same as bdbag_api.archive_bag function except for the addition of the README
        file (and it also supports other compression schemes).
        '''

        try:
            bdbag_api.validate_bag_structure(self.package_dir, skip_remote=True)
        except Exception as e:
            logger.error("Error while archiving bag: %s", e)
            raise e

        zfp = '.'.join([self.package_dir, "zip"])
        with zipfile.ZipFile(zfp, 'w', compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
            if readme_file:
                # Need to convert to crlf line endings, so read and write instead of copy
                with open(readme_file, 'r') as rfile:
                    content = rfile.read()
                readme_base_fname = os.path.basename(readme_file)
                readme_target_file = os.path.join(self.tmp_package_dir.name, readme_base_fname)
                with open(readme_target_file, 'w', newline='\r\n') as rfile:
                    rfile.write(content)
                zf.write(readme_target_file, readme_base_fname)

            for dirpath, dirnames, filenames in os.walk(self.package_dir):
                for name in filenames:
                    filepath = os.path.normpath(os.path.join(dirpath, name))
                    relpath = os.path.relpath(filepath, self.tmp_package_dir.name)
                    if os.path.isfile(filepath):
                        zf.write(filepath, relpath)

        logger.info('Created bag archive: %s' % zf.filename)
        self.archived_file = zf.filename

        return self.archived_file

    def to_bytes(self):
        with open(self.archived_file, mode='rb') as bagf:
            return bagf.read()

    @staticmethod
    def create_from_bytes(data, resolve_bag=False):
        bag = BdBag('pkg')
        bag_archive_fname = os.path.join(bag.tmp_package_dir.name, 'bag.zip')
        with open(bag_archive_fname, mode='wb') as bagf:
            bagf.write(data)
        bag.archived_file = bag_archive_fname
        if resolve_bag:
            bdbag_api.extract_bag(
                bag.archived_file, output_path=bag.package_dir)

            dirlist = [os.path.join(bag.package_dir, f) for f in os.listdir(bag.package_dir)]
            package_dirs = [f for f in dirlist if os.path.isdir(f)]
            package_files = [f for f in dirlist if os.path.isfile(f)]

            bag.package_dir = package_dirs[0]
            bag.resolve_bag()

            # if there is a file in the top-level dir, we can assume it is a
            # readme since archive_bag puts it there
            bag.archive_bag(*package_files)
        return bag
