from subprocess import run
from typing import List, Union, Iterable
from pathlib import Path
from shutil import rmtree
from enum import Enum

from dogebuild.plugins import DogePlugin
from dogebuild.well_known_artifacts import (
    PROTO_SOURCES_DIRECTORY,
    CPP_SOURCES_DIRECTORY,
    HEADERS_DIRECTORY,
    C_SHARP_SOURCES_DIRECTORY,
    JAVA_SOURCES_DIRECTORY,
    JAVASCRIPT_SOURCES_DIRECTORY,
    OBJECTIVE_C_SOURCES_DIRECTORY,
    PHP_SOURCES_DIRECTORY,
    PYTHON_SOURCES_DIRECTORY,
    RUBY_SOURCES_DIRECTORY,
)


class SupportedLanguage(Enum):
    CPP = ("--cpp_out", "cpp", CPP_SOURCES_DIRECTORY)
    C_SHARP = ("--csharp_out", "cs", C_SHARP_SOURCES_DIRECTORY)
    JAVA = ("--java_out", "java", JAVA_SOURCES_DIRECTORY)
    JAVASCRIPT = ("--js_out", "js", JAVASCRIPT_SOURCES_DIRECTORY)
    OBJECTIVE_C = ("--objc_out", "obj_c", OBJECTIVE_C_SOURCES_DIRECTORY)
    PHP = ("--php_out", "php", PHP_SOURCES_DIRECTORY)
    PYTHON = ("--python_out", "py", PYTHON_SOURCES_DIRECTORY)
    RUBY = ("--ruby_out", "rb", RUBY_SOURCES_DIRECTORY)

    def __init__(self, param, build_subdirectory, artifact):
        self.param = param
        self.build_subdirectory = build_subdirectory
        self.artifact = artifact


class ProtobufPlugin(DogePlugin):
    NAME = "protobuf-plugin"

    def __init__(
        self, src: Iterable[Union[Path, str]], src_dir: Union[Path, str] = "src", build_dir: Path = Path("build"),
    ):
        super(ProtobufPlugin, self).__init__(
            artifacts_to_publish=[PROTO_SOURCES_DIRECTORY,]
        )

        self.protoc = "protoc"
        self.proto_sources = list(map(lambda s: str(Path(s).resolve()), src))
        self.src_dir = Path(src_dir).resolve()
        self.build_dir = build_dir.resolve()

        self.add_task(self.proto_sources_dir, aliases=["proto"], phase="proto-sources")
        self.add_task(self.build_cpp_sources, aliases=["cpp"], phase="build")
        self.add_task(self.build_cs_sources, aliases=["cs"], phase="build")
        self.add_task(self.build_java_sources, aliases=["java"], phase="build")
        self.add_task(self.build_js_sources, aliases=["js"], phase="build")
        self.add_task(self.build_objc_sources, aliases=["objc"], phase="build")
        self.add_task(self.build_php_sources, aliases=["php"], phase="build")
        self.add_task(self.build_python_sources, aliases=["py"], phase="build")
        self.add_task(self.build_ruby_sources, aliases=["rb"], phase="build")

    def proto_sources_dir(self):
        return 0, {PROTO_SOURCES_DIRECTORY: [self.src_dir]}

    def build_sources(self, proto_sources_directory: List[Path], lang: SupportedLanguage):
        lang_dir = self.build_dir / lang.build_subdirectory
        lang_dir.mkdir(exist_ok=True, parents=True)
        run(
            [
                self.protoc,
                *map(lambda d: f"-I{d}", proto_sources_directory),
                lang.param,
                f"{lang_dir}",
                *self.proto_sources,
            ],
            check=True,
        )

        if lang in {SupportedLanguage.CPP, SupportedLanguage.OBJECTIVE_C}:
            return 0, {lang.artifact: [lang_dir], HEADERS_DIRECTORY: [lang_dir]}
        else:
            return 0, {lang.artifact: [lang_dir],}

    def build_cpp_sources(self, proto_sources_directory: List[Path]):
        return self.build_sources(proto_sources_directory, SupportedLanguage.CPP)

    def build_cs_sources(self, proto_sources_directory: List[Path]):
        return self.build_sources(proto_sources_directory, SupportedLanguage.C_SHARP)

    def build_java_sources(self, proto_sources_directory: List[Path]):
        return self.build_sources(proto_sources_directory, SupportedLanguage.JAVA)

    def build_js_sources(self, proto_sources_directory: List[Path]):
        return self.build_sources(proto_sources_directory, SupportedLanguage.JAVASCRIPT)

    def build_objc_sources(self, proto_sources_directory: List[Path]):
        return self.build_sources(proto_sources_directory, SupportedLanguage.OBJECTIVE_C)

    def build_php_sources(self, proto_sources_directory: List[Path]):
        return self.build_sources(proto_sources_directory, SupportedLanguage.PHP)

    def build_python_sources(self, proto_sources_directory: List[Path]):
        return self.build_sources(proto_sources_directory, SupportedLanguage.PYTHON)

    def build_ruby_sources(self, proto_sources_directory: List[Path]):
        return self.build_sources(proto_sources_directory, SupportedLanguage.RUBY)

    def clean(self):
        if self.build_dir.exists() and self.build_dir.is_dir():
            rmtree(self.build_dir)
