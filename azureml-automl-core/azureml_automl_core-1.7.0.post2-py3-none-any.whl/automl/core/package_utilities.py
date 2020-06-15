# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Common utilities related to package discovery and version checks."""
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import logging
import operator
import pkg_resources as pkgr
from pkg_resources import Requirement, VersionConflict, WorkingSet
from azureml.automl.core.shared.exceptions import (ManagedEnvironmentCorruptedException,
                                                   OptionalDependencyMissingException)
from azureml.automl.core.shared.reference_codes import ReferenceCodes


AUTOML_PACKAGES = {'azureml-automl-runtime',
                   'azureml-train-automl-runtime',
                   'azureml-core',
                   'azureml-telemetry',
                   'azureml-defaults',
                   'azureml-automl-core',
                   'azureml-pipeline-steps',
                   'azureml-widgets',
                   'azureml-dataprep'
                   'azureml-train-automl-client',
                   'azureml-interpret',
                   'azureml-explain-model',
                   'azureml-train-restclients-hyperdrive',
                   'azureml-train-core',
                   'azureml-pipeline-core'}


_PACKAGES_TO_IGNORE_VERSIONS = {
    'lightgbm'  # Installed from source.
}


def _all_dependencies() -> Dict[str, str]:
    """
    Retrieve the packages from the site-packages folder by using pkg_resources.

    :return: A dict contains packages and their corresponding versions.
    """
    dependencies_versions = dict()
    for d in pkgr.working_set:
        dependencies_versions[d.key] = d.version
    return dependencies_versions


def _is_sdk_package(name: str) -> bool:
    """Check if a package is in sdk by checking the whether the package startswith('azureml')."""
    return name.startswith('azureml')


