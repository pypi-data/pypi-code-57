



# -*- coding: utf-8 -*-
"""
Tasks

..codeauthor Tatsuya Suzuki <tatsuya.suzuki@nftlearning.com>
"""
import os
import re
import sys
import logging as log
import json
import pytest
from invoke import task, run
from invoke import Collection


log.getLogger().setLevel(log.INFO)

@task
def check_all(context):
    check = type_check(context)
    test = test_all(context)
    return check.ok and test.ok

@task
def test_all(context):
    """
    Runs all tests under tests/
    """
    log.getLogger('flake8').setLevel(log.WARNING)
    log.info("Running tests...")
    args = [
        "--quiet",
        "--cov=tests",
        "--cov=delegable",
        "--cov-fail-under=100",
        "--doctest-modules",
        "--flake8",
        "tests",
        "-vv",
        "--cov-report=term-missing"
    ]

    log.info(f'pytest {" ".join(args)}')

    return pytest.main(args)


@task
def type_check(context):
    """
    Runs typechecking
    """
    log.info("Typechecking...")
    cmd = "mypy --ignore-missing-imports --strict-optional delegable tests"
    log.info(cmd)
    result = run(cmd)
    log.info("Completed Typecheck")
    return result


@task
def pip_install_all(context):
    """
    Install ALL libraries
    """
    result = run('pip install -r testing_requirements.txt')
    result = result and run('pip install -r requirements.txt')
    result = result and pip_install_submodules(context)
    return result


@task
def pip_install_requirements(context):
    """
    Install required libraries for PROD
    """
    return run('pip install -r requirements.txt')


@task
def pip_install_test(context):
    """
    Install required libraries for TEST
    """
    return run('pip install -r testing_requirements.txt')


namespace = Collection()


test = Collection('test')
namespace.add_collection(test)
test.add_task(check_all, name='all')
test.add_task(type_check, name='typecheck')
test.add_task(test_all, name='test', default=True)


install = Collection('install')
namespace.add_collection(install)
install.add_task(pip_install_all, name='all')
install.add_task(pip_install_requirements, name='prod')
install.add_task(pip_install_test, name='test')
