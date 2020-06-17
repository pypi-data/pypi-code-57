#! /usr/bin/python
# -*- coding: utf-8 -*-
from foqus.commons import download
from foqus.customers import *
from foqus.pipline_cutomise import *
from foqus.request_api import APIFoqus
from six.moves import http_client

from urllib.parse import urlparse
from urllib.request import urlopen

import imghdr
import mimetypes
import tensorflow as tf
import requests
import shutil
import xlrd

from jsondiff import diff
import os
from pathlib import Path
import json
import glob
api = APIFoqus()


from keras.backend.tensorflow_backend import set_session
from keras.backend.tensorflow_backend import clear_session
from keras.backend.tensorflow_backend import get_session
import tensorflow, gc


# Reset Keras Session
def reset_keras():
    sess = get_session()
    clear_session()
    sess.close()
    sess = get_session()

    logger.info(gc.collect())  # if it's done something you should see a number being outputted

    # use the same config as you used to create the session
    config = tensorflow.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = 1
    config.gpu_options.visible_device_list = "1"
    set_session(tensorflow.Session(config=config))


def get_category(last_json, num_cat):
    for json_value in last_json.values():
        for index_product in range(len(json_value)):
            if str(index_product) == str(num_cat):
                try:
                    logger.info("The_Category_that_will_have_changes: " + str(json_value[index_product]['Categorie']))
                    return str(json_value[index_product]['Categorie'])
                except Exception as e:
                    return None


def write_to_file(status, last_json, path_new_file, category_will_have_changes=None, block_image_n=None,
                  new_file=False):
    try:
        json_value = json.loads(path_new_file)
    except Exception as e:
        json_value = {}
    new_obj = {}
    key = ""
    try:
        for key, json_value in last_json.items():
            for index_product in range(len(json_value)):
                for product in range(len(json_value[index_product]['Photos'])):
                    if new_file:
                        photo = json_value[index_product]['Photos'][product]
                        photo["Status"] = 1
                    if not block_image_n and not "Status" in json_value[index_product]['Photos'][product]:
                        photo = json_value[index_product]['Photos'][product]
                        photo["Status"] = 2
                    if category_will_have_changes \
                            and json_value[index_product]['Categorie'] == category_will_have_changes:
                        if str(product) == str(block_image_n):
                            photo = json_value[index_product]['Photos'][product]
                            photo["Status"] = status
    except Exception as e:
        logger.error("Erooor in_difff_files write_to_file %s" % e)
    new_obj[key] = json_value
    with open(path_new_file, 'w') as outfile:
        json.dump(new_obj, outfile)
    outfile.close()
    return new_obj


