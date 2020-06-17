"""Provides config classes."""
# pylint: disable=R0903
import binascii
import copy
import json
import logging
import math
import multiprocessing
import os
import re
import socket
import tempfile
import zipfile
import zlib
from typing import Any, Optional, List, Type, TypeVar, Union

from pydantic import BaseModel, BaseSettings, validator  # pylint: disable=E0611
from ruamel.yaml import YAML, YAMLError

from .. import sdk_impl
from .. import util, walker, config as root_config

DEFAULT_CONFIG_PATH = os.path.join(root_config.CONFIG_DIRPATH, "cli.yml")
INGEST_CONFIG_PATH = os.path.join(root_config.CONFIG_DIRPATH, "ingest.yaml")
UUID_REGEX = "[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}"
INGEST_OPERATION_REF_REGEX = re.compile(f"(?P<host>.*)/ingests/(?P<ingest_id>{UUID_REGEX})")
GROUP_ID_REGEX = re.compile("^[0-9a-z][0-9a-z.@_-]{0,30}[0-9a-z]$")

CONNECT_TIMEOUT: int = int(os.getenv("FLYWHEEL_CLI_CONNECT_TIMEOUT", "30"))
READ_TIMEOUT: int = int(os.getenv("FLYWHEEL_CLI_READ_TIMEOUT", "60"))

log = logging.getLogger(__name__)


class BaseConfig(BaseSettings):
    """Base config"""

    class ArgparserConfig:
        """Argparser config"""


class ArgparseGroup:
    """Encapsulate config argument into a argparser group"""
    def __init__(self, config_cls, name, **opts):
        self.config_cls = config_cls
        self.name = name
        self.opts = opts


C = TypeVar("C", bound=BaseConfig)  # pylint: disable=C0103

def read_config_file(filepath):
    """Read data from config file"""
    if not os.path.exists(filepath):
        return None
    file_extension = filepath.rsplit(".", maxsplit=1)[-1]
    if file_extension in ("yml", "yaml"):
        try:
            yaml = YAML()
            with open(filepath) as config_file:
                config = yaml.load(config_file)
        except (IOError, YAMLError) as exc:
            raise ConfigError(f"Unable to parse YAML config file: {exc}")
    elif file_extension == "json":
        try:
            with open(filepath) as json_file:
                config = json.load(json_file)
        except (IOError, json.decoder.JSONDecodeError) as exc:
            raise ConfigError(f"Unable to parse JSON file: {exc}")
    else:
        raise ConfigError("Only YAML and JSON files are supported")
    return config


def load_config(cls: Type[C], args) -> C:
    """Load values from namespace and config file"""
    config_from_file = {}

    def load_value(snake_name):
        # try get the value from arguments first
        # then from the loaded config file
        # use any not-None value as valid value
        value = getattr(args, snake_name, None)
        if value is not None:
            return value

        value = config_from_file.get(snake_name)
        if value is not None:
            return value

        dash_name = snake_name.replace("_", "-")
        return config_from_file.get(dash_name)

    if isinstance(cls, ArgparseGroup):
        cls = cls.config_cls
    config_filepath = getattr(args, "config_file") or DEFAULT_CONFIG_PATH
    config_filepath = os.path.expanduser(config_filepath)
    config_from_file = {}
    if not getattr(args, "no_config", None):
        config_from_file = read_config_file(config_filepath) or {}

    values = {}

    for field in cls.__fields__.values():
        snake_name = field.name
        value = load_value(snake_name)
        # only add values which are not None to let BaseSettings load them
        # from environment variables
        if value is not None:
            values[snake_name] = value
    return cls(**values)


