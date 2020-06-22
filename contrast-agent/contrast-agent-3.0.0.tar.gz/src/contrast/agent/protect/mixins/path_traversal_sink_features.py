# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os

from contrast.extern.six.moves.urllib_parse import unquote

from contrast.api.dtm_pb2 import PathTraversalSemanticAnalysisDetails
from contrast.utils.decorators import cached_property
from contrast.utils.stack_trace_utils import StackTraceUtils

import logging

logger = logging.getLogger("contrast")


class PathTraversalSinkFeatures(object):
    KNOWN_SECURITY_BYPASS_MARKERS = ["::$DATA", "::$Index", "" + "\x00"]

    CUSTOM_CODE_CONFIG_KEY = "detect_custom_code_accessing_system_files"
    COMMON_FILE_EXPLOITS_KEY = "detect_common_file_exploits"
    SYSTEM_FILES = [
        "/proc/self",
        "etc/passwd",
        "etc/shadow",
        "etc/hosts",
        "etc/groups",
        "etc/gshadow",
        "ntuser.dat",
        "/Windows/win.ini",
        "/windows/system32/",
        "/windows/repair/",
    ]

    def check_sink_features(self, context, attack_vector, attack):
        new_sample = self.check_custom_code_accessing_system_files(
            context, attack_vector
        ) or self.check_file_security_bypass(context, attack_vector)

        if new_sample:
            if attack is None:
                attack = self.build_base_attack()

            attack.samples.extend([new_sample])
            attack.response = self.response_from_mode(self.mode)
            self.log_rule_matched(None, attack.response)

        return attack

    def check_custom_code_accessing_system_files(self, context, attack_vector):
        if (
            self.is_custom_code_access_sysfile_enabled
            and self.is_custom_code_accessing_file_system(attack_vector)
        ):
            logger.debug(
                "Found custom code trying to access system file: %s", attack_vector
            )
            return self.create_path_traversal_sample(
                context,
                attack_vector,
                PathTraversalSemanticAnalysisDetails.CUSTOM_CODE_ACCESSING_SYSTEM_FILES,
            )

    def check_file_security_bypass(self, context, attack_vector):
        if (
            self.is_common_file_exploits_enabled
            and self.contains_known_attack_signatures(attack_vector)
        ):
            logger.debug(
                "Found attempt to bypass file security checks: %s", attack_vector
            )
            return self.create_path_traversal_sample(
                context,
                attack_vector,
                PathTraversalSemanticAnalysisDetails.COMMON_FILE_EXPLOITS,
            )

    def create_path_traversal_sample(self, context, attack_vector, rep_code):
        sample = self.build_sample(context, None, attack_vector)
        sample.path_traversal_semantic.path = attack_vector
        sample.path_traversal_semantic.findings.append(rep_code)
        return sample

    @cached_property
    def is_custom_code_access_sysfile_enabled(self):
        return self.settings.is_rep_feature_enabled_for_rule(
            self.name, self.CUSTOM_CODE_CONFIG_KEY
        )

    @cached_property
    def is_common_file_exploits_enabled(self):
        return self.settings.is_rep_feature_enabled_for_rule(
            self.name, self.COMMON_FILE_EXPLOITS_KEY
        )

    @staticmethod
    def is_custom_code_accessing_file_system(path):
        return (
            PathTraversalSinkFeatures.is_system_file(path)
            and StackTraceUtils.in_custom_code()
        )

    @staticmethod
    def contains_known_attack_signatures(path):
        unquoted = unquote(path)
        unescaped = unquoted.encode("utf-8").decode("unicode-escape")

        try:
            realpath = os.path.realpath(unescaped).lower().rstrip("/")
        except ValueError as e:
            return str(e) == "embedded null byte"
        except TypeError as e:
            return (
                "NUL" in str(e)
                or "null byte" in str(e)
                or str(e) == "embedded NUL character"
            )
        except Exception as e:
            return "null byte" in str(e).lower()

        return any(
            [
                bypass_markers.lower().rstrip("/") in realpath
                for bypass_markers in PathTraversalSinkFeatures.KNOWN_SECURITY_BYPASS_MARKERS
            ]
        )

    @staticmethod
    def is_system_file(path):
        if not path:
            return False
        unquoted = unquote(path)
        realpath = os.path.realpath(unquoted).lower().rstrip("/")

        return any(
            [
                sys_file.lower().rstrip("/") in realpath
                for sys_file in PathTraversalSinkFeatures.SYSTEM_FILES
            ]
        )