def delta_retrieve_json(customer_name, customer_type, project_name):
    path_json = STREAMS_PATH + customer_type + '/' + customer_name + '/similars/' + project_name
    date = datetime.datetime.today().strftime("%Y-%m-%d:%H-%M")
    path_new_file = STREAMS_PATH + customer_type + '/' + customer_name + '/delta_files/' + project_name + '/'

    if not os.path.isdir(path_new_file):
        try:
            os.makedirs(path_new_file)
        except Exception as e:
            logger.error("Cannot create delta_files directory for customer. "
                         "Please verify permissions ")
            pass

    new_file_status = path_new_file + date + ".json"

    paths = sorted(glob.glob(path_json + "/*.json"), key=os.path.getmtime)
    if len(paths) > 1:
        last_json_path = paths[-1]
        before_last_json_path = paths[-2]
        last_json = json.load(open(last_json_path))
        before_last_json = json.load(open(before_last_json_path))
    elif len(paths) == 1:
        last_json_path = paths[-1]
        last_json = json.load(open(last_json_path))
        before_last_json = {customer_name + "_" + customer_type: []}
    else:
        last_json = {customer_name + "_" + customer_type: []}
        before_last_json = {customer_name + "_" + customer_type: []}
    try:
        difference = diff(before_last_json, last_json)
    except Exception as e:
        logger.error("Error_diff %s" %e)
        difference = {}
    if before_last_json[customer_name + "_" + customer_type] != [] and difference != {} \
            and difference[customer_name + '_' + customer_type]:
        for kcat, cat in difference[customer_name + '_' + customer_type].items():
            category_will_have_changes = get_category(last_json, kcat)
            if category_will_have_changes:
                for kphotos, photos in cat.items():
                    for kchanges, changes in photos.items():
                        if str(kchanges) == '$insert':
                            status = 1
                            for change in changes:
                                for t in change:
                                    if str(t).isnumeric():
                                        block_image_n = str(t)
                                    else:
                                        logger.info("added in: " + block_image_n)
                                        last_json = write_to_file(status, last_json, new_file_status,
                                                                  category_will_have_changes, block_image_n)
                        elif str(kchanges) == '$delete':
                            status = 0
                            for change in changes:
                                block_image_n = str(change)
                                logger.info("deleted in: " + block_image_n)
                                last_json = write_to_file(status, last_json, new_file_status, category_will_have_changes,
                                              block_image_n)

            else:
                try:
                    for kphotos, photos in cat.items():
                        for kchanges, changes in photos.items():
                            if str(kchanges) == '$insert':
                                status = 1
                                for change in changes:
                                    block_image_n = change[0]
                                    logger.info("added in: " + str(block_image_n) + " kcat " + str(kcat))
                                    last_json[customer_name + "_" + customer_type][kcat]['Photos'][int(block_image_n)]["Status"] = 1
                            elif str(kchanges) == '$delete':
                                status = 0
                                for change in changes:
                                    block_image_n = change
                                    logger.info("deleted in: " + str(block_image_n))
                                    delete_block = before_last_json[customer_name + "_" + customer_type][kcat]['Photos'][block_image_n]
                                    delete_block["Status"] = 0
                                    last_json[customer_name + "_" + customer_type][kcat]['Photos'].append(delete_block)
                except Exception as e:
                    logger.error("Erooor in_difff_files delta_retrieve_json %s" % e)
                    write_to_file(1, last_json, new_file_status)

        write_to_file(2, last_json, new_file_status)
    elif difference == {} and len(paths) > 1:
        write_to_file(2, last_json, new_file_status)
    else:
        write_to_file(1, last_json, new_file_status, new_file=True)
    return new_file_status


def load_labels(label_file):
    if '://' in label_file:
        response = urlopen(label_file)
        proto_as_ascii_lines = response.read()
        label = proto_as_ascii_lines.decode('utf-8').split('\n')
    else:
        label = []
        proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
        for l in proto_as_ascii_lines:
            label.append(l.rstrip())
    return label


def count_images_folders(path):
    x = 0
    for i in os.listdir(str(path)):
        x = x + 1
    return x


def load_graph(model_file):
    if '//' in model_file:
        try:

            logger.info('Getting graph from %s' %model_file)
            response = urlopen(model_file).getcode()
            if response == 200:
                graph = tf.Graph()
                graph_def = tf.GraphDef()
                file = urlopen(model_file)
                file_content = file.read()
                graph_def.ParseFromString(file_content)
                with graph.as_default():
                    tf.import_graph_def(graph_def)
                return graph
            else:
                logger.info('file %s Not exisiting in server' %model_file)

        except Exception as e:
            logger.error('Error %s in getting graph from remote server %s'% (e, model_file))
    else:
        graph = tf.Graph()
        graph_def = tf.GraphDef()

        with open(model_file, "rb") as f:
            graph_def.ParseFromString(f.read())
        with graph.as_default():
            tf.import_graph_def(graph_def)
        return graph
    return None


def load_json_data(json_path):
    try:
        with open(json_path) as data_file:
            json_input = json.load(data_file)
    except:
        json_data = open(json_path)
        bom_maybe = json_data.read(3)
        if bom_maybe != codecs.BOM_UTF8:
            json_data.seek(0)
        json_input = json.load(json_data)
    return json_input


