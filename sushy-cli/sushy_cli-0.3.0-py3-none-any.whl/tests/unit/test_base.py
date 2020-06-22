# -*- coding: utf-8 -*-

# Copyright 2020 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from unittest import mock

from sushycli.base import BaseParserMixIn
from sushycli.tests.unit import base


class BaseParserMixInTestCase(base.TestCase):

    def setUp(self):
        super(BaseParserMixInTestCase, self).setUp()

        self.obj = BaseParserMixIn()

    def test__to_json_from_none(self):
        output = self.obj._to_json(None)

        expected = '{}'

        self.assertEqual(expected, output)

    def test__to_json_from_dict(self):
        output = self.obj._to_json({'test': 1})

        expected = '{\n  "test": 1\n}'

        self.assertEqual(expected, output)

    def test__to_json_from_json(self):
        output = self.obj._to_json('{"test": 1}')

        expected = '{\n  "test": 1\n}'

        self.assertEqual(expected, output)

    def test__to_json_malformed(self):
        self.obj.app = mock.MagicMock()

        output = self.obj._to_json('not json')

        expected = '{}'

        self.assertEqual(expected, output)
        self.assertEqual(1, self.obj.app.LOG.error.call_count)
