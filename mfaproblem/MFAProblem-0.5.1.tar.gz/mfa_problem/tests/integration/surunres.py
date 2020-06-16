
import io
import sys
import traceback
import time
import warnings

from unittest import result, util
from unittest.signals import registerResult
from functools import wraps

__unittest = True

"""Customized Test result object"""

def failfast(method):
    @wraps(method)
    def inner(self, *args, **kw):
        if getattr(self, 'failfast', False):
            self.stop()
        return method(self, *args, **kw)
    return inner

STDOUT_LINE = '\nStdout:\n%s'
STDERR_LINE = '\nStderr:\n%s'


class suTestResult(object):
    """Holder for test result information.

    Test results are automatically managed by the TestCase and TestSuite
    classes, and do not need to be explicitly manipulated by writers of tests.

    Each instance holds the total number of tests run, and collections of
    failures and errors that occurred among those test runs. The collections
    contain tuples of (testcase, exceptioninfo), where exceptioninfo is the
    formatted traceback of the error that occurred.
    """
    _previousTestClass = None
    _testRunEntered = False
    _moduleSetUpFailed = False
    def __init__(self, stream=None, descriptions=None, verbosity=None):
        self.failfast = False
        self.failures = []
        self.errors = []
        self.testsRun = 0
        self.skipped = []
        self.expectedFailures = []
        self.unexpectedSuccesses = []
        self.shouldStop = False
        self.buffer = False
        self.tb_locals = False
        self._stdout_buffer = None
        self._stderr_buffer = None
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        self._mirrorOutput = False
        self.success = []
        self.subtestsRun = 0
        self.subtestsRunTot = 0

    def printErrors(self):
        "Called by TestRunner after test run"

    def startTest(self, test):
        "Called when the given test is about to be run"
        self.testsRun += 1
        self.subtestsRun = 0
        self._mirrorOutput = False
        self._setupStdout()

    def _setupStdout(self):
        if self.buffer:
            if self._stderr_buffer is None:
                self._stderr_buffer = io.StringIO()
                self._stdout_buffer = io.StringIO()
            sys.stdout = self._stdout_buffer
            sys.stderr = self._stderr_buffer

    def startTestRun(self):
        """Called once before any tests are executed.

        See startTest for a method called before each test.
        """

    def stopTest(self, test):
        """Called when the given test has been run"""
        self.subtestsRunTot += self.subtestsRun
        self._restoreStdout()
        self._mirrorOutput = False

    def _restoreStdout(self):
        if self.buffer:
            if self._mirrorOutput:
                output = sys.stdout.getvalue()
                error = sys.stderr.getvalue()
                if output:
                    if not output.endswith('\n'):
                        output += '\n'
                    self._original_stdout.write(STDOUT_LINE % output)
                if error:
                    if not error.endswith('\n'):
                        error += '\n'
                    self._original_stderr.write(STDERR_LINE % error)

            sys.stdout = self._original_stdout
            sys.stderr = self._original_stderr
            self._stdout_buffer.seek(0)
            self._stdout_buffer.truncate()
            self._stderr_buffer.seek(0)
            self._stderr_buffer.truncate()

    def stopTestRun(self):
        """Called once after all tests are executed.

        See stopTest for a method called after each test.
        """

    @failfast
    def addError(self, test, err):
        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info().
        """
        msgnbtest = 'Test: ' + str(self.testsRun)
        self.errors.append((test, self._exc_info_to_string(err, test), msgnbtest))
        self._mirrorOutput = True

    @failfast
    def addFailure(self, test, err):
        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info()."""
        msgnbtest = 'Test: ' + str(self.testsRun)
        self.failures.append((test, self._exc_info_to_string(err, test), msgnbtest))
        self._mirrorOutput = True

    def addSubTest(self, test, subtest, err):
        """Called at the end of a subtest.
        'err' is None if the subtest ended successfully, otherwise it's a
        tuple of values as returned by sys.exc_info().
        """
        # By default, we don't do anything with successful subtests, but
        # more sophisticated test results might want to record them.
        self.subtestsRun += 1
        msgnbtest = 'Test: ' + str(self.testsRun) + ' - SubTest: ' + str(self.subtestsRun)
        if err is not None:
            if getattr(self, 'failfast', False):
                self.stop()
            if issubclass(err[0], test.failureException):
                errors = self.failures
            else:
                errors = self.errors
            errors.append((subtest, self._exc_info_to_string(err, test), msgnbtest))
            self._mirrorOutput = True
        else:
            self.success.append((subtest, self._exc_info_to_string('', test), msgnbtest))
            self._mirrorOutput = True

    def addSuccess(self, test):
        "Called when a test has completed successfully"
        #self.success.append(test)
        #self._mirrorOutput = True
        #pass

    def addSkip(self, test, reason):
        """Called when a test is skipped."""
        self.skipped.append((test, reason))

    def addExpectedFailure(self, test, err):
        """Called when an expected failure/error occurred."""
        self.expectedFailures.append(
            (test, self._exc_info_to_string(err, test)))

    @failfast
    def addUnexpectedSuccess(self, test):
        """Called when a test was expected to fail, but succeed."""
        self.unexpectedSuccesses.append(test)

    def wasSuccessful(self):
        """Tells whether or not this result was a success."""
        # The hasattr check is for test_result's OldResult test.  That
        # way this method works on objects that lack the attribute.
        # (where would such result intances come from? old stored pickles?)
        return ((len(self.failures) == len(self.errors) == 0) and
                (not hasattr(self, 'unexpectedSuccesses') or
                 len(self.unexpectedSuccesses) == 0))

    def stop(self):
        """Indicates that the tests should be aborted."""
        self.shouldStop = True

    def _exc_info_to_string(self, err, test):
        """Converts a sys.exc_info()-style tuple of values into a string."""
        if type(err) != str:
            exctype, value, tb = err
            # Skip test runner traceback levels
            while tb and self._is_relevant_tb_level(tb):
                tb = tb.tb_next

            if exctype is test.failureException:
                # Skip assert*() traceback levels
                length = self._count_relevant_tb_levels(tb)
            else:
                length = None
            tb_e = traceback.TracebackException(
                exctype, value, tb, limit=length, capture_locals=self.tb_locals)
            msgLines = list(tb_e.format())
        else:
            msgLines = []

        if self.buffer:
            output = sys.stdout.getvalue()
            error = sys.stderr.getvalue()
            if output:
                if not output.endswith('\n'):
                    output += '\n'
                msgLines.append(STDOUT_LINE % output)
            if error:
                if not error.endswith('\n'):
                    error += '\n'
                msgLines.append(STDERR_LINE % error)
        return ''.join(msgLines)


    def _is_relevant_tb_level(self, tb):
        return '__unittest' in tb.tb_frame.f_globals

    def _count_relevant_tb_levels(self, tb):
        length = 0
        while tb and not self._is_relevant_tb_level(tb):
            length += 1
            tb = tb.tb_next
        return length

    def __repr__(self):
        return ("<%s run=%i errors=%i failures=%i>" %
               (util.strclass(self.__class__), self.testsRun, len(self.errors),
                len(self.failures)))