def add_arguments(config: Union[Type[C], ArgparseGroup], parser):
    """Add arguments to a given parser"""
    groups = {}

    if isinstance(config, ArgparseGroup):
        parser = parser.add_argument_group(config.name, **config.opts)
        cls = config.config_cls
    else:
        cls = config

    group_specs = getattr(cls.ArgparserConfig, "_groups", {})
    for name, opts in group_specs.items():
        opts = copy.copy(opts)
        type_ = opts.pop("type", "argument")
        groups[name] = getattr(parser, f"add_{type_}_group")(**opts)

    for field in cls.__fields__.values():
        # by default add all fields to the parser, except it is marked
        # not to add
        opts = copy.deepcopy(getattr(cls.ArgparserConfig, field.name, {}))

        if not opts:
            # Skip fields that don't have arparser options
            continue

        parser_group = parser
        grp_name = opts.pop("group", None)
        if grp_name:
            parser_group = groups.get(grp_name, parser)

        kwargs = {}
        # prepare flags
        # handle positional arguments
        if opts.pop("positional", False):
            # can't set dest for positional argument
            flags = field.name
        else:
            flags = opts.pop("flags", f"--{field.name.replace('_', '-')}")
            kwargs["dest"] = field.name
        if not isinstance(flags, list):
            flags = [flags]
        # add the remainder opts as is to the kwargs
        kwargs.update(opts)
        # automatically add default value to the help text
        if not field.required:
            kwargs.setdefault("help", "")
            kwargs["help"] = f"{kwargs['help']} (default: {field.default})"
        # set action if necessary
        if field.type_ == bool:
            kwargs["action"] = "store_true"
        parser_group.add_argument(*flags, **kwargs)


class GeneralConfig(BaseSettings):
    """General configuration"""

    config_file: str = DEFAULT_CONFIG_PATH
    no_config: bool = False

    assume_yes: bool = False
    ca_certs: Optional[str]
    timezone: Optional[str]
    quiet: bool = False
    debug: bool = False
    verbose: bool = False

    @staticmethod
    def get_api_key():
        """Load api-key from config"""
        config = sdk_impl.load_config()
        if not config and config.get("key"):
            raise Exception("Not logged in, please login using `fw login`")
        return config["key"]

    def configure_ca_certs(self):
        """Configure ca-certs"""
        if self.ca_certs is not None:
            # Monkey patch certifi.where()
            import certifi  # pylint: disable=import-outside-toplevel
            certifi.where = lambda: self.ca_certs

    def configure_timezone(self):
        """Configure timezone"""
        if self.timezone is not None:
            # Validate the timezone string
            import pytz  # pylint: disable=import-outside-toplevel
            import flywheel_migration  # pylint: disable=import-outside-toplevel

            try:
                tz = pytz.timezone(self.timezone)
            except pytz.exceptions.UnknownTimeZoneError:
                raise ConfigError(f'Unknown timezone: {self.timezone}')

            # Update the default timezone for flywheel_migration and util
            util.DEFAULT_TZ = tz
            flywheel_migration.util.DEFAULT_TZ = tz

            # Also set in the environment
            os.environ['TZ'] = self.timezone

    def startup_initialize(self):
        """Execute configure methods, this should be only called once, when cli starts."""
        if os.environ.get('FW_DISABLE_LOGS') != '1':
            root_config.Config.configure_logging(self)
        self.configure_ca_certs()
        self.configure_timezone()


    @validator("debug")
    def exclusive_logging_flags(cls, val, values):  # pylint: disable=no-self-argument, no-self-use
        """Validate logging mutually exclusive group"""
        if val and values["quiet"]:
            raise ValueError("quiet not allowed with debug")
        return val

    class ArgparserConfig:  # pylint: disable=R0903
        """Argparser options"""
        _groups = {
            "logging": {"type": "mutually_exclusive"},
            "config": {"type": "mutually_exclusive"},
        }
        config_file = {
            "flags": ["-C", "--config-file"],
            "metavar": "PATH",
            "group": "config",
            "help": "Specify configuration options via config file",
        }
        no_config = {
            "group": "config",
            "help": "Do NOT load the default configuration file",
        }
        assume_yes = {
            "flags": ["-y", "--yes"],
            "help": "Assume the answer is yes to all prompts",
        }
        ca_certs = {"help": "The file to use for SSL Certificate Validation"}
        ca_certs = {"help": "Set the effective local timezone for imports"}
        timezone = {"help": "Set the effective local timezone for imports"}
        verbose = {
            "flags": ["-v", "--verbose"],
            "help": "Get more detailed output"
        }
        debug = {
            "flags": ["-d", "--debug"],
            "group": "logging",
            "help": "Turn on debug logging",
        }
        quiet = {
            "flags": ["-q", "--quiet"],
            "group": "logging",
            "help": "Squelch log messages to the console",
        }


