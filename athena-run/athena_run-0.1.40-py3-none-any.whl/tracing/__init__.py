from .local_context import LocalContext
import os

service_name = os.environ.get("ATHENA_SERVICE_NAME", "default")
dry_run = bool(os.environ.get("ATHENA_DRY_RUN", False))
file_output = os.environ.get("ATHENA_FILE_OUTPUT", None)

if file_output:
    dry_run = True

DefaultContext = LocalContext(
    service=service_name, span_id=0, dry_run=dry_run, file_output=file_output
)

import atexit
atexit.register(DefaultContext.flush_buffer_to_agent)
atexit.register(DefaultContext.close_auto_main_span)
atexit.register(DefaultContext.stop_metrics_thread)
