#!/usr/bin/env python3

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


from sfsdk import containers, log, web, remote
from sfsdk import imgsettings
from sfsdk import exrsettings
from sfsdk import authsettings
from sfsdk import techsettings
from sfsdk import stacksettings
from sfsdk import kbsettings
from sfsdk import frameworksettings
import re
import os
import json
import argparse
import sys
import time
import shutil
import pty
import tempfile
import shlex
import tempfile
import random
import simplejson
import subprocess

base_dir = os.path.expanduser('~/sf')

def img_snapshot(name, new_name, force):

    image_settings = imgsettings.settings.get('images', {}).get(name)

    if not new_name:
        new_name = imgsettings.get_snapshot_name(name)

    if not image_settings:
        raise log.FatalMsg("Image %s does not exist, run 'sfsdk img-add' to add it" % name)

    if new_name in imgsettings.settings.get('images', {}).keys():
        raise log.FatalMsg('Image %s already exists' % new_name)

    current_container_conf = imgsettings.get_container_conf(name)

    if containers.container_status(current_container_conf['name']) != 'running':
        raise log.FatalMsg("""Image is not running, consider running 'sfsdk img-watch %s' before running img-snapshot again.""" % (name))

    additional_paths = []

    paths_file = os.path.join(image_settings['build_dir'], '.sfsdk-watch.txt')

    additional_paths = []
    try:
        with open(paths_file, 'r') as stream:
            additional_paths = [ l for l in stream.read().split('\n') if l ]
    except OSError:
        log.debug("Error reading %s" % (paths_file))
        log.warn("Can't find result from img-watch, consider running 'sfsdk img-watch %s' before running img-snapshot again." % (name))

    monitored_paths = techsettings.technologies[image_settings['base_img']].get('default_paths', [])

    # Add additional paths without duplicates
    for additional_path in additional_paths:
        if not (additional_path in monitored_paths or additional_path + '/' in monitored_paths):
            monitored_paths.append(additional_path)

    container_settings = { v['name']:v['default'] for v in imgsettings.get_settings(new_name) }

    imgsettings.add_image_settings(
            new_name,
            base_img = image_settings['base_img'],
            build_dir = None,
            from_dir = image_settings['build_dir'],
            container_settings = container_settings
            )

    new_img_settings = imgsettings.settings.get('images', {}).get(new_name)
    new_build_dir = new_img_settings['build_dir']

    containers.save_container_snapshot(
            container_name = current_container_conf['name'],
            snapshot_folder = new_build_dir,
            from_image_name = image_settings['base_img'],
            modified_paths = monitored_paths
        )

    if monitored_paths:
        log.block("""The following paths have been exported from the running container and applied over the build folder.:

%s

The new project image has been saved as %s.
""" % (
            '\n'.join(monitored_paths),
            new_name
            )
        )

def img_techs(source):

    authsettings.set_source(source)

    source_type, management_url, username, password = authsettings.load_or_ask_for_creds()

    if source_type == 'deployment':
        remote.login_to_deployment(username, password, management_url)
        
        try:
            remote_technologies = remote.get_technologies_via_deployment()
        except simplejson.JSONDecodeError:
            raise log.FatalMsg("Error getting the technologies, is the source a deployment?")
    else:
        remote.login_to_hub(username, password, management_url)
        try:
            remote_technologies = remote.get_technologies_via_hub()
        except simplejson.JSONDecodeError:
            raise log.FatalMsg("Error getting the technologies via the Hub, are you a developer?")

    techsettings.prepare_technologies(remote_technologies)
    techsettings.save()

    log.header("Technologies has been updated:")
    log.block('\n'.join(techsettings.technologies), end='\n\n')

def img_add(name, from_img, build_dir, from_dir, app_dir):

    # Let's stick to the docker image name limitations
    if not re.match('[a-z0-9][a-z0-9_.-]*$', name):
        raise log.FatalMsg('Image name is not valid')

    if not from_img in techsettings.technologies.keys():
        raise log.FatalMsg(
            "Base technology does not exist in %s, run 'sfsdk img-techs' to update the list." % (techsettings.technologies_path)
        )

    container_settings = { v['name']:v['default'] for v in imgsettings.get_settings(name) }

    imgsettings.add_image_settings(
            name,
            base_img = from_img,
            build_dir = build_dir,
            from_dir = from_dir,
            app_dir = app_dir,
            container_settings = container_settings
            )

    image_settings = imgsettings.settings.get('images', {}).get(name)

    log.header("""New image %s has been added""" % name)
    log.block("""
    This new image is based on %s
    The build folder is %s
    """ % (
        from_img,
        image_settings['build_dir'],
        )
    )

