from datetime import datetime, timedelta
import logging
import os
import tarfile
import uuid
import zipfile
import filetype
import requests
import subprocess

from remo_app.remo.utils import utils

logger = logging.getLogger('remo_app')


class NotEnoughFreeDiskSpace(Exception):
    """Raised when there is no enough free space on disk"""
    pass


class ArchiveTypeNotSupported(Exception):
    """Raised when there is no archive unpacker for giving archive type"""
    pass


class Downloader:
    MB = 1024 * 1024
    chunk_size = 8 * MB

    def __init__(self, url: str, destination: str, filename: str = None, verbose=True):
        self.url = url
        self.destination = destination
        self.filename = filename if filename else str(uuid.uuid4())
        self.filepath = os.path.join(destination, self.filename)
        self.verbose = verbose

    def download(self):
        utils.make_dir(self.destination)
        if self.verbose:
            logger.debug(f'Start download from url: {self.url}')
        start = datetime.now()

        self._check_disk_space()
        if not self._download_with_aria():
            self._fallback()

        if self.verbose:
            logger.debug(
                f'Elapsed {timedelta(seconds=int((datetime.now() - start).seconds))}, downloaded from url: {self.url}')

        return self.filepath

    def _check_disk_space(self):
        with requests.get(self.url, stream=True) as resp:
            resp.raise_for_status()
            self._raise_for_disk_space(self._content_size(resp.headers))

    def _download_with_aria(self) -> bool:
        if not utils.is_tool_exists('aria2c'):
            return False

        cmd = f"""aria2c -x4 -d "{self.destination}" -o "{self.filename}" "{self.url}" """
        if self.verbose:
            logger.debug(f'$ {cmd}')
        kwargs = {
            'shell': True,
        }
        if not self.verbose:
            kwargs['stdout'] = subprocess.DEVNULL
            kwargs['stderr'] = subprocess.DEVNULL
        try:
            return_code = subprocess.call(cmd, **kwargs)
            return (return_code == 0)
        except Exception:
            return False

    def _fallback(self):
        with requests.get(self.url, stream=True) as resp:
            self._download_from_requests_stream(resp)

    def _download_from_requests_stream(self, stream):
        with open(self.filepath, 'wb') as f:
            for chunk in stream.iter_content(self.chunk_size):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    @staticmethod
    def _content_size(headers):
        try:
            return int(headers.get('content-length'))
        except (KeyError, TypeError):
            return -1

    def _raise_for_disk_space(self, file_size):
        free = utils.disk_free_space(self.destination)
        if self.verbose:
            logger.debug(f'Free disk space before download: {utils.human_size(free)}')
            logger.debug(f'File size: {utils.human_size(file_size)}')

        if free < file_size:
            raise NotEnoughFreeDiskSpace(f'Not enough disk space to download file from: {self.url}')


class Unpacker:

    @staticmethod
    def unpack(filepath, extract_dir, remove_archive=True):
        raise NotImplementedError

    @staticmethod
    def _unpack(archive_path, extract_dir, archive=None, remove_archive=True, members=None):
        start = datetime.now()
        logger.debug(f'Start extracting archive {archive_path}')
        try:
            utils.make_dir(extract_dir)
            Unpacker._raise_for_disk_space(archive_path, extract_dir)
            archive.extractall(extract_dir, members)
        finally:
            archive.close()
            elapsed = datetime.now() - start
            logger.debug(f'Elapsed {timedelta(seconds=int(elapsed.seconds))}, extracted archive to {archive_path}')
            if remove_archive:
                os.remove(archive_path)

    @staticmethod
    def _raise_for_disk_space(archive_path, extract_dir):
        free = utils.disk_free_space(extract_dir)
        size = utils.file_size(archive_path)
        logger.debug(f'Free disk space before unpack: {utils.human_size(free)}')
        logger.debug(f'Minimum required size: {utils.human_size(size)}')

        if free < size:
            raise NotEnoughFreeDiskSpace(f'Not enough disk space to unpack file: {archive_path}')

    @staticmethod
    def _resolve_path(path):
        return os.path.realpath(os.path.abspath(path))

    @staticmethod
    def _is_resolved_path_starts_with_base(path, base):
        """
        os.path.join will ignore base if path is absolute
        """
        resolved_path = Unpacker._resolve_path(os.path.join(base, path))
        return resolved_path.startswith(base)