def checkUrl(url):
    p = urlparse(url)
    conn = http_client.HTTPConnection(p.netloc)
    conn.request('HEAD', p.path)
    resp = conn.getresponse()
    return resp.status < 400


def is_url_image(image_url):
    image_formats = ("image/png", "image/jpeg", "image/jpg", "binary/octet-stream")
    r = requests.head(image_url)
    if r.headers["content-type"] not in image_formats:
        mimetype, encoding = mimetypes.guess_type(image_url)
        return mimetype and mimetype.startswith('image')
    else:
        return True


def image_extension(image_url):
    r = requests.head(image_url)
    if r.headers["content-type"]:
        return r.headers["content-type"].split('/')[1]
    else:
        return image_url.split('.')[-1]


def max_nb_images(path):
    list_nbrs = []
    for j in os.listdir(path):
        for k in os.listdir(str(path) + "/" + str(j)):
            ext = imghdr.what(str(path) + "/" + str(j) + "/" + str(k))
            if (ext == 'png' and k.split(".")[1] in ['jpg', 'jpeg', 'JPG', 'JPEG']) or \
                    (ext in ['jpeg', 'jpg'] and k.split('.')[1] in ['png', 'PNG']) or (ext is None):
                os.remove(str(path) + "/" + str(j) + "/" + str(k))
                logger.info("Deleting_image as it contains png encoding - " + str(path) + "/" + str(j) + "/" + str(k))
        list_nbrs.append(len(os.listdir(str(path) + "/" + str(j))))
    return max(list_nbrs)


def verif_folder_less_twenty(path):
    image_ext = ['.jpg', '.png', '.jpeg', '.JPG', '.PNG', '.JPEG']
    folder_less_20 = []
    max_nb = max_nb_images(path)
    if max_nb < 20:
        max_nb = 20
    for j in os.listdir(path):
        x = 0
        for i in os.listdir(str(path) + "/" + str(j)):
            if os.path.splitext(i)[1] in image_ext:
                x = x + 1
        if x == 0 :
            shutil.rmtree(str(path) + "/" + str(j))
            logger.info("Deletin Empty folder : " + str(path) + "/" + str(j))
        elif (x <= 20 or x < max_nb):
            logger.info("WARNING: Folder has less images : " + str(j).split('/')[-1])
            folder_less_20.append(str(j).split('/')[-1])
    return folder_less_20, max_nb


def generate_more_images(training_path, folders, max_nb):
    for id_categorie in folders:
        DIR = str(training_path) + "/" + str(id_categorie)
        nb_images = (len(os.listdir(DIR)))
        p = Pipeline2(source_directory=DIR, output_directory=DIR)
        p.rotate(probability=1, max_left_rotation=5, max_right_rotation=5)
        p.flip_left_right(probability=0.5)
        p.zoom_random(probability=0.5, percentage_area=0.8)
        p.flip_top_bottom(probability=0.5)
        p.sample(max_nb - nb_images)
    logger.info("The images increase is done successfully")


def read_tensor_from_image_file(file_name, input_height=299, input_width=299, input_mean=0, input_std=255):
    input_name = "file_reader"
    output_name = "normalized"
    file_reader = tf.read_file(file_name, input_name)
    if file_name.endswith(".png"):
        image_reader = tf.image.decode_png(file_reader, channels = 3,
                                           name='png_reader')
    elif file_name.endswith(".gif"):
        image_reader = tf.squeeze(tf.image.decode_gif(file_reader,
                                                      name='gif_reader'))
    elif file_name.endswith(".bmp"):
        image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
    else:
        image_reader = tf.image.decode_jpeg(file_reader, channels = 3,
                                            name='jpeg_reader')
    float_caster = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0)
    resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    sess = tf.compat.v1.Session()
    result = sess.run(normalized)
    return result


