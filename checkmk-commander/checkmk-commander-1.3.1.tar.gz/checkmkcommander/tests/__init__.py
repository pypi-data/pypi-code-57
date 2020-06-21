#!/usr/bin/env python3

# https://docs.python.org/3/library/unittest.html
# https://python-packaging.readthedocs.io/en/latest/testing.html

# Run this from project main directory:
# python3 -m unittest discover -v

import unittest
import checkmkcommander
import datetime
import tempfile, shutil

class TestChkMethods(unittest.TestCase):

    def test_fetch_time(self):
        ''' Test we get a valid time string '{0:%H:%M:%S}'''

        my_time = checkmkcommander.Chk.fetch_time()
        now = datetime.datetime.now()
        hour, minute, second = my_time.split(':')

        print(f'Got time {my_time}')

        self.assertEqual(int(hour), now.hour, msg='Time error')
        self.assertEqual(int(minute), now.minute, msg='Time error')
        self.assertIsInstance(int(second), int, msg='Time error')
        self.assertGreater(len(my_time), 7, msg='Time string too short.')
        self.assertLess(len(my_time), 9, msg='Time string too short.')

    def test_parse_time(self):
        ''' Input can be  2h, 100, 4h, 5m, 333s.
        Will return a positive number of seconds or -1 for no time.'''

        for timestring in ['1h', '1h ', '3600', '60m', '3600s']:
            self.assertEqual(checkmkcommander.Chk.parse_time(timestring), 3600, msg=f'<{timestring}> not parsed correctly to one hour.')

        for timestring in ['h1', 'h', '-1', '-22', ' ']:
            self.assertEqual(checkmkcommander.Chk.parse_time(timestring), -1, msg=f'Invalid {timestring} not parsed correctly to -1.')

    def test_scrub_secret(self):
        ''' Check urls for the automation secret and scrub it away '''

        secret = 'donotexpose'
        urls = [
            f"https://example.no/front/check_mk/view.py?_transid=-1&_do_actions=yes&_do_confirm=yes&output_format=json&_username=user-api&_secret={secret}&is_service_acknowledged=0&view_name=svcproblems",
            f"https://example.no/front/check_mk/view.py?_transid=-1&_do_actions=yes&_do_confirm=yes&output_format=json&_username=user-api&_secret={secret}"
        ]

        for u in urls:
            print(f"\nTest scrubbing url {u}")
            scrubbed = checkmkcommander.Chk.scrub_secret(u)
            print(f"Result: {scrubbed}")
            self.assertNotIn(secret, scrubbed, msg='Found secret exposed in scrubbed url')

    # https://gist.github.com/odyniec/d4ea0959d4e0ba17a980
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_validate_config(self):
        ''' Read a config '''
        
        self.project_name = "Test"
        self.config_path = self.test_dir + 'config.ini'
        self.api_base_url = ''
        self.checkmkhost = ''
        self.checkmkusername = ''
        self.checkmksecret = ''
        self.delay = 0
        self.url_with_hostname = 'http://wiki.example.com/?q=HOSTNAME'
        self.terminal_command = 'x-terminal-emulator -e ssh HOSTNAME'

        with open(self.config_path, mode='w') as f:
            f.write('''
[main]
host = http://omd.lxd/test/
username = automation
secret = 123456
delay = 5
 ''')

        checkmkcommander.Chk.validate_config(self)
        self.assertEqual(self.checkmkhost, 'http://omd.lxd/test/', msg='Error reading host from config')

if __name__ == '__main__':
    unittest.main()