class ManageConfig(BaseConfig):
    """Manage ingest configuration"""
    ingest_url: Optional[Union[str, dict]]

    @property
    def cluster(self):
        """Cluster"""
        return self.ingest_url.get("cluster")

    @property
    def ingest_id(self):
        """Ingest id"""
        return self.ingest_url.get("ingest_id")


    @validator("ingest_url", pre=True)
    def validate_ingest_url(cls, val):  # pylint: disable=no-self-argument, no-self-use
        """Get the ingest operation url from the config file if not provided."""
        ingest_url = val
        if not ingest_url:
            try:
                config = read_config_file(os.path.expanduser(INGEST_CONFIG_PATH)) or {}
            except ConfigError:
                ingest_url = None
            else:
                ingest_url = config.get("ingest_operation_url")
        if not ingest_url:
            raise ValueError(
                "Couldn't determine the ingest URL, "
                "probably it was started on a different machine or by a different user. "
                "Please specify the ingest URL as a positional argument."
            )
        if isinstance(ingest_url, dict):
            if "cluster" not in ingest_url or "ingest_id" not in ingest_url:
                raise ValueError("'ingest_url' does not contain 'cluster' and/or 'ingest_id'")
            return ingest_url
        match = INGEST_OPERATION_REF_REGEX.match(ingest_url)
        if not match:
            raise ValueError("The provided url should have the following format: <cluster_url>/ingests/<ingest_id>")
        return {
            "cluster": match.group("host"),
            "ingest_id": match.group("ingest_id"),
        }

    class ArgparserConfig:
        """Argparser options"""
        ingest_url = {
            "positional": True,
            "nargs": "?",
            "metavar": "INGEST_URL",
            "help": "The url of the ingest to manage (<cluster_host>/ingests/<ingest_id>)",
        }


class ClusterConfig(BaseConfig):
    """Cluster ingest config"""
    cluster: Optional[str]
    follow: bool = False

    def save_ingest_operation_url(self, ingest_id):
        """Save ingest operation url to the ingest config file.
        It makes possible to use the ingest manager subcommand like `ingest follow` without parameters.
        """
        if not self.cluster:
            raise ConfigError("Saving ingest operation url only supported when using ingest cluster")
        # Ensure directory exists
        config_dir = os.path.dirname(INGEST_CONFIG_PATH)
        os.makedirs(config_dir, exist_ok=True)
        ingest_operation_url = f"{self.cluster}/ingests/{ingest_id}"
        with open(INGEST_CONFIG_PATH, "w") as f:
            yaml = YAML()
            yaml.dump({"ingest_operation_url": ingest_operation_url}, f)
        return ingest_operation_url

    class ArgparserConfig:
        """Argparser config"""
        cluster = {"help": "Ingest cluster url"}
        follow = {
            "flags": ["-f", "--follow"],
            "help": "Follow the progress of the ingest",
        }


class SubjectConfig(BaseModel):
    """Subject configuration schema"""
    code_serial: int = 0
    code_format: str
    map_keys: List[str]


