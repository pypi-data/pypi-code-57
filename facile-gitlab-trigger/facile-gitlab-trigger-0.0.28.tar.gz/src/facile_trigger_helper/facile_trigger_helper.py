"""GitLab trigger module.
This module helps docker bypassing "multi-project pipelines"
capability which is covered on on gitLab silver or higher.
"""

import sys
import time
import argparse
from typing import List
import datetime
from colors import color
import pyfiglet
import gitlab
import yaml


class Runner:
    """
    runnable object which modelate trigger data
    """

    def __init__(self, path, where, device, browser, platform, version, project_id):
        self.path = path
        self.where = where
        self.device = device
        self.browser = browser
        self.platform = platform
        self.version = version
        self.project_id = project_id

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
        -h GitLab host for instance "https://gitlab.facile.it" or "https://gitlab.com"
        -t automation branch which our auotmation are (suggested on MASTER)
        -p automation project id where our automation lives
        -b here is a sort of rule which dev teams should define which keyword will trigg our automation
        -f yaml file which holds the things which should be tested
        -u Create a tunnel using puppet project
        -k Load the capabilities from the project when it is static.
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
        parser.add_argument('-f', '--yaml-file', required=False,
                            help='Yaml file which contains runners', dest='yaml_file')
        parser.add_argument('-k', '--by-project', required=False,
                            help='Runs by project capabilities', dest='by_project', default=False)
        parser.add_argument('-u', '--create-tunnel', required=False,
                            help='create tunnel by trigger', dest='create_tunel', default=False)
        parser.add_argument('-e', '--env-automation', required=False,
                            help='environment to test', dest='env_auto', default="https://qa1.facile.it")

        parsed_args = parser.parse_args(args)

        return parsed_args

    @staticmethod
    def check_project(string_project, yaml_file, by_project):
        """

        :project_id variable aims gitlab id found on project >> General:
        :yaml_file holds the path where we have our automation list:
        :by_project is a flag that once is "True" won't load local yaml
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

                if str(project_id) in string_project.upper() or by_project:
                    if where == "mobile" and not by_project:
                        print(color("Test will run against " + device, fg='yellow'))
                    elif where == "desktop" and not by_project:
                        print(color("Test will run against " +
                                    platform + " " + browser, fg='yellow'))
                    else:
                        print(color("Test will run by project capabilities", fg='yellow'))
                    runner.append(Runner(path, where,
                                         device, browser, platform, version, project_id))

            return runner

    def main(self, args: List[str]):

        """

        :project_id variable aims gitlab id found on project >> General:
        """
        runnable_list = []
        facile_env = "dev"
        # Require parameters
        args = self.convert_args(args)
        # Here where we put our required parameters
        assert args.gitlab_api_token, 'token should be set'
        assert args.project_id, 'project id must be set'
        yaml_file = args.yaml_file #, 'please provide valid yaml path'
        by_project = args.by_project

        #  env to run
        if args.env_auto:
            facile_env = args.env_auto

        print(color("Running automation on " + facile_env + " env", fg='yellow'))
        #  Moving args to local variables
        git_lab_host = args.git_lab_host
        project_id = args.project_id
        api_gilab_token = args.gitlab_api_token
        target_branch = args.target_branch
        create_tunel = args.create_tunel

        # generate tunnel name
        time_stamp = time.time()
        time_stamp_formated = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d-%H-%M-%S')
        tunnel_name = "facile-trigger-" + time_stamp_formated
        
        # ref_name = args.ref_name
        print(args.ref_name)

        if not by_project and yaml_file:
            print(color("Loading dev local profile", fg='yellow'))
            runnable_list = self.check_project(args.ref_name, args.yaml_file, by_project) 

        # here load default list once the project do not want to run test by rules
        if not runnable_list and not by_project:
            print(color("Running default profile", fg='yellow'))
            runnable_list = self.check_project("default", args.yaml_file, by_project)

        # here once the flag by project is true will run static automation getting caps directly in the target project
        if not runnable_list and by_project:
            runner = []
            print(color("Caps profile will run on gitlab.ci target file", fg='yellow'))
            #runnable_list = self.check_project("default", args.yaml_file, by_project)
            runner.append(Runner(path="test", where="", device="", browser="", platform="", version="", project_id=project_id))

            failed_list = self.trigger_pipeline(runner, git_lab_host, api_gilab_token,
                                                target_branch, project_id, tunnel_name)

        # here will run automation list loaded by rules or default
        if runnable_list and not by_project:
            # once the flag tunnel was true will create a tunnel to run the automation
            if create_tunel:
                lambdatest = self.create_tunnel(api_gilab_token, git_lab_host, tunnel_name)

            facile_trigger = pyfiglet.figlet_format("facile.it Trigger Helper", font="larry3d")
            print(color(facile_trigger, fg='yellow'))
            failed_list = self.trigger_pipeline(runnable_list, git_lab_host, api_gilab_token,
                                                target_branch, project_id, tunnel_name, facile_env)

        # Here load the list with the failed automation
        if failed_list:
            count_failed = str(len(failed_list))
            print(color(count_failed + " pipeline(s) failed:", fg='red'))
            for pipe_line_failed in failed_list:
                print(color(pipe_line_failed.web_url, fg='red'))

        # if the tunnel was true delete after running 
        if create_tunel:
            self.delete_tunnel(lambdatest)

    def create_tunnel(self, api_gilab_token, git_lab_host, tunnel_name):
        """

        :Method create a tunnel
        """
        print(color("creating tunnel", fg='yellow'))
        project_id = "705"
        git_trigger = gitlab.Gitlab(git_lab_host, private_token=api_gilab_token)
        project = git_trigger.projects.get(project_id)
        # trigg pipeline which has the tunnel
        create_pipeline = project.pipelines.create({'ref': 'master', 'variables': [{'key': 'T_NAME', 'value': tunnel_name},]})

        pipeline = project.pipelines.get(create_pipeline.id)

        return pipeline


    def delete_tunnel(self, pipeline):
        """

        :Method deletes the tunnel created previously
        """
        print(color("removing tunnel", fg='yellow'))
        pipeline.cancel()

    def trigger_pipeline(self, runnable_list, git_lab_host, api_gilab_token, target_branch, project_id, tunnel_name, facile_env):
        """
        :param args:
        :runnable_list: holds the test runner files 
        :git_lab_host: for instance "https://gitlab.facile.it" or "https://gitlab.com"
        :api_gilab_token: git lab api token
        :target_branch: branch where automation testing is present
        :project_id: Automation project where is present the test that will run
        :tunnel_name: once the flag -u was true where will get the tunnel name
        """
        # support list to run and watch each test inside the pipeline 
        pl_list = []

        # support list which loads each failed test
        failed_list = []

        git_trigger = gitlab.Gitlab(git_lab_host, private_token=api_gilab_token)
        project = git_trigger.projects.get(project_id)

        # create pipeline base on capability passed from dev projects
        # For each created to run all the tests present in the yaml file
        for runnable in runnable_list:
            create_pipeline = project.pipelines.create(
                {'ref': target_branch, 'variables': [{'key': 'RF_PATH', 'value': runnable.path},
                                                     {'key': 'WHERE', 'value': runnable.where},
                                                     {'key': 'DEVICE', 'value': runnable.device},
                                                     {'key': 'PLATFORM', 'value': runnable.platform},
                                                     {'key': 'VERSION', 'value': runnable.version},
                                                     {'key': 'BROWSERNAME', 'value': runnable.browser},
                                                     {'key': 'PROJECT', 'value': runnable.project_id},
                                                     {'key': 'T_NAME', 'value': tunnel_name},
                                                     {'key': 'START_URL', 'value': facile_env},
                                                     ]})
            pl_list.append(create_pipeline)

        # interate within each pipeline | test running
        for current_pipe in pl_list:
            pipeline = project.pipelines.get(current_pipe.id)

            pipe_jobs = pipeline.jobs.list()
            pipeline_jobs_count = len(pipe_jobs)
            pipeline_jobs_count = str(pipeline_jobs_count)
            print(color("Triggered pipeline holds " + pipeline_jobs_count + " jobs", fg='yellow'))
            timeout = time.time() + 60 * 60

            # receive each pipeline created to check when stop "to watch" test runners
            while pipeline.finished_at is None:
                
                pipeline.refresh()

                if pipeline.status == "pending":
                    print(color(project.name + " is " + pipeline.status, fg='yellow'))

                elif pipeline.status == "running":
                    print(color(project.name + " is " + pipeline.status + " on " + pipeline.web_url, fg='blue'))

                elif pipeline.status == "success":
                    print(color(project.name + " is " + pipeline.status, fg='green'))

                elif pipeline.status == "failed":
                    print(color(project.name + " is " + 
                                pipeline.status + " please check on " + pipeline.web_url, fg='red'))
                    self.flag = False and self.flag

                elif pipeline.status == "canceled":
                    print(color(project.name + " is " + pipeline.status, fg='red'))
                    self.flag = False and self.flag

                elif time.time() > timeout:
                    print(color(project.name + " is " + pipeline.status, fg='red'))
                    self.flag = False and self.flag

                time.sleep(2)

            # add failed pipeline to a list
            if pipeline.status == "failed":
                print("adding " + pipeline.web_url + " on failed list")
                failed_list.append(pipeline)
        
        return failed_list

def run_cli(arguments=None):
    """

    :Get args passed from the terminal and place in the gitlabrunner:
    """
    if arguments is None:
        arguments = sys.argv[1:]

    obj_trigger = facile_trigger_helper()
    obj_trigger.main(arguments)

    if not obj_trigger.flag:
        sys.exit(1)

if __name__ == '__main__':
    run_cli(sys.argv[1:])
