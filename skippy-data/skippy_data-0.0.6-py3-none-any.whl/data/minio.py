import os
import logging
from typing import List

from kubernetes import client, config
from minio import Minio
from minio.error import ResponseError

from skippy.data.utils import get_bucket_urn, get_file_name_urn


def list_minio_pods() -> List[str]:
    logging.debug('list minio pods...')
    # Load the configuration when running inside the cluster (by reading envs set by k8s)
    logging.debug('Loading in-cluster config...')
    config.load_incluster_config()
    api = client.CoreV1Api()
    # field selectors are a string, you need to parse the fields from the pods here
    app = 'minio'
    ret = api.list_pod_for_all_namespaces(watch=False, label_selector="app=" + app)
    pods = list()
    for i in ret.items:
        for c in filter(lambda co: co.name == app, i.spec.containers):
            for p in c.ports:
                pods.append("%s:%d" % (i.status.pod_ip, p.container_port))
    logging.debug(pods)
    return pods


def has_pod_file(urn: str, minio_addr: str) -> bool:
    try:
        if has_pod_bucket(get_bucket_urn(urn),minio_addr):
            stat = minio_client(minio_addr).stat_object(get_bucket_urn(urn), get_file_name_urn(urn))
            return stat.size > 0
        else:
            return False
    except ResponseError as err:
        logging.warning('MinioClientException: %s', err.message)
        return False


def has_pod_bucket(bucket: str, minio_addr: str) -> bool:
    try:
        return minio_client(minio_addr).bucket_exists(bucket)
    except ResponseError as err:
        logging.error('MinioClientException: %s', err.message)
        return False


def minio_client(minio_addr: str) -> Minio:
    minio_ac = os.environ.get('MINIO_AC', None)
    minio_sc = os.environ.get('MINIO_SC', None)
    logging.debug('Minio ACCESS_KEY: %s' % minio_ac)
    logging.debug('Minio SECRET_KEY: %s' % minio_sc)
    logging.debug('Connecting to pod : %s' % minio_addr)
    client = Minio(minio_addr,
                   access_key=minio_ac,
                   secret_key=minio_sc,
                   secure=False)
    return client


def download_file(urn: str) -> str:
    logging.info('download file from urn  %s' % urn)
    for minio_addr in list_minio_pods():
        if has_pod_file(urn, minio_addr):
            client = minio_client(minio_addr)
            response = client.get_object(get_bucket_urn(urn), get_file_name_urn(urn))
            content = str(response.read().decode('utf-8'))
            logging.debug('file content: %s' % content)
            return content


def upload_file(urn: str, content: str) -> None:
    logging.info('upload urn  %s' % urn)
    _wfile_name = get_file_name_urn(urn)
    text_file = open(_wfile_name, "wt")
    n = text_file.write(content)
    text_file.close()
    try:
        with open(_wfile_name, 'rb') as file_data:
            for minio_addr in list_minio_pods():
                if has_pod_bucket(get_bucket_urn(urn), minio_addr):
                    client = minio_client(minio_addr)
                    file_stat = os.stat(_wfile_name)
                    client.put_object(get_bucket_urn(urn), _wfile_name, file_data, file_stat.st_size,
                                      content_type='application/json')
                    break
    except ResponseError as e:
        logging.error('MinioClientException: %s', e.message)
