from cnvrg.modules.cnvrg_job import CnvrgJob, LOGS_TYPE_OUTPUT, LOGS_TYPE_ERROR
import cnvrg.helpers.param_build_helper as param_build_helper
from cnvrg.modules.project import Project
import cnvrg.helpers.logger_helper as logger_helper
import cnvrg.helpers.string_helper as string_helper
from cnvrg.modules.errors import UserError
import cnvrg.helpers.apis_helper as apis_helper
import cnvrg.helpers.spawn_helper as spawn_helper
import cnvrg.helpers.control_stdout_helper as control_stdout_helper
import cnvrg.helpers.env_helper as env_helper
import cnvrg.helpers.chart_show_helper as chart_show_helper
from cnvrg.helpers.env_helper import in_experiment
from cnvrg.helpers.url_builder_helper import url_join
from cnvrg.modules.mixins.charts_mixin import ChartsMixin
from cnvrg.helpers.param_helper import wrap_string_to_list
from cnvrg.helpers.libs_helper import check_if_lib_exists
from cnvrg.modules.errors import CnvrgError
from enum import Enum
from typing import List, AnyStr
from cnvrg.helpers.error_catcher import suppress_exception
import numpy as np
import types
import os
import time


class TagType(Enum):
    SINGLE_TAG = "single"
    LINECHART_TAG = "linechart"


