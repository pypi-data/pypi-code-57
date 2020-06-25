import boto3
import os
import io
from io import StringIO
from multiprocessing.connection import wait
from multiprocessing import Process, Pipe
import pandas as pd
from pandas import DataFrame
from tqdm import tqdm
import boto3
import ast
import tempfile
import pickle
from . import infin_ast
from datetime import datetime
import time
from mlflow import start_run, end_run, log_metric, log_param, log_artifacts, set_experiment

#import astpretty

verbose = False

def list_one_dir(client, bucket, prefix_in, recurse, array_of_files):
    print('Listing ' + prefix_in)
    paginator = client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix_in, Delimiter="/")
    for page in page_iterator:

        # print('Files:')
        contents = page.get('Contents')
        if (contents != None):
            # print('   ' + str(contents))
            count = 0;
            for one_content in contents:
                object_name = one_content['Key']
                full_object_name = object_name
                # print(full_object_name)
                array_of_files.append(full_object_name)
                count += 1
            if (count > 0):
                print(str(count) + " files in " + prefix_in)

        # print('Directories:')
        common_prefixes = page.get('CommonPrefixes')
        if (common_prefixes != None):
            for prefix in common_prefixes:
                this_prefix = str(prefix['Prefix'])
                # print('   ' + this_prefix)
                if (bool(recurse) and this_prefix != None ):
                    list_one_dir(client, bucket, this_prefix, recurse, array_of_files)

def num_threads():
    return 8

def info(msg):
    print(__name__ + '[' + str(os.getpid()) + ']' + msg)

def s3downloader(write_pipe, read_pipe, endpoint):
    # info('s3downloader: started. endpoint=' + endpoint)
    session = boto3.Session(profile_name='infinstor')
    client = session.client('s3', endpoint_url=endpoint)
    while (True):
        op = read_pipe.recv()
        if (op == 'download'):
            bucketname = read_pipe.recv()
            filename = read_pipe.recv()
            #info('s3downloader: downloading ' + filename + ' from ' + bucketname)
            obj = client.get_object(Bucket=bucketname, Key=filename)
            strbody = obj['Body']
            datetime = obj['LastModified']
            bts = strbody.read()
            key = datetime.strftime('%Y-%m-%d %H:%M:%S') + ' ' + bucketname + '/' + filename
            write_pipe.send(key)
            write_pipe.send(bts)
        elif (op == 'quit'):
            break

def load_one_csv_from_bytearray(bts):
    s = str(bts, 'utf-8')
    sio = StringIO(s)
    return pd.read_csv(sio)

# returns a pandas DataFrame with index 'YY-MM-dd HH:MM:SS bucketname/filename'
# and one column named RawBytes that contains the raw bytes from the object
def download_objects(endpoint, bucketname, array_of_files, is_csv):
    start_run()
    log_param("object_count", len(array_of_files))

    filebytes = []
    filekeys = []
    toChildProcess = []
    fromChildProcess = []
    processes = []
    available_processes = []
    for i in range(num_threads()):
        r1, w1 = Pipe()
        fromChildProcess.append(r1)
        r2, w2 = Pipe()
        toChildProcess.append(w2) 
        p = Process(target=s3downloader, args=(w1, r2, endpoint, ))
        p.start()
        processes.append(p)
        available_processes.append(True)
        w1.close()
        r2.close()

    with tqdm(total=len(array_of_files)) as pbar:
        read_pipes = []
        next_file = 0
        step = 0
        while (True):
            if (next_file == len(array_of_files)):
                break
            for i in range(num_threads()):
                if (available_processes[i] == True):
                    available_processes[i] = False
                    toChildProcess[i].send('download')
                    toChildProcess[i].send(bucketname)
                    toChildProcess[i].send(array_of_files[next_file])
                    read_pipes.append(fromChildProcess[i])
                    next_file += 1
                    if (next_file == len(array_of_files)):
                        break
                    pbar.update(1)
                    if ((next_file % 10) == 0):
                        log_metric("downloaded", next_file, step=step)
                        step += 1

            if (len(read_pipes) > 0):
                for read_pipe in wait(read_pipes):
                    try:
                        key = read_pipe.recv()
                        bts = read_pipe.recv()
                        for i in range(num_threads()):
                            if (fromChildProcess[i] == read_pipe):
                                available_processes[i] = True
                                break
                        filekeys.append(key)
                        filebytes.append(bts)
                        break
                    except EOFError:
                        info('eof received')
                    finally:
                        read_pipes.remove(read_pipe)

        while (len(read_pipes) > 0):
            for read_pipe in wait(read_pipes):
                try:
                    key = read_pipe.recv()
                    bts = read_pipe.recv()
                    for i in range(num_threads()):
                        if (fromChildProcess[i] == read_pipe):
                            available_processes[i] = True
                            break
                    filekeys.append(key)
                    filebytes.append(bts)
                    continue
                except EOFError:
                    info('eof received')
                finally:
                    read_pipes.remove(read_pipe)
        print('finished reading all files')

    for i in range(num_threads()):
        toChildProcess[i].send('quit')
    for i in range(num_threads()):
        processes[i].join()
    if (is_csv == True):
        rv = pd.concat(map(load_one_csv_from_bytearray, filebytes))
    else:
        data = {'RawBytes': filebytes}
        rv = DataFrame(data, index=filekeys)
    log_metric("downloaded", next_file, step=step)
    end_run()
    return rv

