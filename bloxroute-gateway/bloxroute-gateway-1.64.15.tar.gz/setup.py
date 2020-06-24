import json
import os
import subprocess
import time
from distutils.core import setup
from distutils.sysconfig import get_python_lib
from typing import Tuple, Optional, List

import distro
import requests
import setuptools
from setuptools.command.install import install

ENABLE_DEBUG = True if "ENABLE_DEBUG" in os.environ and os.environ["ENABLE_DEBUG"].upper() == "TRUE" else False

SUPPORTED_OS = {"centos": ["7"], "ubuntu": ["18.04"], "alpine": ["3.8", "3.11"]}

EXTENSIONS_URL = "https://s3.amazonaws.com/downloads.blxrbdn.com/bxextensions/{}/{}-{}/{}"
EXTENSIONS_FILENAME = "bxextensions_{}_{}-{}.tar.gz"

MANIFEST_FILENAME = "MANIFEST.MF"
SCRIPT_FILENAME = "bloxroute-gateway"

README_FILENAME = "README.md"
REQUIREMENTS_FILENAME = "requirements.txt"

BXGATEWAY_DIRECTORY = os.path.join("bxgateway", "src", "bxgateway")
BXGATEWAY_CLI_DIRECTORY = os.path.join("bxgateway", "src", "bloxroute_cli")
BXCOMMON_DIRECTORY = os.path.join("bxcommon", "src", "bxcommon")
BXUTILS_DIRECTORY = os.path.join("bxcommon", "src", "bxutils")

_log_messages = []


def log(message: str):
    global _log_messages
    timestamp = time.strftime("%Y-%m-%d-%H:%M:%S+0000-", time.gmtime())
    _log_messages.append(f"{timestamp}: {message}")


def get_distro_properties() -> Tuple[Optional[str], Optional[str]]:
    distro_os_flavor, distro_os_version, _ = distro.linux_distribution()
    log(f"Detected operating system: {distro_os_flavor}: {distro_os_version}.")

    os_flavor = distro_os_flavor.lower().split()[0]
    if os_flavor in SUPPORTED_OS:
        supported_versions = [os_version
                              for os_version in SUPPORTED_OS[os_flavor]
                              if os_version in distro_os_version]
        if supported_versions:
            assert len(supported_versions) == 1
            return os_flavor, supported_versions[0]

    log(f"Your operating system ({os_flavor}:{distro_os_version}) does not support using C++ extensions. "
        f"Setting bloxroute-gateway to run without them.")
    return None, None


def get_version(src_dir: str) -> str:
    manifest_path = os.path.join(src_dir, MANIFEST_FILENAME)
    try:
        with open(manifest_path) as manifest_file:
            manifest_data = json.load(manifest_file)
        full_version = manifest_data["source_version"]
        trimmed_version = ".".join(full_version.split(".")[:3])
        return trimmed_version
    except (IOError, json.JSONDecodeError) as e:
        raise SystemError(f"Could not read manifest file at: {manifest_path}. Error: {e}")


def get_requirements(src_dir: str) -> List[str]:
    requirements_path = os.path.join(src_dir, REQUIREMENTS_FILENAME)
    requirements = []
    with open(requirements_path) as requirements_file:
        for requirement_line in requirements_file:
            if requirement_line != "\n":
                requirements.append(requirement_line)
    return requirements


def download_extensions(build_path: str, gateway_version: str, os_flavor: str, os_version: str) -> str:
    file_name = EXTENSIONS_FILENAME.format(gateway_version, os_flavor, os_version)
    url = EXTENSIONS_URL.format(gateway_version, os_flavor, os_version, file_name)
    download_file_path = os.path.abspath(os.path.join(build_path, file_name))
    log(f"Downloading C++ extensions from: {url} to {download_file_path}.")

    try:
        download_response = requests.get(url, allow_redirects=False)
        with open(download_file_path, "wb") as download_file:
            download_file.write(download_response.content)
    except Exception as ex:
        raise SystemError(f"Could not download C++ extensions tar.gz, due to {ex}.")

    return download_file_path


def extract_extensions(extensions_file_path: str, build_path: str):
    """
    Extracts C++ extensions from tar ball. Do not extract files to bxextensions/ folder, since
    that would force imports to be for e.g. `bxextensions.task_pool_executor`.

    .so files will be installed at python/site-packages directly.
    """
    extract_path = os.path.abspath(build_path)

    try:
        os.makedirs(extract_path, exist_ok=True)
        subprocess.check_call(["tar", "xvzf", extensions_file_path], cwd=extract_path)
        log(f"C++ extensions have been extracted to {extract_path}.")
    except Exception as ex:
        raise SystemError(f"Failed to extract C++ extensions, due to {ex}.")


