# -*- coding: utf-8 -*-

from attr import attrs, attrib
import concurrent.futures
import json
import queue
import random
import re
import requests
import time
import tuxbuild.exceptions

# We will poll for status change for an average duration of 180 minutes
state_timeout = 10800  # 60 * 180
delay_status_update = 30


def post_request(url, headers, request):
    retry_attempts = 3
    for i in range(1, retry_attempts + 1):
        try:
            response = requests.post(url, data=json.dumps(request), headers=headers)
        except requests.exceptions.ConnectionError as e:
            # We are getting exception from either from Network error
            if i == retry_attempts:
                raise e
            else:
                time.sleep(random.randrange(15))
                continue
        if response.ok:
            return json.loads(response.text)
        else:
            if response.status_code == 400:
                response_data = json.loads(response.text)
                raise tuxbuild.exceptions.BadRequest(
                    f"{response_data.get('status_message')}"
                )
            elif response.status_code in [500, 504] and i < retry_attempts:
                time.sleep(random.randrange(15))
            else:
                response.raise_for_status()


def get_request(url, headers):
    retry_attempts = 30
    for i in range(1, retry_attempts + 1):
        try:
            r = requests.get(url, headers=headers)
        except requests.exceptions.ConnectionError as e:
            # We are getting exception from either from Network error
            if i == retry_attempts:
                raise e
            else:
                time.sleep(random.randrange(15))
                continue
        if r.status_code == 200:
            return json.loads(r.text)
        elif r.status_code in [500, 504, 400] and i < retry_attempts:
            time.sleep(random.randrange(15))
        else:
            r.raise_for_status()  # Some unexpected status that's not caught


@attrs(kw_only=True)
class BuildState:
    build = attrib()
    state = attrib()
    status = attrib(default=None)
    message = attrib()
    warnings = attrib(default=0)
    errors = attrib(default=0)
    icon = attrib()
    cli_color = attrib()
    final = attrib(default=False)