def get_sdk_dependencies(
    all_dependencies_versions: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """
    Return the package-version dict.

    :param all_dependencies_versions:
        If None, then get all and filter only the sdk ones.
        Else, only check within the that dict the sdk ones.
    :return: The package-version dict.
    """
    sdk_dependencies_version = dict()
    if all_dependencies_versions is None:
        all_dependencies_versions = _all_dependencies()
    for d in all_dependencies_versions:
        if _is_sdk_package(d):
            sdk_dependencies_version[d] = all_dependencies_versions[d]

    return sdk_dependencies_version


def _is_version_mismatch(a: str, b: str, custom_azureml_logic: bool = False) -> bool:
    """
    Check if a is a version mismatch from b.

    :param a: A version to compare.
    :type a: str
    :param b: A version to compare.
    :type b: str
    :custom_azureml_logic: Option to ask for check on azureml packages.
        If true, ignore hotfix version.
        If true, `a` can have a minor version 1 lower than `b` without being considered a mismatch.
        As curated environment will release slower than pypi release, the client inference version may
        be greater than the client training version for a short period of time. In order to avoid errors in a
        new installation during this time, we add this functionality.
    :type custom_azureml_logic: bool
    :return: True if a != b. False otherwise.
    :rtype: bool
    """
    if custom_azureml_logic:
        ver_a = a.split('.')
        ver_b = b.split('.')
        # currently azureml release uses the following format
        # major.minor.0<.hot_fix>
        # however previously we followed the format
        # major.0.minor<.hot_fix>
        for i in range(3):
            try:
                if ver_a[i] != ver_b[i]:
                    # As curated environment will release slower than pypi release, the client inference version may
                    # be greater than the training version for a short period of time. In order to avoid errors in a
                    # new installation during this time, we add this functionality.
                    if i == 1 and int(ver_a[i]) + 1 == int(ver_b[i]):
                        # This should allow for any X.Y.Z:
                        # inference Y+1 is not a mismatch
                        # any Z will be supported and not considered mismatch
                        break
                    if i == 2 and ver_a[0] == ver_b[0] and ver_a[1] == ver_b[1]:
                        break
                    return True
            except IndexError:
                return True
        return False
    else:
        return a != b


def _check_dependencies_versions(
    old_versions: Dict[str, str],
    new_versions: Dict[str, str]
) -> Tuple[Set[str], Set[str], Set[str], Set[str]]:
    """
    Check the SDK packages between the training environment and the predict environment.

    Then it gives out 2 kinds of warning combining sdk/not sdk with missing or version mismatch.

    :param old_versions: Packages in the training environment.
    :param new_versions: Packages in the predict environment.
    :return: sdk_dependencies_mismatch, sdk_dependencies_missing,
             other_depencies_mismatch, other_depencies_missing
    """
    sdk_dependencies_mismatch = set()
    other_depencies_mismatch = set()
    sdk_dependencies_missing = set()
    other_depencies_missing = set()

    for d in old_versions.keys():
        if d in new_versions and _is_version_mismatch(old_versions[d], new_versions[d], custom_azureml_logic=False):
            if not _is_sdk_package(d):
                other_depencies_mismatch.add(d)
            elif _is_version_mismatch(old_versions[d], new_versions[d], custom_azureml_logic=True):
                sdk_dependencies_mismatch.add(d)
        elif d not in new_versions:
            if not _is_sdk_package(d):
                other_depencies_missing.add(d)
            else:
                sdk_dependencies_missing.add(d)

    return sdk_dependencies_mismatch, sdk_dependencies_missing, \
        other_depencies_mismatch, other_depencies_missing


def _has_version_discrepancies(sdk_dependencies: Dict[str, str], just_automl: bool = False) -> bool:
    """
    Check if the sdk dependencies are different from the current environment.

    Returns true is there are discrepancies false otherwise.
    """
    current_dependencies = _all_dependencies()
    sdk_mismatch, sdk_missing, other_mismatch, other_missing = _check_dependencies_versions(
        sdk_dependencies, current_dependencies
    )

    if len(sdk_mismatch) == 0 and len(sdk_missing) == 0:
        logging.debug('No issues found in the SDK package versions.')
        return False

    if just_automl and 'azureml-train-automl-client' not in sdk_mismatch and \
            'azureml-train-automl-client' not in sdk_missing:
        logging.debug('No issues found in the azureml-train-automl package')
        return False

    if len(sdk_mismatch) > 0:
        logging.warning('The version of the SDK does not match the version the model was trained on.')
        logging.warning('The consistency in the result may not be guaranteed.')
        message_template = 'Package:{}, training version:{}, current version:{}'
        message = []
        for d in sorted(sdk_mismatch):
            message.append(message_template.format(d, sdk_dependencies[d], current_dependencies[d]))
        logging.warning('\n'.join(message))

    if len(sdk_missing) > 0:
        logging.warning('Below packages were used for model training but missing in current environment:')
        message_template = 'Package:{}, training version:{}'
        message = []
        for d in sorted(sdk_missing):
            message.append(message_template.format(d, sdk_dependencies[d]))
        logging.warning('\n'.join(message))

    return True


def _get_incompatible_dependency_versions(ws: WorkingSet,
                                          packages: Set[str],
                                          ignored_dependencies: Optional[Set[str]] = None) \
        -> Tuple[bool, Dict[str, List[Tuple[Requirement, Optional[Requirement]]]]]:
    """
    Check all the requirements of listed packages and return any incompatible versions or missing packages.

    :param ws: The working set of packages to check the installed packages and versions from.
    :param packages: The set of packages whose requirements should be checked for incompatibilities.
    :param ignored_dependencies: The set of dependencies whose versions should be ignored.
    :return: A boolean representing whether or not at least one incompatibility was found and a Dictionary of the
    package and corresponding list of incompatibilities found. Each entry in the list is a Tuple of package's
    requirement (`class pkg_resources.Requirement`), conflicting installed requirement
    `class pkg_resources.Requirement` or `None` if the required package is not installed.
    """
    _ignored_dependencies = ignored_dependencies if ignored_dependencies is not None else set()  # type: Set[str]
    working_set_packages = ws.by_key    # type: ignore
    incompatibilities = {}  # type: Dict[str, List[Tuple[Requirement, Optional[Requirement]]]]
    do_incompatibilities_exist = False
    for package in packages.intersection(working_set_packages):
        requirements = working_set_packages[package].requires()
        incomp_list = []
        for req in requirements:
            is_incompat, incompat_req = _has_versionconflict_or_not_installed(ws, req)
            if not is_incompat:
                continue

            if req.name in _ignored_dependencies:
                logging.warning('Ignoring version check for {}'.format(req.name))
                continue

            do_incompatibilities_exist = True
            incomp_list.append((req, incompat_req))

        if incomp_list:
            incompatibilities[package] = incomp_list

    return do_incompatibilities_exist, incompatibilities


def _has_versionconflict_or_not_installed(ws: WorkingSet, req: Requirement) -> Tuple[bool, Optional[Requirement]]:
    """
    Check whether a requirement exists in the working set or has an incompatible version installed.

    :param ws: The working set of packages to check the installed packages and versions from.
    :param req: The requirement that needs to be checked for in the working set.
    :return: Tuple with the first element representing whether the package is not installed or has a version
    conflict and the second element being the conflicting requirement that is installed or None if not installed.
    """
    try:
        if ws.find(req) is None:
            return True, None
    except VersionConflict as ex:
        return True, ex.dist

    return False, None


def _get_package_incompatibilities(packages: Set[str],
                                   ignored_dependencies: Optional[Set[str]] = None) -> None:
    """
    Check whether the listed packages's dependencies are met in the current environment or not.
    If not, throws an ``azureml.automl.core.shared.exceptions.OptionalDependencyMissingException``.

    :param packages: The set of packages for which compatibility must be ensured for their dependencies.
    :param ignored_dependencies: The set of dependencies whose versions should be ignored.
    :raises: :class:`azureml.automl.core.shared.exceptions.OptionalDependencyMissingException`
    """
    if not packages:
        return

    do_incompatibilities_exist, incompatible_packages = _get_incompatible_dependency_versions(
        pkgr.working_set,
        packages,
        ignored_dependencies
    )

    if not do_incompatibilities_exist:
        return

    messages = []
    for package, incompat_packages in incompatible_packages.items():
        message_template = '{} requires {} but has {}.'
        for incompatibility in incompat_packages:
            messages.append(message_template.format(package,
                                                    incompatibility[0],
                                                    incompatibility[1] or 'not been installed'))
    exception_message = ';'.join(messages)

    raise OptionalDependencyMissingException.create_without_pii(
        msg="Incompatible/Missing packages found: {}".format(exception_message),
        target=','.join(incompatible_packages.keys()),
        reference_code=ReferenceCodes._PACKAGE_INCOMPATIBILITIES_FOUND)
