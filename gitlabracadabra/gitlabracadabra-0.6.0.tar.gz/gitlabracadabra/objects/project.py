#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Mathieu Parent <math.parent@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from copy import deepcopy

from gitlab.exceptions import GitlabCreateError, GitlabListError

from gitlabracadabra.mixins.labels import LabelsMixin
from gitlabracadabra.mixins.members import MembersMixin
from gitlabracadabra.mixins.milestones import MilestonesMixin
from gitlabracadabra.mixins.mirrors import MirrorsMixin
from gitlabracadabra.mixins.variables import VariablesMixin
from gitlabracadabra.mixins.webhooks import WebhooksMixin
from gitlabracadabra.objects.group import GitLabracadabraGroup
from gitlabracadabra.objects.object import GitLabracadabraObject
from gitlabracadabra.utils import access_level


logger = logging.getLogger(__name__)


class GitLabracadabraProject(GitLabracadabraObject, LabelsMixin, MembersMixin, MilestonesMixin, MirrorsMixin,
                             VariablesMixin, WebhooksMixin):
    EXAMPLE_YAML_HEADER = 'mygroup/myproject:\n'
    DOC = [
        '# Project lifecycle',
        'create_object',
        'delete_object',
        'archived',
        'initialize_with_readme',

        '# General Settings',
        '## Naming, topics, avatar',
        'name',
        'tag_list',
        'description',
        # 'avatar',  # FIXME Gitlabracadabra
        '## Visibility, project features, permissions',
        'visibility',
        'request_access_enabled',
        'issues_access_level',
        'repository_access_level',
        'merge_requests_access_level',
        'forking_access_level',
        'builds_access_level',
        'container_registry_enabled',
        'lfs_enabled',
        # 'metrics_dashboard_access_level',  # FIXME Gitlab
        'packages_enabled',
        'wiki_access_level',
        'snippets_access_level',
        'pages_access_level',
        'emails_disabled',
        # 'show_default_award_emojis',  # FIXME Gitlab
        '## Merge requests',
        'merge_method',
        # 'merge_pipelines_enabled',  # FIXME Gitlab
        'resolve_outdated_diff_discussions',
        'printing_merge_request_link_enabled',
        'remove_source_branch_after_merge',
        'only_allow_merge_if_pipeline_succeeds',
        'allow_merge_on_skipped_pipeline',
        'only_allow_merge_if_all_discussions_are_resolved',
        'suggestion_commit_message',
        # 'merge_requests_template',  # FIXME
        '## Merge request approvals',  # FIXME ...
        'approvals_before_merge',
        # '## Badges',  # FIXME ...
        # '## Default issue template',  # FIXME ...
        # '## Service Desk',  # FIXME ...

        '# Members',
        'members',
        'unknown_members',
        'groups',
        'unknown_groups',

        # '# Integrations',  # FIXME

        '# Webhooks',
        'webhooks',
        'unknown_webhooks',

        '# Repository Settings',
        '## Default branch',
        'default_branch',
        'autoclose_referenced_issues',
        # '## Push Rules',  # FIXME ...
        '## Mirroring repositories',
        'mirrors',
        'mirror',
        'import_url',
        'mirror_user_id',
        'mirror_overwrites_diverged_branches',
        'mirror_trigger_builds',
        'only_mirror_protected_branches',
        '## Protected Branches',
        'protected_branches',
        'unknown_protected_branches',
        '## Protected Tags',
        'protected_tags',
        'unknown_protected_tags',
        # '## Deploy Keys',  # FIXME ...
        # '## Deploy Tokens',  # FIXME ...
        '## Branches',
        'branches',

        '# CI / CD Settings',
        '## General pipelines',
        'build_git_strategy',
        'ci_default_git_depth',
        'build_timeout',
        'ci_config_path',
        'public_builds',
        'auto_cancel_pending_pipelines',
        # 'forward_deployment_enabled',  # FIXME Gitlab
        'build_coverage_regex',
        '## Auto DevOps',
        'auto_devops_enabled',
        'auto_devops_deploy_strategy',
        # '## Protected Environments',  # FIXME ...
        '## Runners',
        'shared_runners_enabled',
        '## Variables',
        'variables',
        'unknown_variables',

        '# Labels',
        'labels',
        'unknown_labels',

        '# Milestones',
        'milestones',
        'unknown_milestones',

        '# Deprecated',
        'issues_enabled',
        'merge_requests_enabled',
        'jobs_enabled',
        'wiki_enabled',
        'snippets_enabled',
    ]
    SCHEMA = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "title": "Project",
        "type": "object",
        "properties": {
            # Standard properties
            "create_object": {
                "type": "boolean",
                "description": "Create object if it does not exists",
            },
            "delete_object": {
                "type": "boolean",
                "description": "Delete object if it exists",
            },
            # https://docs.gitlab.com/ee/api/projects.html#archive-a-project
            # https://docs.gitlab.com/ee/api/projects.html#unarchive-a-project
            "archived": {
                "type": "boolean",
                "description": "Archive or unarchive project",
            },
            # From https://docs.gitlab.com/ee/api/projects.html#create-project
            # and https://docs.gitlab.com/ee/api/projects.html#edit-project
            "initialize_with_readme": {
                "type": "boolean",
                "description": "false by default",
            },
            "name": {
                "type": "string",
                "description": "Project name",
            },
            # "path": {
            #     "type": "string",
            #     "description": "Repository name for new project. "
            #                    "Generated based on name if not provided (generated lowercased with dashes).",
            # },
            "tag_list": {
                "type": "array",
                "description": "Topics",
                "items": {
                    "type": "string",
                },
                "uniqueItems": True,
                "_example": '[GitLab, API, YAML]'
            },
            "description": {
                "type": "string",
                "description": "Project description",
                "_example": "|-\n    🧹 GitLabracadabra 🧙\n\n    :alembic: Adds some magic to GitLab :crystal\\_ball:"
            },
            # "avatar": {
            #     "type": "string",
            #     "description": "Project avatar",
            # },
            "visibility": {
                "type": "string",
                "description": "Project visibility",
                "enum": ["private", "internal", "public"],
            },
            "request_access_enabled": {
                "type": "boolean",
                "description": "Allow users to request access",
            },
            "issues_access_level": {
                "type": "string",
                "description": "Issues access level.",
                "enum": ["disabled", "private", "enabled"],
            },
            "repository_access_level": {
                "type": "string",
                "description": "Repository access level.",
                "enum": ["disabled", "private", "enabled"],
            },
            "merge_requests_access_level": {
                "type": "string",
                "description": "Merge requests access level.",
                "enum": ["disabled", "private", "enabled"],
            },
            "forking_access_level": {
                "type": "string",
                "description": "Forking access level.",
                "enum": ["disabled", "private", "enabled"],
            },
            "builds_access_level": {
                "type": "string",
                "description": "Builds access level.",
                "enum": ["disabled", "private", "enabled"],
            },
            "container_registry_enabled": {
                "type": "boolean",
                "description": "Enable container registry for this project",
            },
            "lfs_enabled": {
                "type": "boolean",
                "description": "Enable LFS",
            },
            "packages_enabled": {
                "type": "boolean",
                "description": "Enable or disable packages repository feature",
            },
            "wiki_access_level": {
                "type": "string",
                "description": "Wiki access level.",
                "enum": ["disabled", "private", "enabled"],
            },
            "snippets_access_level": {
                "type": "string",
                "description": "Snippets access level.",
                "enum": ["disabled", "private", "enabled"],
            },
            "pages_access_level": {
                "type": "string",
                "description": "Forking access level.",
                "enum": ["disabled", "private", "enabled", "public"],
            },
            "emails_disabled": {
                "type": "boolean",
                "description": "Disable email notifications",
            },
            "merge_method": {
                "type": "string",
                "description": "Set the merge method used",
                "enum": ["merge", "rebase_merge", "ff"],
            },
            "resolve_outdated_diff_discussions": {
                "type": "boolean",
                "description": "Automatically resolve merge request diffs discussions on lines changed with a push",
            },
            "printing_merge_request_link_enabled": {
                "type": "boolean",
                "description": "Show link to create/view merge request when pushing from the command line",
            },
            "remove_source_branch_after_merge": {
                "type": "boolean",
                "description": "Enable Delete source branch option by default for all new merge requests",
            },
            "only_allow_merge_if_pipeline_succeeds": {
                "type": "boolean",
                "description": "Set whether merge requests can only be merged with successful jobs",
            },
            "allow_merge_on_skipped_pipeline": {
                "type": "boolean",
                "description": "Set whether or not merge requests can be merged with skipped jobs",
            },
            "only_allow_merge_if_all_discussions_are_resolved": {
                "type": "boolean",
                "description": "Set whether merge requests can only be merged when all the discussions are resolved",
            },
            "suggestion_commit_message": {
                "type": "string",
                "description": "The commit message used to apply merge request suggestions",
            },
            "approvals_before_merge": {
                "type": "integer",
                "description": "How many approvers should approve merge request by default",
                "multipleOf": 1,
                "minimum": 0,
            },
            # From https://docs.gitlab.com/ee/api/members.html#add-a-member-to-a-group-or-project
            # FIXME expires_at not supported
            "members": {
                "type": "object",
                "description": "Members",
                "additionalProperties": {
                    "type": "string",
                    "description": "The permissions level to grant the member.",
                    "enum": ["guest", "reporter", "developer", "maintainer", "owner"],
                },
                "_example": ("\n"
                             "    foo: developer\n"
                             "    bar: maintainer # one of guest, reporter, developer, maintainer, owner\n"),
            },
            "unknown_members": {  # GitLabracadabra
                "type": "string",
                "description": "What to do with unknown members (`warn` by default).",
                "enum": ["warn", "delete", "remove", "ignore", "skip"],
            },
            # From https://docs.gitlab.com/ee/api/projects.html#share-project-with-group_access_level
            # and https://docs.gitlab.com/ee/api/projects.html#delete-a-shared-project-link-within-a-group
            # FIXME expires_at not supported
            "groups": {
                "type": "object",
                "description": "Groups",
                "additionalProperties": {
                    "type": "string",
                    "description": "The permissions level to grant the group.",
                    "enum": ["guest", "reporter", "developer", "maintainer"],
                },
                "_example": ("\n"
                             "    group/foo: guest\n"
                             "    group/bar: reporter # one of guest, reporter, developer, maintainer\n"),
            },
            "unknown_groups": {  # GitLabracadabra
                "type": "string",
                "description": "What to do with unknown groups (`warn` by default).",
                "enum": ["warn", "delete", "remove", "ignore", "skip"],
            },
            # From https://docs.gitlab.com/ee/api/projects.html#hooks
            "webhooks": {
                "type": "array",
                "description": "The list of project's webhooks",
                "items": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The hook URL",
                        },
                        "push_events": {
                            "type": "boolean",
                            "description": "Trigger hook on push events",
                        },
                        "push_events_branch_filter": {
                            "type": "string",
                            "description": "Trigger hook on push events for matching branches only",
                        },
                        "issues_events": {
                            "type": "boolean",
                            "description": "Trigger hook on issues events",
                        },
                        "confidential_issues_events": {
                            "type": "boolean",
                            "description": "Trigger hook on confidential issues events",
                        },
                        "merge_requests_events": {
                            "type": "boolean",
                            "description": "Trigger hook on merge requests events",
                        },
                        "tag_push_events": {
                            "type": "boolean",
                            "description": "Trigger hook on tag push events",
                        },
                        "note_events": {
                            "type": "boolean",
                            "description": "Trigger hook on note events",
                        },
                        "confidential_note_events": {
                            "type": "boolean",
                            "description": "Trigger hook on confidential note events",
                        },
                        "job_events": {
                            "type": "boolean",
                            "description": "Trigger hook on job events",
                        },
                        "pipeline_events": {
                            "type": "boolean",
                            "description": "Trigger hook on pipeline events",
                        },
                        "wiki_page_events": {
                            "type": "boolean",
                            "description": "Trigger hook on wiki events",
                        },
                        "enable_ssl_verification": {
                            "type": "boolean",
                            "description": "Do SSL verification when triggering the hook",
                        },
                        "token": {
                            "type": "string",
                            "description": ("Secret token to validate received payloads; "
                                            "this will not be returned in the response"),
                        },
                    },
                    "required": ["url"],
                    "additionalProperties": False,
                },
                "uniqueItems": True,
                "_example": ("\n"
                             "    - url: http://example.com/api/trigger\n"
                             "      push_events: true\n"
                             "      push_events_branch_filter: \"\"\n"
                             "      issues_events: true\n"
                             "      confidential_issues_events: true\n"
                             "      merge_requests_events: true\n"
                             "      tag_push_events: true\n"
                             "      note_events: true\n"
                             "      confidential_note_events: true\n"
                             "      job_events: true\n"
                             "      pipeline_events: true\n"
                             "      wiki_page_events: true\n"
                             "      enable_ssl_verification: true\n"
                             "      # token: T0k3N\n"),
            },
            "unknown_webhooks": {  # GitLabracadabra
                "type": "string",
                "description": "What to do with unknown webhooks (`warn` by default).",
                "enum": ["warn", "delete", "remove", "ignore", "skip"],
            },
            # From https://docs.gitlab.com/ee/api/projects.html#edit-project
            "default_branch": {
                "type": "string",
                "description": "`master` by default",
            },
            "autoclose_referenced_issues": {
                "type": "boolean",
                "description": "Set whether auto-closing referenced issues on default branch",
            },
            # GitLabracadabra
            "mirrors": {
                "type": "array",
                "description": "The list of project's mirrors",
                "items": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "Repository URL",
                        },
                        "direction": {
                            "type": "string",
                            "description": "Mirror direction",
                            "enum": ["pull", "push"],
                        },
                        "skip_ci": {
                            "type": "boolean",
                            "description": "Skip CI during push",
                        }
                    },
                    "required": ["url"],
                    "additionalProperties": False,
                },
                "uniqueItems": True,
                "_example": ("\n"
                             "    - url: https://gitlab.com/gitlabracadabra/gitlabracadabra.git\n"
                             "      direction: pull # one of pull, push ; only first pull mirror is processed\n"
                             # "      skip_ci: true # defaults to true\n"
                             "  builds_access_level: disabled # Recommended to prevent triggering pipelines on push"),
            },
            # From https://docs.gitlab.com/ee/api/projects.html#edit-project
            "mirror": {
                "type": "boolean",
                "description": "Enables pull mirroring in a project",
            },
            "import_url": {
                "type": "string",
                "description": "URL to import repository from",
            },
            "mirror_user_id": {
                "type": "integer",
                "description": "User responsible for all the activity surrounding a pull mirror event",
            },
            "mirror_overwrites_diverged_branches": {
                "type": "boolean",
                "description": "Pull mirror overwrites diverged branches",
            },
            "mirror_trigger_builds": {
                "type": "boolean",
                "description": "Pull mirroring triggers builds",
            },
            "only_mirror_protected_branches": {
                "type": "boolean",
                "description": "Only mirror protected branches",
            },
            # From https://docs.gitlab.com/ee/api/protected_branches.html#protect-repository-branches
            # FIXME EE features: unprotect_access_level, allowed_to_push, allowed_to_merge, allowed_to_unprotect
            "protected_branches": {
                "type": "object",
                "description": "Protected branches",
                "additionalProperties": {
                    "type": "object",
                    "properties": {
                        "push_access_level": {
                            "type": "string",
                            "description": "Access levels allowed to push (defaults: maintainer access level)",
                            "enum": ["noone", "developer", "maintainer"],
                        },
                        "merge_access_level": {
                            "type": "string",
                            "description": "Access levels allowed to merge (defaults: maintainer access level)",
                            "enum": ["noone", "developer", "maintainer"],
                        },
                    },
                },
                "_example": ("\n"
                             "    master:\n"
                             "      merge_access_level: maintainer # one of noone, developer, maintainer\n"
                             "      push_access_level: noone\n"
                             "    develop:\n"
                             "      merge_access_level: developer\n"
                             "      push_access_level: noone\n"),
            },
            "unknown_protected_branches": {  # GitLabracadabra
                "type": "string",
                "description": "What to do with unknown protected branches (`warn` by default).",
                "enum": ["warn", "delete", "remove", "ignore", "skip"],
            },
            # From https://docs.gitlab.com/ee/api/protected_tags.html#protect-repository-tags
            "protected_tags": {
                "type": "object",
                "description": "Protected tags",
                "additionalProperties": {
                    "type": "string",
                    "description": "Access levels allowed to create (defaults: maintainer access level)",
                    "enum": ["noone", "developer", "maintainer"],
                },
                "_example": ("\n"
                             "    v*: maintainer # one of noone, developer, maintainer\n"
                             "    *: developer # one of noone, developer, maintainer\n"),
            },
            "unknown_protected_tags": {  # GitLabracadabra
                "type": "string",
                "description": "What to do with unknown protected tags (`warn` by default).",
                "enum": ["warn", "delete", "remove", "ignore", "skip"],
            },
            # From https://docs.gitlab.com/ee/api/branches.html#create-repository-branch
            "branches": {
                "type": "array",
                "description": "The list of branches for a project. "
                               "Branches are created in order.",
                "items": {
                    "type": "string",
                },
                "uniqueItems": True,
                "_example": "\n    - master\n    - develop"
            },
            # From https://docs.gitlab.com/ee/api/projects.html#edit-project
            "build_git_strategy": {
                "type": "string",
                "description": "The Git strategy",
                "enum": ["fetch", "clone"],
            },
            "ci_default_git_depth": {
                "type": "integer",
                "description": "Default number of revisions for shallow cloning",
            },
            "build_timeout": {
                "type": "integer",
                "description": "The maximum amount of time in minutes that a job is able run (in seconds)",
            },
            "ci_config_path": {
                "type": "string",
                "description": "The path to CI config file",
                "_example": 'debian/salsa-ci.yml'
            },
            "public_builds": {
                "type": "boolean",
                "description": "If true, jobs can be viewed by non-project-members",
            },
            "auto_cancel_pending_pipelines": {
                "type": "string",
                "description": "Auto-cancel pending pipelines",
                "enum": ["enabled", "disabled"],
            },
            "build_coverage_regex": {
                "type": "string",
                "description": "Test coverage parsing",
            },
            "auto_devops_enabled": {
                "type": "boolean",
                "description": "Enable Auto DevOps for this project",
            },
            "auto_devops_deploy_strategy": {
                "type": "string",
                "description": "Auto Deploy strategy",
                "enum": ["continuous", "manual", "timed_incremental"],
            },
            "shared_runners_enabled": {
                "type": "boolean",
                "description": "Enable shared runners for this project",
            },
            # From https://docs.gitlab.com/ee/api/project_level_variables.html#create-variable
            "variables": {
                "type": "array",
                "description": "The list of project's variables",
                "items": {
                    "type": "object",
                    "properties": {
                        "key": {
                            "type": "string",
                            "description": "The key of a variable.",
                            "pattern": "[a-zA-Z0-9_]+",
                        },
                        "value": {
                            "type": "string",
                            "description": "The value of a variable.",
                        },
                        "variable_type": {
                            "type": "string",
                            "description": "The type of a variable. Available types are: env_var (default) and file.",
                            "enum": ["env_var", "file"],
                        },
                        "protected": {
                            "type": "boolean",
                            "description": "Whether the variable is protected.",
                        },
                        "masked": {
                            "type": "boolean",
                            "description": "Whether the variable is masked.",
                        },
                        "environment_scope": {  # Premium+/Silver+
                            "type": "string",
                            "description": "The environment_scope of the variable.",
                        },
                    },
                    "required": ["key", "value"],
                    "additionalProperties": False,
                },
                "uniqueItems": True,
                "_example": ("\n"
                             "    - key: DAST_DISABLED\n"
                             "      value: '1'\n"
                             "      masked: false\n"
                             "      protected: false\n"
                             "      variable_type: env_var\n"),
            },
            "unknown_variables": {  # GitLabracadabra
                "type": "string",
                "description": "What to do with unknown variables (`warn` by default).",
                "enum": ["warn", "delete", "remove", "ignore", "skip"],
            },
            # From https://docs.gitlab.com/ee/api/labels.html#create-a-new-label
            "labels": {
                "type": "array",
                "description": "The list of project's labels",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the label.",
                        },
                        "color": {
                            "type": "string",
                            "description": "The color of the label.",
                        },
                        "description": {
                            "type": "string",
                            "description": "The description of the label.",
                        },
                        "priority": {
                            "type": "integer",
                            "description": "The priority of the label.",
                        },
                    },
                    "required": ["name"],  # color not required to allow priority override
                    "additionalProperties": False,
                },
                "uniqueItems": True,
                "_example": ("\n"
                             "    - name: critical\n"
                             "      priority: 0\n"
                             "    - name: bug\n"
                             "      priority: 1\n"
                             "    - name: confirmed\n"
                             "      priority: 2\n"),
            },
            "unknown_labels": {  # GitLabracadabra
                "type": "string",
                "description": "What to do with unknown labels (`warn` by default).",
                "enum": ["warn", "delete", "remove", "ignore", "skip"],
            },
            # From https://docs.gitlab.com/ee/api/milestones.html#edit-milestone
            "milestones": {
                "type": "array",
                "description": "The list of project's milestones",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title of a milestone",
                        },
                        "description": {
                            "type": "string",
                            "description": "The description of a milestone",
                        },
                        "due_date": {
                            "type": "string",
                            "description": "The due date of the milestone",
                            "pattern": "^(\\d{4}-\\d{2}-\\d{2})?$",
                        },
                        "start_date": {
                            "type": "string",
                            "description": "The start date of the milestone",
                            "pattern": "^(\\d{4}-\\d{2}-\\d{2})?$",
                        },
                        "state": {
                            "type": "string",
                            "description": "The state event of the milestone",
                            "enum": ["closed", "active"],
                        },
                    },
                    "required": ["title"],
                    "additionalProperties": False,
                },
                "uniqueItems": True,
                "_example": ("\n"
                             "    - title: '1.0'\n"
                             "      description: Version 1.0\n"
                             "      due_date: '2021-01-23' # Quotes are mandatory\n"
                             "      start_date: '2020-01-23' # Quotes are mandatory\n"
                             "      state: active # or closed\n"),
            },
            "unknown_milestones": {  # GitLabracadabra
                "type": "string",
                "description": "What to do with unknown milestones (`warn` by default).",
                "enum": ["warn", "delete", "remove", "ignore", "skip"],
            },
            # From https://docs.gitlab.com/ee/api/projects.html#edit-project
            "issues_enabled": {
                "type": "boolean",
                "description": "Enable issues for this project",
            },
            "merge_requests_enabled": {
                "type": "boolean",
                "description": "Enable merge requests for this project",
            },
            "jobs_enabled": {
                "type": "boolean",
                "description": "Enable jobs for this project",
            },
            "wiki_enabled": {
                "type": "boolean",
                "description": "Enable wiki for this project",
            },
            "snippets_enabled": {
                "type": "boolean",
                "description": "Enable snippets for this project",
            },
            # Below are undocumented settings
            "repository_storage": {
                "type": "string",
                "description": "Which storage shard the repository is on. Available only to admins",
            },
            "external_authorization_classification_label": {
                "type": "string",
                "description": "The classification label for the project",
            },
        },
        "additionalProperties": False,
    }

    IGNORED_PARAMS = ['initialize_with_readme', 'unknown_groups', 'unknown_labels', 'unknown_members',
                      'unknown_milestones', 'unknown_protected_branches', 'unknown_protected_tags', 'unknown_variables',
                      'unknown_webhooks']

    CREATE_KEY = 'name'
    CREATE_PARAMS = ['initialize_with_readme']

    """"web_url()

    Returns the project's web URL.
    (Allows to mock the web URL).
    """
    def web_url(self):
        return self._obj.web_url

    def _get_current_branches(self):
        if not hasattr(self, '_current_branches'):
            try:
                self._current_branches = [branch.name for branch in self._obj.branches.list(all=True)]
            except GitlabListError as err:
                if err.response_code != 403:  # repository_enabled=false?
                    pass
                self._current_branches = None
        return self._current_branches

    """"_process_archived()

    Process the archived param.
    """
    def _process_archived(self, param_name, param_value, dry_run=False, skip_save=False):
        assert param_name == 'archived'  # noqa: S101
        assert not skip_save  # noqa: S101

        current_value = getattr(self._obj, param_name)
        if current_value != param_value:
            if dry_run:
                logger.info('[%s] NOT Changing param %s: %s -> %s (dry-run)',
                            self._name, param_name, current_value, param_value)
                setattr(self._obj, param_name, param_value)
            else:
                logger.info('[%s] Changing param %s: %s -> %s',
                            self._name, param_name, current_value, param_value)
                if param_value:
                    self._obj.archive()
                else:
                    self._obj.unarchive()

    """"_process_branches()

    Process the branches param.
    """
    def _process_branches(self, param_name, param_value, dry_run=False, skip_save=False):
        assert param_name == 'branches'  # noqa: S101
        assert not skip_save  # noqa: S101
        if 'default_branch' in self._content and self._content['default_branch'] in self._get_current_branches():
            # Create from target default branch if it exists
            ref = self._content['default_branch']
        elif self._obj.default_branch in self._get_current_branches():
            # Create from current default branch otherwise
            ref = self._obj.default_branch
        else:
            ref = None
        for branch_name in param_value:
            if branch_name not in self._get_current_branches():
                if ref is None:
                    logger.info('[%s] NOT Creating branch: %s (no reference)',
                                self._name, branch_name)
                elif dry_run:
                    logger.info('[%s] NOT Creating branch: %s (dry-run)',
                                self._name, branch_name)
                    self._current_branches.append(branch_name)
                else:
                    logger.info('[%s] Creating branch: %s',
                                self._name, branch_name)
                    self._obj.branches.create({
                        'branch': branch_name,
                        'ref': ref
                    })
                    self._current_branches.append(branch_name)
            if branch_name in self._get_current_branches():
                # Next branch will be created from this ref
                ref = branch_name

    """"_process_groups()

    Process the groups param.
    """
    def _process_groups(self, param_name, param_value, dry_run=False, skip_save=False):
        assert param_name == 'groups'  # noqa: S101
        assert not skip_save  # noqa: S101
        param_value = deepcopy(param_value)
        unknown_groups = self._content.get('unknown_groups', 'warn')
        # We first check for already shared groups
        for group in self._obj.shared_with_groups:
            if 'group_full_path' not in group:
                # Gitlab < 11.8
                # https://gitlab.com/gitlab-org/gitlab-ce/merge_requests/24052
                group['group_full_path'] = GitLabracadabraGroup.get_full_path_from_id(group['group_id'])
            GitLabracadabraGroup.map_group(group['group_id'], group['group_full_path'])
            if group['group_full_path'] in param_value.keys():
                target_access_level = access_level(param_value[group['group_full_path']])
                if group['group_access_level'] != target_access_level:
                    if dry_run:
                        logger.info('[%s] NOT Changing group %s access level: %s -> %s (dry-run)',
                                     self._name, group['group_full_path'],
                                     group['group_access_level'], target_access_level)
                    else:
                        logger.info('[%s] Changing group %s access level: %s -> %s',
                                     self._name, group['group_full_path'],
                                     group['group_access_level'], target_access_level)
                        self._obj.unshare(group['group_id'])
                        self._obj.share(group['group_id'], target_access_level)
                param_value.pop(group['group_full_path'])
            else:
                if unknown_groups in ['delete', 'remove']:
                    if dry_run:
                        logger.info('[%s] NOT Unsharing from unknown group: %s (dry-run)',
                                    self._name, group['group_full_path'])
                    else:
                        logger.info('[%s] Unsharing from unknown group: %s',
                                    self._name, group['group_full_path'])
                        self._obj.unshare(group['group_id'])
                elif unknown_groups not in ['ignore', 'skip']:
                    logger.warning('[%s] NOT Unsharing from unknown group: %s (unknown_groups=%s)',
                                   self._name, group['group_full_path'], unknown_groups)
        # Remaining groups
        for group_full_path, target_group_access in sorted(param_value.items()):
            group_id = GitLabracadabraGroup.get_id_from_full_path(group_full_path)
            if group_id is None:
                logger.warning('[%s] Group not found %s',
                                self._name, group_full_path)
                continue
            target_access_level = access_level(target_group_access)
            if dry_run:
                logger.info('[%s] NOT Sharing group %s: %s -> %s (dry-run)',
                            self._name, group_full_path,
                            0, target_access_level)
            else:
                logger.info('[%s] Sharing group %s: %s -> %s',
                            self._name, group_full_path,
                            0, target_access_level)
                self._obj.share(group_id, target_access_level)

    """"_process_protected_branches()

    Process the protected_branches param.
    """
    def _process_protected_branches(self, param_name, param_value, dry_run=False, skip_save=False):
        assert param_name == 'protected_branches'  # noqa: S101
        assert not skip_save  # noqa: S101
        unknown_protected_branches = self._content.get('unknown_protected_branches', 'warn')
        current_protected_branches = dict([[protected_branch.name, protected_branch]
                                          for protected_branch in self._obj.protectedbranches.list(all=True)])
        # We first check for already protected branches
        for protected_name, target_config in sorted(param_value.items()):
            target_config_int = {}
            for k, v in target_config.items():
                if k.endswith('_access_level'):
                    target_config_int[k] = access_level(v)
                else:
                    target_config_int[k] = v
            target_config_int['name'] = protected_name
            if protected_name in current_protected_branches:
                current_protected_branch = current_protected_branches[protected_name]
                current_config = {
                    'name': protected_name,
                    'push_access_level': current_protected_branch.push_access_levels[0]['access_level'],
                    'merge_access_level': current_protected_branch.merge_access_levels[0]['access_level'],
                }
            else:
                current_config = {}
            if current_config != target_config_int:
                if dry_run:
                    logger.info('[%s] NOT Changing protected branch %s access level: %s -> %s (dry-run)',
                                 self._name, protected_name, current_config, target_config_int)
                else:
                    logger.info('[%s] Changing protected branch %s access level: %s -> %s',
                                 self._name, protected_name, current_config, target_config_int)
                    if 'name' in current_config:
                        self._obj.protectedbranches.delete(protected_name)
                    try:
                        self._obj.protectedbranches.create(target_config_int)
                    except GitlabCreateError as err:
                        if err.response_code != 409:
                            pass
                        logger.warning('[%s] Unable to create protected branch %s: %s',
                                        self._name, protected_name, err.error_message)
        # Remaining protected branches
        if unknown_protected_branches not in ['ignore', 'skip']:
            for protected_name in current_protected_branches:
                if protected_name not in param_value:
                    if unknown_protected_branches in ['delete', 'remove']:
                        if dry_run:
                            logger.info('[%s] NOT Deleting unknown protected branch: %s (dry-run)',
                                        self._name, protected_name)
                        else:
                            logger.info('[%s] Deleting unknown protected branch: %s',
                                        self._name, protected_name)
                            self._obj.protectedbranches.delete(protected_name)
                    else:
                        logger.warning('[%s] NOT Deleting unknown protected branch: %s'
                                       ' (unknown_protected_branches=%s)',
                                       self._name, protected_name, unknown_protected_branches)

    """"_process_protected_tags()

    Process the protected_tags param.
    """
    def _process_protected_tags(self, param_name, param_value, dry_run=False, skip_save=False):
        assert param_name == 'protected_tags'  # noqa: S101
        assert not skip_save  # noqa: S101
        unknown_protected_tags = self._content.get('unknown_protected_tags', 'warn')
        try:
            current_protected_tags = dict([[protected_tag.name, protected_tag]
                                           for protected_tag in self._obj.protectedtags.list(all=True)])
        except AttributeError:
            logger.error('[%s] Unable to manage protected tags: %s',
                         self._name, 'protected tags requires python-gitlab >= 1.7.0')
            return
        # We first check for already protected tags
        for protected_name, target_config in sorted(param_value.items()):
            target_config = {
                'name': protected_name,
                'create_access_level': access_level(target_config),
            }
            if protected_name in current_protected_tags:
                current_protected_tag = current_protected_tags[protected_name]
                current_config = {
                    'name': protected_name,
                    'create_access_level': current_protected_tag.create_access_levels[0]['access_level'],
                }
            else:
                current_config = {}
            if current_config != target_config:
                if dry_run:
                    logger.info('[%s] NOT Changing protected tag %s access level: %s -> %s (dry-run)',
                                self._name, protected_name, current_config, target_config)
                else:
                    logger.info('[%s] Changing protected tag %s access level: %s -> %s',
                                self._name, protected_name, current_config, target_config)
                    if 'name' in current_config:
                        self._obj.protectedtags.delete(protected_name)
                    self._obj.protectedtags.create(target_config)
        # Remaining protected tags
        if unknown_protected_tags not in ['ignore', 'skip']:
            current_protected_tags = sorted([protected_tag.name
                                             for protected_tag in self._obj.protectedtags.list(all=True)])
            for protected_name in current_protected_tags:
                if protected_name not in param_value:
                    if unknown_protected_tags in ['delete', 'remove']:
                        if dry_run:
                            logger.info('[%s] NOT Deleting unknown protected tag: %s (dry-run)',
                                        self._name, protected_name)
                        else:
                            logger.info('[%s] Deleting unknown protected tag: %s',
                                        self._name, protected_name)
                            self._obj.protectedtags.delete(protected_name)
                    else:
                        logger.warning('[%s] NOT Deleting unknown protected tag: %s (unknown_protected_tags=%s)',
                                       self._name, protected_name, unknown_protected_tags)
