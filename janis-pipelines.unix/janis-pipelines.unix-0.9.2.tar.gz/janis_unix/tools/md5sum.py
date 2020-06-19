from datetime import datetime

from janis_core import (
    ToolArgument,
    ToolInput,
    ToolOutput,
    Stdout,
    Array,
    File,
    ToolMetadata,
    Boolean,
)
from .unixtool import UnixTool


class MD5Sum(UnixTool):
    def tool(self):
        return "md5sum"

    def friendly_name(self):
        return "MD5 Sum"

    def base_command(self):
        return "md5sum"

    def inputs(self):
        return [ToolInput("input_file", File(), position=1)]

    def arguments(self):
        return [ToolArgument("| awk '{print $1}'", position=2, shell_quote=False)]

    def outputs(self):
        return [ToolOutput("out", Stdout())]

    def bind_metadata(self):
        self.metadata.dateUpdated = datetime(2020, 6, 9)
        self.metadata.documentation = (
            "Compute the MD5 message digest of the given file."
        )
