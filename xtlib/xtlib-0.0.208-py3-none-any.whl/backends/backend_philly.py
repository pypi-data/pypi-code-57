#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# backend_philly.py: support for submitting and managing philly jobs
import os
import sys
import json
import shlex
import subprocess
from interface import implements

from xtlib.console import console
from xtlib.report_builder import ReportBuilder
from xtlib.helpers.feedbackParts import feedback as fb

from .backend_base import BackendBase
from .backend_interface import BackendInterface

from xtlib import qfe
from xtlib import utils
from xtlib import errors
from xtlib import pc_utils
from xtlib import scriptor
from xtlib import constants
from xtlib import run_helper
from xtlib import file_utils
from xtlib import process_utils
from xtlib import box_information

#FN_CURLOUTPUT = os.path.realpath(os.path.expanduser("~/.xt/cwd/curl_output.txt"))

class Philly(BackendBase):
    def __init__(self, compute, compute_def, core, config, username=None, arg_dict=None):
        super(Philly, self).__init__(compute, compute_def, core, config, username, arg_dict)

        self.compute = compute
        self.compute_def = compute_def
        self.core = core
        self.config = config
        self.username = username
        self.store = self.core.store

        self.cluster = utils.safe_value(arg_dict, "cluster")
        self.vc = utils.safe_value(arg_dict, "vc")
        
    def get_name(self):
        return "philly"

    def adjust_run_commands(self, job_id, job_runs, using_hp, experiment, service_type, snapshot_dir, args):
        '''
        This method is called to allow the backend to inject needed shell commands before the user cmd.  This 
        base implementation does so by generating a new script file and adding it to the snapshot_dir.
        '''
        pass        

    def get_client_cs(self, service_node_info):
        '''
        Args:
            service_node_info: info that service maps to a compute node for a job
        Returns:
            {"ip": value, "port": value, "box_name": value}
        '''
        cs = None

        job_id = service_node_info["job_id"]
        filter = {"_id": job_id}
        jobs = self.core.store.mongo.get_info_for_jobs(filter, None)
        if not jobs:
            errors.store_error("unknown job_id: {}", job_id)

        # get IP and PORT from job:connect_info_by_node:node_id
        job = jobs[0]

        node_id = service_node_info["node_id"]
        connect_info_by_node = utils.safe_value(job, "connect_info_by_node")
        connect_info = utils.safe_value(connect_info_by_node, node_id)
        if not connect_info:
            errors.controller_not_yet_running("controller has not begun running: job={}, node_id={}".format(job_id, node_id))

        ip = utils.safe_value(connect_info, "ip_addr")
        port = utils.safe_value(connect_info, "controller_port")

        if ip and port:
            cs = {"ip": ip, "port": port, "box_name": node_id}

        return cs

    def provides_container_support(self):
        '''
        Returns:
            returns True if docker run command is handled by the backend.
        '''
        return True
        
        
    def print_jobs(self, result, title, prop, title_prefix, columns):
        console.print("{}, {}:".format(title_prefix, title))
        jobs = result[prop]

        if not jobs:
            console.print("no jobs found\n")
        else:
            # update name
            for job in jobs:
                name = job["name"]
                if name.startswith("ns-bf-"):
                    name = name[6:]
                if "!" in name:
                    index = name.index("!")
                    name = name[:index]
                job["run_name"] = name

            lb = ReportBuilder(self.config, self.store, client=None)
            text, rows = lb.build_formatted_table(jobs, columns)
            console.print(text)

        # for job in jobs:
        #     #console.print("    {:.100s}".format(str(job)))
        #     utils.print_dict_lines(job, "    ")
        #     console.print("-----------------")

    def view_status(self, run_name, workspace, job, monitor, escape_secs, auto_start, 
            stage_flags, status, max_finished):

        result = self.list_jobs(self.cluster, self.vc, username=self.username, status=status, 
            max_finished=max_finished, stage_flags=stage_flags)

        title = "target={} jobs:".format(self.compute)
        columns = ["run_name", "status", "vc", "elapsedTime", "username", "gpus", "retries", "appID"]

        console.print()

        if "queued" in stage_flags:
            self.print_jobs(result, "QUEUED", "queuedJobs", title, columns)

        if "active" in stage_flags:
            self.print_jobs(result, "RUNNING", "runningJobs", title, columns)

        if "completed" in stage_flags:
            self.print_jobs(result, "COMPLETED", "finishedJobs", title, columns)


    def build_env_vars(self, user_env_vars, workspace, experiment, run_name, use_controller, node_id, box_secret, args):

        # start by copying job-common env vars
        env = dict(user_env_vars)

        env["XT_NODE_ID"] = node_id
        env["XT_BOX_SECRET"] = box_secret

        env["XT_WORKSPACE_NAME"] = workspace
        env["XT_EXPERIMENT_NAME"] = experiment
        #env["XT_RUN_NAME"] = run_name + ", philly level"   # proven philly bug workaround

        # cleaner philly bug workaround    
        if not use_controller:
            env["XT_RUN_NAME"] = run_name 

        env["XT_TARGET_FILE"] = ""
        env["XT_RESUME_NAME"] = ""
        
        return env

    def process_data_action(self, cmds, store_data_dir, data_action):
        if data_action == "mount":
            # point to parent data directory (not target, e.g., mnist)
            data_mnt = "/mnt/data/" + store_data_dir

            self.append(cmds, "echo MOUNTING data SHARE={} to local path={}".format(store_data_dir, data_mnt))
            self.append(cmds, 'export XT_DATA_MNT="{}"'.format(data_mnt))
            self.append(cmds, 'export XT_DATA_DIR="{}"'.format(data_mnt))
            self.append(cmds, "ls {}".format(data_mnt), echo_before=True)
        elif data_action == "download":
            dest_dir = "/home/$USER/data/" + store_data_dir

            self.append(cmds, "echo DOWNLOADING data SHARE={} to local path={}".format(store_data_dir, dest_dir))
            self.append(cmds, 'export XT_DATA_DIR="' + dest_dir + '"')
            self.append(cmds, 'mkdir $XT_DATA_DIR -p')

            # make it look like this is parent dir
            dest_dir_ext = dest_dir   # + "/" + store_data_dir

            requests = [ {"container": utils.DATA_STORE_ROOT, "blob_path": store_data_dir, "dest_dir": dest_dir_ext} ]
            sub_cmds = self.create_download_commands("xt", False, True, requests)
            cmds += sub_cmds

    def process_model_action(self, cmds, store_model_dir, model_action):
        if model_action == "mount":
            # point to parent data directory (not target, e.g., mnist)
            model_mnt = "/mnt/models/" + store_model_dir

            self.append(cmds, "echo MOUNTING model SHARE={} to local path={}".format(store_model_dir, model_mnt))
            self.append(cmds, 'export XT_MODEL_MNT="{}"'.format(model_mnt))
            self.append(cmds, 'export XT_MODEL_DIR="{}"'.format(model_mnt))
            self.append(cmds, "ls {}".format(model_mnt), echo_before=True)
        elif model_action == "download":
            dest_dir = "/home/$USER/models/" + store_model_dir

            self.append(cmds, "echo DOWNLOADING model SHARE={} to local path={}".format(store_model_dir, dest_dir))
            self.append(cmds, 'export XT_MODEL_DIR="' + dest_dir + '"')
            self.append(cmds, 'mkdir $XT_MODEL_DIR -p')

            # make it look like this is parent dir
            dest_dir_ext = dest_dir    # + "/" + store_model_dir

            requests = [ {"container": utils.MODELS_STORE_ROOT, "blob_path": store_model_dir, "dest_dir": dest_dir_ext} ]
            sub_cmds = self.create_download_commands("xt", False, True, requests)
            cmds += sub_cmds

    def wrap_cmd_line_for_philly_job(self, user_cmd, store_before_dir, store_output_dir, store_after_dir, 
        store_data_dir, data_action, store_model_dir, model_action, use_controller, args):

        self.is_windows = False
        cmds = []
        pip_freeze = args["pip_freeze"]

        # DEBUG GPU ISSUE
        # NOTE: installing torchvision==0.4.1 *does* causes pytorch to be REINSTALLED without correct GPU support (on Philly)
        # verifyed Feb-18-2020, rfernand2.
        #self.append(cmds, '''python -c "import torch; print('TORCH version', torch.__version__, ' says CUDA available=', torch.cuda.is_available())"''')
        #self.append(cmds, 'pip install torchvision==0.4.1')
        #self.append(cmds, '''python -c "import torch; print('TORCH version', torch.__version__, ' says CUDA available=', torch.cuda.is_available())"''')

        self.add_first_cmds(cmds, "long philly cmd string", change_dir=True)

        # supress annoying warnings in philly log
        self.append(cmds, 'export PATH=$PATH:~/.local/bin')

        # create environment variables for user
        self.append(cmds, 'export XT_CODE_MNT="/mnt/default/' + store_before_dir + '/code"')
        self.append(cmds, 'export XT_OUTPUT_MNT="/mnt/output/' + store_output_dir + '"')
        self.append(cmds, 'export XT_AFTER_MNT="/mnt/output/' + store_after_dir + '"')

        # ensure required directories exist
        self.append(cmds, 'mkdir -p "/home/$USER/.xt"')

        # bug workaround: this creates a 0-len blob in Azure storage that causes problems downstream
        #self.append(cmds, 'mkdir -p "$XT_OUTPUT_MNT"')

        # COPY CODE files from blob fusion INPUT
        self.append(cmds, "echo copying source code from: $XT_CODE_MNT")
        self.append(cmds, 'cp -r "$XT_CODE_MNT" ~/code')
        self.append(cmds, "cd ~/code")

        code_zip = args["code_zip"]
        if code_zip and code_zip != "none":
            # UNZIP code
            self.append(cmds, "echo unzipping " + constants.CODE_ZIP_FN)
            self.append(cmds, 'sudo apt install unzip')
            self.append(cmds, 'unzip {} > __unzip__.log'.format(constants.CODE_ZIP_FN))

        # prevent python from writing byte code (faster for 1-off usage?)        
        self.append(cmds, "export PYTHONDONTWRITEBYTECODE=1")
        self.append(cmds, 'export PYTHONPATH=".:$PYTHONPATH"')

        # now that code files are present and unzipped, we can run the setup
        # commands (which may rely on files like requirements.txt)
        self.add_setup_cmds(cmds, pip_freeze=pip_freeze, args=args)
        self.add_xt_setup_cmds(cmds, self.is_windows)

        if pip_freeze:
            self.append(cmds, "echo final PIP FREEZE:")
            self.append(cmds, "pip freeze > __final_pip_freeze__.log")

        self.add_report_cmds(cmds, True)

        # NOTE: these action commands rely on XT being installed 
        self.process_data_action(cmds, store_data_dir, data_action)
        self.process_model_action(cmds, store_model_dir, model_action)

        # run user's cmd
        if not use_controller:   
            # --direct option; add a shell prefix in front of script
            if not user_cmd.endswith(".py"):
                # do we need this?  it assumes user_cmd contains a 'conda activate cmd'
                prefix = self.config.get("script-launch-prefix", "philly")
                user_cmd = process_utils.make_launch_cmd(prefix, user_cmd, is_script=True)
            
        self.append(cmds, user_cmd)

        self.append(cmds, 'echo ----- END of XT-level processing -----')

        wrapped_cmd = "; ".join(cmds)
        return wrapped_cmd

    def build_azure_volumes(self, input_container, data_container, output_container, data_action, data_writable,
            model_container, model_action, model_writable, args):
        # specify how to mount our azure storage for blobfuse system
        storage_creds = self.config.get_storage_creds()
        
        store_key = storage_creds["key"]
        store_name = storage_creds["name"]

        # use PhillyTools options (best practice) 
        options = ["-o", "attr_timeout=240", "-o", "entry_timeout=240", "-o", "negative_timeout=120", "--log-level=LOG_WARNING", "-o", "allow_other", 
            "--file-cache-timeout-in-seconds=100000"]

        options_readonly = options + ["-o", "ro"]

        # mount CODE and AFTER containers
        volumes = {
            # these are the default set of philly tools mounts 
            "default":  {"type": "blobfuseVolume", "storageAccount": store_name, "containerName": input_container, "path": "/mnt/default", "options": options_readonly}, 
            "output": {"type": "blobfuseVolume", "storageAccount": store_name, "containerName": output_container, "path": "/mnt/output", "options": options}, 
            "_output": {"type": "blobfuseVolume", "storageAccount": store_name, "containerName": output_container, "path": "/mnt/_output", "options": options}
            }

        # mount DATA share
        if data_action == "mount":
            opts = options if data_writable else options_readonly
            volumes["data"] = {"type": "blobfuseVolume", "storageAccount": store_name, "containerName": data_container, "path": "/mnt/data", "options": opts}

        # mount MODELS share
        if model_action == "mount":
            opts = options if model_writable else options_readonly
            volumes["model"] = {"type": "blobfuseVolume", "storageAccount": store_name, "containerName": model_container, "path": "/mnt/models", "options": opts}

        credentials = {"storageAccounts": {store_name: {"key": store_key}}}

        return volumes, credentials

    def submit_job(self, job_id, job_runs, workspace, compute_def, resume_name, 
            repeat_count, using_hp, runs_by_box, experiment, snapshot_dir, controller_scripts, args):
        '''
        Note: backend submitter functions are responsible for:
            - submitting the job (for each node, queue runs for that node)
            - return service job id's

        TODO: eliminate compute_def argument on submit_job, since it has already been passed to the CTR.
        '''
        tmp_files = []

        # now, submit runs by node (a separate philly submit for each node)
        service_info_by_nodes = {}

        cluster = utils.safe_value(compute_def, "cluster")
        vc = utils.safe_value(compute_def, "vc")
        self.username = args["username"]

        fb.feedback("submitting to philly.{}.{}: ".format(cluster, vc), add_seperator=False)

        for i, node_runs in enumerate(job_runs):
            node_id = "node" + str(i)
            box_name = utils.make_box_name(job_id, "philly", i)

            service_node_info = self.submit_runs_for_node(job_id, node_runs, workspace, compute_def, resume_name, repeat_count, using_hp, 
                experiment, runs_by_box, node_id, box_name, args)

            service_info_by_nodes[node_id] = service_node_info

        # remove temp files
        for fn in tmp_files:
            os.remove(fn)

        fb.feedback("done", is_final=True)
        
        monitor_url = "https://philly/#/jobSummary/{}/{}/{}".format(self.cluster, self.vc, self.username)
        service_job_info = {"monitor_url": monitor_url}

        return service_job_info, service_info_by_nodes

    def build_curl(self, cmd):
        fn_cert =  file_utils.get_xtlib_dir() + "/public_certs/philly-cert.crt"
        use_cert = True
        cert_cmd = '--cacert "{}"'.format(fn_cert) if use_cert else "-k"
        explicit = qfe.get_explicit_options()

        fn_pass = os.path.realpath(os.path.expanduser("~/.xt/curl_config.txt"))
        if os.path.exists(fn_pass):
            # FIRST priority: user provided a CURL CONFIG file
            # assume file contains both username and pw
            prefix = "curl {} -s -K '{}' --ntlm  : ".format(cert_cmd, fn_pass)
        elif "username" in explicit or not pc_utils.is_windows():
            # SECOND priority: user provided an explicit username or on LINUX

            # we stop feedback since user will enter text (username/password)
            fb.stop_feedback()

            # we are about to run our curl command, which will prompt user for their password
            console.print("\nTo skip this step, put '-u user:pw' in: {}".format(fn_pass))

            if "username" in explicit:
                username = self.username
            else:
                # we cannot rely on self.username to be the user's username on Philly 
                username = input("Philly username: ")

            # provide username and let user enter password
            prefix = "curl {} -su '{}' --ntlm  : ".format(cert_cmd, username)
        else:
            # THIRD priority: use of windows, we use built-in authentication
            prefix = 'curl -s {} --ntlm --user : '.format(cert_cmd)

        console.diag("curl cmd: {}".format(prefix + cmd))
        return prefix + cmd

    def submit_runs_for_node(self, job_id, node_runs, workspace, compute_def, resume_name, repeat_count, using_hp, experiment, 
            runs_by_box, node_id, box_name, args):
        '''
        in philly, each node that we want to run on is submitted as a separate philly job.  
        '''

        # adjust cmds for philly blob mounting
        # blob paths (without the container)
        store_before_dir = "jobs/" + job_id + "/before"

        store_data_dir = args["data_share_path"]
        data_action = args["data_action"]
        data_writable = args["data_writable"]

        store_model_dir = args["model_share_path"]
        model_action = args["model_action"]
        model_writable = args["model_writable"]
        hold = args["hold"]

        use_controller = (not args["direct_run"])

        # currently, we put all 'data stores' under __data__
        # if store_data_dir:
        #     store_data_dir = utils.DATA_STORE_ROOT + "/" + store_data_dir

        wrapped_cmds = []
        run_names = []

        for run_data in node_runs:
            # run_data = {"run_name": run_name, "run_specs": run_specs, "box_name": box_name, "box_info": box_info, "repeat": repeat_count}
            run_name = run_data["run_name"]
            run_specs = run_data["run_specs"]
            cmd_parts = run_specs["cmd_parts"]

            cmd_line = " ".join(cmd_parts)
            
            store_output_dir = "runs/" + run_name + "/output"
            store_after_dir = "runs/" + run_name + "/after"

            wrapped_cmd = self.wrap_cmd_line_for_philly_job(cmd_line, store_before_dir, 
                store_output_dir, store_after_dir, store_data_dir=store_data_dir, 
                data_action=data_action, store_model_dir=store_model_dir, 
                model_action=model_action, use_controller=use_controller, args=args)
    
            wrapped_cmds.append(wrapped_cmd)
            run_names.append(run_name)

        cluster = utils.safe_value(compute_def, "cluster")  
        vc = utils.safe_value(compute_def, "vc")            
        sku = utils.safe_value(compute_def, "sku").upper()  
        queue = utils.safe_value(compute_def, "queue")      

        env_name = utils.safe_value(self.compute_def, "docker")
        if not env_name:
            errors.config_error("Philly compute target '{}' is missing the required 'docker' property (in XT config file)".format(self.compute))

        env = self.config.get("dockers", env_name, default_value=None)
        if not env:
            errors.config_error("docker '{}' definition not found in XT config file".format(env_name))

        docker_image = utils.safe_value(env, "image")
        if not docker_image:
            errors.config_error("Definition for environment '{}' is missing the required 'image' property".format(env_name))

        registry_name = utils.safe_value(env, "registry")
        if not registry_name:
            errors.config_error("Definition for environment '{}' is missing the required 'registry' property".format(env_name))

        docker_registry = self.config.get("external-services", registry_name, default_value=None)
        if not docker_registry:
            errors.config_error("Definition for environment '{}' is missing the required 'registry' property".format(env_name))

        login_server = utils.safe_value(docker_registry, "login-server")
        if not login_server:
            errors.config_error("Definition for registry '{}' is missing the required 'login-server' property".format(registry_name))

        # philly wants these as a single name
        docker_image = login_server + "/" + docker_image

        # image should look like this: phillyregistry.azurecr.io/microsoft_pytorch:v1.2.0_gpu_cuda9.0_py36_release_gpuenv_hvd0.16.2
        #console.print("philly docker_image=", docker_image)

        # include job_id in name for assist in cancelling by job_id
        # use a pattern to reliably strip off philly prefix and suffix
        philly_name = "/{}/{}/{}/".format(job_id, workspace, run_name)

        # for now, let's focus on single command per nodes
        first_run_name = run_names[0]
        first_wrapped_cmd = wrapped_cmds[0]

        # NOTE: it is not sufficient to just specify env_vars at the 'workers' level, so we specify at top level
        user_env_vars = dict(args["env_vars"])

        first_run = node_runs[0]
        box_secret = first_run["box_secret"]

        env_vars = self.build_env_vars(user_env_vars, workspace, experiment, first_run_name, use_controller, node_id, box_secret, args)

        # build the PHILLY json data
        md = { "name": philly_name, "cluster": cluster, "vc": vc}
        if queue:
            md["queue"] = queue

        nodes = utils.safe_value(compute_def, "nodes", default=1)     # 1

        # in philly, the "count" property specifies the number of docker containers to run with, in a distributed training style, where the output
        # of each container's STDOUT are merged into a one, and the same command line is used in each container.  this will be relevant when xt 
        # supports distributed training for philly, but it is not sufficient for the general xt "nodes" support.  for this reason, we submit
        # a separate philly job for each xt node that we need to run.

        count = 1    # change this for distributed runs

        #workers = {"type": "skuResource", "sku": sku, "count": nodes, "image": docker_image, "environmentVariables": env_vars, "commandLine": wrapped_cmd}
        workers = {"type": "skuResource", "sku": sku, "count": count, "image": docker_image, "commandLine": first_wrapped_cmd, "interactive": hold}

        resources = {"workers": workers}
        input_container = constants.INFO_CONTAINER
        output_container = workspace

        volumes, credentials = self.build_azure_volumes(input_container, utils.DATA_STORE_ROOT, output_container, data_action, 
            data_writable, utils.MODELS_STORE_ROOT, model_action, model_writable, args)

        jd = {"version": "2017-10-01", "metadata": md, "environmentVariables": env_vars, "resources": resources, "volumes": volumes, "credentials": credentials }
        text = json.dumps(jd, indent=4)
        #console.print("json=", text)

        fn = os.path.expanduser("~/.xt/tmp/philly_params.json")
        fn_log = os.path.expanduser("~/.xt/tmp/philly_submit.log")
        file_utils.ensure_dir_exists(file=fn)

        with open(fn, "wt") as outfile:
            outfile.write(text)

        fake_submit = args["fake_submit"]

        if fake_submit:
            service_job_id = "fake_service_id"
        else:
            fn = file_utils.fix_slashes(fn, is_linux=True)
            #curl_cmd = 'curl -k --ntlm --user : -X POST -H "Content-Type: application/json" --data @{} https://philly/api/jobs > {} 2>&1'.format(fn, fn_log)
            curl_cmd = self.build_curl('-X POST -H "Content-Type: application/json" --data @{} https://philly/api/jobs'.format(fn))

            # SUBMIT the job to PHILLY
            result = self.run_curl_cmd(curl_cmd)
            if not "jobId" in result:
                errors.service_error("Unexpected result from Philly job submit: " + str(result))
            service_job_id = result["jobId"]

            mongo = self.store.get_mongo()

            for run_name in run_names:
                # update mongo db info for run with cluster and service_job_id
                mongo.update_mongo_run_from_dict(workspace, run_name, {"cluster": cluster, "vc": vc, "service_run_id": service_job_id})

                #fb.feedback("{}/{}".format(workspace, run_name), id="run_name", add_seperator=False)
                fb.feedback("{}/{}".format(workspace, run_name))
                #console.print("Philly job id:", service_job_id)

        # add service_job_id to runs_by_box entries for this node
        run_datas = runs_by_box[box_name]
        for rd in run_datas:
            rd["service_job_id"] = service_job_id

        # copy to submit-logs
        fnx = "philly_submit_{}.json".format(node_id)
        utils.copy_to_submit_logs(args, fn, fnx)

        service_node_info = {"service_id": service_job_id, "cluster": cluster, "vc": vc, "run_name": run_name, "ws": workspace, 
            "job_id": job_id, "node_id": node_id}

        return service_node_info

    def run_curl_cmd(self, curl_cmd, parse_result=True):
        # run as cmd parts, so we can capture output
        parts = shlex.split(curl_cmd)
        
        # don't redirect errors because that is where PASSWORD PROMPT appears
        run_result = subprocess.run(parts, stdout=subprocess.PIPE) 
        text_result = run_result.stdout.decode('utf-8')
        returncode =  run_result.returncode

        if returncode:      # not text_result:
            msg = "result.returncode=" + str(returncode)
            curl_errors = {6: "Couldn't resolve host"}

            if returncode in curl_errors:
                # errors without msgs
                msg = curl_errors[returncode] + " ({})".format(msg)

            errors.service_error("Unexpected Philly error: {}".format(msg))

        console.diag("run_curl_cmd: result={}".format(text_result))

        # result_text is usually either HTML or JSON
        if parse_result and text_result.startswith("{"):

            try:
                # try to parse as JSON
                text_result = json.loads(text_result)    
                if "Message" in text_result:
                    text_result = text_result["Message"]
            except:
                pass

        return text_result

    def view_console(self, job_id, job_info, info_verb="log", parse_result=True, extra=""):
        '''get snapshot of console output for specified job'''
        # TODO: get this from run
        node_index = 0
        node_id = utils.node_id(node_index)

        service_info_by_node = job_info["service_info_by_node"]  
        node_info = service_info_by_node[node_id]
        philly_job_id = node_info["service_id"]  

        cluster = utils.safe_value(node_info, "cluster")
        vc = utils.safe_value(node_info, "vc")

        log_type = "log"  # log or stdout
        curl_cmd = self.build_curl('"https://philly/api/{}?clusterId={}&vcId={}&jobId={}&logType={}&logRev=latest&content=full&jobType=ns{}"' \
            .format(info_verb, cluster, vc, philly_job_id, log_type, extra))

        result = self.run_curl_cmd(curl_cmd, parse_result)
        return result, philly_job_id

    def list_jobs(self, cluster, vc, username, status=None, max_finished=None, stage_flags=""):
        '''list jobs for specified cluster, vc, username'''
        curl_cmd = self.build_curl('"https://philly/api/list?clusterId={}&vcId={}'.format(cluster, vc))

        if username and username != "all":
            curl_cmd += "&userName=" + username

        if status and status != "all":
            curl_cmd += "&status=" + status

        if max_finished != None:
            curl_cmd += "&numFinishedJobs=" + str(max_finished)

        curl_cmd += '"'  # add the ending quote around the URL

        console.diag("running philly cmd: {}".format(curl_cmd))

        return self.run_curl_cmd(curl_cmd)

    def abort_run(self, workspace, cluster, vc, run_name, service_run_id, before_status=None):

        if not before_status:
            status_cmd = self.build_curl("https://philly/api/status?clusterId={}&vcId={}&jobId={}&jobType=cntk&content=full".format(cluster, vc, service_run_id))
            result = self.run_curl_cmd(status_cmd)

            # Pass, Queued, Running, Failed, Killed
            before_status = result["status"].lower() if "status" in result else "unknown"

        killed = False

        if before_status in ["queued", "running"]:
            abort_cmd = self.build_curl("https://philly/api/abort?clusterId={}&jobId={}".format(cluster, service_run_id))
            result =  self.run_curl_cmd(abort_cmd)
            result = result[service_run_id]

            status = result["status"].lower() if "status" in result else "unknown"
            killed = (status == "cancelled")
        else:
            status = before_status

        cancel_result = {"workspace": workspace, "run_name": run_name, "status": status, "cancelled": killed, "before_status": before_status}
        return cancel_result

    def cancel_runs_by_names(self, workspace, run_names, box_name):
        '''
        Args:
            workspace: the name of the workspace containing the run_names
            run_names: a list of run names
            box_name: the name of the box the runs ran on (pool service)
        Returns:
            cancel_results: a list of kill results records 
                (keys: workspace, run_name, exper_name, killed, status, before_status)
        '''
        cancel_results = []
        run_records = run_helper.get_run_records(self.store, workspace, run_names)

        for rr in run_records:
            cluster = rr["cluster"]
            vc = rr["vc"]
            run_name = rr["_id"]
            service_run_id = rr["service_run_id"]

            cancel_result = self.abort_run(workspace, cluster, vc, run_name, service_run_id)
            cancel_results.append(cancel_result)

        return cancel_results

    def cancel_by_job_core(self, cancel_results, runs_processed, job_id, target_status, target_results):
        # get list of all our jobs (by target_status)
        results = self.list_jobs(self.cluster, self.vc, self.username, status=target_status)
        results = results[target_results]

        for result in results:
            name = result["name"]
            parts = name.split("/")
            if len(parts) == 5:
                #console.print("status=", target_status, ", name=", name)
                prefix, job, workspace, run_name, suffix = parts
                full_name = workspace + "/" + run_name

                if job_id and job != job_id:
                    continue

                if not full_name in runs_processed:
                    # run is part of the job_id we are targeting
                    service_run_id = result["appID"]
                    before_status = result["status"].lower()
                    
                    cancel_result = self.abort_run(workspace, self.cluster, self.vc, run_name, service_run_id, before_status=before_status)
                    cancel_results.append(cancel_result)

                    runs_processed[full_name] = 1

    def cancel_runs_by_job(self, job_id, runs_by_box):
        '''
        Args:
            job_id: the name of the job containing the run_names
            runs_by_box: a dict of box_name/run lists
        Returns:
            cancel_results_by box: a dict of box_name, cancel_result records
                (keys: workspace, run_name, exper_name, killed, status, before_status)
        '''
        cancel_results_by_box = {}
        runs_processed = {}     # don't process a run twice (once from queued, once from running)

        for box_name, runs in runs_by_box.items():        
            cancel_results = []
            self.cancel_by_job_core(cancel_results, runs_processed, job_id, "Queued", "queuedJobs")
            self.cancel_by_job_core(cancel_results, runs_processed, job_id,"Running", "runningJobs")

            cancel_results_by_box[box_name] = cancel_results

        return cancel_results_by_box

    def cancel_runs_by_user(self, box_name):
        '''
        Args:
            box_name: the name of the box the runs ran on (pool service)
        Returns:
            cancel_results: a list of kill results records 
                (keys: workspace, run_name, exper_name, killed, status, before_status)
        '''

        cancel_results = []
        runs_processed = {}     # don't process a run twice (once from queued, once from running)
        
        self.cancel_by_job_core(cancel_results, runs_processed, None, "Queued", "queuedJobs")
        self.cancel_by_job_core(cancel_results, runs_processed, None,"Running", "runningJobs")

        return cancel_results

    def get_ssh_for_run(self, workspace, run_name):
        ''' get the SSH ip address for the specified run'''
        rr = run_helper.get_run_record(self.store, workspace, run_name)

        cluster = rr["cluster"]
        vc = rr["vc"]
        service_run_id = rr["service_run_id"]

        url = "https://philly/api/sshinfo?clusterId={}&vcId={}&jobId={}".format(cluster, vc, service_run_id)     # application_1557431881457_78704"

        curl_cmd = self.build_curl('"{}"'.format(url))
        result = self.run_curl_cmd(curl_cmd)

        containers = result["containers"]
        ssh_cmd = None

        for key, value in containers.items():
            if key != "appmaster":
                ssh_cmd =value
                break

        return ssh_cmd

    # BACKEND API
    def get_node_status(self, service_node_info):
        # https://philly/api/status?clusterId=gcr&vcId=pnrsy&jobId=application_1447977864059_0276&jobType=cntk&content=partial

        cluster = service_node_info["cluster"]
        vc = service_node_info["vc"]
        philly_job_id = service_node_info["service_id"]

        curl_cmd = self.build_curl('"https://philly/api/status?clusterId={}&vcId={}&jobId={}&content=partial"' \
            .format(cluster, vc, philly_job_id))

        result = self.run_curl_cmd(curl_cmd, parse_result=True)
        status = utils.safe_value(result, "status", "unknown")
        return status

    # BACKEND API
    def read_log_file(self, service_node_info, log_name, start_offset=0, end_offset=None, 
        encoding='utf-8', use_best_log=True):
        '''
        returns subset of specified log file as text.
        '''
        cluster = service_node_info["cluster"]
        vc = service_node_info["vc"]
        philly_job_id = service_node_info["service_id"]

        log_type = "stdout"  # log or stdout
        info_verb = "log"
        extra = ""

        try:
            philly_status = self.get_node_status(service_node_info)
        except Exception as ex:
            console.print("Exception in read_log_file: get_node_status ex=" + str(ex))
            philly_status = "unknown"

        simple_status = self.get_simple_status(philly_status)

        curl_cmd = self.build_curl('"https://philly/api/{}?clusterId={}&vcId={}&jobId={}&logType={}&logRev=latest&content=full&jobType=ns{}"' \
            .format(info_verb, cluster, vc, philly_job_id, log_type, extra))
        
        try:
            result = self.run_curl_cmd(curl_cmd, parse_result=True)
        except BaseException as ex:
            console.print("Exception in read_log_file: run_curl_cmd ex=" + str(ex))
            philly_status = "unknown"
            result = ""

        if result == "\n":      
            # some clusters need log_type "log" (vs. "stdout")
            log_type = "log"

            curl_cmd = self.build_curl('"https://philly/api/{}?clusterId={}&vcId={}&jobId={}&logType={}&logRev=latest&content=full&jobType=ns{}"' \
                .format(info_verb, cluster, vc, philly_job_id, log_type, extra))

            try:
                result = self.run_curl_cmd(curl_cmd, parse_result=True)
            except:
                console.print("Exception in read_log_file: run_curl_cmd ex=" + str(ex))
                philly_status = "unknown"
                result = ""

        if len(result) > 1:
            node_status = "running"

        if end_offset:
            new_text = result[start_offset:1+end_offset]
        else:
            new_text = result[start_offset:]

        next_offset = start_offset + len(new_text)

        return {"new_text": new_text, "simple_status": simple_status, "log_name": log_name, "next_offset": next_offset, 
            "service_status": philly_status}

    # API call
    def get_simple_status(self, status):
        # translates an Philly status to a simple status (queued, running, completed)

        queued = ["Queued"]
        running = ["Running"]
        completed = ["Pass", "Failed", "Killed", "unknown"]

        if status in queued:
            ss = "queued"
        elif status in running:
            ss = "running"
        elif status in completed:
            ss = "completed"
        else:
            errors.internal_error("unexpected Philly status value: {}".format(status))

        return ss

    # API call
    def cancel_job(self, service_job_info, service_info_by_node):
        result_by_node = {}

        for node_id, node_info in service_info_by_node.items():
            result = self.cancel_node(node_info)
            result_by_node[node_id] = result

        return result_by_node

    # API call
    def cancel_node(self, service_node_info):
        cluster = service_node_info["cluster"]
        vc = service_node_info["vc"]
        philly_job_id = service_node_info["service_id"]

        philly_status = self.get_node_status(service_node_info)
        simple_status = self.get_simple_status(philly_status)
        cancelled = False

        if simple_status != "completed":
            
            abort_cmd = self.build_curl("https://philly/api/abort?clusterId={}&jobId={}".format(cluster, philly_job_id))
            result =  self.run_curl_cmd(abort_cmd)
            result = result[philly_job_id]

            philly_status = result["status"]
            simple_status = self.get_simple_status(philly_status)
            cancelled = (philly_status == "Killed")     

        result = {"cancelled": cancelled, "service_status": philly_status, "simple_status": simple_status}
        return result
