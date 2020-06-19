import functools
from typing import List
from datetime import datetime
import logging
import os
from uuid import uuid4
import filetype

from django.conf import settings

from remo_app.remo.use_cases.annotation import update_new_annotation
from remo_app.remo.use_cases.annotation.formats import get_supported_formats
from remo_app.remo.models import AnnotationSet, Dataset, DatasetImage, ImageFolder, Annotation
from remo_app.remo.use_cases.jobs.update_annotation_set_statistics import update_annotation_set_statistics
from remo_app.remo.api.constants import TaskType
from remo_app.remo.unpacker.unpackers import unpacker_factory, Downloader
from remo_app.remo.use_cases.jobs.update_dataset_statistics import update_dataset_statistics
from remo_app.remo.utils import utils
from remo_app.remo.utils.progress_info import ProgressInfo

logger = logging.getLogger('remo_app')


class RemoteDatasetUploader:
    def __init__(
        self,
        url,
        user,
        dataset: Dataset,
        annotation_task=None,
        folder: ImageFolder = None,
        annotation_set_id=None,
        class_encoding=None,
        skip_new_classes=False,
    ):
        self.url = url
        self.user = user
        self.dataset = dataset
        self.annotation_task = annotation_task
        self.folder = folder
        self.annotation_set_id = annotation_set_id
        self.class_encoding = class_encoding
        self.skip_new_classes = skip_new_classes

    def upload(self, extract_dir):
        try:
            Downloader(self.url, extract_dir).download()
            images_count, annotations_count, errors = LocalDatasetUploader(
                self.user,
                self.dataset,
                extract_dir,
                annotation_task=self.annotation_task,
                folder=self.folder,
                annotation_set_id=self.annotation_set_id,
                class_encoding=self.class_encoding,
                skip_new_classes=self.skip_new_classes,
            ).upload()
        finally:
            utils.remove_dir(extract_dir)
        return images_count, annotations_count, errors

    @staticmethod
    def _get_archive_name(url):
        return url.rsplit('/', 1)[1]


