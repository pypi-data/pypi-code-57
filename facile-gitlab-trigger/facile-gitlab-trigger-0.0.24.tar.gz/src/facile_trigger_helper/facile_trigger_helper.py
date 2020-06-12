"""GitLab trigger module.
This module helps docker bypassing "multi-project pipelines"
capability which is covered on on gitLab silver or higher.
"""

import sys
import time
import argparse
from typing import List
from colors import color
import pyfiglet
import gitlab
import yaml


class Runner:
    """
    runnable object which modelate trigger data
    """

    def __init__(self, path, where, device, browser, platform, version):
        self.path = path
        self.where = where
        self.device = device
        self.browser = browser
        self.platform = platform
        self.version = version
#    def __init__(self, **kwargs):
#        init_keys = ["path", "where", "device", "browser", "os", "version"]
#        for key in init_keys:
#            setattr(self, key, kwargs.get(key))

class facile_trigger_helper:
    """

        :param args:
        :return: Args trasformed by the user
    """
    def __init__(self):
        self.flag = True

    @staticmethod
    def convert_args(args: List[str]):

        """

        :param args:
        :return: Args trasformed by the user
        """
        parser = argparse.ArgumentParser(
            description='Gilab trigger helper',
            add_help=False)
        parser.add_argument('-a', '--api-token', required=True,
                            help='personal access token (not required when running detached)',
                            dest='gitlab_api_token')
        parser.add_argument('-h', '--host', default='gitlab.com', dest="git_lab_host")
        parser.add_argument('--help', action='help', help='show this help message and exit')
        parser.add_argument('-t', '--target-ref', default='master',
                            help='target ref (branch, tag, commit)', dest='target_branch')
        parser.add_argument('-p', '--project-id', required=True,
                            help='repository id found on settings', dest='project_id')
        parser.add_argument('-b', '--branch-merged', required=True,
                            help='filled by git COMMIT_REF_NAME ', dest='ref_name')
        parser.add_argument('-f', '--yaml-file', required=True,
                            help='filled by git COMMIT_REF_NAME ', dest='yaml_file')

        parsed_args = parser.parse_args(args)

        return parsed_args

    @staticmethod
    def check_project(string_project, yaml_file):
        """

        :project_id variable aims gitlab id found on project >> General:
        """
        runner = []
        print(yaml_file)
        with open(yaml_file) as file:
            projects = yaml.safe_load(file)

            for k, val in projects["projects"].items():

                path = projects["projects"][k]["path"]
                project_id = projects["projects"][k]["project_id"]
                where = projects["projects"][k]["where"]
                browser = projects["projects"][k]["browser"]
                platform = projects["projects"][k]["platform"]
                version = projects["projects"][k]["version"]

                if where == "mobile":
                    device = projects["projects"][k]["device"]
                else:
                    device = ""

                if str(project_id) in string_project.upper():
                    if where == "mobile":
                        print(color("Test will run against " + device, fg='yellow'))
                    else:
                        print(color("Test will run against " + platform + " " + browser, fg='yellow'))
                    runner.append(Runner(path, where, device, browser, platform, version))

            return runner

    def main(self, args: List[str]):

        """

        :project_id variable aims gitlab id found on project >> General:
        """
        # Require parameters
        args = self.convert_args(args)
        assert args.gitlab_api_token, 'token should be set'
        assert args.project_id, 'project id must be set'
        assert args.yaml_file, 'please provide valid yaml path'

        #  Moving args to local variables
        git_lab_host = args.git_lab_host
        project_id = args.project_id
        api_gilab_token = args.gitlab_api_token
        target_branch = args.target_branch

        # ref_name = args.ref_name
        print(args.ref_name)
        runnable_list = self.check_project(args.ref_name, args.yaml_file)

        if not runnable_list:
            print(color("Running default profile", fg='yellow'))
            runnable_list = self.check_project("default", args.yaml_file)

        if runnable_list:
            facile_trigger = pyfiglet.figlet_format("facile.it Trigger Helper", font="larry3d")
            print(color(facile_trigger, fg='yellow'))
            self.trigger_pipeline(runnable_list, git_lab_host, api_gilab_token,
                                           target_branch, project_id)

    def trigger_pipeline(self, runnable_list, git_lab_host, api_gilab_token, target_branch, project_id):
        """

        :project_id variable aims gitlab id found on project >> General:
        """
        pl_list = []
        git_trigger = gitlab.Gitlab(git_lab_host, private_token=api_gilab_token)
        project = git_trigger.projects.get(project_id)

        for runnable in runnable_list:
            create_pipeline = project.pipelines.create(
                {'ref': target_branch, 'variables': [{'key': 'RF_PATH', 'value': runnable.path},
                                                     {'key': 'WHERE', 'value': runnable.where},
                                                     {'key': 'DEVICE', 'value': runnable.device},
                                                     {'key': 'PLATFORM', 'value': runnable.platform},
                                                     {'key': 'VERSION', 'value': runnable.version},
                                                     {'key': 'BROWSERNAME', 'value': runnable.browser},
                                                     ]})
            pl_list.append(create_pipeline)

        for current_pipe in pl_list:
            pipeline = project.pipelines.get(current_pipe.id)
            
            pipe_jobs = pipeline.jobs.list()
            pipeline_jobs_count = len(pipe_jobs)
            pipeline_jobs_count = str(pipeline_jobs_count)
            print(color("Triggered pipeline holds " + pipeline_jobs_count + " jobs", fg='yellow'))
            timeout = time.time() + 60 * 30
            retry = False
            while pipeline.finished_at is None:
                
                
                pipeline.refresh()
                job_trace = pipeline.jobs.list()[0]
                job = project.jobs.get(job_trace.id, lazy=True)

                if pipeline.status == "pending":
                    print(color(project.name + " is " + pipeline.status, fg='yellow'))

                #TODO retry running 
                elif "Binary crashed" in str(job.trace()) and not retry:
                #    if retry:    
                #        status = False
                #    else:
                    print(color("Binary crashed, cancelling...", fg='red'))
                    pipeline.cancel()
                    time.sleep(10)
                    pipeline.retry()

                elif pipeline.status == "running":
                    print(color(project.name + " is " + pipeline.status + " on " + pipeline.web_url, fg='blue'))

                elif pipeline.status == "success":
                    print(color(project.name + " is " + pipeline.status, fg='green'))

                elif pipeline.status == "failed":
                    print(color(project.name + " is " + pipeline.status + " please check on " + pipeline.web_url, fg='red'))
                    self.flag = False and self.flag

                elif pipeline.status == "canceled":
                    print(color(project.name + " is " + pipeline.status, fg='red'))
                    self.flag = False and self.flag

                elif time.time() > timeout:
                    print(color(project.name + " is " + pipeline.status, fg='red'))
                    self.flag = False and self.flag

                time.sleep(2)

def run_cli(arguments=None):
    """

    :project_id variable aims gitlab id found on project >> General:
    """
    if arguments is None:
        arguments = sys.argv[1:]

    obj_trigger = facile_trigger_helper()
    obj_trigger.main(arguments)

    if not obj_trigger.flag:
        sys.exit(1)

if __name__ == '__main__':
    run_cli(sys.argv[1:])
