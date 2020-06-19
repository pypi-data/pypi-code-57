from janis_core import Int, ToolInput, ToolOutput, Stdout, Boolean, ToolMetadata
from .unixtool import UnixTool


class Sleep(UnixTool):
    def tool(self):
        return "sleep"

    def friendly_name(self):
        return "Sleep"

    def base_command(self):
        return "sleep"

    def inputs(self):
        return [
            ToolInput("time", Int(), position=1),
        ]

    def outputs(self):
        return [ToolOutput("out", Stdout())]

    def bind_metadata(self):
        self.metadata.documentation = """sleep for the given number of seconds"""