class Experiment(CnvrgJob, ChartsMixin):
    def __init__(self, experiment=None, owner=None):
        default_owner, project_slug, slug = param_build_helper.parse_params(experiment, param_build_helper.EXPERIMENT)
        owner = owner if owner is not None else default_owner
        if not in_experiment() and not slug:
            raise UserError("Cant create an experiment without slug and outside experiment run")
        slug = slug or env_helper.get_current_job_id()
        super(Experiment, self).__init__(slug, env_helper.EXPERIMENT, Project(url_join(owner, project_slug)))
        self.__data = self.__get_experiment()
        self.chart_metrics = {}

    @staticmethod
    @suppress_exception
    def _create_clean_experiment(project=None, **kwargs):
        if isinstance(project, str):
            project = Project(project)
        project = project or Project()
        resp = apis_helper.post(url_join(project.get_base_url(), 'experiments', 'local'),
                                data={"commit": project.get_current_commit(), **kwargs, **env_helper.get_origin_job()})
        e = resp.get("experiment")
        exp = Experiment(url_join(project.get_project_name(), e.get("slug")), owner=project.owner)
        exp.notify_running()
        exp.set_as_default()
        return exp

    def notify_running(self):
        logger_helper.log_message(
            "{title} is running, follow live at: {url}".format(title=self['title'], url=self.href()))

    def set_as_default(self):
        env_helper.set_current_job_id(self.job_slug)
        env_helper.set_current_job_type("Experiment")


    @staticmethod
    def __run_callable(function_command, title=None, project=None, cwd=None, library=None, **kwargs):
        experiment = Experiment._create_clean_experiment(title=title, project=project, library=library, **kwargs)
        exit_status = control_stdout_helper.\
            run_callable(function_command, arguments=[experiment], callback=lambda x: experiment.log(x), err_callback=lambda x: experiment.log(x, log_type=LOGS_TYPE_ERROR))
        experiment.finish(exit_status=exit_status)
        return experiment

    @staticmethod
    def __run_local(cmd, **kwargs):
        def function_command(experiment=None):
            env = None
            if experiment: env = experiment.as_env()
            return spawn_helper.run_sync(cmd, print_output=True, cwd=kwargs["cwd"], env=env)
        return Experiment.__run_callable(function_command, cmd=cmd, **kwargs)


    def as_env(self):
        return {
            env_helper.ENV_KEYS["current_job_id"]: self.job_slug,
            env_helper.ENV_KEYS["current_job_type"]: "Experiment",
            env_helper.ENV_KEYS["current_project"]: self.project.slug,
            env_helper.ENV_KEYS["current_organization"]: self.project.owner,
        }

    def sync(self, output_dir='output'):
        payload = {
            "job_type": "Experiment",
            "job": self.job_slug,
            "in_exp": "true",
        }
        if self.project.is_git():
            payload["output_dir"] = output_dir

        self.project.sync(**payload)

    def log_artifacts(self, files: list):
        payload = {
            "job_type": "Experiment",
            "job": self.job_slug,
            "in_exp": "true",
            "files": files,
        }
        self.project.sync(**payload)

    @suppress_exception
    def restart(self, message=None, sync=True):
        if not in_experiment():
            raise UserError("Cant restart an experiment outside the experiment itself.")
        if sync: self.sync()
        return apis_helper.post(url_join(self._base_url(), 'restart'), data={"message": message})

    @staticmethod
    def get_utilization():
        return spawn_helper.analyze_pid(pid=os.getpid())

    @suppress_exception
    def __latest_artifacts(self, commit=None):
        resp = apis_helper.get(url_join(self._base_url(), 'artifacts'), {"commit": commit})
        if not resp: return None
        return resp.get("artifacts")

    def artifacts(self, commit=None):
        artifacts = self.__latest_artifacts(commit=commit)
        if not artifacts: return []
        return artifacts

    def __wait_until_success(self, fetch_info=60):
        status = None
        is_running = True
        while status != 'Success' and is_running:
            info = self.__get_experiment()
            if info is None:
                return None
            status = info.get("status")
            is_running = info.get("is_running")
            if status == 'Success':
                return {"status": status, "end_commit": info.get("end_commit")}
            if is_running:
                time.sleep(fetch_info)
        return {"status": status}

    @suppress_exception
    def pull_artifacts(self, path=".", commit=None,wait_until_success=False,fetch_info=60):
        if wait_until_success:
            success_resp = self.__wait_until_success(fetch_info=fetch_info)
            if success_resp and success_resp.get("status") == 'Success':
                commit = success_resp.get("end_commit")
            else:
                raise CnvrgError("Experiment has finished with status: {}, can't pull artifacts".format(success_resp.get("status")))

        artifacts = self.artifacts(commit=commit)
        mapped_files = []
        for artifact in artifacts:
            try:
                fpath = os.path.join(path, artifact.get("fullpath"))
                os.makedirs(os.path.dirname(fpath), exist_ok=True)
                artifact_path = apis_helper.download_file(artifact.get("url"), fpath)
                mapped_files.append({**artifact, **{"path": os.path.abspath(artifact_path)}})
            except Exception as e:
                print(e)
                print("Error while downloading {}".format(artifact.get("name")))
        return mapped_files

    @staticmethod
    def run(command=None, arguments: dict=None, grid: dict=None, title: str=None, project: Project=None, compute: str=None, output_dir: str=None, computes: List=None,
            datasets: List=None, dataset: str=None, local: bool=False, library: str=None, working_directory: str=None, sync_before: bool=True, sync_after: bool=True,
            prerun: bool=True, requirements: bool=True, image: str=None, schedule: str=None, recurring: str=None, git_commit: str=None, git_branch: str=None,
            local_folders: List=None, notify_on_error: bool=False, notify_on_success: bool=False, emails_to_notify: List=None, **kwargs):
        function_command = None
        project = project or Project()
        if sync_before == None: sync_before = not project.git
        if project.git:
            git_commit = git_commit or project.get_git_commit()
            output_dir = output_dir or "output"
            git_branch = git_branch or project.get_git_branch()

        ## sync before
        if sync_before: project.sync(**CnvrgJob.current_job_sync_args(output_dir=output_dir))
        ## support
        computes = computes or wrap_string_to_list(computes) or wrap_string_to_list(compute) or []
        ### by default (if computes empty or no compute) set the local to True
        if local: pass
        elif "local" in computes: local = True
        elif arguments: local = False
        elif grid: local = False
        elif len(computes) == 0: local = True

        ### if command is function, run it as a function and not as a os command
        if isinstance(command, types.FunctionType): function_command = command

        ## merge datasets
        datasets = datasets or wrap_string_to_list(datasets) or wrap_string_to_list(dataset) or []
        if local:
            Experiment.__verify_local_params(computes, datasets, image, arguments or grid)
            if function_command:
                ## set the title to "func: {name of the function}"
                cmd = "func: {func_name}".format(func_name=function_command.__name__)
                experiment = Experiment.__run_callable(function_command, title=title, project=project, library=library, cmd=cmd, git_commit=git_commit, output_dir=output_dir, git_branch=git_branch)
                if not experiment: raise UserError("Cant run experiment, please check your input params")
            else:
                experiment = Experiment.__run_local(cmd=command, title=title, project=project, cwd=working_directory, git_commit=git_commit, git_branch=git_branch,
                                                    library=library)
                if not experiment: raise UserError("Cant run experiment, please check your input params")
        else:
            ## perform an api call to create it.
            Experiment.__verify_remote_params(function_command)
            e = project.run_task(command, arguments=arguments, title=title, templates=computes, datasets=datasets,
                                 library=library,  prerun=prerun, requirements=requirements,
                                 grid=grid,git_branch=git_branch, git_commit=git_commit, output_dir=output_dir, image=image, schedule=schedule, recurring=recurring,
                                 local_folders=local_folders, notify_on_error=notify_on_error, notify_on_success=notify_on_success, emails_to_notify=emails_to_notify, **kwargs)
            if len(e.get("experiments")) == 1:
                exp = Experiment(e.get("experiments")[0], owner=project.owner)
                exp.notify_running()
                exp.set_as_default()
                return exp
            else:
                hyper_search_url = url_join(project.web_url(),
                                            "experiments?grid={grid}".format(grid=e.get("slug")[0:4]))
                logger_helper.log_message(
                    "Grid {grid_slug} is running, follow at: {url}".format(grid_slug=e.get("slug"),
                                                                           url=hyper_search_url))
                return [Experiment(exp_id, owner=project.owner) for exp_id in e.get("experiments")]

        if sync_after:
            project.sync(**CnvrgJob.current_job_sync_args(job=experiment['slug'], job_type="Experiment", output_dir=output_dir))
            experiment.__update(end_commit=project.get_current_commit())
        return experiment


    @staticmethod
    def __verify_local_params(computes: List, datasets: List, image: str, arguments: dict):
        if len(computes) > 0 and "local" not in computes:
            logger_helper.log_warn("Computes list: {compute} will be ignored because running on local machine".format(compute=",".join(computes)))
        if len(datasets) > 0:
            logger_helper.log_warn("Dataset list: {datasets} will be ignored because running on local machine".format(datasets=",".join(ds.get("id") for ds in datasets)))
        if image:
            logger_helper.log_warn("Image: {image} will be ignored because running on local".format(image=image))
        if arguments:
            logger_helper.log_warn("Arguments will be ignored because running on local machine")

    @staticmethod
    def __verify_remote_params(function_command):
        if function_command:
            logger_helper.log_warn("Can't run a function command on remote experiment. please use local compute instead.")
            raise UserError("Can't run a function command on remote experiment. please use local compute instead.")


    def log_param(self, key, value=None):
        tag_data = {
            "key": key,
            "value": value,
            "type": TagType.SINGLE_TAG.value
        }
        self.__send_tag(tag_data)

    def __dict__(self):
        return self.__data

    def log_metric(self, key, Ys: List, Xs: List=None, grouping: List=None, x_axis=None, y_axis=None) -> None:
        """
        a function which can tag an experiment with a chart
        :param key: the name of the chart
        :param Ys: [y1, y2, y3, y4] (float)
        :param Xs: [x1, x2, x3, x4] (date, integer, null)
        :param grouping: [g1, g2, g3, g4]
        :param x_axis: rename the x_axis of the chart
        :param y_axis:rename the y_axis of the chart
        :return:
        """
        if isinstance(Xs, np.ndarray):
            Xs = Xs.tolist()
        if isinstance(Ys, np.ndarray):
            Ys = Ys.tolist()

        if Xs is None or not isinstance(Xs, list):
            if key in self.chart_metrics:
                x_stamp = self.chart_metrics[key]
            else:
                self.chart_metrics[key] = 0
                x_stamp = 0
            Xs = [*range(x_stamp, x_stamp + len(Ys))]
            self.chart_metrics[key] += len(Ys)

        tag_data = {
            "ys": Ys,
            "xs": Xs,
            "key": key,
            "grouping": grouping,
            "x_axis": x_axis,
            "y_axis": y_axis,
            "type": TagType.LINECHART_TAG.value,
        }
        self.__send_tag(tag_data)

    def logs(self, callback=None, poll_every=5):
        job_logs, experiment_is_running = self.__fetch_logs(0)
        offset = len(job_logs)
        callback = callback or logger_helper.log_cnvrg_log
        [callback(l) for l in job_logs]
        while experiment_is_running:
            time.sleep(poll_every)
            job_logs, experiment_is_running = self.__fetch_logs(offset)
            offset += len(job_logs)
            ## filter unknown logs?
            [callback(l) if l else None for l in job_logs]


    @property
    def title(self):
        return self["title"]

    @title.setter
    @suppress_exception
    def title(self, new_title):
        apis_helper.put(url_join(self._base_url(), 'title'), data={"title": new_title})
        self.__data = self.__get_experiment()

    def set_title(self,new_title):
        self.title = new_title

    @suppress_exception
    def show_chart(self, key, **kwargs):
        """

        :param key: chart_key
        :param kwargs: with_legend, legend_loc
        :return:
        """
        chart = apis_helper.get(url_join(self._base_url(), 'charts', key)).get("chart")

        return chart_show_helper.show_chart(chart, **kwargs)

    @suppress_exception
    def __fetch_logs(self, offset, limit=None):
        resp = apis_helper.get(url_join(self._base_url(), 'logs'), data={"offset": offset, "limit": limit})
        return resp.get("logs"), resp.get("experiment").get("is_running")

    @suppress_exception
    def __send_tag(self,tag_data):
        apis_helper.post(url_join(self._base_url(), 'tags'), data={"tag": tag_data})

    @suppress_exception
    def finish(self, exit_status=None):
        apis_helper.post(url_join(self._base_url(), 'finish'), data={"exit_status": exit_status})

    def href(self):
        return self.__data.get("full_href")

    def open(self):
        if check_if_lib_exists("webbrowser"):
            import webbrowser
            webbrowser.open(self.href())
        else:
            logger_helper.log_message("You can find the experiment in: {href}".format(href=self.href()))

    @suppress_exception
    def __get_experiment(self):
        resp = apis_helper.get(self._base_url())
        if not resp: return None
        return resp.get("experiment")

    def _base_url(self):
        return url_join(
            #### hackish :D
            self.project.get_base_url(),string_helper.to_snake_case(self.job_type) + "s", self.job_slug
        )

    def __getitem__(self, item):
        return self.__data.get(item)

    @suppress_exception
    def __update(self, title: str=None, end_commit: str=None):
        payload = {}
        if title: payload["title"] = title
        if end_commit: payload["end_commit"] = end_commit
        return apis_helper.put(self._base_url(), data={"experiment":payload})
