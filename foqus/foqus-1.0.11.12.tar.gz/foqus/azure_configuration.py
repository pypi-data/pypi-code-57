from azure.storage.blob import BlockBlobService, ContentSettings

from foqus.aws_configuration import *

from io import BytesIO

import json
import pickle
import pyarrow.parquet as pq
import urllib
import os
import subprocess




def azure_move_directory(src, dest):
    SAS = AZURE_SAS
    logger.info("moving blobs from original folder: "+str(src)+" to recovery folder on the same azure container: "+str(dest))
    try:
        comm = 'sudo azcopy cp "' + src + '?' + SAS + '" ' + '"' + dest + '?' + SAS + '" --recursive=true --overwrite=ifSourceNewer'
        print(comm)
        process = subprocess.Popen([comm],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=True)
        stdout, stderr = process.communicate()
        stdout, stderr

        supp = 'sudo azcopy rm "' + src + '?' + SAS + '" --recursive=true'
        print(supp)
        process = subprocess.Popen([supp],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=True)
        stdout, stderr = process.communicate()
        stdout, stderr
    except Exception as e:
        logger.error(e)




def upload_folder_into_azure(local_path, directory_path_azure):
    '''
    :param local_path: local path of the folder to upload
    :param directory_path: the path in azure container of the directory
    :return: Nothing
    '''
    block_blob_service = BlockBlobService(account_name=AZURE_ACCOUNT_NAME,
                                          account_key=AZURE_ACCOUNT_KEY)
    try:

        for files in os.listdir(local_path):
            block_blob_service.create_blob_from_path(AZURE_CONTAINER_NAME, os.path.join(directory_path_azure, files),
                                                     os.path.join(local_path, files))
        logger.info('uploading folder %s with success ' % local_path)
    except Exception as e:
        logger.error('Exception in uploading folder in azure storage :' + str(e))


def upload_file_into_azure(file_upload_path, file_local_path):
    '''
    :param file_upload_path: file azure blob path
    :param file_local_path: file local pzth
    :return: Nothing
    '''
    block_blob_service = BlockBlobService(account_name=AZURE_ACCOUNT_NAME,
                                          account_key=AZURE_ACCOUNT_KEY)
    # Upload a blob into a container
    try:
        block_blob_service.create_blob_from_path(
            AZURE_CONTAINER_NAME,
            file_upload_path,
            file_local_path,
            content_settings=ContentSettings(content_type='file')
        )
        logger.info('uploading file %s with success ' % file_local_path)
    except Exception as e:
        logger.error('Exception in uploading file in azure storage :' + str(e))


def list_parquet_files():
    '''
    :return: list of parquets file
    '''
    block_blob_service = BlockBlobService(account_name=AZURE_ACCOUNT_NAME,
                                          account_key=AZURE_ACCOUNT_KEY)

    # block_blob_service.create_container(container_name)
    # block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
    # Upload a blob into a container
    generator = block_blob_service.list_blobs(AZURE_CONTAINER_NAME)
    parquet_files = []
    try:
        for blob in generator:
            if blob.name.endswith('.parquet') and AZURE_VECTORS_PATH in blob.name:
                try:
                    project = blob.name.split('/')[-3]
                    customer_name = blob.name.split('/')[-4]
                    customer_type = blob.name.split('/')[-5]
                    status = db.get_status_project(STATUS_PROJECT_TABLE, customer_name, customer_type,
                                                   'similars', project)
                    if status and status[0] == 2:
                        parquet_files.append(blob.name)
                    else:
                        logger.info('Status Project not 2 %s %s' % (project, status))
                        continue
                except Exception as e:
                    logger.info("Vector not loaded %s" %e)

    except Exception as e:
        logger.error("Exception in listing parquet files ..." + str(e))
    return parquet_files


def load_parquet_from_azure(parquet_file):
    '''
    :param parquet_file: path of parquet file to load from MS azure blob
    :return: the vector data if exist else None
    '''
    byte_stream = BytesIO()
    block_blob_service = BlockBlobService(account_name=AZURE_ACCOUNT_NAME,
                                          account_key=AZURE_ACCOUNT_KEY)
    try:
        block_blob_service.get_blob_to_stream(container_name=AZURE_CONTAINER_NAME, blob_name=parquet_file,
                                              stream=byte_stream)
        df = pq.read_table(source=byte_stream).to_pandas()
    except Exception as e:
        df = None
        # Add finally block to ensure closure of the stream
        byte_stream.close()
        logger.error("exception in loading parquet file ..." + str(e))
    return df


