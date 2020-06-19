import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict
import multiprocessing
from uuid import uuid4

try:
    from remo_app.remo.models import Dataset
except Exception:
    if os.getenv('DJANGO_SETTINGS_MODULE') == "remo_app.config.standalone.settings":
        from remo_app.config.standalone.wsgi import application
    else:
        from config.wsgi import application
    from remo_app.remo.models import Dataset

from django.conf import settings
from remo_app.remo.unpacker.unpackers import Downloader, unpacker_factory
from remo_app.remo.use_cases.annotation.coco import CocoJsonInstanceSegmentation
from remo_app.remo.utils import remove_dir
from remo_app.remo.utils.progress_info import ProgressInfo

from remo_app.remo.models import ImageFolder, DatasetImage, AnnotationSet
from remo_app.remo.use_cases.jobs.dataset import (
    resolve_archive_files,
    resolve_image_files,
    resolve_annotation_files,
    AnnotationParser, has_archive_mimetype, has_image_extension,
)

logger = logging.getLogger('remo_app')


class Progress:
    def __init__(self, queue: multiprocessing.Queue):
        self.closed = False
        self.queue = queue
        self._report({'in_progress': True})

    def _report(self, obj):
        self.queue.put(obj)

    def report_error(self, error):
        if error:
            self._report({'error': error})

    def report_total(self, images: int = 0, annotations: int = 0):
        self._report({'total': {'images': images, 'annotations': annotations}})

    def report_progress(
        self,
        images: int = 0,
        annotations: int = 0,
    ):
        self._report(
            {
                'progress': {
                    'images': images,
                    'annotations': annotations,
                }
            }
        )

    def report_done(
        self,
        done: bool = True,
        images: int = 0,
        annotations: int = 0,
        image_errors: Dict[str, List[str]] = None,
        annotation_errors: Dict[str, List[str]] = None,
    ):
        self._report(
            {
                'done': {
                    'done': done,
                    'images': images,
                    'annotations': annotations,
                    'image_errors': image_errors,
                    'annotation_errors': annotation_errors,
                }
            }
        )

    def report_finish(self):
        if not self.closed:
            self._report({'finish': True})
            self.queue.close()
            self.closed = True

    def report_details(self, details: str):
        self._report({'in_progress_details': details})


def is_tmp_file(file_path: str):
    return file_path.startswith(settings.TMP_DIR)


def remo_log(msg: str, new_line=True, level='INFO'):
    timestamp = datetime.now().strftime("%H:%M:%S")
    end_line = '\n' if new_line else '\r'
    print(f'[{timestamp} RemoApp] {level} - {msg}', end=end_line)


def gen_tmp_dir(name: str):
    extract_dir = os.path.join(settings.TMP_DIR, name, str(uuid4()))
    while os.path.exists(extract_dir):
        extract_dir = os.path.join(settings.TMP_DIR, name, str(uuid4()))
    return extract_dir


