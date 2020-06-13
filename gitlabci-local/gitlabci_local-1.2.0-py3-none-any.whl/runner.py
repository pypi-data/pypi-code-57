#!/usr/bin/env python3

# Libraries
import colored
import docker
import os
from pathlib import Path
import signal
import stat
import sys
import tempfile
import time

# Components
from .main import NAME
from .puller import pull

# Constants
marker_debug = '__GITLAB_CI_LOCAL_DEBUG__'

# Launcher
def launcher(options, jobs):

    # Variables
    result = None

    # Run selected jobs
    for job in jobs:

        # Filter jobs list
        if not options.pipeline and job not in options.names:
            continue

        # Filter stages list
        if options.pipeline and options.names and jobs[job]['stage'] not in options.names:
            continue

        # Filter manual jobs
        job_manual = (jobs[job]['when'] == 'manual')
        if job_manual and not options.manual and job not in options.names:
            continue

        # Raise initial result
        if result == None:
            result = True

        # Run job
        attempt = 0
        expected = result
        result = runner(options, jobs[job], result)

        # Retry job if allowed
        if expected and not result and jobs[job]['retry'] > 0:
            while not result and attempt < jobs[job]['retry']:
                attempt += 1
                result = runner(options, jobs[job], expected)

    # Result
    return True if result else False