def prepare_entrypoint_script(build_path: str, use_extensions: bool):
    script_file_path = os.path.join(build_path, SCRIPT_FILENAME)

    script_contents = ""
    script_contents += f"#!/usr/bin/env bash {os.linesep}\n"
    if os.getenv("LD_LIBRARY_PATH") is None:
        script_contents += f"export LD_LIBRARY_PATH={get_python_lib()}\n"
        os.environ["LD_LIBRARY_PATH"]=get_python_lib()
    else:
        script_contents += f"export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{get_python_lib()}\n"
    script_contents += f"python3 -c 'from bxgateway.main import main; main()'" \
        f" --use-extensions {use_extensions} $* {os.linesep}"

    try:
        with open(script_file_path, "w") as file_handler:
            file_handler.write(script_contents)

        file_permissions = os.stat(script_file_path)
        os.chmod(script_file_path, file_permissions.st_mode | 0o111)
    except Exception as ex:
        raise RuntimeError(f"Failed to write entry point script to {script_file_path}, due to {ex}. "
                           f"Contact support@bloxroute.com for assistance.")


class ExtensionsInstall(install):
    def run(self):
        install.run(self)

        version = get_version(os.path.join("bxgateway", "src", "bxgateway"))
        os_flavor, os_version = get_distro_properties()

        use_extensions = os_flavor is not None and os_version is not None
        if use_extensions:
            try:
                extensions_file_path = download_extensions(self.build_lib, version, os_flavor, os_version)
                extract_extensions(extensions_file_path, self.install_lib)
            except SystemError as e:
                log(f"Extensions installation failure: {e}. Setting system to run without extensions.")
                use_extensions = False
            except RuntimeError as e:
                log(f"Extensions import failed: {e}. Contact support@bloxroute.com for assistance. "
                    f"Setting system to run without extensions.")
                use_extensions = False

        prepare_entrypoint_script(self.build_lib, use_extensions)

        # copy script to executable path
        if not os.path.isdir(self.install_scripts):
            os.makedirs(self.install_scripts)

        source = os.path.join(self.build_lib, SCRIPT_FILENAME)
        target = os.path.join(self.install_scripts, SCRIPT_FILENAME)
        if os.path.isfile(target):
            os.remove(target)

        self.copy_file(source, target)

        if ENABLE_DEBUG:
            log_dump = os.path.join(self.install_scripts, f"bloxroute-gateway-install-{version}.log")
            with open(log_dump, "w") as f:
                f.write("\n".join(_log_messages) + "\n")


def main():
    version = get_version(BXGATEWAY_DIRECTORY)

    requirements = get_requirements(os.path.join("bxgateway")) + get_requirements(
        os.path.join("bxcommon"))

    packages = []
    # TODO: exclude bxcommon.test_utils* –– need to remove dependency on mock class in real code
    packages.extend(setuptools.find_packages("bxcommon/src",
                                             exclude=["bxcommon.test_utils"]))
    # TODO: exclude bxgateway.testing* –– need to remove dependency on testing class in real code
    packages.extend(setuptools.find_packages("bxgateway/src",
                                             exclude=["bxgateway.testing.mocks"]))

    with open(os.path.join("bxgateway", "README.gateway.md")) as f:
        readme = f.read()

    setup(
        name="bloxroute-gateway",
        version=version,
        url="https://bloxroute.com",
        author="bloXroute Labs",
        author_email="support@bloxroute.com",
        description="bloXroute network gateway for scaling blockchains",
        license="MIT",
        long_description=readme,
        long_description_content_type="text/markdown",
        packages=packages,
        install_requires=requirements,
        include_package_data=True,
        package_dir={
            "bxcommon": BXCOMMON_DIRECTORY,
            "bxutils": BXUTILS_DIRECTORY,
            "bxgateway": BXGATEWAY_DIRECTORY,
            "bloxroute_cli": BXGATEWAY_CLI_DIRECTORY
        },
        python_requires="~=3.6",
        classifiers=[
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Development Status :: 4 - Beta",
            "License :: OSI Approved :: MIT License",
        ],
        cmdclass={
            "install": ExtensionsInstall,
        },
        entry_points={
            "console_scripts": ["bloxroute-cli=bloxroute_cli.main:run_main"]
        }
    )


if __name__ == "__main__":
    main()
