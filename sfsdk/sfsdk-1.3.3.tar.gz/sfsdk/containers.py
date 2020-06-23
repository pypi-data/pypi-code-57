# This file is part of the SecureFlag Platform.
# Copyright (c) 2020 SecureFlag Limited.

# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.

# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from sfsdk import log, utils
import docker
import time
import tempfile
import tarfile
import os
import json
import io
import shutil
import sys
import boto3
import base64
import jinja2

dockerc = None

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'dockerfiles'
        )
    )
)

def load():

    global dockerc

    dockerc = docker.from_env()

    try:
        dockerc.info()
    except Exception as e:
        log.debug(str(e))
        raise log.FatalMsg("Error, can't communicate with the Docker daemon")

def image_exists(image_name):

    try:
        dockerc.images.get(image_name)
    except docker.errors.ImageNotFound as _:
        return False
    else:
        return True

def pull_image(registry_url):

    try:
        return dockerc.api.pull(
                registry_url,
                stream = True,
                decode = True
            )
    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)

def tag_image(image_name, tag):

    dockerc.images.get(image_name).tag(tag)

def run_instance(conf):

    global containers

    conf['detach'] = True
    try:
        dockerc.containers.run(**conf)
    except docker.errors.ImageNotFound as e:
        raise log.FatalMsg("Image has not been built yet, run 'sfsdk img-build %s' and retry" % conf['image'])
    except docker.errors.ContainerError as e:
        raise log.FatalMsg('A container named %s already exists' % conf['name'])
    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)

def containers_list():

    try:
         return [ c.name for c in dockerc.containers.list() ]
    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)

def container_exists(container_name):

    try:
        dockerc.containers.get(container_name)
    except docker.errors.NotFound as e:
        return False
    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)

    return True


def container_status(container_name):

    try:
        return dockerc.containers.get(container_name).status
    except docker.errors.NotFound as e:
        pass
    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)

def container_remove(container_name):

    try:
        dockerc.containers.get(container_name).remove(force=True)
    except docker.errors.NotFound as e:
        return False
    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)

    return True

def wait_until_running(container_name, delay = 1, count = 10):

    for i in range(count):

        try:
            container = dockerc.containers.get(container_name)
        except docker.errors.NotFound as e:
            pass
        except docker.errors.APIError as e:
            raise log.FatalMsg(e.explanation)

        if container.status == 'running':
            return

        time.sleep(1)

    raise log.FatalMsg("Container failed running in %d seconds" % (delay*count))

def upload_paths(container_name, paths, dest):

    try:

        container = dockerc.containers.get(container_name)
        tar_file = tar_from_paths(paths)
        container.put_archive(dest, tar_file.read())

    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)

def exec_on_container(container_name, cmd, tty = True, stream = False):

    try:
        container = dockerc.containers.get(container_name)

        if not stream:

            exit_code, output = container.exec_run(
                    cmd,
                    stdout = True,
                    tty = tty
                    )

            return exit_code, output.decode("utf-8").rstrip("\r\n")

        else:

            result = container.exec_run(
                    cmd,
                    stdout = True,
                    tty = tty,
                    stream = True
                    )
            for line in result.output:
                log.block(line.decode("utf-8"))

    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)


def watch_container(container_name, watch_folder = '/home/sf', status_json = '/tmp/sfsdkwatch.json'):

    try:
        container = dockerc.containers.get(container_name)

        if container.exec_run(
                "ls /tmp/sfsdkwatch.py"
                ).exit_code != 0:
            upload_paths(container_name,
                    [ os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "sfsdkwatch.py"
                    ) ], '/tmp')

        _, pgrep_output = container.exec_run(
                "pgrep -f '/usr/bin/python2 /tmp/sfsdkwatch.py'",
                stdout = True
                )

        if not pgrep_output:
            if container.exec_run(
                    "/usr/bin/python2 -c 'import watchdog'"
                    ).exit_code != 0:
                if container.exec_run("sh -c \
                        'apt-get update && \
                        apt-get install -y python-watchdog'",
                        environment = [ "DEBIAN_FRONTEND=noninteractive" ]).exit_code != 0:
                    raise log.FatalMsg("Error installing python-watchdog, check if internet is enabled")

            container.exec_run(
                "/usr/bin/python2 /tmp/sfsdkwatch.py '%s' '%s'" % (watch_folder, status_json), 
                detach = True
                )
    except docker.errors.NotFound:
        raise log.FatalMsg("Container is not running, start it with 'sfsdk run <image-name>' and retry")
    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)

def get_watched_paths(container_name):

    try:
        container = dockerc.containers.get(container_name)

        if container.exec_run(
                "ls /tmp/sfsdkwatch.json"
                ).exit_code != 0:
            return {}
        
        watch_data = container.exec_run("cat /tmp/sfsdkwatch.json").output
        
        if not watch_data:
            return {}
        else:
            return json.loads(watch_data)
    except ValueError as e:
        raise log.FatalMsg('Error reading the modified files')
    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)

def tar_from_paths(paths):
    f = tempfile.NamedTemporaryFile()
    t = tarfile.open(mode='w', fileobj=f)

    for path in paths:
        abs_path = os.path.abspath(path)
        t.add(abs_path, arcname=os.path.basename(path), recursive=True)

    t.close()
    f.seek(0)
    return f

