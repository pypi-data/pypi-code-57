#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import json
import random
import string
import time
from pathlib import Path
from flask import Flask, request, render_template
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class FakeRandom:
    """
    Produces fake-random data based in input.
    """

    build_failure_rate = 0
    api_failure_rate = 0
    duration = False
    build_key_alphabet = string.ascii_letters + string.digits
    git_sha_alphabet = string.hexdigits.lower()

    def __init__(self, data):
        input_key = [data[k] for k in Build.tree_input_keys if k in data]
        input_seed = hash(frozenset(input_key))
        self.input_random = random.Random(input_seed)

        output_key = [data[k] for k in Build.mandatory_keys if k != "kconfig"]
        output_key += [data[k] for k in Build.xor_keys if k in data]
        output_key.append(":".join(sorted(data["kconfig"])))
        output_seed = hash(frozenset(output_key))
        self.output_random = random.Random(output_seed)

    # really random data
    def get_build_key(self):
        alphabet = self.build_key_alphabet
        return "".join(random.choice(alphabet) for i in range(22))

    # fake random data based on the tree (repo + ref|sha)
    def get_git_sha(self):
        alphabet = self.git_sha_alphabet
        return "".join(self.input_random.choice(alphabet) for i in range(22))

    def get_phrase(self):
        return self.input_random.choice(phrases)

    # fake random data based on all the builds parameters

    def get_build_status(self):
        n = self.output_random.randint(1, 100)
        if n <= self.build_failure_rate:
            return "fail"
        else:
            return "pass"

    def get_warnings(self):
        return int(self.output_random.expovariate(1.5))

    def get_errors(self):
        return int(self.output_random.expovariate(2))

    def get_duration(self):
        if self.duration:
            return 1 + self.output_random.expovariate(0.5)
        else:
            return 0.0

    @classmethod
    def generate_api_failures(cls, f):
        """
        Decorator that causes random 50x failures failures
        """

        def wrapper(*args, **kwargs):
            n = random.randint(1, 100)
            if n <= cls.api_failure_rate:
                return ({"tuxbuild_status": "Failure"}, 503)
            return f(*args, **kwargs)

        return wrapper


phrases = """\
In sed nisi orci
Nunc a risus quam
Ut eget lorem dolor
Suspendisse potenti
Aenean id lectus lectus
Integer non lorem purus
Sed in scelerisque purus
Etiam quis ultrices velit
Maecenas vel sodales ipsum
In hac habitasse platea dictumst
Nam fermentum sem in tempor auctor
Quisque gravida at nisl non interdum
Nullam auctor ut nisi vitae convallis
Nam varius elit vitae ultrices mollis
Sed posuere ultrices magna nec aliquam
Sed vulputate metus at tincidunt congue
Praesent sodales lorem id dictum euismod
In in lacus nec neque pulvinar fringilla
Fusce ullamcorper sed nunc vitae bibendum
Sed dapibus ante non nibh egestas finibus
Etiam finibus convallis urna mattis malesuada
Sed sit amet elementum leo, non mattis turpis
Nullam convallis dui sed mi elementum vulputate
Nunc consectetur accumsan nisi, vel sodales magna
Donec nec diam nec ex varius tincidunt ut in diam
""".strip().splitlines()


def check_token(f):
    """
    Decorator for checking authentication token. Any token is OK, but there
    must be one.
    """

    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", None)
        if token:
            return f(*args, **kwargs)
        else:
            return (
                {
                    "tuxbuild_status": "error",
                    "status_message": "Authorization Token required",
                },
                400,
            )

    return wrapper


class Verify(Resource):
    @check_token
    def get(self):
        return {"tuxbuild_status": "valid token"}


api.add_resource(Verify, "/v1/verify")