@attrs(kw_only=True)
class Build:
    git_repo = attrib()
    git_ref = attrib(default=None)
    git_sha = attrib(default=None)
    target_arch = attrib()
    kconfig = attrib()
    toolchain = attrib()
    token = attrib()
    kbapi_url = attrib()
    kconfig_allconfig = attrib(default=None)

    build_data = attrib(default=None)
    build_key = attrib(default=None)
    status = attrib(default={})

    def __attrs_post_init__(self):
        if isinstance(self.kconfig, str):
            self.kconfig = [self.kconfig]
        self.headers = {"Content-Type": "application/json", "Authorization": self.token}
        self.verify_build_parameters()

    def __str__(self):
        git_short_log = self.status.get("git_short_log", "")
        kconfig_allconfig_param = ""
        if self.kconfig_allconfig is not None:
            kconfig_allconfig_param = " and {} as kconfig_allconfig".format(
                self.kconfig_allconfig
            )

        if len(self.kconfig) > 1:
            kconfig = f"{self.kconfig[0]}+{len(self.kconfig)-1}"
        else:
            kconfig = self.kconfig[0]
        return "{} {} ({}{}) with {} @ {}".format(
            git_short_log,
            self.target_arch,
            kconfig,
            kconfig_allconfig_param,
            self.toolchain,
            self.build_data,
        )

    @staticmethod
    def is_supported_git_url(url):
        """
        Check that the git url provided is valid (namely, that it's not an ssh
        url)
        """
        return re.match(r"^(git://|https?://).*$", url) is not None

    def generate_build_request(self):
        """ return a build data in a python dict """
        build_entry = {}
        build_entry["git_repo"] = self.git_repo
        if self.git_ref:
            build_entry["git_ref"] = self.git_ref
        if self.git_sha:
            build_entry["git_sha"] = self.git_sha
        build_entry["target_arch"] = self.target_arch
        build_entry["toolchain"] = self.toolchain
        build_entry["kconfig"] = self.kconfig
        if self.kconfig_allconfig is not None:
            build_entry["kconfig_allconfig"] = self.kconfig_allconfig
        return build_entry

    def verify_build_parameters(self):
        """ Pre-check the build arguments """
        assert self.git_repo, "git_repo is mandatory"
        assert self.is_supported_git_url(
            self.git_repo
        ), "git url must be in the form of git:// or http:// or https://"
        assert (self.git_ref and not self.git_sha) or (
            self.git_sha and not self.git_ref
        ), "Either a git_ref or a git_sha is required"
        assert self.target_arch is not None, "target_arch is mandatory"
        assert self.kconfig, "kconfig is mandatory"
        assert self.toolchain, "toolchain is mandatory"
        assert self.headers is not None, "headers is mandatory"

    def build(self):
        """ Submit the build request """
        data = []
        data.append(self.generate_build_request())
        url = self.kbapi_url + "/build"
        json_data = post_request(url, self.headers, data)
        self.build_data = json_data[0]["download_url"]
        self.build_key = json_data[0]["build_key"]

    def get_status(self):
        """ Fetches the build status and updates the values inside the build object"""
        url = self.kbapi_url + "/status/" + self.build_key
        self.status = get_request(url, self.headers)

    def wait_on_status(self, status):
        """
            Wait until the given status changes

            For example, if status is 'queued', wait_for_status
            will return once the status is no longer 'queued'

            Will timeout after state_timeout
        """
        timeout = time.time() + state_timeout

        while time.time() < timeout:
            self.get_status()
            if self.status["tuxbuild_status"] != status:
                break
            time.sleep(random.randrange(delay_status_update))
        else:
            raise tuxbuild.exceptions.Timeout(
                f"Build timed out after {state_timeout/60} minutes; abandoning"
            )

    def watch(self):
        waiting_states = [
            BuildState(
                build=self,
                state="queued",
                message="Queued",
                icon="⏳",
                cli_color="white",
            ),
            BuildState(
                build=self,
                state="building",
                message="Building",
                icon="⚗️ ",
                cli_color="cyan",
            ),
        ]
        for state in waiting_states:
            yield state
            self.wait_on_status(state.state)

        errors = 0
        warnings = 0
        state = self.status["tuxbuild_status"]
        status = self.status["build_status"]

        if status == "pass":
            warnings = self.status["warnings_count"]
            if warnings == 0:
                icon = "🎉"
                message = "Pass"
                cli_color = "green"
            else:
                icon = "👾"
                cli_color = "yellow"
                if warnings == 1:
                    message = "Pass (1 warning)"
                else:
                    message = "Pass ({} warnings)".format(warnings)
        elif status == "fail":
            icon = "👹"
            cli_color = "bright_red"
            errors = self.status["errors_count"]
            if errors == 1:
                message = "Fail (1 error)"
            else:
                message = "Fail ({} errors)".format(errors)
            error_message = self.status.get("status_message")
            if error_message:
                message += f" with status message '{error_message}'"
        else:
            icon = "🔧"
            cli_color = "bright_red"
            message = self.status["status_message"]

        finished = BuildState(
            build=self,
            state=state,
            status=status,
            final=True,
            message=message,
            icon=icon,
            cli_color=cli_color,
            warnings=warnings,
            errors=errors,
        )
        yield finished

    def wait(self):
        state = None
        for s in self.watch():
            state = s
        return state

    def _get_field(self, field):
        """ Retrieve an individual field from status.json """
        self.get_status()
        return self.status.get(field, None)

    @property
    def warnings_count(self):
        """ Get the warnings_count for the build """
        return int(self._get_field("warnings_count"))

    @property
    def errors_count(self):
        """ Get the errors_count for the build """
        return int(self._get_field("errors_count"))

    @property
    def tuxbuild_status(self):
        """ Get the tuxbuild_status for the build """
        return self._get_field("tuxbuild_status")

    @property
    def build_status(self):
        """ Get the build_status for the build """
        return self._get_field("build_status")

    @property
    def status_message(self):
        """ Get the build_status for the build """
        return self._get_field("status_message")


class BuildSet:
    def __init__(self, builds, **kwargs):
        self.builds = []
        for item in builds:
            data = kwargs.copy()
            data.update(item)
            self.builds.append(Build(**data))
        self.headers = {
            "Content-type": "application/json",
            "Authorization": "{}".format(kwargs["token"]),
        }
        self.kbapi_url = kwargs["kbapi_url"]

    def build(self):
        """ Submit the build request """

        builds_list = self.builds[:]
        data = []
        url = self.kbapi_url + "/build"
        for build_object in self.builds:
            data.append(build_object.generate_build_request())
        json_data = post_request(url, self.headers, data)
        for build_config in json_data:
            for build_object in builds_list:
                if (
                    build_config.items()
                    >= build_object.generate_build_request().items()
                ):
                    build_object.build_data = build_config["download_url"]
                    build_object.build_key = build_config["build_key"]
                    # We may have build set with same parameters multiple times
                    # hence remove the build from builds list after mapping
                    builds_list.remove(build_object)
                    break

    def __watch_build__(self, build, results):
        for state in build.watch():
            results.put(state)

    def watch(self):
        results = queue.Queue()
        n = len(self.builds)

        with concurrent.futures.ThreadPoolExecutor(max_workers=n) as executor:
            for build in self.builds:
                executor.submit(self.__watch_build__, build, results)

            finished = 0
            while finished < n:
                state = results.get()
                yield state
                if state.final:
                    finished += 1

    def wait(self):
        states = []
        for s in self.watch():
            if s.final:
                states.append(s)
        return states

    @property
    def status_list(self):
        """ Return a list of build status dictionaries """
        return [build.status for build in self.builds]