def img_build(name, skip_base_img, source):

    image_settings = imgsettings.settings.get('images', {}).get(name)

    if not image_settings:
        raise log.FatalMsg("Image %s does not exist, run 'sfsdk img-add --from-img <base image> %s' to add it" % (name, name))

    base_img = image_settings['base_img']

    if not skip_base_img and not containers.image_exists(base_img):

        base_tech_settings = techsettings.technologies.get(base_img)
        if base_tech_settings == None:
            raise log.FatalMsg("Error, can't find technology image %s on %s technologies.yml" % (base_img, source))

        base_image_url = base_tech_settings.get('imageUrl')
        if not base_image_url:
            raise log.FatalMsg("Error, can't find technology image %s.imageUrl is set on %s technologies.yml" % (base_img, source))

        log.block('Pulling technology image %s from %s' % (base_img, base_image_url), end='\n')

        pulled = True

        try:
            pull_stream = containers.pull_image(
                base_image_url
            )
        except log.FatalMsg as e:
            raise log.FatalMsg("Error pulling technology: %s" % e)

        for line in pull_stream:

            if 'error' in line:
                log.warn('Error pulling technology image: %s' % line['error'])
                pulled = False
            elif 'status' in line and line['status'] == 'Downloading':
                log.block('Pulling the image layer %s %s...' % (line['id'], line['progress'].split(' ')[-1]), end='\t\t\r')

            sys.stdout.flush()

        containers.tag_image(base_image_url, base_img)

        if pulled:
            log.header("Technology image has been pulled and tagged as %s"  % (base_img))
        else:
            raise log.FatalMsg("Error pulling technology image, try manually with running 'docker pull %s' and 'docker tag %s %s'" % (base_image_url, base_image_url, base_img))

    log.block('Building exercise image %s...' % name, end='\n')
    build_generator = containers.build_image(image_settings['build_dir'], name)

    built = False

    for line in build_generator:
        if 'stream' in line:
            output = line['stream'].strip('\n')
            log.block(output, end='\n', prefix='')

            if output.startswith('Successfully built'):
                built = True

    if built:
        log.header("Build complete")
    else:
        raise log.FatalMsg("The build of the image failed. Debug the build manually running\ndocker build -t %s %s" % (name, image_settings['build_dir']))

def img_shell(name, command):

    image_settings = imgsettings.settings.get('images', {}).get(name)

    if not image_settings:
        raise log.FatalMsg("Image %s does not exist, run 'sfsdk img-add' to add it" % name)

    container_settings = imgsettings.get_container_conf(name)
    container_name = container_settings['name']

    os.execvp("docker", [ "docker", "exec", "-it", container_name ] + shlex.split(command))

def img_run(name, force, exercise_name = None):

    image_settings = imgsettings.settings.get('images', {}).get(name)

    if not image_settings:
        raise log.FatalMsg("Image %s does not exist, run 'sfsdk img-add' to add it" % name)

    container_settings = imgsettings.get_container_conf(name)
    container_name = container_settings['name']

    container_exists = containers.container_exists(container_name)
    container_status = containers.container_status(container_name)

    if container_exists and not force:
        if container_status == 'running':
            raise log.FatalMsg("Container %s is already running, you can stop and rebuild it." % container_name)
        else:
            raise log.FatalMsg("Container %s is not running, run 'sfsdk img-run %s --force' to delete and re-run" % (container_name, name))

    if exercise_name:
        container_settings['environment']['EXERCISE'] = exrsettings.get_exercise_environment_variable(exercise_name)

    if container_status != None:
        containers.container_remove(container_name)

    containers.run_instance(container_settings)

    log.header("Container of image %s has been started" % name, end='\n\n')

    data = [
            [ "Container name:", container_name ],
            [ "RDP port:", '127.0.0.1:%s' % image_settings['container']['external_rdp_port'] ],
            [ "RDP credentials:", 'sf:' + image_settings['container']['rdp_password']  ],
            [ "Application port:", '127.0.0.1:%s' % image_settings['container']['external_http_port'] ]
        ]

    log.tablify(data)