class Zip(Unpacker):
    formats = {
        'application/zip'
    }

    @staticmethod
    def unpack(archive_path, extract_dir, remove_archive=True):
        archive = zipfile.ZipFile(archive_path)
        Unpacker._unpack(archive_path, extract_dir, archive, remove_archive,
                         Zip._filter_valid_members(archive.infolist()))

    @staticmethod
    def _filter_valid_members(members):
        base = Unpacker._resolve_path(".")
        for m in members:
            if not Unpacker._is_resolved_path_starts_with_base(m.filename, base):
                logger.error(f'{m.filename}  is blocked (illegal path)')
            else:
                yield m


class ZipTool(Unpacker):
    formats = {
        'application/zip'
    }

    @staticmethod
    def unpack(archive_path, extract_dir, remove_archive=True):
        if utils.is_tool_exists('unzip'):
            start = datetime.now()
            logger.debug(f'Start extracting archive {archive_path}')
            try:
                utils.make_dir(extract_dir)
                Unpacker._raise_for_disk_space(archive_path, extract_dir)
                cmd = f"""unzip -qq "{archive_path}" -d "{extract_dir}" """
                logger.debug(f'$ {cmd}')
                subprocess.run(cmd, shell=True, check=True)

                logger.debug(
                    f'Elapsed {timedelta(seconds=int((datetime.now() - start).seconds))}, extracted archive to {archive_path}')
                if remove_archive:
                    os.remove(archive_path)
            except Exception as err:
                if isinstance(err, NotEnoughFreeDiskSpace):
                    raise
                Zip().unpack(archive_path, extract_dir, remove_archive)
        else:
            Zip().unpack(archive_path, extract_dir, remove_archive)


class Tar(Unpacker):
    formats = {
        'application/gzip',
        'application/x-xz',
        'application/x-tar',
        'application/x-bzip2'
    }

    @staticmethod
    def unpack(archive_path, extract_dir, remove_archive=True):
        archive = tarfile.open(archive_path)
        Unpacker._unpack(archive_path, extract_dir, archive, remove_archive, Tar._filter_valid_members(archive))

    @staticmethod
    def _filter_valid_members(members):
        base = Unpacker._resolve_path(".")

        for m in members:
            if not Unpacker._is_resolved_path_starts_with_base(m.name, base):
                logger.error(f'{m.name}  is blocked (illegal path)')
            elif m.issym() and not Tar._is_resolved_link_starts_with_base(m.name, m.linkname, base):
                logger.error(f'{m.name} is blocked: Hard link to {m.linkname}')
            elif m.islnk() and not Tar._is_resolved_link_starts_with_base(m.name, m.linkname, base):
                logger.error(f'{m.name} is blocked: Symlink to  {m.linkname}')
            else:
                yield m

    @staticmethod
    def _is_resolved_link_starts_with_base(filename, linkname, base):
        """
        Links are interpreted relative to the directory containing the link
        """
        resolved_path = Unpacker._resolve_path(os.path.join(base, os.path.dirname(filename)))
        return Unpacker._is_resolved_path_starts_with_base(linkname, base=resolved_path)


class TarTool(Unpacker):
    formats = {
        'application/gzip',
        'application/x-xz',
        'application/x-tar',
        'application/x-bzip2'
    }

    @staticmethod
    def unpack(archive_path, extract_dir, remove_archive=True):
        if utils.is_tool_exists('tar'):
            start = datetime.now()
            logger.debug(f'Start extracting archive {archive_path}')
            try:
                utils.make_dir(extract_dir)
                Unpacker._raise_for_disk_space(archive_path, extract_dir)
                cmd = f'tar xf "{archive_path}" -C {extract_dir}'
                logger.debug(f'$ {cmd}')
                subprocess.run(cmd, shell=True, check=True)
                logger.debug(
                    f'Elapsed {timedelta(seconds=int((datetime.now() - start).seconds))}, extracted archive to {archive_path}')
                if remove_archive:
                    os.remove(archive_path)
            except Exception as err:
                if isinstance(err, NotEnoughFreeDiskSpace):
                    raise
                Tar().unpack(archive_path, extract_dir, remove_archive)
        else:
            Tar().unpack(archive_path, extract_dir, remove_archive)


def unpacker_factory(filepath):
    implementations = (ZipTool, TarTool)

    mime = filetype.guess_mime(filepath)
    for imp in implementations:
        if mime in imp.formats:
            return imp

    raise ArchiveTypeNotSupported(f'Could not find unpacker for file: {filepath}, MIME: {mime}')
