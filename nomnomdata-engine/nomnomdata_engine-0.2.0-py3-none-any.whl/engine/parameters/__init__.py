import json
from dataclasses import dataclass
from enum import Enum as pyEnum
from typing import List

from nomnomdata.engine.components import ParameterType
from nomnomdata.engine.errors import ValidationError


class CodeDialectType(str, pyEnum):
    ABAP = "abap"
    ABC = "abc"
    ACTIONSCRIPT = "actionscript"
    ADA = "ada"
    APACHE_CONF = "apache_conf"
    APEX = "apex"
    APPLESCRIPT = "applescript"
    ASCIIDOC = "asciidoc"
    ASL = "asl"
    ASSEMBLY_X86 = "assembly_x86"
    AUTOHOTKEY = "autohotkey"
    BATCHFILE = "batchfile"
    BRO = "bro"
    C9SEARCH = "c9search"
    C_CPP = "c_cpp"
    CIRRU = "cirru"
    CLOJURE = "clojure"
    COBOL = "cobol"
    COFFEE = "coffee"
    COLDFUSION = "coldfusion"
    CSHARP = "csharp"
    CSOUND_DOCUMENT = "csound_document"
    CSOUND_ORCHESTRA = "csound_orchestra"
    CSOUND_SCORE = "csound_score"
    CSP = "csp"
    CSS = "css"
    CURLY = "curly"
    D = "d"
    DART = "dart"
    DIFF = "diff"
    DJANGO = "django"
    DOCKERFILE = "dockerfile"
    DOT = "dot"
    DROOLS = "drools"
    EDIFACT = "edifact"
    EIFFEL = "eiffel"
    EJS = "ejs"
    ELIXIR = "elixir"
    ELM = "elm"
    ERLANG = "erlang"
    FORTH = "forth"
    FORTRAN = "fortran"
    FSHARP = "fsharp"
    FSL = "fsl"
    FTL = "ftl"
    GCODE = "gcode"
    GHERKIN = "gherkin"
    GITIGNORE = "gitignore"
    GLSL = "glsl"
    GOBSTONES = "gobstones"
    GOLANG = "golang"
    GRAPHQLSCHEMA = "graphqlschema"
    GROOVY = "groovy"
    HAML = "haml"
    HANDLEBARS = "handlebars"
    HASKELL = "haskell"
    HASKELL_CABAL = "haskell_cabal"
    HAXE = "haxe"
    HJSON = "hjson"
    HTML = "html"
    HTML_ELIXIR = "html_elixir"
    HTML_RUBY = "html_ruby"
    INI = "ini"
    IO = "io"
    JACK = "jack"
    JADE = "jade"
    JAVA = "java"
    JAVASCRIPT = "javascript"
    JSON = "json"
    JSONIQ = "jsoniq"
    JSP = "jsp"
    JSSM = "jssm"
    JSX = "jsx"
    JULIA = "julia"
    KOTLIN = "kotlin"
    LATEX = "latex"
    LESS = "less"
    LIQUID = "liquid"
    LISP = "lisp"
    LIVESCRIPT = "livescript"
    LOGIQL = "logiql"
    LOGTALK = "logtalk"
    LSL = "lsl"
    LUA = "lua"
    LUAPAGE = "luapage"
    LUCENE = "lucene"
    MAKEFILE = "makefile"
    MARKDOWN = "markdown"
    MASK = "mask"
    MATLAB = "matlab"
    MAZE = "maze"
    MEL = "mel"
    MIXAL = "mixal"
    MUSHCODE = "mushcode"
    NIX = "nix"
    NSIS = "nsis"
    OBJECTIVEC = "objectivec"
    OCAML = "ocaml"
    PASCAL = "pascal"
    PERL = "perl"
    PERL6 = "perl6"
    PHP = "php"
    PHP_LARAVEL_BLADE = "php_laravel_blade"
    PIG = "pig"
    PLAIN_TEXT = "plain_text"
    POWERSHELL = "powershell"
    PRAAT = "praat"
    PROLOG = "prolog"
    PROPERTIES = "properties"
    PROTOBUF = "protobuf"
    PUPPET = "puppet"
    PYTHON = "python"
    R = "r"
    RAZOR = "razor"
    RDOC = "rdoc"
    RED = "red"
    RHTML = "rhtml"
    RST = "rst"
    RUBY = "ruby"
    RUST = "rust"
    SASS = "sass"
    SCAD = "scad"
    SCALA = "scala"
    SCHEME = "scheme"
    SCSS = "scss"
    SH = "sh"
    SJS = "sjs"
    SLIM = "slim"
    SMARTY = "smarty"
    SNIPPETS = "snippets"
    SOY_TEMPLATE = "soy_template"
    SPACE = "space"
    SPARQL = "sparql"
    STYLUS = "stylus"
    SVG = "svg"
    SWIFT = "swift"
    TCL = "tcl"
    TERRAFORM = "terraform"
    TEX = "tex"
    TEXT = "text"
    TEXTILE = "textile"
    TOML = "toml"
    TSX = "tsx"
    TURTLE = "turtle"
    TWIG = "twig"
    TYPESCRIPT = "typescript"
    VALA = "vala"
    VBSCRIPT = "vbscript"
    VELOCITY = "velocity"
    VERILOG = "verilog"
    VHDL = "vhdl"
    VISUALFORCE = "visualforce"
    WOLLOK = "wollok"
    XML = "xml"
    XQUERY = "xquery"
    YAML = "yaml"

    def __str__(self):
        return self.value


@dataclass
class Code(ParameterType):
    type = "code"
    dialect: CodeDialectType


@dataclass
class JSON(ParameterType):
    type = "json"

    def validator(self, val):
        try:
            json.loads(val)
        except json.JSONDecodeError:
            raise ValidationError("Not valid JSON")


@dataclass
class SQLDialectType(str, pyEnum):
    PGSQL = "pgsql"
    MYSQL = "mysql"
    REDSHIFT = "redshift"
    SQL = "sql"
    SQLSERVER = "sqlserver"


@dataclass
class SQL(ParameterType):
    type = "sql"
    dialect: SQLDialectType = SQLDialectType.SQL


@dataclass
class MetaDataTable(ParameterType):
    type = "metadata_table"


@dataclass
class Boolean(ParameterType):
    type = "boolean"


@dataclass
class Text(ParameterType):
    type = "text"


@dataclass
class Int(ParameterType):
    type = "int"
    max: int = None
    min: int = None

    def validate(self, val):
        if not isinstance(val, int):
            raise ValidationError(f"{type(val)} is not expected Integer type")
        if self.min and val < self.min:
            raise ValidationError(f"{val} is smaller than specified minimum [{self.min}]")
        if self.max and val > self.max:
            raise ValidationError(f"{val} is larger than specified maximum [{self.max}]")


@dataclass
class String(ParameterType):
    type = "string"


@dataclass
class Enum(ParameterType):
    type = "enum"
    choices: List[str]

    def validate(self, val):
        if not isinstance(val, str):
            raise ValidationError(f"{type(val)} is not a string")
        elif val not in self.choices:
            raise ValidationError(f"{val} is not a valid choice")


class Connection(ParameterType):
    type = "connection"
