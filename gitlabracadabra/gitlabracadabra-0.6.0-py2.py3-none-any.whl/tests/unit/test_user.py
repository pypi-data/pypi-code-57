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
from gitlabracadabra.objects.user import GitLabracadabraUser
from gitlabracadabra.tests.utils import my_vcr


class TestUser(TestCase):
    def setUp(self):
        gitlabracadabra.manager._gitlab = Gitlab(  # noqa: S106
            'http://localhost',
            private_token='DKkdC5JmKWWZgXZGzg83',
        )

    def tearDown(self):
        gitlabracadabra.manager._gitlab = None

    @my_vcr.use_cassette
    def test_no_create(self, cass):
        obj = GitLabracadabraUser('memory', 'no_create_user', {})
        obj.process()
        self.assertEqual(cass.all_played, True)

    @my_vcr.use_cassette
    def test_create(self, cass):
        obj = GitLabracadabraUser('memory', 'create_user', {
            'create_object': True,
            'email': 'create_user@example.org',
            'name': 'Create User',
            'password': 'P@ssw0rdNot24get',
        })
        obj.process()
        self.assertEqual(cass.all_played, True)

    @my_vcr.use_cassette
    def test_delete(self, cass):
        obj = GitLabracadabraUser('memory', 'delete_this_user', {'delete_object': True})
        obj.process()
        self.assertEqual(cass.all_played, True)

    @my_vcr.use_cassette
    def test_exists(self, cass):
        obj = GitLabracadabraUser('memory', 'user_exists', {})
        obj.process()
        self.assertEqual(cass.all_played, True)

    @my_vcr.use_cassette
    def notest_simple_parameters(self, cass):
        obj = GitLabracadabraUser('memory', 'test/user_simple_parameters', {
            'name': 'user-with-simple-parameters',
            'description': 'user with simple parameters',
            'visibility': 'public',
            'lfs_enabled': False,
            'request_access_enabled': True,
            # 'shared_runners_minutes_limit': 42,  # EE, admin-only
        })
        obj.process()
        self.assertEqual(cass.all_played, True)

    @my_vcr.use_cassette
    def test_get_id_from_username(self, cass):
        # Clean up
        GitLabracadabraUser._USERS_USERNAME2ID = {}
        GitLabracadabraUser._USERS_ID2USERNAME = {}
        ret = GitLabracadabraUser.get_id_from_username('user_mapping')
        self.assertEqual(ret, 9)
        self.assertEqual(cass.all_played, True)

    @my_vcr.use_cassette
    def test_get_username_from_id(self, cass):
        # Clean up
        GitLabracadabraUser._USERS_USERNAME2ID = {}
        GitLabracadabraUser._USERS_ID2USERNAME = {}
        ret = GitLabracadabraUser.get_username_from_id(9)
        self.assertEqual(ret, 'user_mapping')
        self.assertEqual(cass.all_played, True)
