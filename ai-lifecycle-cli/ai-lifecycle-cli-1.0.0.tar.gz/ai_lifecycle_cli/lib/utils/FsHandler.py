#  © Copyright IBM Corporation 2020.

from pathlib import Path
from datetime import datetime
import shutil
import json
import uuid
import os


class FsHandler:

    def __init__(self):
        self.default_tmp_dir_path = Path('/var/tmp/ai-lifecycle-cli/{}'.format(uuid.uuid4()))
        self.ts_now = int(datetime.timestamp(datetime.now()))

    def setup_default_dir(self):
        """
        Create default directories if they don't exist yet
        """
        Path(self.default_tmp_dir_path).mkdir(parents=True, exist_ok=True)

    def get_default_dir(self):
        """
        Returns path to default temp directories

        :return: str
        """
        return self.default_tmp_dir_path

    def setup_dir(self, path):
        """
        Create directory under specified path if it doesn't exist yet

        :param path:
        :return: Void
        """
        Path(path).mkdir(parents=True, exist_ok=True)

    def cleanup_default_dir(self):
        """
        Cleanup default directory
        """
        shutil.rmtree(str(self.default_tmp_dir_path))

    def create_serialize_directory_structure(self, target_path, asset_types):
        """
        Creates asset files directory

        :param target_path: target path where directories will stay
        :return: Void
        """
        Path(target_path).mkdir(parents=True, exist_ok=True)
        Path.joinpath(target_path, "assettypes").mkdir(parents=True, exist_ok=True)
        Path.joinpath(target_path, "assets").mkdir(parents=True, exist_ok=True)
        Path.joinpath(target_path, "assets", ".METADATA").mkdir(parents=True, exist_ok=True)
        for asset_type in asset_types:
            Path.joinpath(target_path, "assets", str(asset_type)).mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy(
                str(Path(__file__).parent.parent / "resources" / "wml_model.json"),
                str(Path.joinpath(target_path, "assettypes")))
            shutil.copy(
                str(Path(__file__).parent.parent / "resources" / "wml_pipeline.json"),
                str(Path.joinpath(target_path, "assettypes")))
        except:
            print("Couldn't copy assetfiles")

    def cleanup_serialize_directory_structure(self, target_path, asset_types):
        """
        Cleans up asset files directory from empty dirs

        :param target_path:
        :param asset_types:
        :return: Void
        """
        for asset_type in asset_types:
            if len(os.listdir(str(Path.joinpath(target_path, "assets", str(asset_type))))) == 0:
                shutil.rmtree(str(Path.joinpath(target_path, "assets", str(asset_type))))

    def create_manifest_json(self, exported_time, version, type, name, description, folder_path):
        """
        Creates manifest json file

        :param exported_time: current time
        :param version: version
        :param type: container type (ie. project, space)
        :param name: source naem
        :param description: source description
        :param folder_path: path to serialized directory
        :return: void
        """
        manifest_template = dict(
            exported_at=exported_time,
            format_version=version,
            container=dict(
                type=type,
                name=name,
                description=description
            )
        )

        with open(str(Path.joinpath(folder_path, "manifest.json")), 'w') as manifest_json:
            json.dump(manifest_template, manifest_json)

    def archive_dirs(self, dir_paths, target_path):
        """
        Archive directories to local file system

        :param file_paths: list of dir paths
        :param target_path: target path
        :return: list(str)
        """
        dest_list = list()
        if target_path is None:
            target_path = os.getcwd()
        for dir_path in dir_paths:
            dir_path_with_ts = Path(str(dir_path) + '_{}'.format(self.ts_now))
            shutil.make_archive(str(dir_path_with_ts), 'zip', str(dir_path))
            dest = shutil.move(str(dir_path_with_ts.with_suffix('.zip')), str(target_path))
            dest_list.append(dest)

        return dest_list

    def archive_files(self, file_paths, target_path):
        """
        Archive files to local file system

        :param file_paths:
        :param target_path:
        :return: str
        """
        if target_path is None:
            target_path = os.getcwd()

        archive_path = self.default_tmp_dir_path / 'archive'
        self.setup_dir(archive_path)

        for file_path in file_paths:
            shutil.copy(str(file_path), str(archive_path))

        archive_path_with_ts = Path(str(archive_path) + '_{}'.format(self.ts_now))
        shutil.make_archive(str(archive_path_with_ts), 'zip', str(archive_path))

        dest = shutil.move(str(archive_path_with_ts.with_suffix('.zip')), target_path)

        return dest

    def unpack_archive(self, archive_path, target_path):
        """
        Unpack archive to local file system

        :param archive_path:
        :param target_path:
        :return: str
        """
        if target_path is None:
            target_path = os.getcwd()

        shutil.unpack_archive(str(archive_path), str(target_path), 'zip')

        return target_path

    def get_file_from_archive(self, archive_path, filepath):
        """
        Retrieve file from directory

        :param archive_path:
        :param target_path:
        :return:
        """
        target_path = self.unpack_archive(archive_path, self.get_default_dir() / "meta")
        if os.path.isfile(str(target_path / filepath)):
            return target_path / filepath
        else:
            return None

    def list_files(self, source_dir, recursive=False, files_only=False):
        """
        Return list of files under directory

        :param dir:
        :param recursive:
        :param files_only:
        :return:
        """
        file_list = []
        dir_list = []
        if recursive:
            for root, dirs, files in os.walk(str(Path(source_dir))):
                file_list.extend([root + "/" + file for file in files])
            if not files_only:
                dir_list.extend([root + "/" + dir for dir in dirs])
            dir_list = list(set(dir_list))
            file_list.extend(dir_list)
        else:
            file_list = os.listdir(str(Path(source_dir)))
        return file_list

    def copy_file(self, source_path):
        """
        Copy file

        :param source_path:
        :return:
        """
        shutil.copy(str(Path(source_path)), str(Path(source_path).with_suffix('.new')))
        return Path(source_path).with_suffix('.new')

    def overwrite_file(self, source_path, target_path):
        """
        Overwrite file with existing file name

        :param source_path:
        :param target_path:
        :return: str
        """
        Path(target_path).rename(Path(target_path).with_suffix('.old'))
        Path(source_path).rename(Path(target_path))
        os.remove(str(Path(target_path).with_suffix('.old')))

    def move_file(self, source_path, target_path):
        """
        Move file

        :param source_path:
        :param target_path:
        :return:
        """
        return shutil.move(source_path, target_path)

    def move_files(self, source_paths, target_path):
        """
        Move multiple files

        :param source_paths:
        :param target_path:
        :return:
        """
        dest_paths = []
        for source_path in source_paths:
            dest_paths.append(self.move_file(source_path, target_path))
        return dest_paths
