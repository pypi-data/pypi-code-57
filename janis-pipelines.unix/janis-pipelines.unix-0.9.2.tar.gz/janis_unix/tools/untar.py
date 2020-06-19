from janis_core import Array, ToolInput, ToolOutput, WildcardSelector, File
from ..data_types.tarfile import TarFile
from .unixtool import UnixTool


class Untar(UnixTool):
    def tool(self):
        return "untar"

    def friendly_name(self):
        return "Tar (unarchive)"

    def base_command(self):
        return ["tar", "xf"]

    def inputs(self):
        return [ToolInput("tarfile", TarFile, position=0)]

    def outputs(self):
        return [ToolOutput("out", Array(File), glob=WildcardSelector("*.java"))]
