from __future__ import division, print_function
import os
import sys
from collections import OrderedDict
from pkg_resources import resource_filename
from textwrap import dedent
from unittest import TestCase

from codetree.config import Config, ConfigResults, Directive, InvalidDirective
from codetree.handlers.basic import HandlerResult
from codetree import six

if six.PY2:
    import mock
else:
    from unittest import mock


class TestConfig(TestCase):

    def _concurrent_test(self, config_file, expected_tree_set):
        """
        Tests on a config file to be processed concurrently.
        The testing we do for each config file is identical and abstracted in
        this method.
        We ensure that directives are produced in correct topological order,
        that all expected directives are present, and that their dependencies
        are what we expect them to be.

        :param config_file:
            The configuration file to process to ensure it results in what we
            expect
        :param expected_tree_set:
            A set with the locations we expect to get as a result. It has to
            be a set because strict ordering is not guaranteed, proper
            hierarchical order is determined with expected_lengths.
            Since we care about dependencies, set elements should be tuples
            of (location, dependency) where dependency can be None.
        """
        config = Config(config_file)

        # Test for topological ordering
        nodes = {}
        for d in config.concurrent_directives():
            # If a node has a parent, ensure we have seen the parent before
            if d[1]:
                self.assertIn(d[1], nodes)
            # Ensure we don't see a node twice
            self.assertNotIn(d[0], nodes)
            # Store the node, keyed by its location (first element of tuple)
            nodes[d[0]] = d
        # Ensure we have the items we expect in the list of seen nodes
        # concurrent_directives returns directives so we have to map them to
        # locations first. This is to make it easier to build the expected data
        # lists
        nodes_with_locations = [(directive.location,
                                 dep.location if dep else None)
                                for (directive, dep) in nodes.values()]
        self.assertEqual(set(nodes_with_locations), expected_tree_set)

    def _concurrent_config_build_test(self, config_file, workers=None):
        """
        Ensure the config is built (i.e processed) correctly using
        concurrency, verifying correct calling of futures
        """

        # Mock the executor to check if it gets submitted the correct jobs
        # and is shut down properly
        mock_executor = mock.Mock()
        # Next, mock the Directive.run method so it doesn't actually process
        # anything, just returns success.
        with mock.patch('concurrent.futures.ThreadPoolExecutor', autospec=True,
                        return_value=mock_executor) as mock_tpe,\
            mock.patch('codetree.config.Directive.run',
                       return_value=True):
            config = Config(config_file)
            config.build(dry_run=False, workers=workers)
            # Ensure the executor was created and shut down properly
            if workers:
                mock_tpe.assert_called_with(max_workers=workers)
            else:
                mock_tpe.assert_called_with(max_workers=len(config.directive_map))
            mock_executor.shutdown.assert_called_once_with(wait=True)

            # Note we rebuild the tree here using the same algorithm as the
            # config object, because the config's tree was eaten
            # while iterating through it
            tree = {'': []}
            for path_as_array in sorted([location.split("/") for location in
                                         config.directive_map.keys()]):
                parent = "/".join(path_as_array[:-1])
                child = "/".join(path_as_array)
                tree[parent].append(child)
                # Add my list of children
                tree[child] = []
            # Ensure the expected directive methods and their dependencies
            # were submitted to the executor. We check only for presence, not
            # order, as that's done elsewhere.
            for parent, directives in tree.items():
                if parent:
                    dep_callable = config.futures[parent].result
                else:
                    dep_callable = mock.ANY  # stand-in for the lambdas
                for directive in directives:
                    mock_executor.submit.assert_any_call(
                        config.directive_map[directive].run_with_dependency,
                        dep_callable)

    def test_missing_parent_directive(self):
        """ Test a config with a missing parent directory
        """
        test_filename = resource_filename("tests", "/test_data/missing_parent")
        self.assertRaises(InvalidDirective, Config, test_filename)

        os.mkdir('dir')
        with mock.patch('logging.warn') as mock_log:
            conf = Config(test_filename)
            mock_log.assert_called_once_with("Parent directory dir is not specified "
                                             "in the configuration, using existing directory")
            assert 'dir/subdir' in conf.tree['']

        os.rmdir('dir')

    def test_directive_ordering_simple(self):
        """
        Ensure a simple directive list is read in the expected
        order. This is a bit naive since all 3 directives have the same
        length so we're not really testing ordering at all.
        """
        test_filename = resource_filename("tests", "/test_data/simple_1")
        self._concurrent_test(test_filename,
                              set([('bar', None),
                                   ('baz', None),
                                   ('foo', None)]))

    def test_directive_ordering_tricky(self):
        """
        Ensure a slightly trickier directive list is read in the expected
        order. The expected data is ordered by hand and by a human, actual
        order may be different but as long as the constraints we check are
        honored, it should be OK.
        """
        expected_concurrent_contents = [('foo', None),
                                        ('faodir', None),
                                        ('foofum', None),
                                        ('foofighter', None),
                                        ('foo/bar', 'foo'),
                                        ('foo/baz', 'foo'),
                                        ('foo/baz/quux', 'foo/baz')]
        config_name = resource_filename('tests', "test_data/tricky_1")
        self._concurrent_test(config_name,
                              set(expected_concurrent_contents))
        self._concurrent_config_build_test(config_name)
        self._concurrent_config_build_test(config_name, 2)

    def test_directive_ordering_real_1(self):
        """
        A real file from an actual project.
        """
        expected_concurrent_contents = [
            ('ubuntu', None),
            ('apache2', None),
            ('apache2/exec.d', 'apache2'),
            ('apache2/exec.d/basenode', 'apache2/exec.d'),
            ('haproxy', None),
            ('haproxy/exec.d', 'haproxy'),
            ('haproxy/exec.d/basenode', 'haproxy/exec.d'),
            ('gunicorn', None),
            ('pgbouncer', None),
            ('pgbouncer/exec.d', 'pgbouncer'),
            ('pgbouncer/exec.d/basenode', 'pgbouncer/exec.d'),
            ('postgresql', None),
            ('postgresql/exec.d', 'postgresql'),
            ('postgresql/exec.d/basenode', 'postgresql/exec.d'),
            ('certification', None),
            ('certification/exec.d', 'certification'),
            ('certification/exec.d/basenode', 'certification/exec.d'),
            ('sample-project', None),
            ('sample-project/third-party', 'sample-project'),
            ('rabbitmq-server', None),
            ('rabbitmq-server/exec.d', 'rabbitmq-server'),
            ('rabbitmq-server/exec.d/basenode', 'rabbitmq-server/exec.d'),
            ('certification-web', None),
            ('nrpe-external-master', None)]
        config_name = resource_filename('tests',
                                        "test_data/collect_1")
        self._concurrent_test(config_name,
                              set(expected_concurrent_contents))
        self._concurrent_config_build_test(config_name)
        self._concurrent_config_build_test(config_name, 2)

    def test_directive_ordering_real_2(self):
        """
        Another real file from an actual project.
        """
        expected_concurrent_contents = [
            ('jobs', None),
            ('jobs/rootfs', 'jobs'),
            ('jobs/android', 'jobs'),
            ('jobs/tarball', 'jobs'),
            ('jobs/android-barajas', 'jobs'),
            ('jobs/android-tangxi', 'jobs'),
            ('jobs/image-puller', 'jobs'),
            ('storage', None),
            ('apache2', None),
            ('apache2/exec.d', 'apache2'),
            ('apache2/exec.d/basenode', 'apache2/exec.d'),
            ('jenkins', None),
            ('jenkins/exec.d', 'jenkins'),
            ('jenkins/exec.d/basenode', 'jenkins/exec.d'),
            ('jenkins/files', 'jenkins'),
            ('jenkins/files/jenkins.deb', 'jenkins/files'),
            ('jenkins/files/plugins', 'jenkins/files'),
            ('jenkins/files/plugins/notification.hpi',
             'jenkins/files/plugins'),
            ('archiver', None),
            ('open-port', None),
            ('capomastro', None),
            ('capomastro/exec.d', 'capomastro'),
            ('capomastro/exec.d/basenode', 'capomastro/exec.d'),
            ('postgresql', None),
            ('postgresql/exec.d', 'postgresql'),
            ('postgresql/exec.d/basenode', 'postgresql/exec.d'),
            ('apache-openid', None),
            ('rabbitmq-server', None),
            ('rabbitmq-server/exec.d', 'rabbitmq-server'),
            ('rabbitmq-server/exec.d/basenode', 'rabbitmq-server/exec.d'),
            ('system-image-server', None),
            ('block-storage-broker', None),
            ('nrpe-external-master', None)]
        config_name = resource_filename('tests',
                                        "test_data/collect_2")
        self._concurrent_test(config_name,
                              set(expected_concurrent_contents))
        self._concurrent_config_build_test(config_name)
        self._concurrent_config_build_test(config_name, 2)

    def test_directive_collect_info(self):
        # This will be used for the result object
        class Object(object):
            pass

        d = Directive()

        # If it's a directory, return an empty dict
        result = Object()
        result.collect_location = '@'
        self.assertEqual(d.collect_info(result), {})

        # If it's a valid location, check our collect_info
        result.collect_location = 'cs:nrpe-33'
        result.dest = 'tests/test_data/collect_info'
        collect_info = d.collect_info(result)
        self.assertEqual(collect_info["collect_url"], 'cs:nrpe-33')
        expected_hashes = {
            'file-with-content.txt': '12e5f06f48001f1a4e017906478f3bd4b8084770a3453da7dca8b8c86dacb973',
            'non_empty_subdir/some_real_content.txt':
                'a79ddd2fdef1bc71bb67139399804f3633d0fbd6e431e29f50b0bb9cde61cc8a',  # noqa
            'some_real_content.txt': 'a79ddd2fdef1bc71bb67139399804f3633d0fbd6e431e29f50b0bb9cde61cc8a',
            }
        self.assertEqual(collect_info["hashes"], expected_hashes)

    def test_empty_collect_file(self):
        # Test that an empty collect file (or a file with comments only)
        # is handled correctly and doesn't throw an error due to 0 workers.
        collect_config = Config('tests/test_data/comments_only')
        self.assertEqual(collect_config.build(), [])


