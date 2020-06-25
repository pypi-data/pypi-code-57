import argparse
import concurrent.futures
import os
import subprocess
import sys
from collections import OrderedDict

from graphops import Graphops
from helpers import read_selection

_AUTHOR = "Aki Mäkinen"
_REPOSITORY = "https://github.com/XC-/git-workspace"
_LICENSE = "MIT"

WORKSPACE_FILE = ".workspace"
WORKSPACE_GIT_CONFIGURATION = ".workspace-git-config"
WORKSPACE_DIR = None

DEFAULT_LOCATION = "$HOME/.local/bin"
SCRIPT_NAME = os.path.basename(__file__)

_DEBUG = os.getenv("DEBUG")


def debug_print(*args):
    if _DEBUG is not None:
        print(*args)


def disabled(msg):
    print(msg)
    exit(1)


def search_workspace():
    directory = os.getcwd()
    while directory != "/":
        debug_print(directory)
        if WORKSPACE_FILE in os.listdir(directory):
            return directory
        directory = os.path.realpath(os.path.join(directory, ".."))
    return None


def read_repositories(wsdir):
    repositories = {}

    with open(os.path.join(wsdir, WORKSPACE_FILE), "r") as file:
        lines = file.readlines()

    for line in lines:
        cleaned = line.strip()
        if cleaned:
            debug_print(cleaned)
            name = cleaned.split("/")[-1].split(".")[0]
            repositories[name] = cleaned

    return OrderedDict(sorted(repositories.items()))


def read_git_configuration(wsdir):
    gitconfiguration = {}

    with open(os.path.join(wsdir, WORKSPACE_GIT_CONFIGURATION), "r") as file:
        lines = file.readlines()

    for line in lines:
        parts = line.strip().split("=")
        gitconfiguration[parts[0]] = parts[1]

    return gitconfiguration


def install():
    userinput = input(f"Install to directory [{DEFAULT_LOCATION}]: ")
    if userinput:
        target = userinput
    else:
        target = DEFAULT_LOCATION
    target = os.path.join(target, os.path.basename(__file__))
    script_path = os.path.realpath(__file__)
    sp = subprocess.run(f"ln -s {script_path} {target}", shell=True)
    return sp.returncode


def init_workspace():
    workspacedir = search_workspace()
    if workspacedir is not None:
        print(f"Found a workspace from {workspacedir}, "
              f"will not continue as nested workspaces are not supported at the moment.")
        exit(1)
    wsfile = open(WORKSPACE_FILE, "w+")
    wsfile.close()

    with open(WORKSPACE_GIT_CONFIGURATION, "w+") as f:
        f.write("GITUSER=\n")
        f.write("GITHOST=\n")


def git_clone(wsdir, repositories, git_configuration):
    gc = git_configuration

    def clone(repo):
        sp = subprocess.run(f"git clone {gc['GITUSER']}@{gc['GITHOST']}:{repo}",
                            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            cwd=wsdir)
        if sp.returncode > 0:
            print(f"Failed to clone {repo}: ")
            debug_print(sp.stderr.decode("utf-8"))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_clone = {executor.submit(clone, repo): repo for name, repo in repositories.items()}
        for future in concurrent.futures.as_completed(future_to_clone):
            repo = future_to_clone[future]
            print(f"Finished cloning {repo}")


