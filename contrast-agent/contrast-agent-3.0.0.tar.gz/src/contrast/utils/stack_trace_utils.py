# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import ast
import os
import sys
import traceback

from contrast.api.dtm_pb2 import StackTraceElement, TraceStack
from contrast.utils.decorators import fail_safely
from contrast.utils.library_reader import get_active_library_names_from_pkg
from contrast.utils.module_parser import get_ast_parsed_code

import logging

logger = logging.getLogger("contrast")


APPLIES_MARKER = "cs__"
PATCH_MARKER = "__cs"
PY_FILE_EXTENSION = ".py"
UTILS_MODULES = "contrast/utils"
NONETYPE = "NoneType"

CONTRAST_EXTENSIONS = ("contrast/assess_extensions", "contrast/patches")

DJANGO_EXCEPTION_PATH = "core/handlers/exception.py"
DJANGO_DEPRECATION_PATH = "utils/deprecation.py"

VIRTUAL_ENV = "VIRTUAL_ENV"
SITE_PACKAGES = "site-packages"


class StackTraceUtils(object):
    """
    Utility class to grab the latest stack frames based on depth and skip

    Can skip certain frames like our own

    Returns a list of StackTraceElement elements for the DTM
    """

    SORTED_SYS_PATH = sorted(sys.path, key=len, reverse=True)

    @staticmethod
    def build(
        skip=0,
        depth=10,
        ignore=False,
        ignore_string="/contrast/",
        class_lookup=False,
        for_trace=False,
    ):
        frames = traceback.extract_stack()
        frames.reverse()  # moves most recent to the front

        if ignore:
            # ignore frames with contrast or __cs
            def stack_filter(frame):
                if isinstance(frame, tuple):
                    return (
                        ignore_string not in frame[0]
                        and UTILS_MODULES not in frame[0]
                        and not any(
                            extension in frame[0] for extension in CONTRAST_EXTENSIONS
                        )
                        and not frame[2].startswith(APPLIES_MARKER)
                        and not frame[2].startswith(PATCH_MARKER)
                        and not frame[0].endswith(DJANGO_EXCEPTION_PATH)
                        and not frame[0].endswith(DJANGO_DEPRECATION_PATH)
                    )

                return (
                    ignore_string not in frame.filename
                    and UTILS_MODULES not in frame.filename
                    and not any(
                        extension in frame.filename for extension in CONTRAST_EXTENSIONS
                    )
                    and not frame.name.startswith(APPLIES_MARKER)
                    and not frame.name.startswith(PATCH_MARKER)
                    and not frame.filename.endswith(DJANGO_EXCEPTION_PATH)
                    and not frame.filename.endswith(DJANGO_DEPRECATION_PATH)
                )

            frames = [frame for frame in frames if stack_filter(frame)]

        max_frames = skip + depth
        return StackTraceUtils.to_element_list(
            frames[skip:max_frames], class_lookup, for_trace
        )

    @staticmethod
    def to_element_list(frames, class_lookup, for_trace):
        cached_classes = dict()
        return [
            y
            for y in [
                StackTraceUtils.to_element(x, class_lookup, cached_classes, for_trace)
                for x in frames
            ]
            if y is not None
        ]

    @staticmethod
    def to_element(string, class_lookup, cached_classes, for_trace):
        try:
            return StackTraceUtils._to_element(
                string, class_lookup, cached_classes, for_trace
            )
        except RuntimeError:
            return None

    @staticmethod
    def _to_element(summary, class_lookup, cached_classes, for_trace):
        if not summary:
            return

        name_by_path = dict()

        # TODO handle <lambda> and __call__ method names
        if isinstance(summary, tuple):
            # in python 2 traceback returns a tuple
            path = summary[0]
            method = summary[2]
            line_number = summary[1]
        else:
            # python 3 is a FrameSummary
            path = summary.filename
            method = summary.name
            line_number = summary.lineno

        element = TraceStack() if for_trace else StackTraceElement()
        element.line_number = line_number

        element.file_name = StackTraceUtils.filename_formatter(path)

        if class_lookup:
            try:
                found_class = StackTraceUtils.find_class(
                    name_by_path, path, element.file_name, cached_classes, line_number
                )
            except Exception:
                found_class = None

            if found_class is None:
                # If the method for the view is not in a class, set the declaring class to NoneType
                element.declaring_class = NONETYPE
            elif not isinstance(found_class, str):
                element.declaring_class = found_class.__name__
            else:
                element.declaring_class = found_class
        else:
            element.declaring_class = path

        element.method_name = method

        return element

    @staticmethod
    def find_class(name_by_path, path, file_name, cached_classes, line_number):
        if not path:
            return

        if path in name_by_path:
            return name_by_path[path]

        if not os.path.exists(path) or not os.path.isfile(path):
            return None

        parsed = get_ast_parsed_code(path)

        classes = [node for node in ast.walk(parsed) if isinstance(node, ast.ClassDef)]
        class_names = [node.name for node in classes]

        if file_name in cached_classes:
            cached_classes[file_name] = set(class_names).union(
                cached_classes[file_name]
            )
        else:
            cached_classes[file_name] = set(class_names)

        best_class = None

        if len(classes) > 0:
            for cls in classes:
                if line_number > cls.lineno:
                    for item in parsed.body:
                        if isinstance(item, ast.ClassDef) and item.lineno > cls.lineno:
                            best_class = item.name
                            break

        name_by_path[path] = best_class

        return best_class

    @staticmethod
    @fail_safely("Unable to create file_name", log_level="debug")
    def filename_formatter(file_name):
        if file_name.startswith("<frozen"):
            return file_name

        formatted = None

        if VIRTUAL_ENV in os.environ and SITE_PACKAGES in file_name:
            # agent is running in a python virtualenv
            python_lib = os.path.join(
                "lib", ("python{}.{}".format(*sys.version_info[:2]))
            )
            virtual_site = os.path.join(
                os.environ.get(VIRTUAL_ENV), python_lib, SITE_PACKAGES
            )
            formatted = file_name.replace(virtual_site, "")

        if file_name.startswith(os.getcwd()):
            formatted = file_name.replace(os.getcwd(), "")

        if not formatted:
            for sys_path in StackTraceUtils.SORTED_SYS_PATH:
                if file_name.startswith(sys_path):
                    formatted = file_name.replace(sys_path, "")
                    break

        formatted = formatted or file_name

        return formatted.replace("/", ".").lstrip(".")

    @staticmethod
    def in_custom_code():
        current_stack_trace = StackTraceUtils.build(depth=4, ignore=True)
        for trace in current_stack_trace:
            if trace and isinstance(trace, StackTraceElement):
                file_name = trace.file_name
                if file_name.endswith(".py") or file_name.endswith(".pyc"):
                    file_name = file_name[:-3]
                if StackTraceUtils.is_custom_module(file_name):
                    return True
        return False

    @staticmethod
    def is_custom_module(file_name):
        """

        Given a file name, determines if the file is a custom module.

        If a library name is in the file_name, we can say that the file is part of that library
        Obviously this can go wrong if users are naming their custom modules library names but hopefully import errors
        deter people away from this.

        ex:
        file_name = 'flask.router.Router'
        active_library_names = ['flask', 'wsgi', 'sqlalchemy', 'git']
        returns False

        file_name = 'core.utils.docker_constants'
        active_library_names = ['flask', 'wsgi', 'sqlalchemy', 'git']
        return True

        :param file_name: string of file_name without file type (contrast.utils.stack_trace_utils)
        :return: True if no active libraries are in the file_name else False
        """
        active_libraries_names = get_active_library_names_from_pkg()
        for library_name in active_libraries_names:
            if file_name.startswith(library_name):
                return False
        return True