def img_stop(names):

    image_names = imgsettings.resolve_images(names)

    for name in image_names:

        image_settings = imgsettings.settings.get('images', {}).get(name)

        if not image_settings:
            raise log.FatalMsg("Image %s does not exist, run 'sfsdk img-add' to add it" % name)

        container_settings = imgsettings.get_container_conf(name)
        container_name = container_settings['name']

        container_was_running = (containers.container_status(container_name) != 'running')

        if not container_was_running:

            if not containers.container_remove(container_name):
                log.warn("Container %s is not running" % container_name)
            else:
                log.header("Container %s has been stopped" % container_name, prefix='', end='\n')

def img_watch(name, folder, count):

    image_settings = imgsettings.settings.get('images', {}).get(name)

    if not image_settings:
        raise log.FatalMsg("Image %s does not exist, run 'sfsdk img-add' to add it" % name)

    output_file = os.path.join(image_settings['build_dir'], '.sfsdk-watch.txt')
    
    container_settings = imgsettings.get_container_conf(name)

    container_name = container_settings['name']
    log.debug("Writing img-watch output to %s" % output_file)
    log.header("Please wait, preparing %s to run img-watch.." % (container_name))

    containers.watch_container(container_name, watch_folder = folder)
    last_json_output = []

    try:

        i = 0
        found = 0

        while True:

            if count == 0:
                pass
            elif i > count:
                break
            else:
                i+=1

            exit_code, output = containers.exec_on_container(
                    container_name,
                    'cat /tmp/sfsdkwatch.json',
                    )

            if exit_code == 0 and output:

                found += 1
                if found == 1:
                    log.header("Started watching changes in %s folder.." % (folder))


                try:
                    json_output = json.loads(output)
                except json.JSONDecodeError as e:
                    continue

                if sorted(json_output) != sorted(last_json_output):
                    last_json_output = json_output[:]

                    log.header("%s Changed files and folders:" % (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

                    directory_list = '\n'.join(last_json_output)
                    log.block(directory_list + '\n\n')

                    with open(output_file, 'w+') as stream:
                        stream.write(directory_list)

            time.sleep(1)

    except KeyboardInterrupt:
        pass

def img_ls():

    data = [ ]

    for image_name, image_data in imgsettings.settings['images'].items():

        img_running = (containers.container_status(image_data['container']['container_name']) == 'running')

        data.append([
            image_name,
            'Yes' if img_running else 'No',
            image_data['container']['container_name'] if img_running else '',
            image_data['container']['external_rdp_port'] if img_running else '',
            'sf:' + image_data['container']['rdp_password'] if img_running else '',
            image_data['container']['external_http_port'] if img_running else '',
            ]
        )

    log.tablify(
            data,
            header = [
                'Name',
                'Running',
                'Container name',
                'RDP port',
                'RDP creds',
                'Application port'
            ]
        )

def img_rm(names, force):

    image_names = imgsettings.resolve_images(names)

    for name in image_names:

        image_settings = imgsettings.settings.get('images', {}).get(name)

        if not image_settings:
            raise log.FatalMsg("Image %s does not exist, run 'sfsdk img-add' to add it" % name)

        try:
            imgsettings.remove_image(name, force)
        except log.FatalMsg as e:
            log.warn(str(e))
        else:
            log.header("Image %s data has been removed" % name)


def exercise_edit(source):

    authsettings.set_source(source)

    source_type, management_url, username, password = authsettings.load_or_ask_for_creds()

    if source_type == 'deployment':
        remote.login_to_deployment(username, password, management_url)
        web.get_remote_technologies_func = remote.get_technologies_via_deployment
        web.get_remote_technology_func = remote.get_technology_via_deployment_by_uuid
        web.get_remote_vulnerabilities_func = remote.get_vulnerabilities_via_deployment
        web.get_remote_vulnerability_func = remote.get_vulnerability_via_deployment_by_uuid
        web.get_remote_frameworks_func = remote.get_frameworks_via_deployment
    else:
        remote.login_to_hub(username, password, management_url)
        web.get_remote_technologies_func = remote.get_technologies_via_hub
        web.get_remote_technology_func = remote.get_technology_via_hub_by_uuid
        web.get_remote_vulnerabilities_func = remote.get_vulnerabilities_via_hub
        web.get_remote_vulnerability_func = remote.get_vulnerability_via_hub_by_uuid
        web.get_remote_frameworks_func = remote.get_frameworks_via_hub

    web.run_editor()


def config(source):

    log.warn("""Warning: this saves your credentials in %s in an insecure way.
Skip this (press Ctrl-C) to be prompted every time the authentication is required.""" % authsettings.settings_path)

    authsettings.set_source(source)

    source_type, management_url, username, password = authsettings.load_or_ask_for_creds(
            doing_config=True
        )

    if not source in authsettings.settings['sources']:
        authsettings.settings['sources'][source] = {}

    authsettings.settings['sources'][source]['type'] = source_type
    authsettings.settings['sources'][source]['username'] = username
    authsettings.settings['sources'][source]['password'] = password

    if source_type == 'deployment':
        authsettings.settings['sources'][source]['url'] = management_url

    authsettings.save_to_file()

def publish(image_name, exercise_name, source):

    authsettings.set_source(source)

    source_type, management_url, username, password = authsettings.load_or_ask_for_creds()

    if source_type == 'deployment':
        remote.login_to_deployment(username, password, management_url)
        aws_creds = remote.get_s3_creds_via_deployment()
        aws_arn = remote.get_arn_via_deployment()
        get_remote_vulnerability_func = remote.get_vulnerability_via_deployment_by_uuid
        get_remote_technology_func = remote.get_technology_via_deployment_by_uuid
    else:
        remote.login_to_hub(username, password, management_url)
        aws_creds = remote.get_s3_creds_via_hub()
        aws_arn = remote.get_arn_via_hub()
        get_remote_vulnerability_func = remote.get_vulnerability_via_hub_by_uuid
        get_remote_technology_func = remote.get_technology_via_hub_by_uuid

    tmp_dir_path = tempfile.mkdtemp(prefix='sfsdk-publish-archive-dir-')

    tmp_archive = tempfile.NamedTemporaryFile(
            prefix = 'sfsdk-publish-archive',
            )
    tmp_archive.close()

    log.debug('Building publish data in {tmp_dir_path} zipped to {tmp_archive.name}')

    shutil.copytree(
        imgsettings.settings['images'][image_name]['build_dir'], 
        os.path.join(tmp_dir_path, 'build')
    )

    exercise_data = exrsettings.get_exercise_by_name(exercise_name)
    with open(os.path.join(tmp_dir_path, 'exercise.json'), 'w') as f:
            json.dump(exercise_data, f, indent=4)

    for flag_i, flag_data in enumerate(exercise_data['flags']):
        kb_uuid = flag_data['kb']['uuid']

        kb_data = get_remote_vulnerability_func(kb_uuid)
        # Support both via_hub and via_deployment return messages
        if not kb_data or kb_data.get('errorMsg') == 'NotFound':
            kb_data = kbsettings.get_kb_by_uuid(kb_uuid)

        if not kb_data:
            raise log.FatalMsg(f"Error, can't find local or remote KB with uuid {kb_uuid}")

        with open(os.path.join(tmp_dir_path, f'kb_{flag_i}.json'), 'w') as f:
                json.dump(kb_data, f, indent=4)
    
    stack_uuid = exercise_data['stack']['uuid']
    stack_data = get_remote_technology_func(stack_uuid)
    if not stack_data or stack_data.get('errorMsg') == 'NotFound':
        # Support both via_hub and via_deployment return messages
        stack_data = stacksettings.get_stack_by_uuid(stack_uuid)

    if not stack_data:
        raise log.FatalMsg(f"Error, can't find local or remote stack with uuid {exercise_data['stack']['uuid']}")
    with open(os.path.join(tmp_dir_path, 'stack.json'), 'w') as f:
            json.dump(stack_data, f, indent=4)

    shutil.make_archive(tmp_archive.name, 'zip', tmp_dir_path)

    remote.push_to_s3(
            tmp_archive.name,
            aws_creds,
            username,
            aws_arn
    )

def deploy(image_name, exercise_name, source):

    authsettings.set_source(source)

    source_type, management_url, username, password = authsettings.load_or_ask_for_creds()

    if source_type != 'deployment':
        raise log.FatalMsg(
            "Error, deploying requires administrative privileges on a SecureFlag CE instance"
            )

    remote.login_to_deployment(username, password, management_url)
    aws_creds = remote.get_ecr_creds_via_deployment()
    aws_arn = remote.get_arn_via_deployment()

    exercise_settings = exrsettings.get_exercise_by_name(exercise_name)
    image_settings = imgsettings.settings.get('images', {}).get(image_name)

    if not image_settings:
        raise log.FatalMsg("Image %s does not exist, run 'sfsdk img-add' to add it" % image_name)

    if not containers.image_exists(image_name):
        raise log.FatalMsg("Image %s has not been built yet, run img-build to build it" % image_name)

    # Obtain the imageUrl from the instance
    image_url = remote.create_repo_and_get_image_url_via_deployment(image_name)

    # Save it to the exercise settings
    # exercise_settings['image']['imageUrl'] = image_url
    # exrsettings.save_exercise_meta(exercise_settings)

    exercises_uuids = [ e['uuid'] for e in remote.get_exercises_via_deployment() ]
    new_exercise_data = remote.push_exercise_and_get_new_json(exercise_settings, exercises_uuids)

    # Fix the folder based on the uuid
    exrsettings.update_exercise_folder(
            old_exercise_dir=os.path.join(exrsettings.workspace_dir, exercise_name),
            new_exercise_data=new_exercise_data
            )

    log.header("Exercise %s has been pushed with uuid %s" % (exercise_name, new_exercise_data['uuid']))

    # Push the image
    pushed = True
    push_stream = containers.tag_and_push_image(aws_creds, image_name, image_url, aws_arn)
    for line in push_stream:

        if 'error' in line:
            log.warn('Error pushing the image: %s' % line['error'])
            pushed = False
        elif 'status' in line and line['status'] == 'Pushing':
            log.block('Pushing the image layer %s %s...' % (line['id'], line['progress'].split(' ')[-1]), end='\t\t\r')

        sys.stdout.flush()

    if pushed:
        log.header("Image %s has been pushed to %s" % (image_name, image_url))

def exercise_ls(source):

    authsettings.set_source(source)

    log.block('\n'.join(exrsettings.ls_exercises()), end = '\n')

def exercise_rm(names):

    for name in names:
        try:
            exrsettings.remove_exercise(name)
        except log.FatalMsg as e:
            log.warn(str(e))
        else:
            log.header("Exercise %s has been removed" % name)

def _get_argparser():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser')

    imgtechs = subparsers.add_parser('img-techs', help='Update the list of base technologies')
    imgtechs.add_argument(
            '--source', dest='source', help='Source name')

    parser_add = subparsers.add_parser('img-add', help='Add new image')
    parser_add.add_argument(
        '-f', '--from-img', dest='from_img', help='Base technology image', required=True)
    parser_add.add_argument(
        '-b', '--build-dir', dest='build_dir', help='Build folder')
    parser_add.add_argument(
        '-i', '--import-build', dest='from_dir', help='Import build directory')
    parser_add.add_argument(
        '-a', '--import-app', dest='app_dir', help='Import application directory')
    parser_add.add_argument('name', help='New image name')

    parser_ls = subparsers.add_parser('img-ls', help='List images')

    parser_build = subparsers.add_parser('img-build', help='Build an image')
    parser_build.add_argument('-s', '--skip-base-img', dest='skip_base_img', help='Skip pulling base image', action='store_true')
    parser_build.add_argument('name', help='Image to build')
    parser_build.add_argument(
            '--source', dest='source', help='Source name')

    parser_run = subparsers.add_parser('img-run', help='Run last build')
    parser_run.add_argument('name', help='Project to run')
    parser_run.add_argument('-f', '--force', dest='force', help='Remove previous containers', action='store_true')
    parser_run.add_argument(
        '--exercise-name', dest='exercise_name', help='Pass exercise metadata'
        )

    parser_stop = subparsers.add_parser('img-stop', help='Stop running image')
    parser_stop.add_argument('names', nargs='+', help='Images names (or "all")')

    parser_shell = subparsers.add_parser('img-shell', help='Interact with a running image')
    parser_shell.add_argument('name', help='Run interactive shell on a running image')
    parser_shell.add_argument('-c', '--command', help='Command to execute', default='/bin/bash')

    parser_watch = subparsers.add_parser('img-watch', help='Keep track of the fs changes on a running image')
    parser_watch.add_argument(
        '-f', '--folder', dest='folder', help='Folder to watch', default='/home/sf')
    parser_watch.add_argument(
        '-c', '--count', dest='count', help=argparse.SUPPRESS, default=0, type=int)
    parser_watch.add_argument('name', help='Running image to watch')

    snapshot = subparsers.add_parser('img-snapshot', help='Save the current state as new')
    snapshot.add_argument(
        '--new-name', dest='new_name', help='The new image name')
    snapshot.add_argument(
        '-f', '--force', dest='force', help='Overwrite the export directory', action='store_true')
    snapshot.add_argument('name', help='Running image to snapshot')

    parser_rm = subparsers.add_parser('img-rm', help='Remove local image')
    parser_rm.add_argument('names', nargs='+', help='Images names')
    parser_rm.add_argument(
        '-f', '--force', dest='force', help='Delete the build folder', action='store_true')

    parser_exercise_ls = subparsers.add_parser('exercise-ls', help='List local exercises')
    parser_exercise_ls.add_argument(
            '--source', dest='source', help='Source name')

    exercise_edit = subparsers.add_parser('exercise-edit', help='Manage exercises via web editor')
    exercise_edit.add_argument(
            '--source', dest='source', help='Source name')

    exercise_rm = subparsers.add_parser('exercise-rm', help='Remove local exercise')
    exercise_rm.add_argument('names', nargs='+', help='Exercises names')

    push = subparsers.add_parser('deploy', help='Push exercise and image to a deployment')
    push.add_argument(
        '--image-name', dest='image_name', help='The image to push', required=True)
    push.add_argument(
        '--exercise-name', dest='exercise_name', help='The exercise name', required=True
        )
    push.add_argument(
            '--source', dest='source', help='Source name')

    publish = subparsers.add_parser('publish', help='Publish exercise and image on the SecureFlag Hub')
    publish.add_argument(
        '--image-name', dest='image_name', help='The image to publish', required=True)
    publish.add_argument(
        '--exercise-name', dest='exercise_name', help='The exercise name', required=True
        )
    publish.add_argument(
        '--source', dest='source', help='Source name')


    config = subparsers.add_parser('config', help='Configure authentication')
    config.add_argument(
            '--source', dest='source', help='Source name', default = 'default')

    parser.add_argument(
        '--verbose', '-v', dest='verbose', help='Verbose', action='store_true')

    return parser

def cli():

    parser = _get_argparser()

    kwargs = vars(parser.parse_args())

    if not kwargs.get('subparser'):
        parser.print_help()
        raise log.FatalMsg()

    imgsettings.load(base_dir)

    authsettings.load(base_dir)
    authsettings.set_source(kwargs.get('source'))

    # Initialize docker client
    containers.load()

    # Use another base_dir to support multiple sources
    sources_folder = os.path.join(
            base_dir,
            'srcs',
            authsettings.current_source
        )

    # Load settings from disk
    exrsettings.load(sources_folder)
    techsettings.load(sources_folder)
    kbsettings.load(sources_folder)
    stacksettings.load(sources_folder)
    frameworksettings.load(sources_folder)

    # Set verbose and remove from arguments
    if kwargs['verbose']:
        log.set_verbose()

    del kwargs['verbose']

    globals()[kwargs.pop('subparser').replace('-', '_')](**kwargs)



if __name__ == "__main__":

    try:
        cli()
    except log.FatalMsg as e:
        log.warn(str(e))
        sys.exit(1)
    except KeyboardInterrupt as e:
        print('')