def ws_state(wsdir, repositories):
    name_length = 10
    for k, v in repositories.items():
        if len(k) + 2 > name_length:
            name_length = len(k) + 2

    print(f"{'Directory':<{name_length}} "
          f"{'Current branch':<60} "
          f"{'Behind origin/master':<25} "
          f"{'Uncommitted files':<25} "
          f"{'Untracked files':<25}")
    for name, repo in repositories.items():
        cbsp = subprocess.run(f"git --git-dir={wsdir}/{name}/.git branch | grep \* | cut -d ' ' -f2",
                              shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        if cbsp.returncode > 0:
            current_branch = "error"
        else:
            current_branch = cbsp.stdout.strip().decode("utf-8")

        bdsp = subprocess.run(f"git --git-dir={wsdir}/{name}/.git rev-list "
                              f"--count {current_branch}..origin/master 2>/dev/null",
                              shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        if bdsp.returncode > 0:
            branch_diff = "error"
        else:
            branch_diff = bdsp.stdout.strip().decode("utf-8")

        mcsp = subprocess.run(f"git ls-files --modified | wc -w",
                              shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, cwd=os.path.join(wsdir, name))
        if mcsp.returncode > 0:
            modified_count = "error"
        else:
            modified_count = mcsp.stdout.strip().decode("utf-8")

        ucsp = subprocess.run(f"git ls-files --exclude-standard --others | wc -l",
                              shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, cwd=os.path.join(wsdir, name))
        if ucsp.returncode > 0:
            untracked_count = "error"
        else:
            untracked_count = ucsp.stdout.strip().decode("utf-8")

        print(f"{name:<{name_length}} "
              f"{current_branch:<60} "
              f"{branch_diff:<25} "
              f"{modified_count:<25} "
              f"{untracked_count:<25}")


def in_repository_operation(op, repositories, wsdir):
    for name, repo in repositories.items():
        if not os.path.exists(os.path.join(wsdir, name)):
            print(f"Repository {name} not found. Skipping...")
            continue

        print(f"**** {name} ****")
        sp = subprocess.run(f"git {op}", stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, shell=True, cwd=os.path.join(wsdir, name))
        print(sp.stdout.decode("utf-8"))
        if sp.returncode > 0:
            print(sp.stderr.decode("utf-8"))

        print(f"{'':-^60}")


def main():
    ws = search_workspace()
    gconf = {}
    reps = {}
    if ws is not None:
        gconf = read_git_configuration(ws)
        reps = read_repositories(ws)

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Git Workspace

Aki Mäkinen
https://gitlab.com/blissfulreboot/python/git-workspace
Licensed under MIT license
        """,
        epilog="""
Configuration:

  Configuration is currently in two parts. One is shareable workspace file and the other one will be user specific
  configuration containing git host and user. This is to allow for example multiple bitbucket accounts and ssh keys.
  Downside is that in the first version of this script, the user and host must be the same for all repositories.
  This is something to be looked into.

  $WORKSPACE_FILE:
    - One line, one repository
    - <path>/<repository>.git
    - e.g.
      MyGithubAccount/exmplarepository.git
      MyFriendsGithubAccount/collaborativerepository.git

  $WORKSPACE_GIT_CONFIGURATION:
    - Git user
    - Git host
    - e.g.
      GITUSER=git
      GITHOST=github.com
      
  .git-ws.graphops example:
    {
      "deploy": {
        "script": "foobar3.sh",
        "requires": ["a", "b"]
      }
    }
        """
    )

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("init",
                          help="Create a new (empty) workspace definition to the current directory")
    subparsers.add_parser("clone",
                          help="Clone the repositories defined in the $WORKSPACE_FILE file")
    subparsers.add_parser("state",
                          help="Display workspace state")
    subparsers.add_parser("help",
                          help="Display this help and exit")
    command_parser = subparsers.add_parser("command",
                          help="The command can also be any CLI command such as 'ls -la' or 'echo'."
                               "It will be run under each workspace directory.")
    command_parser.add_argument("clicommand",
                                nargs=argparse.REMAINDER,
                                help="CLI command as if run in the directory")
    go_parser = subparsers.add_parser("graphops",
                                      aliases=["go"],
                                      help="Graphops commands")
    go_subparsers = go_parser.add_subparsers(dest="go")

    # SIMULATION
    go_simulate_parser = go_subparsers.add_parser("simulate",
                                                  help="Run simulation of the operation pipeline")
    go_simulate_parser.add_argument("operation",
                                    action="store",
                                    default=None,
                                    nargs="?",
                                    help="Operation pipeline name")
    go_simulate_parser.add_argument("--env_var",
                                    action="append",
                                    default=[],
                                    help="Define environment variable to pass to the pipeline")

    # EXECUTE
    go_execute_parser = go_subparsers.add_parser("execute",
                                                 help="Run the operation pipeline")
    go_execute_parser.add_argument("operation",
                                   action="store",
                                   default=None,
                                   nargs="?",
                                   help="Operation pipeline name")
    go_execute_parser.add_argument("--env_var",
                                    action="append",
                                   default=[],
                                    help="Define environment variable to pass to the pipeline")

    # VISUALIZE
    go_subparsers.add_parser("visualize",
                             help="Visualize the pipelines as directed graphs")
    go_subparsers.add_parser("visualize-and-save",
                             help="Visualize the pipelines as directed graphs and save")

    # LIST OPERATIONS
    go_subparsers.add_parser("operations",
                             help="List available operations")
    go_subparsers.add_parser("",
                             help="List available operations")
    args = vars(parser.parse_args())

    if os.environ.get("DEBUG") == "true":
        print(args)

    commands = {
        "push": lambda: disabled("Push is disabled because it is not safe to do as a workspace wide operation."),
        "go": {
            "simulate": lambda operation, env: Graphops(ws, env).simulate_execute_operation(operation),
            "execute": lambda operation, env: Graphops(ws, env).execute_operation(operation),
            "visualize": lambda: Graphops(ws).visualize_operations(),
            "visualize-and-save": lambda: Graphops(ws).visualize_operations_and_save(),
            "operations": lambda: Graphops(ws).list_operations()
        }
    }

    cmd = args.get("command")
    # Help and init as special cases first
    if cmd == "help" or cmd == None:
        parser.print_help()
    elif cmd == "init":
        if ws is not None:
            print("Nested workspaces are not currently supported")
            exit(1)
        init_workspace()
    elif ws is not None or len(reps.keys()) > 0:
        if cmd == "command":
            if len(args.get("clicommand")) == 0:
                print("No CLI command specified")
                exit(1)
            in_repository_operation(" ".join(args.get("clicommand")), reps, ws)
        elif cmd == "clone":
            git_clone(ws, reps, gconf)
        elif cmd == "state":
            ws_state(ws, reps)
        elif cmd in ["graphops", "go"]:
            go_cmd = args.get("go")
            if go_cmd is None:
                go_cmd = read_selection(commands["go"].keys(), "Select graphops command...").get("selection")
            if go_cmd in ["simulate", "execute"]:
                commands["go"][go_cmd](args.get("operation"), args.get("env_var", []))
            elif go_cmd in ["visualize", "visualize-and-save", "operations"]:
                commands["go"][go_cmd]()
        else:
            print(f"Unkown command: {cmd}")
            exit(1)
    else:
        print("Workspace is either empty or was not found.")
        exit(1)
