# from __future__ import absolute_import
#
# from unittest import mock
# import unittest
# import os
# import shutil
#
# import sciunit2.cli
# import sciunit2.workspace
#
# # these are important packages, used through arguments
# from humanfriendly.testing import touch, CaptureOutput
# from humanfriendly.testing import make_dirs as mkdir
#
#
# class LocalCase(unittest.TestCase):
#     project_dir = 'sciunit-test'
#
#     def setUp(self):
#         self.workspace_patch = mock.patch(
#             'sciunit2.workspace.location_for',
#             lambda s: os.path.join(self.project_dir, s))
#         self.workspace_patch.start()
#
#     def tearDown(self):
#         self.workspace_patch.stop()
#         shutil.rmtree(self.project_dir, True)
#
#
# def main(*args):
#     with mock.patch('sys.argv', ['x'] + list(args)):
#         sciunit2.cli.main()
#
#
# class Sciunit:
#     def exec(*args):
#         # interactive exec is not supported with the API
#         args = ('exec',) + args
#         main(*args)
#
#     def commit(*args):
#         args = ('commit',) + args
#         main(*args)
#
#     def copy(*args):
#         args = ('copy',) + args
#         main(*args)
#
#     def create(*args):
#         args = ('create',) + args
#         main(*args)
#
#     def diff(*args):
#         args = ('diff',) + args
#         main(*args)
#
#     def given(*args):
#         args = ('given',) + args
#         main(*args)
#
#     def list(*args):
#         args = ('list',) + args
#         main(*args)
#
#     def open(*args):
#         args = ('open',) + args
#         main(*args)
#
#     def push(*args):
#         args = ('push',) + args
#         main(*args)
#
#     def repeat(*args):
#         args = ('repeat',) + args
#         main(*args)
#
#     def rm(*args):
#         args = ('rm',) + args
#         main(*args)
#
#     def show(*args):
#         args = ('show',) + args
#         main(*args)
#
#     def sort(*args):
#         args = ('sort',) + args
#         main(*args)