"""customized Running tests"""

class _WritelnDecorator(object):
    """Used to decorate file-like objects with a handy 'writeln' method"""
    def __init__(self,stream):
        self.stream = stream

    def __getattr__(self, attr):
        if attr in ('stream', '__getstate__'):
            raise AttributeError(attr)
        return getattr(self.stream,attr)

    def writeln(self, arg=None):
        if arg:
            self.write(arg)
        self.write('\n') # text-mode streams translate to \r\n if needed


class suTextTestResult(suTestResult):
    """A test result class that can print formatted text results to a stream.

    Used by TextTestRunner.
    """
    separator1 = '=' * 70
    separator2 = '-' * 70

    def __init__(self, stream, descriptions, verbosity):
        super(suTextTestResult, self).__init__(stream, descriptions, verbosity)
        self.stream = stream
        self.showAll = verbosity > 1
        self.dots = verbosity == 1
        self.descriptions = descriptions

    def getDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return '\n'.join((str(test), doc_first_line))
        else:
            return str(test)

    def startTest(self, test):
        super(suTextTestResult, self).startTest(test)
        if self.showAll:
            self.stream.write(self.getDescription(test))
            self.stream.write(" ... ")
            self.stream.flush()

    def addSuccess(self, test):
        super(suTextTestResult, self).addSuccess(test)
        if self.showAll:
            self.stream.writeln("ok")
        elif self.dots:
            self.stream.write('.')
            self.stream.flush()

    def addError(self, test, err):
        super(suTextTestResult, self).addError(test, err)
        if self.showAll:
            self.stream.writeln("ERROR")
        elif self.dots:
            self.stream.write('E')
            self.stream.flush()

    def addFailure(self, test, err):
        super(suTextTestResult, self).addFailure(test, err)
        if self.showAll:
            self.stream.writeln("FAIL")
        elif self.dots:
            self.stream.write('F')
            self.stream.flush()

    def addSkip(self, test, reason):
        super(suTextTestResult, self).addSkip(test, reason)
        if self.showAll:
            self.stream.writeln("skipped {0!r}".format(reason))
        elif self.dots:
            self.stream.write("s")
            self.stream.flush()

    def addExpectedFailure(self, test, err):
        super(suTextTestResult, self).addExpectedFailure(test, err)
        if self.showAll:
            self.stream.writeln("expected failure")
        elif self.dots:
            self.stream.write("x")
            self.stream.flush()

    def addUnexpectedSuccess(self, test):
        super(suTextTestResult, self).addUnexpectedSuccess(test)
        if self.showAll:
            self.stream.writeln("unexpected success")
        elif self.dots:
            self.stream.write("u")
            self.stream.flush()

    def printErrors(self):
        if self.dots or self.showAll:
            self.stream.writeln()
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)
        self.printErrorList('SUCCESS', self.success)

    def printErrorList(self, flavour, errors):
        for test, err, nb in errors:
            self.stream.writeln(self.separator1)
            self.stream.writeln("%s (%s): %s" % (flavour, nb, self.getDescription(test)))
            self.stream.writeln(self.separator2)
            self.stream.writeln("%s" % err)


