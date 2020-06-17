"""Utilities for Java."""

import json
import os
from datetime import datetime
from pathlib import Path
from subprocess import DEVNULL, check_output  # nosec
from typing import Tuple

from ._compatibility import check_java_version
from ._edition import Edition

_JAVA_HOME_ENVIRONMENT_VARIABLE = "JAVA_HOME"

DEFAULT_JAR_PATH = Path(__file__).parent / "data" / "atoti.jar"


def get_java_path():
    """Get the path to Java."""
    java_path = (
        os.path.join(os.environ[_JAVA_HOME_ENVIRONMENT_VARIABLE], "bin", "java")
        if _JAVA_HOME_ENVIRONMENT_VARIABLE in os.environ
        else "java"
    )
    return java_path


def retrieve_info_from_jar() -> Tuple[Edition, datetime]:
    """Retrieve info from the embedded JAR."""
    java_path = get_java_path()
    check_java_version(java_path, [11])
    output = str(
        check_output(
            [java_path, "-jar", str(DEFAULT_JAR_PATH), "--info"], stderr=DEVNULL
        ),
        "utf-8",
    )
    try:
        info = json.loads(output.strip().splitlines()[-1])
        return (
            next(edition for edition in Edition if str(edition) == info["edition"]),
            datetime.fromtimestamp(int(info["licenseEndDate"]) / 1000),
        )
    except:
        raise RuntimeError(
            f"Could not retrieve info about the embedded JAR output: {output}"
        )
