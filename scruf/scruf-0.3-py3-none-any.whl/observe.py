import sys


class Observer:
    """
    Abstract class for observing test runs
    """

    def notify_file_open_error(self, filename, exception):
        """Notify when there is an error opening a test file

        Default implementation: print error to stderr

        Dispatched when a call to `open` on a test file raises either `OSError` or
        `IOError`. At this point we bail on testing the file

        Parameters
        ----------
        filename : str
            The file that opening was attempted on
        exception : { "OSError", "IOError" }
        """
        print(
            "Failed to open file {}: {}".format(filename, exception), file=sys.stderr,
        )

    def notify_test_progression_error(self, filename, exception):
        """Notify when there is an error trying to parse a file

        Default implementation: print error to stderr

        Dispatched when a call to `scruf.parser.Parser.parse` raises a
        `scruf.parser.ProgressionError`. At this point we bail on testing the file

        Parameters
        ----------
        filename : str
        exceptoin : scruf.parse.ProgressionError
        """
        print(
            "Error when parsing {}: {}".format(filename, exception), file=sys.stderr,
        )

    def notify_execute_setup_error(self, filename, exception):
        """Notify when there is an error constructing an executor object for a test file

        Default implementation: print error to stderr

        Dispatched when a call to `scruf.execute.Executor` raises a
        `execute.FailedToCreateTestDirError` exception. At this point we bail on testing
        the file

        Parameters
        ----------
        filename : str
        exception : scruf.execute.FailedToCreateTestDirError
        """
        print(
            "Failed to setup test environment for {}: {}".format(filename, exception),
            file=sys.stderr,
        )

    def notify_before_testing_file(self, filename):
        """Notify once we've opened a file for testing

        Default implementation: noop

        Parameters
        ----------
        filename : str
        """
        pass

    def notify_before_tests_run(self, tests):
        """Notify before a set of tests are run

        Default implementation: noop

        Parameters
        ----------
        tests : list of `scruf.test.Test`
            The tests to be run
        """
        pass

    def notify_setup_command_failure(self, test, test_number, setup_command, result):
        """Notify when a setup command is run and returns nonzero

        Default implementation: noop

        If this is triggered we will bail on the current test

        Parameters
        ----------
        test : scurf.test.Test
            The test the setup command belongs to
        setup_command : str
        result : scruf.execute.Result
        """

        pass

    def notify_before_test_run(self, test, test_number):
        """Notify before a single test is run

        Default implementation: noop

        Parameters
        ----------
        test : scruf.test.Test
            The test to be run

        test_number : int
            1-based index of the test in the tests being run
        """
        pass

    def notify_test_error(self, test, test_number, error):
        """Notify when there is a failure running a test

        Default implementation: noop

        This will be called if an error arises from `scruf.run.run_test()`. If this
        occurs the test will be skipped.

        Parameters
        ----------
        test : scruf.test.Test
        test_number : int
        error : { "scruf.compare.RegexError", "scruf.execute.OutOfLinesError" }
            The error that occurred during `scruf.run.run_test()`

        """
        pass

    def notify_test_success(self, test, test_number):
        """
        Notify when a test succeeded

        Default implementation: noop

        Parameters
        ----------
        test : scruf.test.Test
        test_number : int
        """
        pass

    def notify_test_failure(self, test, test_number, failed_comparisons):
        """Notify when a test fails

        Default implementation: noop

        Parameters
        ----------
        test : scruf.test.Test
        test_number : int
        failed_comparisons : list of dicts
            The list of failed comparisons, i.e. outputs from `scruf.run.run_test` with
            "comparison_result" == False
        """
        pass
