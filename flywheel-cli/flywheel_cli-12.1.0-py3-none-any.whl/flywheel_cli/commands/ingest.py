"""ingest subcommand"""

import atexit
import logging
import os
import sys

from pydantic import ValidationError

from .. import util
from ..ingest.client import APIClient, DBClient
from ..ingest.client import db
from ..ingest import config
from ..ingest import reporter
from ..ingest import schemas as T
from ..ingest import worker

log = logging.getLogger(__name__)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


def add_commands(subparsers):
    """Add command to a given subparser"""
    # ingest w dicom strategy
    IngestCommand(config.DicomConfig, subparsers, "dicom", help="Ingest dicom files")
    # ingest w folder strategy
    IngestCommand(config.FolderConfig, subparsers, "folder", help="Ingest a folder")
    # ingest w template strategy
    IngestCommand(config.TemplateConfig, subparsers, "template", help="Ingest a folder using a template")
    # add follow subcommand
    FollowCommand(subparsers, "follow")
    ## add abort subcommand
    AbortCommand(subparsers, "abort")
    return subparsers


class Config:  # pylint: disable=R0903
    """Wrapper class around a dict which contains different configurations
    and provides easy access by dot notation
    """
    def __init__(self, configs):
        self.configs = configs

    def __getattr__(self, name):
        conf = self.configs.get(name)
        if not conf:
            raise AttributeError(f"Unknown attribute: {name}")
        return conf


class Command:
    """Base command that adds the general configutaion"""
    configs = {}

    def __init__(self, parent, name, **parser_kwargs):
        self.config = None
        # setup parser
        if parser_kwargs.get("add_help", True):
            parser_kwargs.setdefault("help", self.__class__.__doc__)
        self.parser = parent.add_parser(name, **parser_kwargs)
        self.parser.set_defaults(func=self.run)
        self.parser.set_defaults(config=self.load_config)
        # setup configs
        self.configs = {
            **self.configs,
            "general": config.ArgparseGroup(config.GeneralConfig, "General")
        }
        # finally add config arguments to the parser
        self.add_arguments()

    def add_arguments(self):
        """Add all config arguments to the parser"""
        for cls in self.configs.values():
            config.add_arguments(cls, self.parser)

    def load_config(self, args):
        """Load all config"""
        if getattr(args, "help", False):
            self.parser.print_help()
            sys.exit(0)
            return
        loaded = {}
        for name, cls in self.configs.items():
            try:
                loaded[name] = config.load_config(cls, args)
            except ValidationError as err:
                errors = "\n".join(f"{e['loc'][0]}: {e['msg']}" for e in err.errors())
                self.parser.error(f"The following errors found during parsing configuration:\n{errors}")
        self.config = Config(loaded)
        self.config.general.startup_initialize()

    def run(self, args):
        """Body of the command"""


class IngestCommand(Command):
    """Ingest subcommand"""
    configs = {
        "ingest": config.IngestConfig,
        "reporter": config.ArgparseGroup(
            config.ReporterConfig,
            "Reporter",
            description=(
                "These config options are only available when using "
                "cluster mode with the --follow argument "
                "or when using local worker."
            ),
        ),
        "cluster": config.ArgparseGroup(
            config.ClusterConfig,
            "Cluster",
            description="These config options apply when using a cluster to ingest data.",
        ),
        "worker": config.ArgparseGroup(
            config.WorkerConfig,
            "Worker",
            description=(
                "These config options are only available when using "
                "local worker (--cluster is not defined)"
            ),
        )
    }

    def __init__(self, strategy_config_cls, *args, **kwargs):
        self.configs = {
            "strategy": strategy_config_cls,
            **self.configs
        }
        super().__init__(*args, **kwargs)

    def run(self, args):
        if self.config.cluster.cluster:
            self.run_cluster_ingest()
        else:
            self.run_local_ingest()

    def run_local_ingest(self):
        """Run local ingest with local workers and sqlite databse backend"""
        log.debug(f"Using database: {self.config.worker.db_url}")
        if not self.config.general.debug:
            # delete db file on exit if not in debug mode
            filepath = self.config.worker.db_url.replace("sqlite:///", "")
            atexit.register(delete_file, filepath)
        # essetial to start workers (fork) before initiating flywheel client anywhere
        worker_pool = worker.WorkerPool(self.config.worker)
        worker_pool.start()
        db.set_lock(worker_pool.lock)
        ingest_db = DBClient(self.config.worker.db_url)
        ingest_db.create_ingest(self.config.ingest, self.config.strategy)
        self.load_subjects(ingest_db)
        ingest_db.start()
        reporter_ = reporter.Reporter(ingest_db, self.config.reporter)
        try:
            reporter_.run()
        except KeyboardInterrupt:
            ingest_db.abort()
            # wait for workers to shut down
            worker_pool.join()
            # and print the final report
            reporter_.final_report()
        finally:
            log.debug("Shutting down workers gracefully")
            worker_pool.shutdown()

    def run_cluster_ingest(self):
        """Run cluster managed ingest"""
        ingest_api = APIClient(self.config.cluster.cluster)
        ingest_api.create_ingest(self.config.ingest, self.config.strategy)
        self.load_subjects(ingest_api)
        ingest_url = self.config.cluster.save_ingest_operation_url(ingest_api.ingest_id)
        ingest_api.start()

        print(f"Started ingest {ingest_url}")
        print("Use `fw ingest follow` to see progress or `fw ingest abort` to abort it")

        if self.config.cluster.follow:
            reporter.Reporter(ingest_api, self.config.reporter).run()

    def load_subjects(self, client):
        """Load subjects if it was requested"""
        if self.config.ingest.load_subjects:
            with open(self.config.ingest.load_subjects, "r") as fp:
                client.load_subject_csv(fp)


class FollowCommand(Command):
    """Follow the progress of a cluster managed ingest operation"""
    configs = {
        "reporter": config.ReporterConfig,
        "manage": config.ManageConfig,
    }

    def run(self, args):
        ingest_api = APIClient.from_url(self.config.manage.cluster, self.config.manage.ingest_id)
        reporter.Reporter(ingest_api, self.config.reporter).run()


class AbortCommand(Command):
    """Abort a cluster managed ingest operation"""
    configs = {"manage": config.ManageConfig}

    def run(self, args):
        ingest_api = APIClient.from_url(self.config.manage.cluster, self.config.manage.ingest_id)
        ingest = ingest_api.ingest
        if T.IngestStatus.is_terminal(ingest.status):
            print(f"Ingest already {ingest.status}")
            return
        msg = "Are you sure you want to abort the ingest?"
        if self.config.general.assume_yes or util.confirmation_prompt(msg):
            ingest_api.abort()


def delete_file(filepath):
    """Delete a given file if exists"""
    if os.path.exists(filepath):
        log.debug(f"Clean up file: {filepath}")
        os.remove(filepath)