def fill_prediction_table(path_file_Final, customer_type, customer_name, customer_universe):
    table_name = "predict_" + customer_type + '_' + customer_name + '_' + customer_universe
    db.create_prediction_table(table_name)
    workbook = xlrd.open_workbook(path_file_Final)
    sheet = workbook.sheet_by_name(workbook.sheet_names()[0])
    nRows = sheet.nrows

    db.delete_predict_table(table_name)
    for i in range(1, nRows):
        row_values = sheet.row_values(i)
        if row_values[12] != "":
            principal_categorie = str((row_values[12]))
        else:
            if row_values[10] != "":
                principal_categorie = str((row_values[10]))
            else:
                principal_categorie = str((row_values[8]))
        db.add_prediction_table(table_name, row_values, principal_categorie)


def classification_similars(customer_name, customer_type, project_name):
    api.apipost("classification_similars", customer_name, customer_type, project_name)


def process_customer_stream_from_json(json_path, customer_name, customer_type, project_name):
    json_path = delta_retrieve_json(customer_name, customer_type, project_name)
    request_post = api.apipost('retrieve_images_json', customer_name, customer_type, project_name, json_path)
    response_text = json.loads(request_post.text)
    response = response_text['response']
    deleted_image = response_text['deleted_images']
    if int(response) != 0:
        path_out = OUTPUT_PATH + customer_type + '/' + customer_name + '/images/' + project_name + '/'
        try:
            import os
            folders = next(os.walk(path_out))[1]
        except Exception as e:
            folders = []
            logger.error("Folders_training_similars %s" % e)
        if len(folders) > 0:
            try:
                projects = db.get_training_detalis(STATUS_PROJECT_TABLE, customer_name, customer_type, project_name,
                                                   'classification')
                train_details = json.loads(projects[0])
            except :
                logger.info("First time training for project %s client %s with type %s" % (project_name, customer_name, customer_type))
                train_details = {}
            if set(train_details.get('categories', [])) != set(deleted_image.keys()):
                    logger.info("Categories Not the same, repeating classification process")
                    classification_similars(customer_name, customer_type, project_name)

        generate_similarity_vector(customer_name, customer_type, deleted_image, project_name)


def process_customer_stream_cms(json_path, customer_name, customer_type, project_name):
    streams_path = STREAMS_PATH + customer_type + '/' + customer_name + '/similars/' + project_name + '/'+ \
                   'cms_json_file.json'
    streams_paths3 = STREAMS_S3 + customer_type + '/' + customer_name + '/similars/' + project_name + '/'
    if '://' in json_path:
        download(json_path, streams_path)
    else:
        streams_path = json_path
    upload_file_into_s3(streams_path, streams_paths3)
    # TODO appel fonction process customer from stream après traitement de fichier json des produits
    # process_customer_stream_from_json(json_path, customer_name, customer_type,project_name)


def get_redirect_url(url):
    try:
        image = requests.get(url)
        if image.url == url:
            return is_url_image(url)
        else:
            return is_url_image(image.url)
    except:
        return False


def detection_error_training(excel_path, customer_name, customer_type, customer_universe):
    api.apipost('training_text_detection', customer_name, customer_type, None, excel_path, customer_universe)


def equilibrate_customer_samples_count(excel_path, customer_name, customer_type, customer_universe):
    api.apipost('correction_training', customer_name, customer_type, None, excel_path, customer_universe)


def shopify_training(customer_name, customer_type, url_shop, project, INPUT_SESSION_UUID):
    api.apipost('shopify_training', customer_name, customer_type, None, None, project, url_shop, INPUT_SESSION_UUID)


def generate_similarity_vector(customer_name="vector", customer_type='vector', deleted_image={}, project_name=None):
    vector_response = api.apipost('training_similars', customer_name, customer_type, project_name, deleted_image, None)
    response_text = json.loads(vector_response.text)
    response_from_parquet = response_text['response']
    if response_from_parquet == 2:
        return True
    return False


def text_training_retrieve_json(excel_path, customer_name, customer_type, customer_universe, project_name):
    send_email_when_training_started(customer_name, project_name, 'classification', 'Training started')
    if project_name:
        operation = 'training_classification'
    else:
        operation = 'training_text_detection'

    api.apipost(operation, customer_name, customer_type, project_name, excel_path, customer_universe)

