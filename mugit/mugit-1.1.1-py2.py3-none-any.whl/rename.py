"""
rename.py

This command is used to change the names of branches currently selected
in the workspace.

Copyright (c) 2020 Richard Walters
"""

from __future__ import print_function
from __future__ import absolute_import

import os
import subprocess
import sys

from .manifest import Manifest
from .repository import Repository

class Rename:
    description = "rename currently selected branches"

    @staticmethod
    def PrintUsage():
        print("usage: mugit rename <-l|-r> [--] <OLD_BRANCH> <NEW_BRANCH> [PATH]..")
        print("   or: mugit rename -h|-?|--help")
        print("")
        print("    -h          Print this usage information and exit")
        print("    -?          Print this usage information and exit")
        print("    --help      Print this usage information and exit")
        print("    -l          Rename local branches and push them to remotes")
        print("    -r          Remove old remote branches and update remote heads")
        print("")
        print("    OLD_BRANCH  Old name of branches to be renamed")
        print("    NEW_BRANCH  New name of branches to be renamed")
        print("    PATH        Optional repository selector (default is all)")
        print("")
        print("Rename the currently selected branches using the given OLD_BRANCH name")
        print("to use the given NEW_BRANCH name instead.  Go through the entire")
        print("workspace by default, unless one or more PATH names are given, in which")
        print("case, only rename the branches matching in those repositories.")
        print("")
        print("This command is currently designed to be used in the following way, due to")
        print("limitations on what can be done through git alone:")
        print("1. Run this command with the -l option, to change the branch")
        print("   names locally and push them as new branches to the remotes.")
        print("2. If the old branch name happens to be the \"default\" branch in any remotes,")
        print("   go to the remotes through other means (example: for GitHub, navigate")
        print("   a web browser to https://github.com/(username)/(repo)/settings/branches")
        print("   and use the interface there) to switch the default branches, in order to")
        print("   allow for the old branches to be deleted in the next step.")
        print("3. Run this command again with the -r option instead, to delete the old")
        print("   branch names from the remotes and update the remote heads.")

    @staticmethod
    def __call__(args):
        needHelp = False
        createNewBranches = False
        deleteOldBranches = False
        acceptingOptions = True
        unknownOptions = []
        oldBranch = None
        newBranch = None
        paths = []
        for arg in args:
            if (
                acceptingOptions
                and (len(arg) >= 1)
                and (arg[0] == '-')
            ):
                if (
                    (len(arg) >= 2)
                    and (arg[1] == '-')
                ):
                    option = arg
                    if option == "--":
                        acceptingOptions = False
                    elif option == "--help":
                        needHelp = True
                    else:
                        unknownOptions.append(option)
                else:
                    for i in range(1, len(arg)):
                        option = arg[i]
                        if option in ['h', '?']:
                            needHelp = True
                        elif option == 'l':
                            createNewBranches = True
                        elif option == 'r':
                            deleteOldBranches = True
                        else:
                            unknownOptions.append(option)
            else:
                if oldBranch:
                    if newBranch:
                        paths.append(arg)
                    else:
                        newBranch = arg
                else:
                    oldBranch = arg
        if needHelp:
            Rename.PrintUsage()
            return 0
        if len(unknownOptions) > 0:
            for option in unknownOptions:
                print("error: unknown option: %s" % (option))
            Rename.PrintUsage()
            return 1
        if not (createNewBranches or deleteOldBranches):
            print("error: either -l or -r option required")
            print("")
            Rename.PrintUsage()
            return 1
        if oldBranch is None:
            print("error: no old branch name specified")
            print("")
            Rename.PrintUsage()
            return 1
        if newBranch is None:
            print("error: no new branch name specified")
            print("")
            Rename.PrintUsage()
            return 1
        manifest = Manifest.FromWorkspace()
        originalWorkingDirectory = os.getcwd()
        changed = False
        try:
            for repository in manifest.repositories:
                doCreateStep = (
                    createNewBranches
                    and (repository.branch == oldBranch)
                )
                doDeleteStep = (
                    deleteOldBranches
                    and (repository.branch == newBranch)
                    and repository.RemoteBranchExists(oldBranch)
                )
                if (
                    (
                        (repository.path in paths)
                        or len(paths) == 0
                    )
                    and (doCreateStep or doDeleteStep)
                ):
                    remote = repository.remote
                    os.chdir(os.path.join(manifest.root, repository.path))
                    if doCreateStep:
                        print("%s: branch %s -> %s" % (repository.name, oldBranch, newBranch))
                        sys.stdout.flush()
                        repository.branch = newBranch
                        renameBranch = subprocess.Popen(
                            ["git", "branch", "-m", oldBranch, newBranch],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True
                        )
                        out, err = renameBranch.communicate()
                        if renameBranch.returncode > 0:
                            print(err, file=sys.stderr)
                            raise Exception("%s: error renaming branch %s to %s" % (repository.name, oldBranch, newBranch))
                        pushNewBranch = subprocess.Popen(
                            ["git", "push", "-u", remote, newBranch],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True
                        )
                        out, err = pushNewBranch.communicate()
                        if pushNewBranch.returncode > 0:
                            print(err, file=sys.stderr)
                            raise Exception("%s: error pushing new branch %s to remote %s" % (repository.name, newBranch, remote))
                        changed = True
                    if doDeleteStep and remote:
                        print("%s: deleting remote %s branch %s" % (repository.name, remote, oldBranch))
                        sys.stdout.flush()
                        deleteOldBranch = subprocess.Popen(
                            ["git", "push", remote, "--delete", oldBranch],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True
                        )
                        out, err = deleteOldBranch.communicate()
                        if deleteOldBranch.returncode > 0:
                            print(err, file=sys.stderr)
                            raise Exception("%s: error deleting old branch %s on remote %s" % (repository.name, oldBranch, remote))
                        print("%s: resetting default remote %s branch" % (repository.name, remote))
                        sys.stdout.flush()
                        updateRemoteHead = subprocess.Popen(
                            ["git", "remote", "set-head", remote, "-a"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True
                        )
                        out, err = updateRemoteHead.communicate()
                        if updateRemoteHead.returncode > 0:
                            print(err, file=sys.stderr)
                            raise Exception("%s: error updating remote %s head" % (repository.name, remote))
                        print("%s: pruning remote %s tracking branches" % (repository.name, remote))
                        sys.stdout.flush()
                        pruneRemoteTrackingBranches = subprocess.Popen(
                            ["git", "fetch", "--prune", remote],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True
                        )
                        out, err = pruneRemoteTrackingBranches.communicate()
                        if pruneRemoteTrackingBranches.returncode > 0:
                            print(err, file=sys.stderr)
                            raise Exception("%s: error pruning remote %s tracking branches" % (repository.name, remote))
        except Exception as exc:
            print("error: %s" % (str(exc)), file=sys.stderr)
            return 1
        finally:
            os.chdir(originalWorkingDirectory)
        if changed:
            open(os.path.join(manifest.name + ".xml"), "wt").write(manifest.ToXML())
        return 0
