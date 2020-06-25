# import logging
# from typing import List
#
# from git import Repo
#
# import forge_template.util.log_util as log_utils
#
# FORGE_REMOTE_NAME = "forge-template"
#
#
# def push_content_to_repo(repo: Repo, repo_name: str) -> None:
#     repo.index.add("*")
#     added_files = [key[0] for key in repo.index.entries.keys()]
#     repo.git.commit("-m", "initial commit")
#     repo.git.push("--set-upstream", "origin", "master")
#     for added_file in added_files:
#         log_utils.print_success_added(repo_name, "Repository", added_file, "File")
#
#
# def check_remotes_to_add(repo: Repo, remote_name: str, remotes_to_rename: List, remotes_to_add: List) -> None:
#     origin_exists = is_remote_in_remotes(repo, "origin")
#     if origin_exists:
#         remotes_to_rename.append(["origin", FORGE_REMOTE_NAME])
#         remotes_to_add.append(remote_name)
#
#
# def add_remotes(remotes_to_add: List, url: str, repo: Repo, remotes_added: List) -> None:
#     for remote in remotes_to_add:
#         repo.create_remote(remote, url=url)
#         remotes_added.append(remote)
#         log_utils.print_success_created(remote, "Remote")
#
#
# def rename_remotes(remotes_to_rename: List, repo: Repo, renamed_remotes: List) -> List:
#     for (old_name, new_name) in remotes_to_rename:
#         if is_remote_in_remotes(repo, old_name):
#             repo.remote(old_name).rename(new_name)
#             renamed_remotes.append((new_name, old_name))
#             logging.info(f"Renamed remote {old_name} to {new_name}")
#     return renamed_remotes
#
#
# def remove_remotes(remote_list: List, repo: Repo) -> None:
#     for remote in remote_list:
#         if is_remote_in_remotes(repo, remote):
#             repo.git.remote("rm", remote)
#             log_utils.print_success_deleted(remote, "Remote")
#
#
# def is_remote_in_remotes(repo: Repo, remote_name: str) -> bool:
#     return remote_name in [remote.name for remote in repo.remotes]
