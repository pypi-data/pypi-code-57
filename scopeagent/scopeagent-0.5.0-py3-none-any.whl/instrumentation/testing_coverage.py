from coverage import Coverage
from contextlib import contextmanager

from scopeagent.tracer import tags


@contextmanager
def add_coverage(tracer, fqn):
    code_path_enabled = tracer.recorder.metadata[tags.CODE_PATH_ENABLED]
    cov = None
    if code_path_enabled:
        # We remove previously stored data
        cov = Coverage()
        cov.start()
        cov.switch_context(str(fqn))
    try:
        yield (code_path_enabled, cov)
    finally:
        if code_path_enabled:
            cov.stop()
            cov.save()