class Build:
    """
    This class encapsulates "builds", by just storing JSON data on disk.
    """

    xor_keys = ["git_ref", "git_sha"]

    build_input_keys = ["target_arch", "toolchain", "kconfig"]

    tree_input_keys = ["git_repo"] + xor_keys

    mandatory_keys = ["git_repo"] + build_input_keys

    root = Path.home() / ".cache" / "tuxbuild" / "api-v1"

    @classmethod
    def validate(cls, data):
        errors = []
        for key in cls.mandatory_keys:
            if key not in data:
                errors.append("%r missing" % key)
        if len(set(data) & set(cls.xor_keys)) > 1:
            errors.append("Only one of %r is allowed" % cls.xor_keys)
        if errors:
            raise ValueError(repr(errors))

    @staticmethod
    def get(key):
        build = Build.root / (key + ".json")
        return json.loads(build.read_text())

    @staticmethod
    def put(key, data, url_root=None):
        if not key:
            r = FakeRandom(data)
            key = r.get_build_key()
            data = data.copy()
            data.update(
                {
                    "build_key": key,
                    "download_url": f"{url_root}{key}/",
                    "tuxbuild_status": "queued",
                    "build_status": "queued",
                    "__date__": time.time(),
                    "__duration__": r.get_duration(),
                }
            )
        build = Build.root / (key + ".json")
        build.parent.mkdir(parents=True, exist_ok=True)
        with build.open("w") as f:
            f.write(json.dumps(data))
        return data


class RequestBuild(Resource):
    @FakeRandom.generate_api_failures
    @check_token
    def post(self):
        json_data = request.get_json(force=True)
        if not isinstance(json_data, list):
            return (
                {
                    "tuxbuild_status": "error",
                    "status_message": "invalid input: expected list of build dictionaries",
                },
                400,
            )
        result = []
        for item in json_data:
            try:
                Build.validate(item)
            except Exception as e:
                return (
                    {"tuxbuild_status": "Invalid Request", "status_message": str(e)},
                    400,
                )
        for item in json_data:
            result.append(Build.put(None, item, request.url_root))
        return result


api.add_resource(RequestBuild, "/v1/build")


class GetBuildStatus(Resource):
    @FakeRandom.generate_api_failures
    @check_token
    def get(self, build_key):
        build = Build.get(build_key)
        if build["tuxbuild_status"] == "complete":
            return build

        if build["tuxbuild_status"] == "queued":
            # promote to building
            build["tuxbuild_status"] = "building"
            build["build_status"] = "building"

            r = FakeRandom(build)
            if "git_sha" in build:
                shortsha = build["git_sha"][0:12]
            else:
                fakesha = r.get_git_sha()
                fakesha += fakesha[0:8]
                shortsha = fakesha[0:12]
                build["git_sha"] = fakesha
            build["git_describe"] = f"vX.Y-rcN-g{shortsha}"
            msg = r.get_phrase()
            build["git_short_log"] = f'{shortsha} ("{msg}")'

        elif build["tuxbuild_status"] == "building":
            if FakeRandom.duration:
                now = time.time()
                if now < float(build["__date__"]) + float(build["__duration__"]):
                    return build

            # promote to complete
            build["tuxbuild_status"] = "complete"

            r = FakeRandom(build)
            status = r.get_build_status()
            build["build_status"] = status

            build["warnings_count"] = r.get_warnings()
            if status == "pass":
                build["errors_count"] = 0
                build["status_message"] = "build completed"
            else:
                build["errors_count"] = 1 + r.get_errors()
        Build.put(build_key, build, request.url_root)
        return build


api.add_resource(GetBuildStatus, "/v1/status/<build_key>")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/<build_key>/")
def build(build_key):
    build = Build.get(build_key)
    return render_template("build.html", build=build)


@click.command()
@click.option("--build-failure-rate", type=int, default=0)
@click.option("--api-failure-rate", type=int, default=0)
@click.option("--duration", is_flag=True)
@click.option("--port", type=int, default=5000)
def run(build_failure_rate, api_failure_rate, duration, port):
    FakeRandom.build_failure_rate = build_failure_rate
    FakeRandom.api_failure_rate = api_failure_rate
    FakeRandom.duration = duration
    app.run(port=port)


if __name__ == "__main__":
    run()
