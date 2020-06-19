import concurrent
import os
import time
from concurrent.futures.process import ProcessPoolExecutor
from datetime import datetime
import json
import logging
from typing import List

import requests
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.conf import settings
from remo_app.remo.api.constants import JobType, TaskType, AnnotationSetType
from remo_app.remo.api.views.mixins import UpdateDatasetModelMixin, DestroyDatasetModelMixin
from remo_app.remo.api.serializers import (
    ListDatasetSerializer,
    DatasetSerializer
)
from remo_app.remo.services.file_store import FileStore
from remo_app.remo.services.uploads import uploads
from remo_app.remo.use_cases.annotation import update_new_annotation
from remo_app.remo.use_cases.annotation.class_encoding.class_encoding import ClassEncodingType, \
    CustomClassEncoding
from remo_app.remo.use_cases.annotation.class_encoding.csv_parser import parse_csv_class_encoding, \
    parse_raw_csv_class_encoding
from remo_app.remo.use_cases.annotation.class_encoding.factory import class_encoding_factory
from remo_app.remo.use_cases.annotation_tasks import parse_annotation_task
from remo_app.remo.use_cases.jobs.dataset import LocalDatasetUploader, \
    upload_local_files, RemoteDatasetUploader, has_annotation_extension  # job_upload_dataset, process_files
from remo_app.remo.models import Dataset, ImageFolder, AnnotationSet, Task
from remo_app.remo import utils
# from remo_app.remo.use_cases.jobs.jobs import enqueue_dataset_job
# from remo_app.remo.use_cases import is_remo_local
from remo_app.remo.use_cases.jobs.update_annotation_set_statistics import update_annotation_set_statistics
from remo_app.remo.use_cases.jobs.update_dataset_statistics import update_dataset_statistics

logger = logging.getLogger('remo_app')