def process_upload_session(
    queue: multiprocessing.Queue,
    user,
    upload_dir_path: str,
    local_files: List[str],
    dataset: Dataset,
    folder: ImageFolder,
    annotation_task: str,
    annotation_set_id: int,
    class_encoding,
    skip_new_classes,
    urls: List[str],
):
    logger.debug(f'[WORKER #{os.getpid()}]: started')
    msg = f'Adding Images to Dataset `{dataset.name}` (ID {dataset.id})'
    if annotation_set_id:
        annotation_set = AnnotationSet.objects.get(id=annotation_set_id)
        msg = f'Adding Images and Annotations to Dataset `{dataset.name}` (ID {dataset.id}), in Annotation set `{annotation_set.name}` (ID {annotation_set.id})'
    logger.info(msg)

    progress = Progress(queue)
    progress.report_details('Collecting data')

    scan_dirs = [upload_dir_path]
    if local_files:
        scan_dirs.extend(local_files)

    # download all data
    if urls:
        msg = 'Downloading data'
        progress.report_details(msg)
        logger.info(msg)
        for url in urls:
            extract_dir = gen_tmp_dir('url')
            scan_dirs.append(extract_dir)
            try:
                Downloader(url, extract_dir, verbose=False).download()
            except Exception as err:
                msg = f'Failed download from URL, error: {err}'
                progress.report_error({'type': 'url', 'value': url, 'error': msg})

    # extract all archives
    archives = resolve_archive_files(scan_dirs)
    if archives:
        msg = 'Extracting archives'
        progress.report_details(msg)
        logger.info(msg)
        for file_path in archives:
            filename = os.path.basename(file_path)
            if not has_archive_mimetype(file_path):
                msg = f'File format not supported'
                progress.report_error({'type': 'archive', 'value': filename, 'error': msg})
                continue

            extract_dir = gen_tmp_dir('extract')
            try:
                remove_archive = is_tmp_file(file_path)
                unpacker_factory(file_path).unpack(file_path, extract_dir, remove_archive=remove_archive)
            except Exception as err:
                msg = f'Failed extract archive, error: {err}'
                progress.report_error({'type': 'archive', 'value': filename, 'error': msg})

            scan_dirs.append(extract_dir)
            archives.extend(resolve_archive_files([extract_dir]))

    # scan all files
    annotation_files = []
    if annotation_task:
        msg = 'Collecting annotation files ...'
        progress.report_details(msg)
        remo_log(msg, new_line=False)

        annotation_files = resolve_annotation_files(scan_dirs)
        msg = f'Collecting annotation files - found {len(annotation_files)} files'
        progress.report_details(msg)
        remo_log(msg)

        # download images from COCO annotations
        coco_dir = gen_tmp_dir('coco')
        for file_path in annotation_files:
            with open(file_path) as fp:
                coco = CocoJsonInstanceSegmentation(fp)
                if coco.is_applicable(file_path, fp):
                    progress.report_details('Downloading data')
                    errs = coco.download_images(dataset.id, coco_dir)
                    progress.report_done(image_errors=errs)
        scan_dirs.append(coco_dir)

    msg = 'Collecting image files ...'
    progress.report_details(msg)
    remo_log(msg, new_line=False)

    image_files = resolve_image_files(scan_dirs)
    msg = f'Collecting image files - found {len(image_files)} files'
    progress.report_details(msg)
    remo_log(msg)
    progress.report_total(images=len(image_files), annotations=len(annotation_files))

    # upload images
    if image_files:
        progress.report_details('Processing images')
        progress_info = ProgressInfo(len(image_files), 'images', text='Uploading images')
        for file_path in image_files:
            progress.report_progress(images=1)
            done, err = upload_image(file_path, dataset, folder)
            progress.report_done(done=done, images=1, image_errors=err)
            progress_info.report()

    # upload annotations
    if annotation_files:
        progress.report_details('Processing annotation files')
        parser = AnnotationParser(
            user,
            dataset,
            annotation_task,
            folder,
            annotation_set_id=annotation_set_id,
            class_encoding=class_encoding,
            skip_new_classes=skip_new_classes,
        )

        for i, file_path in enumerate(annotation_files, start=1):
            logger.info(f'Uploading annotations for file {i}/{len(annotation_files)}')
            progress.report_progress(annotations=1)
            annotation_errors = None
            name = os.path.basename(file_path)
            done = False
            try:
                with open(file_path, 'r') as fp:
                    count, err = parser.parse(file_path, fp)
                    done = count > 0
                    if err:
                        annotation_errors = {name: [err]}
            except Exception as err:
                annotation_errors = {name: [err]}
            progress.report_done(done=done, annotations=1, annotation_errors=annotation_errors)

    # delete tmp folders
    for dir_path in scan_dirs:
        if os.path.exists(dir_path) and dir_path.startswith(settings.TMP_DIR):
            remove_dir(dir_path)

    # --------------------------------
    progress.report_finish()
    logger.debug(f'[WORKER #{os.getpid()}]: finished')


def upload_image(file_path, dataset, folder) -> (bool, Dict[str, List[str]]):
    """
    :return: done, errors
    """
    name = os.path.basename(file_path)
    try:
        if not has_image_extension(file_path):
            return False, {name: ['File format not supported']}

        if DatasetImage.is_duplicate(dataset, name):
            return True, {name: ['not added (Duplicated image)']}

        dataset_image = DatasetImage(dataset=dataset, folder=folder)
        if is_tmp_file(file_path):
            dataset_image = dataset_image.upload_image_from_file(file_path)
        else:
            dataset_image = dataset_image.link_local_file(file_path)

        if dataset_image.is_new():
            dataset_image.save()

    except Exception as err:
        return False, {name: [f"Failed to {'upload' if is_tmp_file(file_path) else 'link'} image, error: {err}"]}

    return True, {}
