from abc import ABC

from janis_core import CommandTool


class UnixTool(CommandTool, ABC):
    def tool_module(self):
        return "unix"

    def container(self):
        return "ubuntu:latest"

    def version(self):
        return "v1.0.0"