class DatasetViewSet(UpdateDatasetModelMixin,
                     DestroyDatasetModelMixin,
                     viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    throttle_scope = 'uploads'

    def get_serializer_class(self):
        if self.action == 'list':
            return ListDatasetSerializer
        return DatasetSerializer

    def get_queryset(self):
        # TODO: restrict to team when it will be implemented, #272
        return Dataset.objects.filter(Q(user=self.request.user) | Q(is_public=True),
                                      is_archived=False)

    def create(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            data = {}

        name = data.get('name', 'Dataset')
        is_public = data.get('is_public', False)
        if not request.user.is_superuser:
            is_public = False

        dataset = Dataset.objects.create(name=name,
                                         is_public=is_public,
                                         user=self.request.user)
        return Response(self.get_serializer(dataset).data)

    @action(['post'], detail=True, url_path='duplicate')
    def duplicate(self, request, pk=None):
        new_dataset = self.get_dataset(pk)
        new_dataset.pk = None
        new_dataset.is_public = False  # New dataset is always private
        new_dataset.user = request.user
        new_dataset.created_at = timezone.now()
        new_dataset.quantity = 0
        new_dataset.size_in_bytes = 0

        new_dataset.save()
        new_dataset.clone_relations_from(self.get_dataset(pk))
        # new_dataset.users_shared.set([])
        new_dataset.save()

        update_dataset_statistics(new_dataset)
        for annotation_set in new_dataset.annotation_sets.all():
            update_annotation_set_statistics(annotation_set)
            for annotation in annotation_set.annotations.all():
                # TODO: fix issue with not coping skip status
                update_new_annotation(annotation)

        return Response(self.get_serializer(new_dataset).data)

    def get_dataset(self, pk):
        return self.get_queryset().filter(id=pk).first()

    def _validate_annotation_set_id(self, request, dataset):
        annotation_set_id = request.query_params.get('annotation_set_id', None)
        if annotation_set_id:
            try:
                annotation_set_id = int(annotation_set_id)
            except ValueError:
                return None, Response({
                    'error': 'Annotation_set_id should be integer value.'
                }, status=status.HTTP_400_BAD_REQUEST)

            anotation_set = AnnotationSet.objects.filter(id=annotation_set_id).first()
            if not anotation_set:
                return None, Response({
                    'error': f'Annotation set #{annotation_set_id} was not found.'
                }, status=status.HTTP_404_NOT_FOUND)

            if anotation_set.dataset != dataset:
                return None, Response({
                    'error': f'Annotation set #{annotation_set_id} was not found in Dataset #{dataset.id}'
                }, status=status.HTTP_404_NOT_FOUND)

        return annotation_set_id, None

    @action(['post'], detail=True, url_path='upload')
    def upload(self, request, pk):
        dataset = Dataset.objects.filter(id=pk, user=request.user).first()

        annotation_set_id, resp = self._validate_annotation_set_id(request, dataset)
        if resp:
            return resp

        if not dataset or dataset.is_public and not request.user.is_superuser:
            return Response({
                'error': 'Only admin can edit public datasets.'
            }, status=status.HTTP_403_FORBIDDEN)

        if request.content_type.startswith('application/json') or request.content_type.startswith(
            'application/x-www-form-urlencoded'):
            return self.process_json_payload(request, dataset, annotation_set_id=annotation_set_id)
        elif request.content_type.startswith('multipart/form-data'):
            return self.process_multipart_payload(request, dataset, annotation_set_id=annotation_set_id)

        return Response({
            'error': f"Not supported payload format: {request.content_type}",
        }, status=400)

    # @staticmethod
    # def process_request(request, dataset, annotation_set_id, send_end=None):
    #     result = None
    #     if request.content_type.startswith('application/json') or request.content_type.startswith(
    #         'application/x-www-form-urlencoded'):
    #         result = DatasetViewSet._upload_from_url(request, dataset, annotation_set_id=annotation_set_id)
    #     elif request.content_type.startswith('multipart/form-data'):
    #         result = DatasetViewSet._upload_from_request(request, dataset, annotation_set_id=annotation_set_id)
    #
    #     if send_end:
    #         send_end.send(result)
    #     else:
    #         return result

    def validate_annotation_set(self, user_id: int, dataset: Dataset, annotation_set_id: int = None,
                                annotation_task: str = None, annotation_set_name: str = None):
        annotation_task = parse_annotation_task(annotation_task)
        resp = DatasetViewSet._validate_annotation_set_task(annotation_task, annotation_set_id)
        if resp:
            return resp, annotation_task, annotation_set_id

        if annotation_set_id and not annotation_task:
            s = AnnotationSet.objects.get(id=annotation_set_id)
            annotation_task = TaskType(s.task.name)
        annotation_set, resp = DatasetViewSet._create_new_annotation_set(dataset, annotation_set_name,
                                                                         annotation_task,
                                                                         annotation_set_id, user_id)
        if resp:
            return resp, annotation_task, annotation_set_id

        if annotation_set:
            annotation_set_id = annotation_set.id
        return None, annotation_task, annotation_set_id

    def validate_input_parameters_from_multipart(self, data, user, dataset: Dataset, annotation_set_id=None):
        params = {
            'session_id': data.get('session_id'),
            'dataset': dataset,
            'user': user
        }
        complete_session = data.get('complete', False)
        if complete_session in ['true', 'True']:
            complete_session = True
        params['complete'] = complete_session

        resp, annotation_task, annotation_set_id = self.validate_annotation_set(
            user.id, dataset, annotation_set_id, data.get('annotation_task'), data.get('annotation_set_name')
        )
        if resp:
            return resp, params
        params['annotation_task'] = annotation_task
        params['annotation_set_id'] = annotation_set_id

        encoding_params = {'type': data.get('class_encoding_type', 'autodetect')}
        raw_class_encoding = data.get('class_encoding_raw_content')
        if isinstance(raw_class_encoding, str):
            raw_class_encoding = raw_class_encoding.split('\n')
            encoding_params['raw_content'] = raw_class_encoding
            encoding_params['type'] = 'custom'
        class_encoding = DatasetViewSet._parse_class_encoding(encoding_params)
        skip_new_classes = data.get('skip_new_classes', False)
        if skip_new_classes in ['true', 'True']:
            skip_new_classes = True
        params['skip_new_classes'] = skip_new_classes
        params['class_encoding'] = class_encoding

        folder_id = data.get('folder_id')
        folder = DatasetViewSet.get_folder(folder_id, dataset)
        params['folder'] = folder
        return None, params


    def validate_input_parameters_from_json(self, data, user, dataset: Dataset, annotation_set_id=None):
        params = {
            'session_id': data.get('session_id'),
            'dataset': dataset,
            'user': user
        }
        complete_session = data.get('complete', False)
        if complete_session in ['true', 'True']:
            complete_session = True
        params['complete'] = complete_session

        resp, annotation_task, annotation_set_id = self.validate_annotation_set(user.id, dataset,
                                                                                annotation_set_id,
                                                                                data.get('annotation_task'),
                                                                                data.get(
                                                                                    'annotation_set_name'))
        if resp:
            return resp, params
        params['annotation_task'] = annotation_task
        params['annotation_set_id'] = annotation_set_id

        class_encoding = DatasetViewSet._parse_class_encoding(data.get('class_encoding'))
        skip_new_classes = data.get('skip_new_classes', False)
        if skip_new_classes in ['true', 'True']:
            skip_new_classes = True
        params['skip_new_classes'] = skip_new_classes
        params['class_encoding'] = class_encoding

        folder_id = data.get('folder_id')
        folder = DatasetViewSet.get_folder(folder_id, dataset)
        params['folder'] = folder

        input_urls = data.get('urls', [])
        url_errors = []
        urls = []
        for url in input_urls:
            ok, error = DatasetViewSet._validate_url(url)
            if ok:
                urls.append(url)
            else:
                url_errors.append({'url': url, 'error': error})
        params['urls'] = urls
        params['url_errors'] = url_errors
        params['local_files'] = data.get('local_files')
        return None, params

    def process_json_payload(self, request, dataset: Dataset, annotation_set_id=None):
        resp, params = self.validate_input_parameters_from_json(json.loads(request.body), request.user,
                                                                dataset, annotation_set_id)
        if resp:
            return resp

        session = uploads.get_or_create_session(params['session_id'], dataset, request.user)
        if not session:
            return Response({'error': f'session_id: {params["session_id"]} was not found'},
                            status=status.HTTP_404_NOT_FOUND)

        if session.can_append(dataset, request.user):
            session.append(**params)

        if params['complete']:
            uploads.start_session(session.id)

        return Response({'session_id': session.id})

    def process_multipart_payload(self, request, dataset: Dataset, annotation_set_id=None):
        resp, params = self.validate_input_parameters_from_multipart(request.data, request.user, dataset, annotation_set_id)
        if resp:
            return resp

        session = uploads.get_or_create_session(params['session_id'], dataset, request.user)
        if not session:
            return Response({'error': f'session_id: {params["session_id"]} was not found'}, status=status.HTTP_404_NOT_FOUND)

        if session.can_append(dataset, request.user):
            store = FileStore(session)
            store.save_files(request.data.getlist('files'))
            session.append(**params)

        if params['complete']:
            uploads.start_session(session.id)

        return Response({'session_id': session.id})

    @staticmethod
    def _upload_from_url(request, dataset: Dataset, annotation_set_id=None):
        data = json.loads(request.body)

        session_id = data.get('session_id', str(uuid4()))
        print('Session id:', session_id)

        annotation_task = parse_annotation_task(data.get('annotation_task'))
        resp = DatasetViewSet._validate_annotation_set_task(annotation_task, annotation_set_id)
        if resp:
            return resp

        if annotation_set_id and not annotation_task:
            s = AnnotationSet.objects.get(id=annotation_set_id)
            annotation_task = TaskType(s.task.name)

        annotation_set_name = data.get('annotation_set_name', None)
        annotation_set, resp = DatasetViewSet._create_new_annotation_set(dataset, annotation_set_name,
                                                                         annotation_task,
                                                                         annotation_set_id, request.user.id)
        if resp:
            return resp

        if annotation_set:
            annotation_set_id = annotation_set.id

        class_encoding = DatasetViewSet._parse_class_encoding(data.get('class_encoding'))

        skip_new_classes = data.get('skip_new_classes', False)
        if skip_new_classes in ['true', 'True']:
            skip_new_classes = True

        urls = data.get('urls', [])
        folder_id = data.get('folder_id')
        folder = DatasetViewSet.get_folder(folder_id, dataset)

        for url in urls:
            ok, error = DatasetViewSet._validate_url(url)
            if not ok:
                return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        uploads.start_session(session_id)

        with ProcessPoolExecutor(max_workers=1) as executor:
            results = executor.submit(process_upload_from_url, request.user, data.get('local_files'), dataset,
                                      folder, annotation_task, annotation_set_id, class_encoding,
                                      skip_new_classes, urls)

        # recv_end, send_end = Pipe(False)
        # p = Process(target=process_upload_from_url, args=(request.user, data.get('local_files'), dataset, folder, annotation_task, annotation_set_id, class_encoding, skip_new_classes, urls, send_end))
        # p.start()
        # resp = recv_end.recv()
        # p.join()
        err = results.exception()
        if err:
            print('Exception:', err)
            return Response({'files uploaded': 0, 'annotations': 0, 'errors': [err]})

        return Response(results.result())

        # img_count, annotation_count, errs = DatasetViewSet._upload_local_files(request.user,
        #                                                                    data.get('local_files'), dataset,
        #                                                                    folder, annotation_task,
        #                                                                    annotation_set_id=annotation_set_id,
        #                                                                    class_encoding=class_encoding,
        #                                                                    skip_new_classes=skip_new_classes)
        #
        # for url in urls:
        #     extract_dir = os.path.join(settings.TMP_DIR, 'url', str(uuid4()))
        #     images_count, annotations_count, errors = RemoteDatasetUploader(url, request.user, dataset,
        #                                                                     annotation_task,
        #                                                                     folder,
        #                                                                     annotation_set_id=annotation_set_id,
        #                                                                     class_encoding=class_encoding,
        #                                                                     skip_new_classes=skip_new_classes
        #                                                                     ).upload(extract_dir)
        #     img_count += images_count
        #     annotation_count += annotations_count
        #     errs += errors
        #
        # return Response({'files uploaded': img_count, 'annotations': annotation_count, 'errors': errs})

    @staticmethod
    def _store_file(file, dir_path):
        if not DatasetViewSet._is_valid_file(file):
            return 0

        file_path = os.path.join(dir_path, file.name)
        with open(file_path, "wb") as output:
            for chunk in file.chunks():
                output.write(chunk)
        logger.debug(f'File saved to: {file_path}')

        if has_annotation_extension(file_path):
            time.sleep(1)

        return 1

    @staticmethod
    def _is_valid_file(file):
        mime = utils.guess_mime(file)
        if file.size > settings.MAX_FILE_SIZE:
            logger.warning(
                f'File {file.name}: size {utils.human_size(file.size)} exceed max file size for upload')
            return False

        if (mime not in settings.IMAGE_MIME_TYPES
            and mime not in settings.ARCHIVE_MIME_TYPES
            and mime not in settings.ANNOTATION_MIME_TYPES):
            logger.warning(f'File {file.name}: content type {file.content_type} not supported')
            return False

        return True

    @staticmethod
    def _store_files(request):
        files = request.data.getlist('files')
        dir_path = os.path.join(settings.TMP_DIR, 'requests', str(uuid4()))
        utils.make_dir(dir_path)

        counts = map(lambda file: DatasetViewSet._store_file(file, dir_path), files)
        return sum(counts), dir_path

    @staticmethod
    def _parse_folder_id(request):
        folder_id = request.query_params.get('folder_id')
        if not folder_id:
            return None

        try:
            folder_id = int(folder_id)
        except ValueError:
            return None

        return folder_id

    @staticmethod
    def _is_valid_folder_id(folder_id: int, dataset):
        if folder_id <= 0:
            return False

        exists = ImageFolder.objects.filter(pk=folder_id, dataset=dataset).first()
        return bool(exists)

    @staticmethod
    def get_folder(folder_id: int, dataset: Dataset):
        if folder_id is not None:
            try:
                return ImageFolder.objects.get(pk=max(folder_id, 0), dataset=dataset)
            except (ValueError, ImageFolder.DoesNotExist):
                logger.error(f'Folder with id {folder_id} was not found')

    @staticmethod
    def _upload_from_request(request, dataset: Dataset, annotation_set_id=None):
        session_id = request.data.get('session_id', str(uuid4()))

        annotation_task = parse_annotation_task(request.data.get('annotation_task'))
        resp = DatasetViewSet._validate_annotation_set_task(annotation_task, annotation_set_id)
        if resp:
            return resp

        annotation_set_name = request.data.get('annotation_set_name', None)
        annotation_set, resp = DatasetViewSet._create_new_annotation_set(dataset, annotation_set_name,
                                                                         annotation_task,
                                                                         annotation_set_id, request.user.id)
        if resp:
            return resp

        if annotation_set:
            annotation_set_id = annotation_set.id

        encoding_params = {
            'type': request.data.get('class_encoding_type', 'autodetect')
        }
        raw_class_encoding = request.data.get('class_encoding_raw_content')
        if isinstance(raw_class_encoding, str):
            raw_class_encoding = raw_class_encoding.split('\n')
            encoding_params['raw_content'] = raw_class_encoding
            encoding_params['type'] = 'custom'

        class_encoding = DatasetViewSet._parse_class_encoding(encoding_params)

        skip_new_classes = request.data.get('skip_new_classes', False)
        if skip_new_classes in ['true', 'True']:
            skip_new_classes = True

        if annotation_set_id and not annotation_task:
            s = AnnotationSet.objects.get(id=annotation_set_id)
            annotation_task = TaskType(s.task.name)

        file_store = FileStore(None)
        file_store.save_files(request)

        count, dir_path = DatasetViewSet._store_files(request)

        uploads.start_session(session_id)

        with ProcessPoolExecutor(max_workers=1) as executor:
            results = executor.submit(process_upload_from_request, request.user,
                                      request.data.getlist('local_files'), dataset, folder, annotation_task,
                                      annotation_set_id, class_encoding, skip_new_classes, dir_path)

        # recv_end, send_end = Pipe(False)
        # p = Process(target=process_upload_from_request, args=(request.user, request.data.getlist('local_files'), dataset, folder, annotation_task, annotation_set_id, class_encoding, skip_new_classes, dir_path, send_end))
        # p.start()
        # resp = recv_end.recv()
        # p.join()
        # if isinstance(results, concurrent.futures.Future):
        err = results.exception()
        if err:
            print('Exception:', err)
            return Response({'files uploaded': 0, 'annotations': 0, 'errors': [err]})
        # print('Result:', results.result())
        # print('Exception info:', results.exception_info())
        # print('Results:', results, type(results))
        return Response(results.result())

        # local_imgs, local_annotations, local_errs = DatasetViewSet._upload_local_files(request.user,
        #                                                                      request.data.getlist('local_files'),
        #                                                                      dataset,
        #                                                                      folder, annotation_task,
        #                                                                      annotation_set_id=annotation_set_id,
        #                                                                      class_encoding=class_encoding,
        #                                                                      skip_new_classes=skip_new_classes)
        # try:
        #     upload_imgs, upload_annotations, upload_errs = (LocalDatasetUploader(request.user, dataset, dir_path,
        #                                                                          annotation_task=annotation_task,
        #                                                                          folder=folder,
        #                                                                          annotation_set_id=annotation_set_id,
        #                                                                          class_encoding=class_encoding,
        #                                                                          skip_new_classes=skip_new_classes).upload())
        # finally:
        #     utils.remove_dir(dir_path)
        #
        # imgs = local_imgs + upload_imgs
        # annotations = local_annotations + upload_annotations
        # errs = local_errs + upload_errs
        #
        # return Response({'files uploaded': imgs, 'annotations': annotations, 'errors': errs})

    @staticmethod
    def _validate_annotation_set_task(annotation_task, annotation_set_id):
        if annotation_set_id and annotation_task:
            s = AnnotationSet.objects.get(id=annotation_set_id)
            annotation_set_task = TaskType(s.task.name)
            if annotation_set_task != annotation_task:
                return Response({
                    'error': f'Annotation set #{annotation_set_id} task ({annotation_set_task}) does not match with giving task - {annotation_task}'},
                    status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def _create_new_annotation_set(dataset, annotation_set_name, annotation_task, annotation_set_id, user_id):
        if isinstance(annotation_set_name, str):
            annotation_set_name = annotation_set_name.strip()
        else:
            return None, None

        if not annotation_set_name:
            return None, None

        if annotation_set_id:
            return None, Response({
                'error': f'You can not create new annotation set with giving id #{annotation_set_id}'},
                status=status.HTTP_400_BAD_REQUEST)

        if not annotation_task:
            return None, None

        s = AnnotationSet.objects.filter(dataset=dataset, name=annotation_set_name).first()
        if s:
            t = TaskType(s.task.name)
            if t != annotation_task:
                return None, Response({
                    'error': f'Annotation set with giving name "{annotation_set_name}" has different task: {t}'},
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return s, None

        try:
            with transaction.atomic():
                task = Task.objects.get(type=annotation_task.name)
                s = AnnotationSet.objects.create(
                    name=annotation_set_name,
                    type=AnnotationSetType.image.value,
                    task=task,
                    user_id=user_id,
                    dataset=dataset
                )
        except IntegrityError:
            s = AnnotationSet.objects.filter(dataset=dataset, name=annotation_set_name).first()
            if not s:
                return None, Response({
                    'error': f'Failed to create and retrieve annotation set with giving name "{annotation_set_name}".'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return s, None

    @staticmethod
    def _parse_class_encoding(class_encoding):
        """
        class_encoding = {
            'type': autodetect | custom | WordNet | GoogleKnowledgeGraph,
            'classes': {'label': 'class_name'} | 'local_path': '<path>' | 'raw_content': [..lines..]
        }
        """
        if not class_encoding:
            class_encoding = {'type': 'autodetect'}

        encoding_type = class_encoding.get('type')
        if encoding_type == ClassEncodingType.autodetect:
            return None

        if encoding_type == ClassEncodingType.custom:
            classes = class_encoding.get('classes')
            if classes:
                return CustomClassEncoding(classes)

            local_path = class_encoding.get('local_path')
            if local_path:
                return parse_csv_class_encoding(local_path)

            raw_content = class_encoding.get('raw_content')
            if raw_content:
                return parse_raw_csv_class_encoding(raw_content)

        if encoding_type in [ClassEncodingType.word_net, ClassEncodingType.google_knowledge_graph]:
            return class_encoding_factory.get(encoding_type)

        return None

    @staticmethod
    def _upload_local_files(user, local_files: List[str], dataset: Dataset, folder: ImageFolder,
                            annotation_task: TaskType = None, annotation_set_id=None, class_encoding=None,
                            skip_new_classes=False) -> (
        int, int, []):
        if local_files:
            return upload_local_files(user, local_files, dataset, folder, annotation_task,
                                      annotation_set_id=annotation_set_id, class_encoding=class_encoding,
                                      skip_new_classes=skip_new_classes)
        return 0, 0, []

    @staticmethod
    def _validate_url(url):
        try:
            validate = URLValidator()
            validate(url)
        except ValidationError:
            return False, 'invalid URL'

        error = None
        try:
            resp = requests.get(url, stream=True)
            if resp.status_code != 200:
                error = 'invalid URL'
            resp.close()
        except Exception as err:
            error = str(err)

        return error is None, error


def process_upload_from_url(user, local_files, dataset, folder, annotation_task, annotation_set_id,
                            class_encoding, skip_new_classes, urls, send_end=None):
    logger.info(f'Started uploading process from url: {os.getpid()}')
    img_count, annotation_count, errs = 0, 0, []
    try:
        img_count, annotation_count, errs = DatasetViewSet._upload_local_files(user,
                                                                               local_files, dataset,
                                                                               folder, annotation_task,
                                                                               annotation_set_id=annotation_set_id,
                                                                               class_encoding=class_encoding,
                                                                               skip_new_classes=skip_new_classes)

        for url in urls:
            extract_dir = os.path.join(settings.TMP_DIR, 'url', str(uuid4()))
            images_count, annotations_count, errors = RemoteDatasetUploader(url, user, dataset,
                                                                            annotation_task,
                                                                            folder,
                                                                            annotation_set_id=annotation_set_id,
                                                                            class_encoding=class_encoding,
                                                                            skip_new_classes=skip_new_classes
                                                                            ).upload(extract_dir)
            img_count += images_count
            annotation_count += annotations_count
            errs += errors
    except Exception as err:
        msg = f'Uploading process from url unexpectedly terminated by: {err}'
        logger.info(msg)
        errs.append(msg)

    resp = {'files uploaded': img_count, 'annotations': annotation_count, 'errors': errs}
    logger.info(f'Finished uploading process from url: {os.getpid()}')
    if send_end:
        send_end.send(resp)
    else:
        return resp


def process_upload_from_request(user, local_files, dataset, folder, annotation_task, annotation_set_id,
                                class_encoding, skip_new_classes, dir_path, send_end=None):
    logger.info(f'Started uploading process from request: {os.getpid()}')
    imgs, annotations, errs = 0, 0, []
    # try:
    local_imgs, local_annotations, local_errs = DatasetViewSet._upload_local_files(user,
                                                                                   local_files,
                                                                                   dataset,
                                                                                   folder,
                                                                                   annotation_task,
                                                                                   annotation_set_id=annotation_set_id,
                                                                                   class_encoding=class_encoding,
                                                                                   skip_new_classes=skip_new_classes)
    upload_imgs, upload_annotations, upload_errs = (LocalDatasetUploader(user, dataset, dir_path,
                                                                         annotation_task=annotation_task,
                                                                         folder=folder,
                                                                         annotation_set_id=annotation_set_id,
                                                                         class_encoding=class_encoding,
                                                                         skip_new_classes=skip_new_classes).upload())
    imgs = local_imgs + upload_imgs
    annotations = local_annotations + upload_annotations
    errs = local_errs + upload_errs
    # except Exception as err:
    #     msg = f'Uploading process from url request terminated by: {err}'
    #     logger.info(msg)
    #     errs.append(msg)
    # finally:
    utils.remove_dir(dir_path)

    resp = {'files uploaded': imgs, 'annotations': annotations, 'errors': errs}
    logger.info(f'Finished uploading process from request: {os.getpid()}')
    if send_end:
        send_end.send(resp)
    else:
        return resp