class LocalDatasetUploader:
    def __init__(
        self,
        user,
        dataset: Dataset,
        dataset_dir,
        archive_name='',
        annotation_task=None,
        folder: ImageFolder = None,
        annotation_set_id=None,
        class_encoding=None,
        skip_new_classes=False,
    ):
        self.user = user
        self.dataset = dataset
        self.dataset_dir = dataset_dir
        self.archive_name = archive_name
        self.annotation_task = annotation_task
        self.folder = folder
        self.annotation_set_id = annotation_set_id
        self.class_encoding = class_encoding
        self.skip_new_classes = skip_new_classes

    def upload(self) -> (int, int, []):
        image_count, img_errors = self.upload_images()

        files = self._filter_files(self.dataset_dir, self._is_archive)
        arr_image_count, arr_annotations_count, arr_errs = self.upload_archives(files)
        annotations_count, errs = self.upload_annotations()
        update_dataset_statistics(self.dataset)
        return (
            image_count + arr_image_count,
            annotations_count + arr_annotations_count,
            img_errors + arr_errs + errs,
        )

    def upload_images(self):
        start = datetime.now()
        logger.debug(
            f'Uploading imgs to dataset {self.dataset}, dir {self.dataset_dir}, task {self.annotation_task}'
        )
        count, errors = self._upload_images_to_dataset()
        if count > 0:
            self.dataset.update()
        logger.debug(
            f'Elapsed: {datetime.now() - start}, uploaded #{count} images to dataset (ID: {self.dataset.id}) {self.dataset}, dir {self.dataset_dir}, task {self.annotation_task}'
        )
        return count, errors

    def upload_archives(self, files) -> (int, int, []):
        total_images, total_annotations, total_errs = 0, 0, []

        if len(files) == 0:
            return total_images, total_annotations, total_errs

        logger.debug(f'Processing archives for dataset {self.dataset}, task {self.annotation_task}')
        for file_path in files:
            extract_dir = os.path.join(self.dataset_dir, 'extract', str(uuid4()))
            try:
                unpacker_factory(file_path).unpack(file_path, extract_dir)
                images, annotations, errs = LocalDatasetUploader(
                    self.user,
                    self.dataset,
                    extract_dir,
                    os.path.basename(file_path),
                    self.annotation_task,
                    self.folder,
                ).upload()
                total_images += images
                total_annotations += annotations
                total_errs += errs
            finally:
                utils.remove_dir(extract_dir)

        return total_images, total_annotations, total_errs

    def upload_annotations(self) -> (int, []):
        start = datetime.now()
        logger.debug(
            f'Uploading annotations to dataset {self.dataset}, dir {self.dataset_dir}, task {self.annotation_task}'
        )
        annotations_count, errs = self._upload_annotations()
        logger.debug(
            f'Elapsed: {datetime.now() - start}, uploaded {annotations_count} annotations to dataset (ID: {self.dataset.id}) {self.dataset}, dir {self.dataset_dir}, task {self.annotation_task}'
        )
        return annotations_count, errs

    def _upload_images_to_dataset(self):
        files = self._resolve_files(self.folder, self._is_image)
        progress = ProgressInfo(len(files), items='img')
        counts = 0
        errors = []
        for pair in files:
            count, err = self._upload_single_image(*pair, progress)
            counts += count
            if err:
                errors.append(err)

        return counts, errors

    @staticmethod
    def _filter_files(dir_path, filter_func=None):
        files = []
        for dirpath, _, filenames in os.walk(dir_path):
            for name in filenames:
                file_path = os.path.join(dirpath, name)
                ok = bool(not filter_func or filter_func(file_path))
                if not utils.is_system_file(file_path) and ok:
                    files.append(file_path)
        return files

    def count_files(self) -> int:
        files = self._filter_files(self.dataset_dir)
        return len(files)

    def _resolve_files(self, parent_folder, filter_func):
        files = []
        for dirpath, _, filenames in os.walk(self.dataset_dir):
            # path inside dataset dir
            # folder_subpath = dirpath[len(self.dataset_dir) + 1:]
            # folder_subpath = self._skip_root_folder_when_matches_archive_name(folder_subpath, self.archive_name)
            # folder = None
            for name in filenames:
                file_path = os.path.join(dirpath, name)
                if not utils.is_system_file(file_path) and filter_func(file_path):
                    # folder = self._get_folder(folder, folder_subpath, self.dataset, parent_folder)
                    files.append((file_path, parent_folder))

        return files

    def _upload_single_image(self, file_path, folder, progress: ProgressInfo):
        name = os.path.basename(file_path)
        result = 0
        error_msg = ''
        try:
            if DatasetImage.is_duplicate(self.dataset, file_path):
                error_msg = 'Found duplicated image, it will be skipped. Filename {}'.format(name)
                logger.warning(error_msg)
            else:
                dataset_image = DatasetImage(dataset=self.dataset, folder=folder)
                dataset_image = dataset_image.upload_image_from_file(file_path)
                if dataset_image.is_new():
                    dataset_image.save()

                result = 1
        except Exception as err:
            error_msg = f'Failed to upload image {name}, error: {err}'
            logger.error(error_msg)

        progress.report()
        return result, error_msg

    def drop_images(self):
        files = self._filter_files(self.dataset_dir, self._is_image)
        for file_path in files:
            os.remove(file_path)

    def drop_annotations(self):
        files = self._filter_files(self.dataset_dir, self._is_annotation)
        for file_path in files:
            os.remove(file_path)

    @staticmethod
    def _get_folder(folder, folder_path, dataset, parent=None):
        if folder_path == "":
            return parent if folder is None else folder

        folder = None
        names = folder_path.split(os.path.sep)
        for name in names:
            try:
                folder = ImageFolder.objects.get(name=name, dataset=dataset, parent=parent)
            except (ValueError, ImageFolder.DoesNotExist):
                folder = ImageFolder.objects.create(name=name, dataset=dataset, parent=parent)
            parent = folder
        return folder

    @staticmethod
    def _is_image(name):
        mime = filetype.guess_mime(name)
        return mime in settings.IMAGE_MIME_TYPES

    @staticmethod
    def _is_archive(name):
        mime = filetype.guess_mime(name)
        return mime in settings.ARCHIVE_MIME_TYPES

    @staticmethod
    def _is_annotation(name):
        return not (LocalDatasetUploader._is_image(name) or LocalDatasetUploader._is_archive(name))

    @staticmethod
    def _skip_root_folder_when_matches_archive_name(folder_subpath, archive_name):
        """
        In case with this dataset https://www.figure-eight.com/dataset/open-images-annotated-with-bounding-boxes/
        Dataset divided on multiple parts like https://datasets.figure-eight.com/figure_eight_datasets/open-images/zip_files_copy/train_00.zip
        after extracting this archive there is folder 'train_00' with files inside, and it creates folder in our dataset 'train_00'.
        But we want to have one dataset without this separate parts, which relates to archive organization.

        So, in such case when folder_subpath has root folder 'train_00', and archive name 'train_00.zip', we skip root folder
        and create all nested folders.
        """

        # split path on root dir and tail
        folder_subpath_list = folder_subpath.split(os.path.sep, 1)

        # add empty tail if needed
        if len(folder_subpath_list) == 1:
            folder_subpath_list.append("")
        root_dir, tail = folder_subpath_list

        # skip root dir, if it matches with archive name
        common_prefix = os.path.commonprefix([root_dir, archive_name])
        return tail if root_dir == common_prefix else folder_subpath

    def _upload_annotations(self) -> (int, []):
        if self.annotation_task is None:
            return 0, []

        errs = []
        formats = get_supported_formats(self.annotation_task)
        if len(formats) == 0:
            if self.annotation_task:
                err_msg = (
                    f'Annotation format for {self.annotation_task} not recognised. '
                    'Please check the documentation to see supported formats.'
                )
                logger.warning(err_msg)
                errs.append(err_msg)
            return 0, errs

        annotation_parser = AnnotationParser(
            self.user,
            self.dataset,
            self.annotation_task,
            self.folder,
            annotation_set_id=self.annotation_set_id,
            class_encoding=self.class_encoding,
            skip_new_classes=self.skip_new_classes,
        )
        annotations_count = 0

        for dirpath, _, filenames in os.walk(self.dataset_dir):
            for name in filenames:
                file_path = os.path.join(dirpath, name)
                if utils.is_system_file(file_path) or self._is_image(file_path):
                    continue

                with open(file_path) as fp:
                    logger.debug(f'Parsing file {file_path}')
                    count, err = annotation_parser.parse(file_path, fp)
                    annotations_count += count
                    if err:
                        errs.append(err)
        return annotations_count, errs


