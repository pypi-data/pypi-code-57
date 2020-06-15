#  Copyright (C) 2020 Servly AI.
#  See the LICENCE file distributed with this work for additional
#  information regarding copyright ownership.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from typing import Dict
import logging

import click
import colorama

import modelzoo


def _format_model_info(info: Dict):
    pass


@click.group()
@click.option(
    "--timeout",
    default=10,
    type=int,
    help="time to wait in seconds before timing out an API call",
)
@click.option("--logging-level", type=click.Choice(["info", "debug"]), default="info")
@click.version_option()
def cli(timeout: int, logging_level: str) -> None:
    levels = {"info": logging.INFO, "debug": logging.DEBUG}
    logging.basicConfig(format="%(levelname)s:%(message)s", level=levels[logging_level])
    colorama.init()


@cli.command()
def list() -> None:
    print(modelzoo.list())


@cli.command()
@click.argument("model_name", type=str, required=True)
def logs(model_name) -> None:
    print(modelzoo.logs(model_name))


@cli.command()
@click.argument("model_name", type=str, required=True)
def info(model_name: str) -> None:
    print(modelzoo.info(model_name))


@cli.command()
@click.argument("model_name", type=str, required=True)
@click.option(
    "--wait/--no-wait",
    default=False,
    help="wait for the model to start before exiting",
)
def stop(model_name: str, wait: bool) -> None:
    modelzoo.stop(model_name)
    if wait:
        modelzoo.wait(model_name, modelzoo.ModelState.STOPPED)


@cli.command()
@click.argument("model_name", type=str, required=True)
@click.option(
    "--wait/--no-wait",
    default=False,
    help="wait for the model to start before exiting",
)
def start(model_name: str, wait: bool) -> None:
    modelzoo.start(model_name)
    if wait:
        modelzoo.wait(model_name, modelzoo.ModelState.HEALTHY)


@cli.command()
@click.option("--api-key", default=None, type=str)
def auth(api_key: str) -> None:
    # Do nothing because the init() workflow will execute by default in cli()
    modelzoo.config.save_api_key(api_key)