def load_pickle_files(prefix):
    '''
    :param prefix: prefix of the pickle file to load
    :return: the data of the pickle file if exist else None
    '''
    try:
        base_url = AZURE_CUSTOM_DOMAIN_BLOB + AZURE_CONTAINER_NAME + '/'
        file = urllib.request.urlopen(base_url + prefix)
        file_loaded = pickle.load(file)
    except Exception as e:
        file_loaded = None
        logger.error("exception in loading pickel file ..." + str(e))
    return file_loaded


def load_json_file_azure(prefix):
    '''
    :param prefix: the jsonfile prefix to load
    :return: the data of the json file else empty dict
    '''
    json_loaded = {}
    try:
        base_url = AZURE_CUSTOM_DOMAIN_BLOB + AZURE_CONTAINER_NAME + '/'
        json_file = urllib.request.urlopen(base_url + prefix)
        json_loaded = json.loads(json_file.read().decode('utf-8'))
    except Exception as e:
        logger.error("exception in loading json file ..." + str(e))
    return json_loaded


# delete blob
def delete_blob(path_blob_to_delete):
    '''
    :param path_blob_to_delete: the path of the blob
    :return:
    '''
    block_blob_service = BlockBlobService(account_name=AZURE_ACCOUNT_NAME,
                                          account_key=AZURE_ACCOUNT_KEY)
    try:
        block_blob_service.delete_blob(AZURE_CONTAINER_NAME, path_blob_to_delete)
        logger.info("blob %s deleted with success " % path_blob_to_delete)
    except Exception as e:
        logger.error("exception in deleting blob " + str(e))


def load_vectors_from_azure(vectors):
    '''
    :param vectors: dict with vectors names and values initialised to empty dict
    :return: json with all vectors with values
    '''
    # lis parquet_files
    parquet_files = list_parquet_files()
    for p in parquet_files:
        logger.info('Parquet to load ===> %s' % p)
        # load parquet files from azure
        vector_key = (p.split('/part')[0]).split('/')[-1].split('.parquet')[0]
        vector_data = load_parquet_from_azure(p)
        if vector_data is not None:
            vectors[vector_key] = vector_data
            logger.info('Parquet %s  loaded successfully' % vector_key)
        else:
            logger.info('Parquet %s not loaded' % vector_key)
    logger.info("Vectors keys : %s" % vectors.keys())
    return vectors


def list_repository_files(prefix):
    '''
    :return: list of parquets file
    '''
    block_blob_service = BlockBlobService(account_name=AZURE_ACCOUNT_NAME,
                                          account_key=AZURE_ACCOUNT_KEY)
    generator = block_blob_service.list_blobs(AZURE_CONTAINER_NAME)
    files = []
    try:
        for blob in generator:
            if prefix in blob.name:
                files.append(blob.name)
    except Exception as e:
        logger.error("Exception in listing parquet files ..." + str(e))
    return files


def create_delete_container_azure(container_name):
    # container_name = "deleted-" + AZURE_CONTAINER_NAME
    from azure.storage.blob import BlockBlobService, PublicAccess
    blob_service = BlockBlobService(account_name=AZURE_ACCOUNT_NAME,
                                    account_key=AZURE_ACCOUNT_KEY)
    # container_name = "deleted-" + AZURE_CONTAINER_NAME
    result = blob_service.create_container(container_name)
    blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
    if not result:
        logger.info("Container already created")
    return result


def copy_azure_file(blob_name, copy_from_container, copy_to_container):
    create_delete_container_azure(copy_to_container)
    from azure.storage.blob import BlockBlobService
    blob_service = BlockBlobService(account_name=AZURE_ACCOUNT_NAME,
                                    account_key=AZURE_ACCOUNT_KEY)
    try:
        # except Exception as e:
        blob_url = blob_service.make_blob_url(copy_from_container, blob_name)
        # blob_url:https://demostorage.blob.core.windows.net/image-container/pretty.jpg

        blob_service.copy_blob(copy_to_container, blob_name, blob_url)
        #for move the file use this line
        blob_service.delete_blob(copy_from_container, blob_name)
    except Exception as e:
        logger.info('blob_name  %s not found error is %s' % (blob_name, e))


def copy_azure_files(blob_name):

        blob_service = BlockBlobService(account_name=AZURE_ACCOUNT_NAME, account_key=AZURE_ACCOUNT_KEY)
        copy_from_container = 'backup'
        copy_to_container = 'buckupdev'

        blob_url = blob_service.make_blob_url(copy_from_container, blob_name)
        # blob_url:https://demostorage.blob.core.windows.net/image-container/pretty.jpg

        blob_service.copy_blob(copy_to_container, blob_name, blob_url)

        #for move the file use this line
        blob_service.delete_blob(copy_from_container, blob_name)


def copying_files():
    for blob_name in list_repository_files('backup/devBUCUP/'):
        logger.info('====> copying %s' %blob_name)
        copy_azure_files(blob_name)