class IngestConfig(BaseConfig):
    """Ingest configuration"""

    src_fs: str
    symlinks: bool = False
    include_dirs: List[str] = []
    exclude_dirs: List[str] = []
    include: List[str] = []
    exclude: List[str] = []
    compression_level: int = zlib.Z_DEFAULT_COMPRESSION
    ignore_unknown_tags: bool = False
    encodings: List[str] = []
    de_identify: bool = False
    deid_profile: str = "minimal"
    deid_profiles: List[Any] = []
    skip_existing: bool = False
    no_audit_log: bool = False
    subject_config: Optional[SubjectConfig]
    load_subjects: Optional[str]
    max_retries: int = 3
    assume_yes: bool = False
    detect_duplicates: bool = False

    @validator("compression_level")
    def validate_compression_level(cls, val):  # pylint: disable=no-self-argument, no-self-use
        """Validate compression level."""
        if val not in range(-1, 9):
            raise ValueError("Compression level needs to be between 0-9")
        return val

    def create_walker(self, **kwargs):
        """Create walker"""
        for key in ("include", "exclude", "include_dirs", "exclude_dirs"):
            kwargs[key] = util.merge_lists(kwargs.get(key, []), getattr(self, key, []))
        kwargs.setdefault("follow_symlinks", self.symlinks)

        return walker.create_walker(self.src_fs, **kwargs)

    def register_encoding_aliases(self):
        """Register common encoding aliases"""
        import encodings  # pylint: disable=import-outside-toplevel
        for encoding_spec in self.encodings:
            key, _, value = encoding_spec.partition('=')
            encodings.aliases.aliases[key.strip().lower()] = value.strip().lower()

    def get_compression_type(self):
        """Returns compression type"""
        if self.compression_level == 0:
            return zipfile.ZIP_STORED
        return zipfile.ZIP_DEFLATED

    class ArgparserConfig:  # pylint: disable=R0903
        """Argparser options"""
        src_fs = {
            "positional": True,
            "metavar": "SRC",
            "help": "The path to the folder to import",
        }
        symlink = {"help": "Follow symbolic links that resolve to directories"}
        include_dirs = {
            "metavar": "PATTERN",
            "nargs": "+",
            "help": "Patterns of directories to include",
        }
        exclude_dirs = {
            "metavar": "PATTERN",
            "nargs": "+",
            "help": "Patterns of directories to exclude",
        }
        include = {
            "metavar": "PATTERN",
            "nargs": "+",
            "help": "Patterns of filenames to include",
        }
        exclude = {
            "metavar": "PATTERN",
            "nargs": "+",
            "help": "Patterns of filenames to exclude",
        }
        compression_level = {
            "help": (
                "The compression level to use for packfiles -1 by default. "
                "0 for store. "
                "A higher compression level number means more compression."
            )
        }
        ignore_unknown_tags = {"help": "Ignore unknown dicom tags when parsing dicom files"}
        encodings = {
            "nargs": "+",
            "help": "Set character encoding aliases. E.g. win_1251=cp1251",
        }
        de_identify = {"help": "De-identify DICOM files"}
        deid_profile = {
            "metavar": "NAME",
            "help": "Use the De-identify profile by name",
        }
        skip_existing = {"help": "Skip import of existing files"}
        no_audit_log = {"help": "Skip uploading audit log to the target projects"}
        load_subjects = {
            "metavar": "PATH",
            "help": "Load subjects from the specified file",
        }
        detect_duplicates = {
            "help": ("Identify duplicate data conflicts within source data "
                     "and duplicates between source data and data in Flywheel. "
                     "Duplicates are skipped and noted in audit log"),
        }


class ReporterConfig(BaseConfig):
    """Follow ingest configuration"""
    assume_yes: bool = False
    verbose: bool = False
    refresh_interval: int = 1
    save_audit_logs: Optional[str]
    save_deid_logs: Optional[str]
    save_subjects: Optional[str]


    class ArgparserConfig:  # pylint: disable=R0903
        """Argparser options"""
        save_audit_logs = {
            "metavar": "PATH",
            "help": "Save audit log to the specified path on the current machine",
        }
        save_deid_logs = {
            "metavar": "PATH",
            "help": "Save deid log to the specified path on the current machine",
        }
        save_subjects = {
            "metavar": "PATH",
            "help": "Save subjects to the specified file",
        }


class WorkerConfig(BaseConfig):  # pylint: disable=R0903
    """Ingest worker configuration"""
    db_url: Optional[str]
    sleep_time: int = 1
    jobs: int = max(1, math.floor(multiprocessing.cpu_count() / 2))
    max_tempfile: int = 50
    buffer_size: int = 65536
    worker_name: str = socket.gethostname()
    # kubernetes default termination grace period is 30 seconds
    # keep it lower in the worker to have time to set ingest/task status
    # if it can't complete the task in time
    termination_grace_period: int = 15

    @validator("db_url")
    def db_required(cls, val):  # pylint: disable=no-self-argument, no-self-use
        """Validate that database connection string is not None"""
        if not val:
            random_part = binascii.hexlify(os.urandom(16)).decode("utf-8")
            filepath = os.path.join(tempfile.gettempdir(), f"flywheel_cli_ingest_{random_part}.db")
            return f"sqlite:///{filepath}"
        return val

    class ArgparserConfig:  # pylint: disable=R0903
        """Argparser options"""
        jobs = {"help": "The number of concurrent jobs to run (e.g. scan jobs)"}
        sleep_time = {
            "metavar": "SECONDS",
            "help": "Number of seconds to wait before trying to get a task",
        }
        max_tempfile = {
            "help": "The max in-memory tempfile size, in MB, or 0 to always use disk",
        }


# Ingest strategy configs

