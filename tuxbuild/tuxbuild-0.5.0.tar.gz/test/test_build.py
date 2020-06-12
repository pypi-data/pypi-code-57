# -*- coding: utf-8 -*-

import pytest
import tuxbuild.build
import requests
from mock import patch
import tuxbuild.exceptions


@pytest.mark.parametrize(
    "url,result",
    [
        ("git@github.com:torvalds/linux.git", False),  # ssh type urls not supported
        ("https://github.com/torvalds/linux.git", True),
        ("http://github.com/torvalds/linux.git", True),
        ("git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git", True),
        ("https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git", True),
        (
            "https://kernel.googlesource.com/pub/scm/linux/kernel/git/torvalds/linux.git",
            True,
        ),
    ],
)
def test_is_supported_git_url(url, result):
    assert tuxbuild.build.Build.is_supported_git_url(url) == result


headers = {"Content-type": "application/json", "Authorization": "header"}


class TestPostRequest:
    def test_post_request_pass(self, sleep, post, response):
        request = {"a": "b"}
        response._content = b'{"a": "b"}'
        assert tuxbuild.build.post_request(
            url="http://foo.bar.com/pass", headers=headers, request=request
        ) == {"a": "b"}
        post.assert_called_with(
            "http://foo.bar.com/pass", data='{"a": "b"}', headers=headers
        )

    def test_post_request_timeout(self, sleep, post, response):
        request = {"a": "b"}
        response.status_code = 504

        with pytest.raises(requests.exceptions.HTTPError):
            tuxbuild.build.post_request(
                url="http://foo.bar.com/timeout", headers=headers, request=request
            )
        assert sleep.call_count == 2

    def test_post_request_bad_request(self, sleep, post, response):
        request = {"a": "b"}
        response.status_code = 400
        response._content = b'{"tuxbuild_status": "a", "status_message": "b"}'

        with pytest.raises(tuxbuild.exceptions.BadRequest):
            tuxbuild.build.post_request(
                url="http://foo.bar.com/bad_request", headers=headers, request=request
            )
        assert sleep.call_count == 0


class TestGetRequest:
    def test_get_request_pass(self, sleep, get, response):
        response._content = b'{"a": "b"}'

        assert tuxbuild.build.get_request(
            url="http://foo.bar.com/pass", headers=headers
        ) == {"a": "b"}
        get.assert_called_with("http://foo.bar.com/pass", headers=headers)

    def test_get_request_timeout(self, sleep, get, response):
        response.status_code = 504

        with pytest.raises(requests.exceptions.HTTPError):
            tuxbuild.build.get_request(
                url="http://foo.bar.com/timeout", headers=headers
            )
        assert sleep.call_count == 29

    def test_get_request_500(self, sleep, get, response):
        response.status_code = 500

        with pytest.raises(requests.exceptions.HTTPError):
            tuxbuild.build.get_request(
                url="http://foo.bar.com/timeout", headers=headers
            )
        assert sleep.call_count == 29

    def test_get_request_bad_request(self, sleep, get, response):
        response.status_code = 400

        with pytest.raises(requests.exceptions.HTTPError):
            tuxbuild.build.get_request(
                url="http://foo.bar.com/bad_request", headers=headers
            )
        assert sleep.call_count == 29

    def test_get_request_connectionfailure(self, sleep, get):
        get.side_effect = requests.exceptions.ConnectionError
        with pytest.raises(requests.exceptions.ConnectionError):
            tuxbuild.build.get_request(
                url="http://foo.bar.com/connection_failure", headers=headers
            )
        assert sleep.call_count == 29


@pytest.fixture
def global_var():
    pytest.start_time = 0


def mock_get_status(self):
    self.status["tuxbuild_status"] = "Queued"


def mock_time():
    pytest.start_time += 1
    return pytest.start_time


@pytest.fixture
def build_attrs():
    return {
        "git_repo": "http://github.com/torvalds/linux",
        "git_ref": "master",
        "target_arch": "arm",
        "kconfig": "defconfig",
        "toolchain": "gcc-9",
        "token": "test_token",
        "kbapi_url": "http://test/foo",
    }


