import inspect
import logging
import traceback

import six
import wrapt
from copy import copy

from . import run_once
from ..tracer import tags
from ..tracer.exception import get_exception_log_fields
from ..formatters.coverage import format_coverage
from .testing_coverage import add_coverage

logger = logging.getLogger(__name__)


class TestResultProxy(wrapt.ObjectProxy):
    def __init__(self, wrapped, span):
        super(TestResultProxy, self).__init__(wrapped)
        self._span = span

    def addError(self, test, err):
        etype, value, tb = err
        self._span.set_tag(tags.TEST_STATUS, tags.TEST_STATUS_FAIL)
        self._span.set_tag(tags.ERROR, True)
        kv = {
            tags.EVENT: 'error',
            tags.MESSAGE: ''.join(traceback.format_exception_only(etype, value)).strip(),
        }
        kv.update(get_exception_log_fields(etype, value, tb))
        self._span.log_kv(kv)
        return self.__wrapped__.addError(test, err)

    def addFailure(self, test, err):
        etype, value, tb = err
        self._span.set_tag(tags.TEST_STATUS, tags.TEST_STATUS_FAIL)
        self._span.set_tag(tags.ERROR, True)
        kv = {
            tags.EVENT: 'test_failure',
            tags.MESSAGE: 'Test failed',
        }
        kv.update(get_exception_log_fields(etype, value, tb))
        self._span.log_kv(kv)
        return self.__wrapped__.addFailure(test, err)

    def addSuccess(self, test):
        self._span.set_tag(tags.TEST_STATUS, tags.TEST_STATUS_PASS)
        return self.__wrapped__.addSuccess(test)

    def addSkip(self, test, reason):
        self._span.set_tag(tags.TEST_STATUS, tags.TEST_STATUS_SKIP)
        self._span.log_kv({tags.EVENT: 'test_skip', tags.MESSAGE: reason})
        return self.__wrapped__.addSkip(test, reason)

    def addExpectedFailure(self, test, err):
        etype, value, tb = err
        self._span.set_tag(tags.TEST_STATUS, tags.TEST_STATUS_PASS)
        kv = {
            tags.EVENT: 'expected_failure',
            tags.MESSAGE: 'Test failed as expected',
        }
        kv.update(get_exception_log_fields(etype, value, tb))
        self._span.log_kv(kv)
        return self.__wrapped__.addExpectedFailure(test, err)

    def addUnexpectedSuccess(self, test):
        self._span.set_tag(tags.TEST_STATUS, tags.TEST_STATUS_FAIL)
        self._span.set_tag(tags.ERROR, True)
        self._span.log_kv({tags.EVENT: 'unexpected_success', tags.MESSAGE: 'Test passed unexpectedly'})
        return self.__wrapped__.addUnexpectedSuccess(test)


# If a test is skipped by unittest.skip, it will be wrapped (due to functools.update_wrapper).
# Not available on Python 2.7.
def _get_unittest_wrapped(test_method):
    unwrapped_test_method = test_method
    while hasattr(unwrapped_test_method, '__wrapped__'):
        unwrapped_test_method = unwrapped_test_method.__wrapped__

    return unwrapped_test_method


def _run_test(tracer, wrapped, instance, result):
    try:
        test_method = getattr(instance, instance._testMethodName)
        test_method = _get_unittest_wrapped(test_method)
        file = inspect.getsourcefile(test_method)
        lines, first_line = inspect.getsourcelines(test_method)
        code = '%s:%d:%d' % (file, first_line, first_line + len(lines) - 1)
    except (IOError, OSError, TypeError):
        code = ''

    if six.PY2:
        name = instance.__class__.__name__
    else:
        name = instance.__class__.__qualname__

    test_suite = '%s.%s' % (instance.__class__.__module__, name)
    test_name = instance._testMethodName

    test_has_passed = False
    with tracer.start_active_span(
        operation_name=instance._testMethodName,
        tags={
            tags.SPAN_KIND: tags.TEST,
            tags.TEST_FRAMEWORK: 'unittest',
            tags.TEST_SUITE: test_suite,
            tags.TEST_NAME: test_name,
            tags.TEST_CODE: code,
        },
    ) as scope:
        scope.span.context.baggage[tags.TRACE_KIND] = tags.TEST

        fqn = (test_suite, test_name)
        # If we want the test to appear SKIPPED in the report, we need to run `wrapped`
        # We could do it by
        # setattr(instance, instance._testMethodName, lambda: instance.skipTest('Cached by Scope'))
        # https://stackoverflow.com/questions/19031953/skip-unittest-test-without-decorator-syntax
        if tracer.runner_enabled:
            should_cache = fqn in tracer.tests_to_cache
            if should_cache:
                test_has_passed = True
                scope.span.set_tag(tags.TEST_STATUS, tags.TEST_STATUS_CACHE)
                return test_has_passed, None

        with add_coverage(tracer, fqn) as (code_path_enabled, coverage):
            test_result = wrapped(TestResultProxy(result, scope.span))

        test_has_passed = (
            scope.span.tags[tags.TEST_STATUS] == tags.TEST_STATUS_PASS
            or scope.span.tags[tags.TEST_STATUS] == tags.TEST_STATUS_SKIP
        )

        if code_path_enabled:
            scope.span.set_tag(
                tags.TEST_COVERAGE, format_coverage(coverage),
            )

        return test_has_passed, test_result


def _django_compat_retry_setup(test, has_already_run):
    # It is possible that this is a Django Test. In these tests
    # there are custom setup and tear down steps:
    # https://github.com/django/django/blob/44da7abda848f05caaed74f6a749038c87dedfda/django/test/testcases.py#L267
    if has_already_run and hasattr(test, '_pre_setup'):
        test._pre_setup()


def _django_compat_retry_tear_down(test, test_has_passed, is_last_iteration):
    # https://github.com/django/django/blob/44da7abda848f05caaed74f6a749038c87dedfda/django/test/testcases.py#L274
    if not test_has_passed and not is_last_iteration and hasattr(test, '_post_teardown'):
        test._post_teardown()


@run_once
def patch(tracer):
    def test_case_run_wrapper(wrapped, instance, args, kwargs):
        logger.debug('intercepting test: instance=%s args=%s kwargs=%s', instance, args, kwargs)
        # result argument to UnitTest.run() is optional. If not given, default is created.
        if args:
            result = args[0]
        elif 'result' in kwargs:
            result = kwargs['result']
        else:
            result = instance.defaultTestResult()

        original_result = copy(result)

        if not tracer.runner_enabled:
            _, test_result = _run_test(tracer, wrapped, instance, result)
            return test_result

        num_test_runs = 0
        test_has_passed = False

        while num_test_runs < 1 + tracer.fail_retries and not test_has_passed:
            has_already_run = num_test_runs > 0

            if has_already_run:
                # If we are retrying, we reset the result to the original one
                result = copy(original_result)

            _django_compat_retry_setup(instance, has_already_run)

            test_has_passed, test_result = _run_test(tracer, wrapped, instance, result)

            num_test_runs = num_test_runs + 1
            is_last_iteration = num_test_runs == 1 + tracer.fail_retries

            _django_compat_retry_tear_down(instance, test_has_passed, is_last_iteration)

        return test_result

    try:
        logger.debug('patching module=unittest name=TestCase')
        wrapt.wrap_function_wrapper('unittest', 'TestCase.run', test_case_run_wrapper)
    except ImportError:
        logger.debug('module not found module=unittest')