class DicomConfig(BaseConfig):
    """Config class for dicom ingest strategy"""
    strategy_name = "dicom"
    group: str
    project: str
    subject: Optional[str]
    session: Optional[str]

    @validator("group")
    def validate_group_id(cls, val):  # pylint: disable=no-self-argument, no-self-use
        """Validate group id"""
        return util.group_id(val)

    class ArgparserConfig:
        """Argparser config"""
        group = {
            "positional": True,
            "nargs": "?",
            "metavar": "GROUP_ID",
            "help": "The id of the group",
        }
        project = {
            "positional": True,
            "nargs": "?",
            "metavar": "PROJECT_LABEL",
            "help": "The label of the project",
        }
        subject = {
            "metavar": "LABEL",
            "help": "Override value for the subject label",
        }
        session = {
            "metavar": "LABEL",
            "help": "Override value for the session label",
        }


class FolderConfig(BaseConfig):
    """Config class for folder import strategy"""
    strategy_name = "folder"
    group: Optional[str]
    project: Optional[str]
    dicom: str = "dicom"
    pack_acquisitions: Optional[str]
    root_dirs: int = 0
    no_subjects: bool = False
    no_sessions: bool = False
    group_override: Optional[str]
    project_override: Optional[str]

    @validator("group")
    def validate_group(cls, val):  # pylint: disable=no-self-argument, no-self-use
        """Validate group id"""
        if val:
            return util.group_id(val)
        return val

    @validator("group_override")
    def validate_group_override(cls, val):  # pylint: disable=no-self-argument, no-self-use
        """Validate group id"""
        if val:
            return util.group_id(val)
        return val

    class ArgparserConfig:
        """Argparser config"""
        _groups = {
            "acq": {"type": "mutually_exclusive"},
            "no_level": {"type": "mutually_exclusive"},
        }
        group = {
            "flags": ["-g", "--group"],
            "metavar": "ID",
            "help": "The id of the group, if not in folder structure",
        }
        project = {
            "flags": ["-p", "--project"],
            "metavar": "LABEL",
            "help": "The label of the project, if not in folder structure",
        }
        dicom = {
            "group": "acq",
            "metavar": "NAME",
            "help": "The name of dicom subfolders to be zipped prior to upload",
        }
        pack_acquisitions = {
            "group": "acq",
            "metavar": "TYPE",
            "help": "Acquisition folders only contain acquisitions of TYPE and are zipped prior to upload",
        }
        root_dirs = {"help": "The number of directories to discard before matching"}
        no_subjects = {
            "group": "no_level",
            "help": "no subject level (create a subject for every session)",
        }
        no_sessions = {
            "group": "no_level",
            "help": "no session level (create a session for every subject)",
        }
        group_override = {
            "flags": ["--group-override"],
            "metavar": "ID",
            "help": "Force using this group id",
        }
        project_override = {
            "flags": ["--project-override"],
            "metavar": "LABEL",
            "help": "Force using this project label",
        }


class TemplateConfig(BaseConfig):
    """Template ingest strategy configuration"""
    strategy_name = "template"
    template: Union[str, List]
    group: Optional[str]
    project: Optional[str]
    no_subjects: bool = False
    no_sessions: bool = False
    group_override: Optional[str]
    project_override: Optional[str]

    @validator("group")
    def validate_group(cls, val):  # pylint: disable=no-self-argument, no-self-use
        """Validate group id"""
        if val:
            return util.group_id(val)
        return val

    @validator("group_override")
    def validate_group_override(cls, val):  # pylint: disable=no-self-argument, no-self-use
        """Validate group id"""
        if val:
            return util.group_id(val)
        return val

    class ArgparserConfig:
        """Argparser config"""
        template = {
            "positional": True,
            "nargs": "?",
            "metavar": "TEMPLATE",
            "help": "The template string",
        }
        group = {
            "flags": ["-g", "--group"],
            "metavar": "ID",
            "help": "The id of the group, if not in folder structure",
        }
        project = {
            "flags": ["-p", "--project"],
            "metavar": "LABEL",
            "help": "The label of the project, if not in folder structure",
        }
        no_subjects = {
            "group": "no_level",
            "help": "no subject level (create a subject for every session)",
        }
        no_sessions = {
            "group": "no_level",
            "help": "no session level (create a session for every subject)",
        }
        group_override = {
            "flags": ["--group-override"],
            "metavar": "ID",
            "help": "Force using this group id",
        }
        project_override = {
            "flags": ["--project-override"],
            "metavar": "LABEL",
            "help": "Force using this project label",
        }


StrategyConfig = Union[DicomConfig, FolderConfig, TemplateConfig]


class ConfigError(ValueError):
    """ConfigError"""