# Runner
def runner(options, job_data, last_result):

    # Variables
    local_runner = False
    result = False
    time_start = time.time()

    # Filter when
    if last_result and job_data['when'] not in ['on_success', 'manual', 'always']:
        return last_result
    if not last_result and job_data['when'] not in ['on_failure']:
        return last_result

    # Prepare image
    image = job_data['image']

    # Prepare local runner
    if image in ['local']:
        local_runner = True

    # Prepare network
    network = 'bridge'
    if options.network:
        network = options.network

    # Header
    if not options.quiet:
        print(' %s===[ %s%s: %s%s %s(%s) %s]===%s' %
              (colored.fg('green') + colored.attr('bold'),
               colored.fg('yellow') + colored.attr('bold'), job_data['stage'],
               colored.fg('yellow') + colored.attr('bold'), job_data['name'],
               colored.fg('cyan') + colored.attr('bold'), image,
               colored.fg('green') + colored.attr('bold'), colored.attr('reset')))
        print(' ', flush=True)

    # Create Docker client
    client = docker.from_env()

    # Acquire project path
    pathProject = options.path
    pathParent = str(Path(pathProject).parent)

    # Prepare working directory
    if options.workdir:
        pathWorkDir = os.path.abspath(options.workdir)
    else:
        pathWorkDir = pathProject

    # Prepare entrypoint and scripts
    entrypoint = job_data['entrypoint']
    scriptsAfter = []
    scriptsBefore = []
    scriptsCommands = []
    scriptsDebug = []

    # Prepare before_scripts
    if options.before:
        scriptsBefore += job_data['before_script']

    # Prepare scripts
    scriptsCommands += job_data['script']
    if not local_runner:
        if options.bash:
            scriptsCommands = []
        if options.bash or options.debug:
            scriptsDebug += ['echo "' + marker_debug + '"', 'tail -f /dev/null']

    # Prepare after_scripts
    if options.after:
        scriptsAfter += job_data['after_script']

    # Prepare commands
    scriptFile = tempfile.NamedTemporaryFile(delete=True)
    with open(scriptFile.name, mode='w') as scriptStream:

        # Prepare execution context
        scriptStream.write('#!/bin/sh')
        scriptStream.write('\n')
        scriptStream.write('result=1')
        scriptStream.write('\n')

        # Prepare before_script/script context
        scriptStream.write('(')
        scriptStream.write('\n')
        scriptStream.write('set -ex')
        scriptStream.write('\n')

        # Prepare before_script commands
        if len(scriptsBefore) > 0:
            scriptStream.write('{')
            scriptStream.write('\n')
            scriptStream.write('\n'.join(scriptsBefore))
            scriptStream.write('\n')
            scriptStream.write('} && ')
            scriptStream.flush()

        # Prepare script commands
        if len(scriptsCommands) > 0:
            scriptStream.write('{')
            scriptStream.write('\n')
            scriptStream.write('\n'.join(scriptsCommands))
            scriptStream.write('\n')
            scriptStream.write('}')
            scriptStream.flush()
        else:
            scriptStream.write('false')
            scriptStream.flush()

        # Finish before_script/script context
        scriptStream.write('\n')
        scriptStream.write(') 2>&1')
        scriptStream.write('\n')
        scriptStream.write('result=${?}')
        scriptStream.flush()

        # Prepare debug script commands
        if len(scriptsDebug) > 0:
            scriptStream.write('\n')
            scriptStream.write('(')
            scriptStream.write('\n')
            scriptStream.write('set -x')
            scriptStream.write('\n')
            scriptStream.write('\n'.join(scriptsDebug))
            scriptStream.write('\n')
            scriptStream.write(') 2>&1')
            scriptStream.flush()

        # Prepare after_script commands
        if len(scriptsAfter) > 0:
            scriptStream.write('\n')
            scriptStream.write('(')
            scriptStream.write('\n')
            scriptStream.write('set -ex')
            scriptStream.write('\n')
            scriptStream.write('{')
            scriptStream.write('\n')
            scriptStream.write('\n'.join(scriptsAfter))
            scriptStream.write('\n')
            scriptStream.write('}')
            scriptStream.write('\n')
            scriptStream.write(') 2>&1')
            scriptStream.flush()

        # Prepare execution result
        scriptStream.write('\n')
        scriptStream.write('exit "${result}"')
        scriptStream.write('\n')

    # Prepare script execution
    script_stat = os.stat(scriptStream.name)
    os.chmod(scriptStream.name, script_stat.st_mode | stat.S_IEXEC)
    scriptFile.file.close()

    # Prepare mounts
    temp_dir = tempfile.gettempdir()
    volumes = {
        pathParent: {
            'bind': pathParent,
            'mode': 'rw'
        },
        temp_dir: {
            'bind': temp_dir,
            'mode': 'rw'
        },
        '/var/run/docker.sock': {
            'bind': '/var/run/docker.sock',
            'mode': 'rw'
        }
    }

    # Extend mounts
    if options.volume:
        for volume in options.volume:
            volume_nodes = volume.split(':')

            # Parse HOST:TARGET:MODE
            if len(volume_nodes) == 3:
                volume_host = os.path.abspath(os.path.expandvars(volume_nodes[0]))
                volume_target = os.path.expandvars(volume_nodes[1])
                volume_mode = volume_nodes[2]

            # Parse HOST:TARGET
            elif len(volume_nodes) == 2:
                volume_host = os.path.abspath(os.path.expandvars(volume_nodes[0]))
                volume_target = os.path.expandvars(volume_nodes[1])
                volume_mode = 'rw'

            # Parse VOLUME
            else:
                volume_host = os.path.abspath(os.path.expandvars(volume))
                volume_target = os.path.abspath(os.path.expandvars(volume))
                volume_mode = 'rw'

            # Clear volume overrides
            for volume in list(volumes.keys()):
                if volume_target == volumes[volume]['bind']:
                    volumes.pop(volume)

            # Append volume mounts
            volumes[volume_host] = {'bind': volume_target, 'mode': volume_mode}

    # Prepare variables
    variables = dict()
    for variable in job_data['variables']:
        variables[variable] = os.path.expandvars(str(job_data['variables'][variable]))

    # Container execution
    if not local_runner:

        # Image validation
        if not image:
            raise ValueError(
                'Missing image for "%s / %s"' % (job_data['stage'], job_data['name']))
        try:
            client.images.get(image)
        except docker.errors.ImageNotFound:
            pull(image)

        # Launch container
        container = client.containers.run(
            image, command=scriptFile.name, detach=True, entrypoint=entrypoint,
            environment=variables, network_mode=network, privileged=True, remove=False,
            stdout=True, stderr=True, stream=True, volumes=volumes,
            working_dir=pathWorkDir)

        # Create interruption handler
        def interruptHandler(signal, frame):
            print(' ')
            print(' ')
            print(
                ' %s> WARNING: %sUser interruption detected, stopping the container...%s'
                % (colored.fg('yellow') + colored.attr('bold'),
                   colored.attr('reset') + colored.attr('bold'), colored.attr('reset')))
            print(' ', flush=True)
            container.stop(timeout=0)

        # Register interruption handler
        originalINTHandler = signal.getsignal(signal.SIGINT)
        originalTERMHandler = signal.getsignal(signal.SIGTERM)
        signal.signal(signal.SIGINT, interruptHandler)
        signal.signal(signal.SIGTERM, interruptHandler)

        # Execution wrapper
        success = False

        # Show container logs
        try:
            for line in container.logs(stream=True):
                if marker_debug in line.decode():
                    break
                sys.stdout.buffer.write(line)
                sys.stdout.buffer.flush()
        except:
            pass

        # Runner bash or debug mode
        if options.bash or options.debug:
            print(' ')
            exit_code, output = container.exec_run('which bash')
            shell = 'sh'
            if exit_code == 0:
                shell = 'bash'
            print(
                ' %s> INFORMATION: %sUse \'%sdocker exec -it %s %s%s\' commands for debugging. Interrupt with Ctrl+C...%s'
                % (colored.fg('yellow') + colored.attr('bold'), colored.attr('reset') +
                   colored.attr('bold'), colored.fg('cyan'), container.name, shell,
                   colored.attr('reset') + colored.attr('bold'), colored.attr('reset')))
            print(' ', flush=True)

        # Check container status
        wait = container.wait()
        success = (wait['StatusCode'] == 0)

        # Stop container
        container.stop(timeout=0)
        time.sleep(0.1)

        # Remove container
        container.remove(force=True)

        # Unregister interruption handler
        signal.signal(signal.SIGINT, originalINTHandler)
        signal.signal(signal.SIGTERM, originalTERMHandler)

        # Result evaluation
        if job_data['when'] in ['on_failure', 'always']:
            result = last_result
        elif success:
            result = True

    # Native execution
    else:

        # Prepare environment
        _environ = dict(os.environ) # or os.environ.copy()
        os.environ.update(variables)

        # Native execution
        scripts = []
        if entrypoint:
            scripts += entrypoint
        scripts += [scriptFile.name]
        success = (os.system(' '.join(scripts)) == 0)

        # Result evaluation
        if job_data['when'] in ['on_failure', 'always']:
            result = last_result
        elif success:
            result = True

        # Restore environment
        os.environ.clear()
        os.environ.update(_environ)

    # Initial job details
    job_details = ''
    job_details_list = []

    # Prepare when details
    if job_data['when'] not in ['on_success']:
        job_details_list += ['when: %s' % (job_data['when'])]

    # Prepare allow_failure details
    if job_data['allow_failure']:
        job_details_list += ['failure allowed']

    # Prepare job details
    if job_details_list:
        job_details = ' (' + ', '.join(job_details_list) + ')'

    # Evalulate duration time
    time_duration = time.time() - time_start
    time_seconds = '%.0f second%s' % (time_duration % 60,
                                      's' if time_duration % 60 > 1 else '')
    time_minutes = ''
    if time_duration >= 60:
        time_minutes = '%.0f minute%s ' % (time_duration / 60,
                                           's' if time_duration / 60 > 1 else '')
    time_string = time_minutes + time_seconds

    # Footer
    print(' ', flush=True)
    if not options.quiet:
        print(' %s> Result: %s in %s%s%s' %
              (colored.fg('yellow') + colored.attr('bold'), colored.fg('green') +
               colored.attr('bold') + 'Success' if result else colored.fg('red') +
               colored.attr('bold') + 'Failure', time_string, colored.fg('cyan') +
               colored.attr('bold') + job_details, colored.attr('reset')))
        print(' ')
        print(' ', flush=True)

    # Allowed failure result
    if job_data['when'] not in ['on_failure', 'always'
                                ] and not result and job_data['allow_failure']:
        result = True

    # Result
    return result
