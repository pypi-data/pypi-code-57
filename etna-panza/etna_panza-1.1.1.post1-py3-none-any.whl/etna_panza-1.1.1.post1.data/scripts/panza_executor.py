#!python

from quixote import new_context
from quixote.inspection import new_inspection_result, KOError, InternalError, TimeoutError
import panza
import os
import json
import sys
import traceback
from typing import Dict, Any
from panza._utils import augment_syspath

os.chdir("/moulinette/workdir")

with open("/moulinette/context.json", 'r') as context_file:
    context: Dict[str, Any] = json.load(context_file)

os.remove("/moulinette/context.json")

job_failure = None

results = []

with augment_syspath(["/moulinette"]):
    with new_context(resources_path="/moulinette/resources", delivery_path="/moulinette/rendu", **context):
        blueprint = panza.BlueprintLoader.load_from_directory("/moulinette", complete_load=True)

        print(f"Running inspectors for {blueprint.name}")
        for inspector in blueprint.inspectors:
            with new_inspection_result() as result:
                try:
                    inspector()
                except (KOError, InternalError, AssertionError, TimeoutError) as e:
                    result["assertion_failure"] = str(e)
                    if inspector.is_critical:
                        print("Critical step failure, skipping remaining inspectors")
                        break
                except Exception as e:
                    print(f"Unexpected exception escaped from inspector: {type(e).__name__}: {e}")
                    traceback.print_exc(file=sys.stdout)
                    job_failure = e
                    break
                finally:
                    results.append(result)


with open("/moulinette/result.json", 'w') as f:
    if job_failure is not None:
        result = {"error": {"message": str(job_failure)}}
    else:
        result = {"success": {"results": results}}
    json.dump(result, f, indent=4)

print("Done")