class FuncLister(ast.NodeVisitor):
    def __init__(self, glbs):
        self.glbs = glbs;

    def visit_FunctionDef(self, node):
        self.glbs[node.name] = "'" + node.name + "'";
        # print(node.name)
        self.generic_visit(node)

def actually_run_transformation(client, endpoint, cache_path, is_pandas_df, bucketname,\
        prefix_in, xformname):
    xform_obj = client.get_object(Bucket='infinstor-pseudo-bucket', Key='transforms/' + xformname)
    strbody = xform_obj['Body']
    bts = strbody.read()
    s = str(bts, 'utf-8')
    # print(s)

    array_of_files = []
    list_one_dir(client, bucketname, prefix_in, True, array_of_files)
    print('Total Number Of Objects: ' + str(len(array_of_files)))
    objects = download_objects(endpoint, bucketname, array_of_files, False)

    transformAst = infin_ast.extract_transform(src_str=s)
    # XXX we should use the following statement to figure out what
    # kind of an object the infin_transform function returns
    # infin_ast.add_type_statements(transformAst)
    transformSrc = infin_ast.get_source(transformAst)

    if (verbose == True):
        print('transformSrc=' + transformSrc);

    transformSrc = transformSrc + "\ninfin_transform(objects)\n"

    tree = ast.parse(transformSrc)
    # Add all functions in xformcode to the globals dictionary
    glb = {}
    fl = FuncLister(glb)
    fl.visit(tree)
    glb['objects'] = objects;
    #astpretty.pprint(tree)
    compliedcode = compile(tree, "<string>", "exec")
    exec(compliedcode, glb)
    # save result of transformation in cache
    if (is_pandas_df == True):
        fd, tmpf_name = tempfile.mkstemp(suffix='.pkl')
        os.close(fd)
        objects.to_pickle(tmpf_name)
        client.put_object(Body=open(tmpf_name, 'rb'), Bucket='infinstor-pseudo-bucket',\
                Key=cache_path)
        os.remove(tmpf_name)
    else:
        print('saving tf.data.Dataset unimplemented')
    return objects

def read_raw_and_xform_to_pd(time_spec, service_name, bucketname, prefix_in, xformname):
    endpoint = "https://" + time_spec + ".s3proxy." + service_name + ".com:443/";
    print('endpoint=' + endpoint)
    session = boto3.Session(profile_name='infinstor')
    client = session.client('s3', endpoint_url=endpoint)

    # check if we can download a cached version
    cache_path = 'cache/' + xformname + '/' + time_spec + '/'\
            + bucketname + '/' + prefix_in + 'pd.DataFrame'
    print('Looking up cache entry ' + cache_path)
    try:
        s3obj = client.get_object(Bucket='infinstor-pseudo-bucket', Key=cache_path)
        print('cache hit for ' + cache_path)
        body_bytes = s3obj['Body'].read()
        cached_obj = pickle.loads(body_bytes)
    except client.exceptions.NoSuchKey:
        print('cache miss for ' + cache_path)
        cached_obj = actually_run_transformation(client, endpoint, cache_path, True,\
                bucketname, prefix_in, xformname)
    finally:
        return cached_obj

def read_raw_and_xform_to_ds(time_spec, service_name, bucketname, prefix_in, xformname):
    endpoint = "https://" + time_spec + ".s3proxy." + service_name + ".com:443/";
    print('endpoint=' + endpoint)
    session = boto3.Session(profile_name='infinstor')
    client = session.client('s3', endpoint_url=endpoint)

    # check if we can download a cached version
    cache_path = 'cache/' + xformname + '/' + time_spec + '/'\
            + bucketname + '/' + prefix_in + 'tf.data.Dataset'
    print('Looking up cache entry ' + cache_path)
    try:
        cached_obj = client.get_object(Bucket='infinstor-pseudo-bucket', Key=cache_path)
        print('cache hit for ' + cache_path)
        # XXX read and deserialize here
    except client.exceptions.NoSuchKey:
        print('cache miss for ' + cache_path)
        cached_obj = actually_run_transformation(client, endpoint, cache_path, False,\
                bucketname, prefix_in, xformname)
    finally:
        return cached_obj

def run_xform_periodically(seconds, time_spec, service_name, bucketname, prefix_in, xformname):
    endpoint = "https://" + time_spec + ".s3proxy." + service_name + ".com:443/";
    print('endpoint=' + endpoint)

def run_xform_periodically(seconds, service_name, bucketname, prefix_in, xformname):
    while (True):
        start_time = datetime.utcnow()
        time.sleep(seconds)
        end_time = datetime.utcnow()
        time_spec = 'tm' + start_time.strftime("%Y%m%d%H%M%S")\
                + '-tm' + end_time.strftime("%Y%m%d%H%M%S")
        read_raw_and_xform_to_pd(time_spec, service_name, bucketname, prefix_in, xformname)
