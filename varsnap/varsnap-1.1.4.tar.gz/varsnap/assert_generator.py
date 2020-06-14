import logging
import sys
import unittest

from qualname import qualname
from typing import Iterable, Tuple

from . import core


varsnap_logger = logging.getLogger(core.__name__)
varsnap_logger.handlers = []
varsnap_logger.disabled = True
varsnap_logger.propagate = False

test_logger = logging.getLogger(__name__)
test_logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
test_logger.addHandler(handler)


def test() -> Tuple[bool, Iterable[Tuple[bool, str]]]:
    results = []
    for consumer in core.CONSUMERS:
        consumer_name = qualname(consumer.target_func)
        test_logger.info("Running Varsnap tests for %s" % consumer_name)
        result = consumer.consume()
        results.append(result)
    overall_result = all([x[0] for x in results])
    return overall_result, results


class TestVarsnap(unittest.TestCase):
    def test_varsnap(self) -> None:
        overall_result, results = test()
        if not results:
            raise unittest.case.SkipTest('No Snaps found')
        logs = [x[1] for x in results if not x[0]]
        logs_formatted = "\n\n".join(logs)
        self.assertTrue(overall_result, logs_formatted)