def tar_from_bytes(data):
    f = io.BytesIO()

    for chunk in data:
        f.write(chunk)

    f.seek(0)

    return tarfile.open(fileobj=f)

def is_empty_folder(snapshot_folder):

    if not os.path.isdir(snapshot_folder):
        os.makedirs(snapshot_folder)
        
    if [ x for x in os.listdir(snapshot_folder) if x != '.keep' ]:
        return False

    return True

def generate_dockerfile(build_folder, from_img, modified_paths = []):

    with open(
            os.path.join(build_folder, 'Dockerfile'),
            'w'
            ) as dockerfile:

        dockerfile.write(
            jinja_env.get_template('Dockerfile.%s.tpl' % from_img).render(
                paths = modified_paths,
            )
        )

def append_to_dockerfile(build_folder, modified_paths = []):

    with open(
            os.path.join(build_folder, 'Dockerfile'),
            'a'
            ) as dockerfile:

        dockerfile.write(
            jinja_env.get_template('file-copy.tpl').render(
                paths = modified_paths,
            )
        )

def create_snapshot(snapshot_folder, from_image_name, snapshot_tmp, modified_paths):

    exercise_src = os.path.join(snapshot_tmp, 'sf/exercise/app')
    exercise_dest = os.path.join(snapshot_folder, 'app')

    if os.path.exists(exercise_src):
        utils.merge_tree(
            exercise_src, 
            exercise_dest,
            preserve_symlinks = True,
            )
    else:
        os.makedirs(exercise_dest, exist_ok = True)

    dest_home = os.path.join(snapshot_folder, 'fs/home/sf')
    
    utils.merge_tree(
        os.path.join(snapshot_tmp, 'sf'), 
        dest_home,
        preserve_symlinks = True,
    )
    
    # Exercise has been copied already 
    exercise_in_root = os.path.join(snapshot_folder, 'fs/home/sf/exercise/app')
    if os.path.exists(exercise_in_root):
        shutil.rmtree(exercise_in_root)

    append_to_dockerfile(
            build_folder = snapshot_folder, 
            modified_paths = modified_paths)

def extract_modified_from_tar(tar_file, modified_paths):

    snapshot_tmp = tempfile.mkdtemp(prefix='sdk.snapshot.')

    members_to_extract = []
    for m in tar_file.getmembers():
        file_path = os.path.join('/home', m.name)

        # Standardize output using an ending / if folders.
        if m.isdir():
            file_path = os.path.join(file_path, '')

        # Extract everything starts with modified_paths
        if any((mp for mp in modified_paths + [ '/home/sf/exercise' ] if file_path.startswith(mp) and not m in [n.name for n in members_to_extract])):
            members_to_extract.append(m)

    tar_file.extractall(path=snapshot_tmp, members=members_to_extract)

    return snapshot_tmp

def save_container_snapshot(container_name, snapshot_folder, from_image_name, modified_paths):

    try:
        container = dockerc.containers.get(container_name)
    except docker.errors.NotFound as e:
        raise log.FatalMsg("Can't find container %s" % container_name)
    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)

    try:
        tar_data, _ = container.get_archive('/home/sf')
    except Exception as e:
        log.debug(str(e))
        raise log.FatalMsg("Error pulling data from container")

    tar_file = tar_from_bytes(tar_data)

    try:
        snapshot_tmp = extract_modified_from_tar(
            tar_file, 
            modified_paths
        )
    except Exception as e:
        log.debug(str(e))
        raise log.FatalMsg("Error extracting data from container")

    create_snapshot(snapshot_folder, from_image_name, snapshot_tmp, modified_paths)

def build_image(exercise_path, image_name):

    try:
        return dockerc.api.build(
                path=exercise_path,
                tag=image_name,
                decode=True
                )
    except docker.errors.APIError as e:
        log.warn("Error building %s from %s" % (image_name, exercise_path))
        raise log.FatalMsg(e.explanation)

def tag_and_push_image(aws_creds, image_name, ecr_repo_name, aws_arn):

    _docker_login_with_ecr(aws_creds, aws_arn)

    dockerc.images.get(image_name).tag(ecr_repo_name)

    return dockerc.images.push(ecr_repo_name, stream=True, decode=True)

def image_remove(image_name):

    try:
        dockerc.images.remove(image_name, force=True)
    except docker.errors.NotFound as e:
        return False
    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)

    return True

def _docker_login_with_ecr(aws_creds, aws_arn):

    region_name = aws_arn.split(":")[5].replace('hub-uploads-', '')

    ecr_client = boto3.client(
        'ecr',
        aws_access_key_id=aws_creds['accessKeyId'],
        aws_secret_access_key=aws_creds['secretAccessKey'],
        aws_session_token=aws_creds['sessionToken'],
        region_name=region_name
    )

    ecr_credentials = (
        ecr_client
        .get_authorization_token()
        ['authorizationData'][0])

    ecr_username = 'AWS'

    ecr_password = (
        base64.b64decode(ecr_credentials['authorizationToken'])
        .replace(b'AWS:', b'')
        .decode('utf-8'))

    ecr_url = ecr_credentials['proxyEndpoint']

    # get Docker to login/authenticate with ECR
    dockerc.login(
        username=ecr_username, 
        password=ecr_password, 
        registry=ecr_url,
        reauth=True,
        dockercfg_path='/dev/null' # Hack to ignore the real config
    )

    return ecr_url