class AnnotationParser:
    def __init__(
        self,
        user,
        dataset: Dataset,
        annotation_task,
        folder: ImageFolder = None,
        annotation_set_id=None,
        class_encoding=None,
        skip_new_classes=False,
    ):
        self.user = user
        self.dataset = dataset
        self.annotation_task = annotation_task
        self.folder = folder
        self.annotation_set_id = annotation_set_id
        self.class_encoding = class_encoding
        self.skip_new_classes = skip_new_classes

    def parse(self, file_path, annotation_fp) -> (int, str):
        msg = ''
        annotation_file_name = os.path.basename(file_path)
        err_msg = (
            f"Annotation format for {self.annotation_task} not recognised for file '{annotation_file_name}'. "
            "Please check the documentation to see supported formats."
        )
        formats = get_supported_formats(self.annotation_task)
        if len(formats) == 0:
            if self.annotation_task:
                msg = err_msg
                logger.warning(err_msg)
            return 0, msg

        details = []
        annotations_count = 0
        for annotation_format in formats:
            if annotation_format.is_applicable(file_path, annotation_fp):
                parser = annotation_format(annotation_fp)
                parser.folder = self.folder
                parser.class_encoding = self.class_encoding
                images_mapping = parser.fetch_images_mapping(self.dataset.id)

                try:
                    annotations_count += parser.save_annotations(
                        self.dataset.id,
                        self.user.id,
                        images_mapping,
                        annotation_set_id=self.annotation_set_id,
                        skip_new_classes=self.skip_new_classes,
                    )
                except Exception as err:
                    logger.error(err)
                    details.append(str(err))
                    continue
                finally:
                    if len(parser.errors):
                        details += parser.errors

        if annotations_count > 0:
            logger.debug(f'Added {annotations_count} annotation(s)')
            self.dataset.update()

            for annotation_set in AnnotationSet.objects.filter(dataset=self.dataset):
                update_annotation_set_statistics(annotation_set)
                for annotation in Annotation.objects.filter(annotation_set=annotation_set):
                    update_new_annotation(annotation)

        if annotations_count == 0 or details:
            msg = _format_error_msg(err_msg, details, annotation_file_name)

        return annotations_count, msg


