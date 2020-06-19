from janis_core import Array, File, ToolInput, ToolOutput, Stdout, Boolean, ToolMetadata
from .unixtool import UnixTool


class Awk(UnixTool):
    def tool(self):
        return "awk"

    def friendly_name(self):
        return "Awk"

    def base_command(self):
        return "awk"

    def inputs(self):
        return [
            ToolInput("script", File, position=1, prefix="-f"),
            ToolInput("input_files", Array(File), position=2),
        ]

    def outputs(self):
        return [ToolOutput("out", Stdout())]

    def bind_metadata(self):
        self.metadata.documentation = """run an awk script"""