class TestConfigResults(TestCase):
    def test_true(self):
        cr = ConfigResults()
        self.assertTrue(cr)

        cr.append(HandlerResult(True))
        self.assertTrue(cr)

        cr.append(HandlerResult(True))
        self.assertTrue(cr)

    def test_false(self):
        cr = ConfigResults()
        cr.append(HandlerResult(False))
        self.assertFalse(cr)

        cr.append(HandlerResult(True))
        self.assertFalse(cr)

    def test_generate_config(self):
        cr = ConfigResults()
        self.assertEqual("", cr.generate_config())

        cr.append(HandlerResult(True, dest="my-charm",
                                source="git+ssh://git.launchpad.net/~my-team/my-project/+git/my-repo",
                                revision="243e6594eff4cc3e903b299ec8c74b0d8aa617e2"))
        cr.append(HandlerResult(True, dest="nrpe", source="cs:nrpe"))
        cr.append(HandlerResult(True, dest="ntp", source="lp:charms/trusty/ntp", revision="27",
                                options=OrderedDict([("revno", "22"), ("overwrite", "true")])))

        expected = dedent("""\
                    my-charm  git+ssh://git.launchpad.net/~my-team/my-project/+git/my-repo;revno=243e6594eff4cc3e903b299ec8c74b0d8aa617e2
                    nrpe  cs:nrpe
                    ntp  lp:charms/trusty/ntp;overwrite=true,revno=27
                    """)
        self.assertEqual(expected, cr.generate_config())
