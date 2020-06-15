from git_pr_branch.repo import GitRemote, GitBranch


def get_remote_for_pr(repo, pr):
    track_remote = None
    # Look for an existing remote
    for remote in repo.get_remotes():
        remote_repo = remote.get_server_repo()
        if remote_repo.fullname == pr.head_fullname:
            track_remote = remote
    # Create remote if needed
    if not track_remote:
        track_remote = GitRemote.create(pr.head_username, pr.head_ssh)
    return track_remote


def create_pr_branch(pr, branch_id, remote, reference):
    branch_name = f"PR/{pr.number}/{branch_id}"
    remote.fetch(reference, quiet=True)
    branch = GitBranch.create_from(branch_name, "FETCH_HEAD")
    branch.set_upstream_to(remote, pr.head_branch, quiet=True)
    return branch