def _format_error_msg(err_msg, details, annotation_file_name):
    msg = err_msg
    log_msg = msg
    results = []

    if details:
        rest_details = set()
        missing_files = set()
        failed_download_image = 'Failed to download image'
        cannot_find_img = 'Cannot find image in db'
        for err in details:
            if err.startswith(failed_download_image):
                missing_files.add(err[len(failed_download_image) :].strip())
            elif err.startswith(cannot_find_img):
                missing_files.add(err[len(cannot_find_img) :].strip())
            else:
                rest_details.add(err)

        if rest_details:
            msg = '{} \n Details: \n * {}\n'.format(msg, '\n * '.join(rest_details))
            log_msg = msg
            # logger.warning(log_msg)
            results.append(log_msg)

        if missing_files:

            if len(missing_files) == 1:
                msg = f"Annotations without matching image. Annotation file '{annotation_file_name}' has annotations for '{missing_files.pop()}', which can't be found in the dataset."
                log_msg = msg
            elif len(missing_files) > 1:
                msg = f"Annotations without matching image. Annotation file '{annotation_file_name}' has annotations for {len(missing_files)} images, which can't be found in the dataset:\n"
                log_msg = msg
                for name in missing_files:
                    log_msg += f"\t * {name}\n"

            # logger.warning(log_msg)
            results.append(log_msg)
    else:
        # logger.warning(log_msg)
        results.append(log_msg)

    return '\n'.join(results) if results else msg


def file_has_extension(path, extensions: set):
    _, extension = os.path.splitext(path)
    extension = extension.lower()
    return extension in extensions


def has_archive_extension(path):
    return file_has_extension(path, settings.ARCHIVE_FILE_EXTENSIONS)


def has_image_extension(path):
    return file_has_extension(path, settings.IMAGE_FILE_EXTENSIONS)


def has_annotation_extension(path):
    return file_has_extension(path, settings.ANNOTATION_FILE_EXTENSIONS)


def safe(default_value=None):
    def wrapper(func):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as err:
                logger.error(err)
            return default_value
        return wrapper_func
    return wrapper


@safe(default_value=False)
def file_has_mimetype(path, mimetypes: set):
    mime = filetype.guess_mime(path)
    return mime in mimetypes


def has_archive_mimetype(path):
    return file_has_mimetype(path, settings.ARCHIVE_MIME_TYPES)


def has_image_mimetype(path):
    return file_has_mimetype(path, settings.IMAGE_MIME_TYPES)


def has_no_mimetype(path):
    return file_has_mimetype(path, {None})


def resolve_archive_files(pathes) -> List[str]:
    return resolve_files(pathes, has_archive_mimetype)


def resolve_annotation_files(pathes) -> List[str]:
    return resolve_files(pathes, has_annotation_extension)


def resolve_image_files(pathes) -> List[str]:
    return resolve_files(pathes, has_image_mimetype)