@patch.object(tuxbuild.build.Build, "get_status", mock_get_status)
@patch("time.time", mock_time)
@patch("time.sleep")
def test_get_status(stub_sleep, global_var, build_attrs):
    b = tuxbuild.build.Build(**build_attrs)
    b.status["tuxbuild_status"] = "Queued"
    with pytest.raises(tuxbuild.exceptions.Timeout):
        b.wait_on_status("Queued")


def test_global_var(global_var):
    assert pytest.start_time == 0


@pytest.fixture
def build(build_attrs):
    return tuxbuild.build.Build(**build_attrs)


class TestBuild:
    def test_kconfig(self, build):
        assert type(build.kconfig) == list

    @pytest.mark.parametrize(
        "attr,value",
        (
            ("git_repo", None),
            ("git_ref", None),
            ("target_arch", None),
            ("kconfig", None),
            ("kconfig", ()),
            ("toolchain", None),
        ),
    )
    def test_requires_mandatory_attributes(self, build_attrs, attr, value):
        build_attrs[attr] = value
        with pytest.raises(AssertionError) as assertion:
            tuxbuild.build.Build(**build_attrs)
        assert attr in str(assertion)

    def test_validates_git_url(self, build_attrs):
        build_attrs["git_repo"] = "ssh://foo.com:bar.git"
        with pytest.raises(AssertionError) as assertion:
            tuxbuild.build.Build(**build_attrs)
        assert "git url must be in the form" in str(assertion)

    def test_headers(self, build):
        assert build.headers["Content-Type"] == "application/json"
        assert build.headers["Authorization"] == build.token

    def test_git_sha(self, build_attrs):
        del build_attrs["git_ref"]
        build_attrs["git_sha"] = "deadbeef"
        build = tuxbuild.build.Build(**build_attrs)
        assert build.git_sha == "deadbeef"

    def test_git_ref_or_git_sha_required(self, build_attrs):
        del build_attrs["git_ref"]
        with pytest.raises(AssertionError) as assertion:
            tuxbuild.build.Build(**build_attrs)
        assert "git_ref" in str(assertion)
        assert "git_sha" in str(assertion)

    def test_submit_build_git_ref(self, build, build_attrs, mocker):
        post_request = mocker.patch("tuxbuild.build.post_request")
        api_build_url = build_attrs["kbapi_url"] + "/build"

        build.build()
        post_request.assert_called_with(
            api_build_url,
            mocker.ANY,
            [
                {
                    "git_repo": build_attrs["git_repo"],
                    "git_ref": build_attrs["git_ref"],
                    "toolchain": build_attrs["toolchain"],
                    "target_arch": build_attrs["target_arch"],
                    "kconfig": [build_attrs["kconfig"]],
                }
            ],
        )

    def test_submit_build_git_sha(self, build, build_attrs, mocker):
        post_request = mocker.patch("tuxbuild.build.post_request")
        api_build_url = build_attrs["kbapi_url"] + "/build"

        build.git_ref = None
        build.git_sha = "badbee"
        build.build()
        post_request.assert_called_with(
            api_build_url,
            mocker.ANY,
            [
                {
                    "git_repo": build_attrs["git_repo"],
                    "git_sha": "badbee",
                    "toolchain": build_attrs["toolchain"],
                    "target_arch": build_attrs["target_arch"],
                    "kconfig": [build_attrs["kconfig"]],
                }
            ],
        )


class TestWatch:
    @staticmethod
    def watch(obj):
        states = []
        for state in obj.watch():
            states.append(state)
        return states


