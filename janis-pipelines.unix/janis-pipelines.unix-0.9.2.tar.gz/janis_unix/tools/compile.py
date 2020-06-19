#
# Compile a java file
#

from typing import List

from janis_core import ToolInput, ToolOutput, ToolArgument, WildcardSelector, File
from .unixtool import UnixTool


class Compile(UnixTool):
    def tool(self):
        return "javacompiler"

    def friendly_name(self):
        return "Java compiler"

    def base_command(self):
        return "javac"

    def container(self):
        return "openjdk:8"

    def arguments(self) -> List[ToolArgument]:
        return [ToolArgument(".", "-d")]  # CurrentWorkingDirectory()

    def inputs(self):
        return [ToolInput("file", File(), position=1)]

    def outputs(self):
        return [ToolOutput("out", File(), glob=WildcardSelector("*.class"))]
