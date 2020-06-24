import inspect
import logging


import wrapt

from scopeagent.tracer import tags
from ..formatters.coverage import format_coverage
from .testing_coverage import add_coverage
from . import run_once

logger = logging.getLogger(__name__)


def _run_test(tracer, wrapped, args, kwargs):
    testfn = args[0].obj
    try:
        file = inspect.getsourcefile(testfn)
        lines, first_line = inspect.getsourcelines(testfn)
        code = "%s:%d:%d" % (file, first_line, first_line + len(lines))
    except (IOError, OSError):
        code = ""

    test_has_passed = False
    with tracer.start_active_span(
        operation_name=testfn.__name__,
        tags={
            tags.SPAN_KIND: tags.TEST,
            tags.TEST_FRAMEWORK: 'pytest',
            tags.TEST_SUITE: testfn.__module__,
            tags.TEST_NAME: testfn.__name__,
            tags.TEST_CODE: code,
        },
    ) as scope:
        scope.span.context.baggage[tags.TRACE_KIND] = tags.TEST
        fqn = (testfn.__module__, testfn.__name__)
        if tracer.runner_enabled:
            should_cache = fqn in tracer.tests_to_cache
            if should_cache:
                test_has_passed = True
                scope.span.set_tag(tags.TEST_STATUS, tags.TEST_STATUS_CACHE)
                return test_has_passed, None

        with add_coverage(tracer, fqn) as (code_path_enabled, coverage):
            results = wrapped(*args, **kwargs)

        if code_path_enabled:
            scope.span.set_tag(
                tags.TEST_COVERAGE, format_coverage(coverage),
            )

        for result in results:
            if result.outcome == 'failed':
                scope.span.set_tag(tags.TEST_STATUS, tags.TEST_STATUS_FAIL)
                scope.span.set_tag(tags.ERROR, True)
                logger.debug(type(result.longrepr))
                break
            elif result.outcome == 'skipped':
                scope.span.set_tag(tags.TEST_STATUS, tags.TEST_STATUS_SKIP)
                break

        if tags.TEST_STATUS not in scope.span.tags:
            scope.span.set_tag(tags.TEST_STATUS, tags.TEST_STATUS_PASS)

        test_has_passed = (
            scope.span.tags[tags.TEST_STATUS] == tags.TEST_STATUS_PASS
            or scope.span.tags[tags.TEST_STATUS] == tags.TEST_STATUS_SKIP
        )

        return test_has_passed, results


@run_once
def patch(tracer):
    def runtestprotocol_wrapper(wrapped, instance, args, kwargs):
        logger.debug("intercepting test: instance=%s args=%s kwargs=%s", instance, args, kwargs)

        if not tracer.runner_enabled:
            _, results = _run_test(tracer, wrapped, args, kwargs)
            return results

        num_test_runs = 0
        test_has_passed = False

        while not test_has_passed and (num_test_runs < 1 + tracer.fail_retries):
            test_has_passed, results = _run_test(tracer, wrapped, args, kwargs)
            num_test_runs = num_test_runs + 1

        return results

    try:
        logger.debug("patching module=_pytest.runner name=runtestprotocol")
        wrapt.wrap_function_wrapper('_pytest.runner', 'runtestprotocol', runtestprotocol_wrapper)

    except ImportError:
        logger.debug("module not found module=_pytest.runner")
