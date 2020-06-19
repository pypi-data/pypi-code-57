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

from unittest import TestCase

from gitlab import Gitlab

import gitlabracadabra.manager
from gitlabracadabra.objects.application_settings import GitLabracadabraApplicationSettings
from gitlabracadabra.tests.utils import my_vcr


class TestApplicationSettings(TestCase):
    def setUp(self):
        gitlabracadabra.manager._gitlab = Gitlab(  # noqa: S106
            'http://localhost',
            private_token='DKkdC5JmKWWZgXZGzg83',
        )

    def tearDown(self):
        gitlabracadabra.manager._gitlab = None

    @my_vcr.use_cassette
    def test_settings(self, cass):
        obj = GitLabracadabraApplicationSettings('memory', 'application_settings', {
            'admin_notification_email': 'admin@example.org',
            'after_sign_out_path': 'https://logout.example.org/',
            'after_sign_up_text': '/sign/up',
            'akismet_api_key': 'abcd',
            'akismet_enabled': True,
            'allow_local_requests_from_hooks_and_services': True,
            'archive_builds_in_human_readable': '1 month',
            'authorized_keys_enabled': False,
            'auto_devops_domain': 'app.example.org',
            'auto_devops_enabled': False,
            'commit_email_hostname': 'users.noreply.gitlab.example.org',
            'container_registry_token_expire_delay': 10,
            'default_artifacts_expire_in': '15 days',
            'default_branch_protection': 1,
            # 'default_ci_config_path': 'global/path', # TODO
            'default_group_visibility': 'internal',
            'default_project_creation': 1,
            'default_projects_limit': 42,
            'default_project_visibility': 'internal',
            'default_snippet_visibility': 'internal',
            'diff_max_patch_bytes': 102420,
            'disabled_oauth_sign_in_sources': ['github'],
            'dns_rebinding_protection_enabled': False,
            'domain_blacklist_enabled': True,
            'domain_blacklist': ['foo.example.com'],
            'domain_whitelist': ['bar.example.com'],
            'dsa_key_restriction': 1024,
            'ecdsa_key_restriction': 384,
            'ed25519_key_restriction': 256,
            'email_author_in_body': True,
            'enabled_git_access_protocol': 'http',
            'enforce_terms': True,
            # 'external_auth_client_cert': 'FOO',  # FIXME 'is not a valid X509 certificate.'
            # 'external_auth_client_key': 'BAR', # 'could not read private key, is the passphrase correct?'
            'external_auth_client_key_pass': 'BAZ',
            'external_authorization_service_default_label': 'toto',
            # 'external_authorization_service_enabled': True,  # FIXME Or the API will fail
            'external_authorization_service_timeout': 0.42,
            'external_authorization_service_url': 'https://authz.example.org/',
            'first_day_of_week': 'sunday',
            'gitaly_timeout_default': 110,
            'gitaly_timeout_fast': 20,
            'gitaly_timeout_medium': 60,
            'grafana_enabled': True,
            'grafana_url': '/-/grafana2',
            'gravatar_enabled': False,
            'hashed_storage_enabled': True,
            'help_page_hide_commercial_content': True,
            'help_page_support_url': 'https://help.example.org/',
            'help_page_text': 'Help!',
            'hide_third_party_offers': True,
            'home_page_url': 'https://home.example.org/',
            'housekeeping_bitmaps_enabled': False,
            'housekeeping_enabled': False,
            'housekeeping_full_repack_period': 100,
            'housekeeping_gc_period': 400,
            'housekeeping_incremental_repack_period': 20,
            'html_emails_enabled': False,
            'import_sources': [
                'github',
                'bitbucket',
                # 'bitbucket_server',
                'gitlab',
                'google_code',
                'fogbugz',
                'git',
                'gitlab_project',
                # 'gitea',
                'manifest',
                # 'phabricator',
            ],
            'instance_statistics_visibility_private': True,
            'local_markdown_version': 1,
            'max_artifacts_size': 200,
            'max_attachment_size': 20,
            'max_pages_size': 200,
            'metrics_enabled': True,
            'metrics_host': 'influxdb.example.org',
            'metrics_method_call_threshold': 20,
            'metrics_packet_size': 2,
            'metrics_pool_size': 32,
            'metrics_port': 18089,
            'metrics_sample_interval': 30,
            'metrics_timeout': 20,
            'mirror_available': False,
            'pages_domain_verification_enabled': False,
            'password_authentication_enabled_for_git': False,
            'password_authentication_enabled_for_web': False,
            'performance_bar_allowed_group_path': 'test',
            'plantuml_enabled': True,
            'plantuml_url': 'https://plantuml.example.org/',
            'polling_interval_multiplier': 2.0,
            'project_export_enabled': False,
            'prometheus_metrics_enabled': False,
            'protected_ci_variables': True,
            'recaptcha_enabled': True,
            'recaptcha_private_key': 'FOO',
            'recaptcha_site_key': 'BAR',
            'receive_max_input_size': 42,
            'repository_checks_enabled': False,
            # 'repository_storages': ['nfs'],  # FIXME
            'require_two_factor_authentication': True,
            'restricted_visibility_levels': ['public'],
            'rsa_key_restriction': 1024,
            'send_user_confirmation_email': True,
            'session_expire_delay': 20160,
            'shared_runners_enabled': False,
            'shared_runners_text': 'Shared runner text',
            'sign_in_text': 'Sign in text',
            'signup_enabled': False,
            'terminal_max_session_time': 3600,
            'terms': 'Terms',
            'throttle_authenticated_api_enabled': True,
            'throttle_authenticated_api_period_in_seconds': 7200,
            'throttle_authenticated_api_requests_per_period': 14400,
            'throttle_authenticated_web_enabled': True,
            'throttle_authenticated_web_period_in_seconds': 7200,
            'throttle_authenticated_web_requests_per_period': 14400,
            'throttle_unauthenticated_enabled': True,
            'throttle_unauthenticated_period_in_seconds': 7200,
            'throttle_unauthenticated_requests_per_period': 7200,
            'time_tracking_limit_to_hours': True,
            'two_factor_grace_period': 96,
            'unique_ips_limit_enabled': True,
            'unique_ips_limit_per_user': 20,
            'unique_ips_limit_time_window': 7200,
            'usage_ping_enabled': True,
            'user_default_external': True,
            'user_default_internal_regex': '.*@.*\\.example.org',
            'user_oauth_applications': False,
            'user_show_add_ssh_key_message': False,
            'version_check_enabled': True,
            'web_ide_clientside_preview_enabled': True,
        })
        obj.process()
        self.assertEqual(cass.all_played, True)