class suTextTestRunner(object):
    """A test runner class that displays results in textual form.

    It prints out the names of tests as they are run, errors as they
    occur, and a summary of the results at the end of the test run.
    """
    resultclass = suTextTestResult

    def __init__(self, stream=None, descriptions=True, verbosity=1,
                 failfast=False, buffer=False, resultclass=None, warnings=None,
                 *, tb_locals=False):
        """Construct a TextTestRunner.

        Subclasses should accept **kwargs to ensure compatibility as the
        interface changes.
        """
        if stream is None:
            stream = sys.stderr
        self.stream = _WritelnDecorator(stream)
        self.descriptions = descriptions
        self.verbosity = verbosity
        self.failfast = failfast
        self.buffer = buffer
        self.tb_locals = tb_locals
        self.warnings = warnings
        if resultclass is not None:
            self.resultclass = resultclass

    def _makeResult(self):
        return self.resultclass(self.stream, self.descriptions, self.verbosity)

    def run(self, test):
        "Run the given test case or test suite."
        result = self._makeResult()
        registerResult(result)
        result.failfast = self.failfast
        result.buffer = self.buffer
        result.tb_locals = self.tb_locals
        with warnings.catch_warnings():
            if self.warnings:
                # if self.warnings is set, use it to filter all the warnings
                warnings.simplefilter(self.warnings)
                # if the filter is 'default' or 'always', special-case the
                # warnings from the deprecated unittest methods to show them
                # no more than once per module, because they can be fairly
                # noisy.  The -Wd and -Wa flags can be used to bypass this
                # only when self.warnings is None.
                if self.warnings in ['default', 'always']:
                    warnings.filterwarnings('module',
                            category=DeprecationWarning,
                            message=r'Please use assert\w+ instead.')
            startTime = time.time()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()
            try:
                test(result)
            finally:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()
            stopTime = time.time()
        timeTaken = stopTime - startTime
        result.printErrors()
        if hasattr(result, 'separator2'):
            self.stream.writeln(result.separator2)
        run = result.testsRun
        runsub = result.subtestsRunTot
        self.stream.writeln("Ran %d test%s and %d subtest%s in %.3fs" %
                            (run, run != 1 and "s" or "", runsub, runsub != 1 and "s" or "",timeTaken))
        self.stream.writeln()

        expectedFails = unexpectedSuccesses = skipped = 0
        try:
            results = map(len, (result.expectedFailures,
                                result.unexpectedSuccesses,
                                result.skipped))
        except AttributeError:
            pass
        else:
            expectedFails, unexpectedSuccesses, skipped = results

        infos = []
        if not result.wasSuccessful():
            self.stream.write("FAILED")
            failed, errored = len(result.failures), len(result.errors)
            if failed:
                infos.append("failures=%d" % failed)
            if errored:
                infos.append("errors=%d" % errored)
        else:
            self.stream.write("OK")
        if skipped:
            infos.append("skipped=%d" % skipped)
        if expectedFails:
            infos.append("expected failures=%d" % expectedFails)
        if unexpectedSuccesses:
            infos.append("unexpected successes=%d" % unexpectedSuccesses)
        if infos:
            self.stream.writeln(" (%s)" % (", ".join(infos),))
        else:
            self.stream.write("\n")
        return result
