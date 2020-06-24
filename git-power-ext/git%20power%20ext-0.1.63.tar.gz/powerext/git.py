import subprocess
from . import common

def fetch():
    print("### Updating from remote ⏬⏬")
    subprocess.run(["git fetch -p"], shell=True)

def checkout(branch):
    print(f"\nchecking out {branch}")
    subprocess.run(["git", "checkout", branch])

def pull(branch):
    checkout(branch)
    merge()

def get_remote_name():
    return subprocess.run(["git remote"], shell=True, capture_output=True, universal_newlines=True).stdout.strip()

def get_current_branch():
    return subprocess.run(["git symbolic-ref --short -q HEAD"], shell=True, capture_output=True, universal_newlines=True).stdout.strip()

def get_merged_branches(branch="master"):
    # checkout(branch)
    merged_branches = common.get_list_from_string(subprocess.run([f"git branch -r --merged {branch} --no-contains {branch} | egrep -v \"(^\*|master)\""], shell=True, capture_output=True, universal_newlines=True).stdout.replace(f"{get_remote_name()}/", ""))
    return merged_branches

def get_branches_deleted_remotely():
    return common.get_list_from_string(subprocess.run(["git for-each-ref --format '%(refname) %(upstream:track)' refs/heads | awk '$2 == \"[gone]\" {sub(\"refs/heads/\", \"\", $1); print $1}'"], shell=True, capture_output=True, universal_newlines=True).stdout)

def get_all_branches(remote:bool=True):
    remote_option = "-r"
    if not remote:
        remote_option = ""
    return common.get_list_from_string(subprocess.run([f"git branch {remote_option} | egrep -v \"(^\*|master)\""], shell=True, capture_output=True, universal_newlines=True).stdout)

def get_stale_branches(days_since_updated:int=90):
    all_remote_branches = get_all_branches()
    stale_branches = []
    for branch in all_remote_branches:
        if subprocess.run([f"git log -1 --since={days_since_updated}.days -s {branch}"], shell=True, capture_output=True, universal_newlines=True).stdout == "":
            stale_branches.append(branch)
    remote_name = get_remote_name()
    return common.replace_every_string(f"{remote_name}/", "", stale_branches) 

def delete_branch(branch, local, remote=False, remote_name="origin", force=False):
    if local:
        delete_option = "-d"
        if force:
            delete_option = "-D"
        subprocess.run([f"git branch {delete_option} {branch}"], shell=True, universal_newlines=True)

    if remote:
        subprocess.run([f"git push {remote_name} :{branch}"], shell=True, universal_newlines=True)

def merge():
    subprocess.run(["git merge"], shell=True)

def pull_all_branches():
    fetch()
    current_branch = get_current_branch()
    all_remote_branches = common.replace_every_string(f"{get_remote_name()}/", "", get_all_branches())
    for remote_branch in all_remote_branches:
        checkout(remote_branch)
        merge() 
    checkout(current_branch)

""" A list of branches not pushed you need to keep them safe 
"""
def get_local_branches_not_in_remote():
    local_branches = set(get_all_branches(remote=False))
    remote_branches = set(common.replace_every_string(f"{get_remote_name()}/", "", get_all_branches(remote=True)))
    return local_branches - remote_branches

""" A list of branches that pushed and can be deleted safely 
    (enhancement needs to be done to make sure that local matches the reference/hash of the tracking remote)
"""
def get_local_branches_that_in_remote():
    local_branches = set(get_all_branches(remote=False))
    remote_branches = set(common.replace_every_string(f"{get_remote_name()}/", "", get_all_branches(remote=True)))
    return local_branches & remote_branches
