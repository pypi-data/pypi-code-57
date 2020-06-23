#!/usr/bin/env python3
# This file is part of the SecureFlag Platform.
# Copyright (c) 2020 SecureFlag Limited.

# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.

# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import unittest
from sfsdk import cli, containers, log
from sfsdk import imgsettings, techsettings, authsettings, exrsettings
import json
import requests
import tempfile
import multiprocessing
import time
import os

base_dir = tempfile.mkdtemp(prefix='sfsdk-tests-') 
settings_path = os.path.join(
        base_dir,
        'login.yml' 
    )

# Load authsettings from the real folder
auth_base_dir = os.path.expanduser('~/sf')
authsettings.load(auth_base_dir)

#log.set_verbose()

developer_source = 'developer-test-account'

class TestEdit(unittest.TestCase):

    def setUp(self):
        techsettings.load(base_dir)
        exrsettings.load(base_dir)

        self.p = multiprocessing.Process(target=cli.exercise_edit, args=(developer_source,))
        self.p.start()

        # Give some time for flask to spin up
        time.sleep(2)

        res = requests.post(
                'http://localhost:5000/handler', 
                json={"action":"getUserCToken"},
        ).json()
        self.ctoken = res.get('ctoken')
        self.assertTrue(self.ctoken)

    def tearDown(self):
        self.p.terminate()
        self.p.join()


    @unittest.skipUnless(authsettings.settings.get('sources', {}).get(developer_source),
                                 "No developer creds in login.yml")
    def test_wrong_ctoken(self):

        res = requests.post(
                'http://localhost:5000/handler', 
                json={"action":"getAllKbs", "ctoken": '1'*19},
        ).json()
        self.assertEqual(res.get('result'), 'error')

    @unittest.skipUnless(authsettings.settings.get('sources', {}).get(developer_source),
                                 "No developer creds in login.yml")
    def test_exercise_api(self):

        # Check exercise list is empty
        res_exercises = requests.post(
                'http://localhost:5000/handler', 
                json={"action":"getExercises", "ctoken": self.ctoken },
        ).json()
        self.assertEqual(len(res_exercises), 0)

        # Push exercise sample
        test_folder = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(test_folder, 'exercise-sample.json'), "r") as f:
            json_data = json.load(f)

        json_data['action'] = 'addExercise'
        json_data['ctoken'] = self.ctoken

        res_add_exercise = requests.post(
                'http://localhost:5000/handler', 
                json=json_data,
        ).json()
        self.assertEqual(res_add_exercise.get('result'), 'success')

        # Check the list of exercises has now 1 length
        res_exercises = requests.post(
                'http://localhost:5000/handler', 
                json={"action":"getExercises", "ctoken": self.ctoken },
        ).json()
        self.assertEqual(len(res_exercises), 1)

        # Check exercise detail
        res_exercise_details = requests.post(
                'http://localhost:5000/handler', 
                json={
                    "action":"getExerciseDetails", 
                    "ctoken": self.ctoken, 
                    "uuid": res_add_exercise.get("uuid") 
                },
        ).json()
        self.assertEqual(res_exercise_details['title'], json_data['title'])

        # Update exercise detail
        json_data['action'] = 'updateExercise'
        json_data['title'] = 'NEW TITLE'
        json_data['uuid'] = res_add_exercise.get("uuid")

        res_add_exercise = requests.post(
                'http://localhost:5000/handler', 
                json=json_data,
        ).json()
        self.assertEqual(res_add_exercise.get('result'), 'success')

        # Check the list of exercises is still 1 length
        res_exercises = requests.post(
                'http://localhost:5000/handler', 
                json={"action":"getExercises", "ctoken": self.ctoken },
        ).json()
        self.assertEqual(len(res_exercises), 1)

        # Check exercise detail
        res_exercise_details = requests.post(
                'http://localhost:5000/handler', 
                json={
                    "action":"getExerciseDetails", 
                    "ctoken": self.ctoken, 
                    "uuid": res_add_exercise.get("uuid") 
                },
        ).json()
        self.assertEqual(res_exercise_details['title'], json_data['title'])

    @unittest.skipUnless(authsettings.settings.get('sources', {}).get(developer_source),
                                 "No developer creds in login.yml")
    def test_kb_api(self):

        res_kbs = requests.post(
                'http://localhost:5000/handler', 
                json={"action":"getAllKbs", "ctoken": self.ctoken },
        ).json()
        self.assertTrue(res_kbs)
        self.assertTrue(res_kbs[0].get('uuid'))

        res_kb = requests.post(
                'http://localhost:5000/handler', 
                json={"action":"getKBItem", "ctoken": self.ctoken, "uuid": res_kbs[0].get('uuid') },
        ).json()
        self.assertTrue(res_kb)
        self.assertTrue(res_kb.get('uuid'))

    @unittest.skipUnless(authsettings.settings.get('sources', {}).get(developer_source),
                                 "No developer creds in login.yml")
    def test_stack_api(self):
        res_stacks = requests.post(
                'http://localhost:5000/handler', 
                json={"action":"getAllStacks", "ctoken": self.ctoken },
        ).json()
        self.assertTrue(res_stacks)
        self.assertTrue(res_stacks[0].get('uuid'))

        res_stack = requests.post(
                'http://localhost:5000/handler', 
                json={"action":"getStackItem", "ctoken": self.ctoken, "uuid": res_stacks[0].get('uuid') },
        ).json()
        self.assertTrue(res_stack)
        self.assertTrue(res_stack.get('uuid'))

if __name__ == '__main__':
    unittest.main()