@safe(default_value=[])
def resolve_files(pathes, filter_func) -> List[str]:
    """
    Scans for files and filter by function
    :param filter_func: func(file_path) -> bool, keeps files if func returns True
    """
    files = set()
    for path in pathes:
        if os.path.isfile(path) and filter_func(path):
            files.add(path)
        elif os.path.isdir(path):
            for dirpath, _, filenames in os.walk(path):
                for name in filenames:
                    file_path = os.path.join(dirpath, name)
                    if not utils.is_system_file(file_path) and filter_func(file_path):
                        files.add(file_path)
    return list(files)


def upload_local_files(
    user,
    local_files: List[str],
    dataset: Dataset,
    folder: ImageFolder,
    annotation_task: TaskType = None,
    annotation_set_id=None,
    class_encoding=None,
    skip_new_classes=False,
) -> (int, int, []):
    if not local_files:
        return 0, 0, []
    arch_images, arch_annotations, arch_errs = _upload_local_archives(
        user,
        local_files,
        dataset,
        folder,
        annotation_task,
        annotation_set_id=annotation_set_id,
        class_encoding=class_encoding,
    )
    img_count, img_errs = _upload_local_images(local_files, dataset, folder)
    annotation_count, errs = _parse_local_annotations(
        user,
        local_files,
        dataset,
        folder,
        annotation_task,
        annotation_set_id=annotation_set_id,
        class_encoding=class_encoding,
        skip_new_classes=skip_new_classes,
    )
    return img_count + arch_images, annotation_count + arch_annotations, img_errs + errs + arch_errs


def _upload_local_archives(
    user,
    local_files: List[str],
    dataset: Dataset,
    folder: ImageFolder,
    annotation_task: TaskType,
    annotation_set_id=None,
    class_encoding=None,
):
    files = resolve_archive_files(local_files)
    extract_dir = os.path.join(settings.TMP_DIR, 'requests', str(uuid4()))
    utils.make_dir(extract_dir)
    try:
        images, annotations, errs = LocalDatasetUploader(
            user,
            dataset,
            extract_dir,
            annotation_task=annotation_task,
            folder=folder,
            annotation_set_id=annotation_set_id,
            class_encoding=class_encoding,
        ).upload_archives(files)
    finally:
        utils.remove_dir(extract_dir)
    return images, annotations, errs


def _upload_local_images(local_files: List[str], dataset: Dataset, folder: ImageFolder):
    uploaded_img_count = 0
    files = resolve_image_files(local_files)
    errors = []
    for file_path in files:
        try:
            name = os.path.basename(file_path)
            if DatasetImage.is_duplicate(dataset, name):
                msg = 'Found duplicated image, it will be skipped. Filename '.format(name)
                errors.append(msg)
                logger.warning(msg)
                continue

            dataset_image = DatasetImage(dataset=dataset, folder=folder)
            dataset_image = dataset_image.link_local_file(file_path)
            if dataset_image.is_new():
                dataset_image.save()
                uploaded_img_count += 1
        except Exception as err:
            msg = "Failed to link image: {}, ERROR: {}".format(name, err)
            logger.error(msg)
            errors.append(msg)

    return uploaded_img_count, errors


def _parse_local_annotations(
    user,
    local_files: List[str],
    dataset: Dataset,
    folder: ImageFolder,
    annotation_task: TaskType,
    annotation_set_id=None,
    class_encoding=None,
    skip_new_classes=False,
):
    files = resolve_annotation_files(local_files)
    total_count = 0
    errs = []
    parser = AnnotationParser(
        user,
        dataset,
        annotation_task,
        folder,
        annotation_set_id=annotation_set_id,
        class_encoding=class_encoding,
        skip_new_classes=skip_new_classes,
    )
    for file_path in files:
        try:
            with open(file_path, 'r') as fp:
                count, err = parser.parse(file_path, fp)
                total_count += count
                if err:
                    errs.append(err)
        except Exception as err:
            logger.error(err)
            errs.append(err)
    return total_count, errs