class TestBuildWatch(TestWatch):
    @pytest.fixture(autouse=True)
    def get_status(self, mocker):
        return mocker.patch("tuxbuild.build.Build.get_status")

    def test_watch(self, build):
        watch = iter(build.watch())
        s1 = next(watch)
        assert s1.state == "queued"

        s2 = next(watch)
        assert s2.state == "building"

        build.status["tuxbuild_status"] = "completed"
        build.status["build_status"] = "pass"
        build.status["warnings_count"] = 0
        s3 = next(watch)
        assert s3.state == "completed"

    def test_watch_pass(self, build):
        build.status["build_status"] = "pass"
        build.status["warnings_count"] = 0

        states = self.watch(build)
        assert len(states) > 1
        state = states[-1]
        assert state.state == "completed"
        assert state.status == "pass"
        assert state.warnings == 0

    def test_watch_pass_warnings(self, build):
        build.status["build_status"] = "pass"
        build.status["warnings_count"] = 5

        state = self.watch(build)[-1]
        assert "Pass (5 warnings)" in state.message
        assert state.warnings == 5

    def test_watch_pass_one_warning(self, build):
        build.status["build_status"] = "pass"
        build.status["warnings_count"] = 1

        state = self.watch(build)[-1]
        assert "Pass (1 warning)" in state.message
        assert state.warnings == 1

    def test_watch_fail(self, build):
        build.status["build_status"] = "fail"
        build.status["errors_count"] = 5

        state = self.watch(build)[-1]
        assert "Fail (5 errors)" in state.message
        assert state.errors == 5

    def test_watch_fail_1_error(self, build):
        build.status["build_status"] = "fail"
        build.status["errors_count"] = 1

        state = self.watch(build)[-1]
        assert "Fail (1 error)" in state.message
        assert state.errors == 1

    def test_watch_fail_status_message(self, build):
        build.status["build_status"] = "fail"
        build.status["errors_count"] = 1
        build.status["status_message"] = "failed to foo the bar"

        state = self.watch(build)[-1]
        assert "with status message 'failed to foo the bar'" in state.message

    def test_watch_not_completed(self, build):
        build.status["build_status"] = None
        build.status["tuxbuild_status"] = "error"
        build.status["status_message"] = "the infrastructure failed"
        state = self.watch(build)[-1]
        assert state.state != "completed"
        assert state.status is None
        assert "the infrastructure failed" in state.message

    def test_output_with_multiple_kconfigs(self, build):
        build.kconfig = ["defconfig", "https://raw.foo.com/kconfig/myconfig.txt"]
        assert "(defconfig+1)" in str(build)
        assert "https://raw.foo.com/kconfig/myconfig.txt" not in str(build)


class TestBuildWait:
    def test_wait(self, build, mocker):
        watch = mocker.patch("tuxbuild.build.Build.watch")
        build.wait()
        assert watch.call_count > 0

    def test_wait_returns_last_state(self, build, mocker):
        watch = mocker.patch("tuxbuild.build.Build.watch")
        first = mocker.MagicMock()
        last = mocker.MagicMock()
        watch.return_value = [first, last]
        assert build.wait() is last


@pytest.fixture
def builds():
    return [
        {"toolchain": "gcc-9", "target_arch": "x86", "kconfig": "defconfig"},
        {"toolchain": "gcc-8", "target_arch": "x86", "kconfig": "defconfig"},
        {"toolchain": "gcc-9", "target_arch": "arm64", "kconfig": "defconfig"},
        {"toolchain": "gcc-8", "target_arch": "arm64", "kconfig": "defconfig"},
    ]


@pytest.fixture
def build_set(build_attrs, builds):
    return tuxbuild.build.BuildSet(
        builds,
        git_repo=build_attrs["git_repo"],
        git_ref=build_attrs["git_ref"],
        kbapi_url=build_attrs["kbapi_url"],
        token=build_attrs["token"],
    )


class TestBuildSet:
    def test_expand_spec(self, build_set):
        assert len(build_set.builds) == 4
        assert build_set
        assert build_set.builds[0].git_repo is not None


class TestBuildSetWatch(TestWatch):
    def test_watch(self, build_set, mocker):
        build_watch = mocker.patch("tuxbuild.build.Build.watch")
        state1 = mocker.MagicMock()
        state1.final = False
        state2 = mocker.MagicMock()
        state2.final = True
        build_watch.return_value = [state1, state2]

        states = self.watch(build_set)
        assert len(states) == 2 * len(build_set.builds)


class TestBuildSetWait:
    def test_wait(self, build_set, mocker):
        watch = mocker.patch("tuxbuild.build.BuildSet.watch")
        state1 = mocker.MagicMock()
        state1.final = False
        state2 = mocker.MagicMock()
        state2.final = True
        watch.return_value = [state1, state1, state2, state2]

        results = build_set.wait()
        assert results == [state2, state2]
