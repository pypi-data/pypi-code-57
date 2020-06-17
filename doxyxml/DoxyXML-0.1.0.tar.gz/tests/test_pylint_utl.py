#!/usr/bin/env python
"""
Testing string utl module
"""
import os
import os.path as opth
import re
import sys
import unittest

from .quality import pylint_utl

sys.setrecursionlimit(max([10000, sys.getrecursionlimit() * 1000]))


class TestPylintUtl(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Helper method for the preparation of teh tests from this class
        :return: None
        """
        cls.pylint_results_err_warn_file_path = pylint_utl.pylint_results_err_warn_file_path
        cls.pylint_results_err_warn_file_path_summary = pylint_utl.pylint_results_err_warn_file_path_summary

        cls.pylint_results_conv_ref_file_path = pylint_utl.pylint_results_conv_ref_file_path
        cls.pylint_results_conv_ref_file_path_summary = pylint_utl.pylint_results_conv_ref_file_path_summary

        root_references_results = os.environ.get("TESTS_RESULTS_PATH")
        if root_references_results:
            cls.pylint_results_err_warn_file_path = opth.abspath(
                opth.join(root_references_results, opth.basename(cls.pylint_results_err_warn_file_path)))
            cls.pylint_results_err_warn_file_path_summary = opth.abspath(
                opth.join(root_references_results, opth.basename(cls.pylint_results_err_warn_file_path_summary)))

            cls.pylint_results_conv_ref_file_path = opth.abspath(
                opth.join(root_references_results, opth.basename(cls.pylint_results_conv_ref_file_path)))
            cls.pylint_results_conv_ref_file_path_summary = opth.abspath(
                opth.join(root_references_results, opth.basename(cls.pylint_results_conv_ref_file_path_summary)))

    def test_a_run_category_err_warn(self):
        """
        Run code inspection on Error and Warning categories of messages.
        """
        out_arr = pylint_utl.generate_quality_report(
            in_results_file_path=self.pylint_results_err_warn_file_path,
            in_results_file_path_summary=self.pylint_results_err_warn_file_path_summary,
            in_pylintrc_type=pylint_utl.PYLINTRC_TYPE_ERR_WARN)
        nb_results_found = len(out_arr)
        print("test_code_quality ERR_WARN:nb_results_found %d" % nb_results_found)

        self.assertTrue(opth.exists(self.pylint_results_err_warn_file_path_summary),
                        msg="No reference code inspection results found: "
                            "%s" % self.pylint_results_err_warn_file_path_summary)

        with open(self.pylint_results_err_warn_file_path_summary, 'r') as f:
            data = f.read()
            nb_err = int(re.findall(r'NB_ERROR:(\d+)', data)[0])
            nb_warn = int(re.findall(r'NB_WARNING:(\d+)', data)[0])

        print("test_code_quality;NB_ERROR:%d;NB_WARNING:%d" % (nb_err, nb_warn))
        if nb_err > 0:
            with open(self.pylint_results_err_warn_file_path, 'r') as f:
                lines = f.readlines()
            print("Errors:")
            for l in lines:
                if re.search(r"E\d+", l):
                    print("\t" + l.strip())
        self.assertEqual(0, nb_err, msg="%d Code Inspection ERRORs found" % nb_err)
        self.assertEqual(0, nb_warn, msg="%d Code Inspection Warnings found" % nb_warn)

    def test_b_run_category_conv_ref(self):
        """
        Run code inspection on Convention and Refactor categories of messages
        :return: Number of results found from the present run and number of previous results
        :rtype: Union[int, int]
        :return:
        :rtype:
        """
        out_arr = pylint_utl.generate_quality_report(
            in_results_file_path=self.pylint_results_conv_ref_file_path,
            in_results_file_path_summary=self.pylint_results_conv_ref_file_path_summary,
            in_pylintrc_type=pylint_utl.PYLINTRC_TYPE_CONV_REF)
        nb_results_found = len(out_arr)
        print("test_code_quality CONV_REF:nb_results_found %d" % nb_results_found)

        assert opth.exists(self.pylint_results_conv_ref_file_path_summary), \
            "No reference code inspection results found:%s" % self.pylint_results_conv_ref_file_path_summary

        with open(self.pylint_results_conv_ref_file_path_summary, 'r') as f:
            data = f.read()
            nb_conv = int(re.findall(r'NB_CONVENTION:(\d+)', data)[0])
            nb_ref = int(re.findall(r'NB_REFACTOR:(\d+)', data)[0])

        print("test_code_quality;NB_CONVENTION:%d;NB_REFACTOR:%d" % (nb_conv, nb_ref))

    def test_d_check_sanity_script_com(self):
        """
        Identify unexpected character from script file
        """
        pylint_results_file_path = pylint_utl.pylint_sanity_results_file_path

        out_arr = pylint_utl.check_sanity_script()
        nb_results_found = len(out_arr)
        print("test_code_quality check sanity script:nb_results_found %d" % nb_results_found)

        with open(pylint_results_file_path, 'w') as f:
            for row in out_arr:
                f.write("%s\n" % '{}'.format(row))


if __name__ == '__main__':
    unittest.main()
