from typing import Optional
import time

from . import _info, model_state

from yaspin.spinners import Spinners
import yaspin


def wait(
    model_name: str,
    target_state: model_state.ModelState,
    api_key: Optional[str] = None,
    timeout_seconds: int = 300,
) -> None:
    """
    Wait for a model to transition to a desired state.

    Arguments:
        model_name: String name of the model
        target_state:
            A target :py:class:`modelzoo.ModelState` to wait for the model to
            transition to.
        timeout_seconds:
            Maximum number of seconds to wait for.
        api_key:
            Optional API key that, if provided, will override the API key
            available to the environment.

    Returns:
        Dictionary of model metadata
    """
    start = time.time()

    print("Waiting for '{}' to transition to {}".format(model_name, target_state))
    with yaspin.yaspin(Spinners.bouncingBall) as sp:
        while True:
            model_info = _info.info(model_name, api_key)
            state = model_state.ModelState(model_info["state"]["name"])
            description = model_info["state"]["description"]
            if description:
                sp.text = "{} {}: {}".format(model_name, state, description)
            else:
                sp.text = "{} {}".format(model_name, state, description)

            if state == target_state:
                sp.ok("✅")
                return model_info
            elif state in model_state.TERMINAL_STATES:
                sp.fail("💥")
                return model_info

            waited_time = time.time() - start
            if waited_time >= timeout_seconds:
                sp.text = "Timeout reached at {} seconds".format(waited_time)
                sp.fail("💥")
                return model_info

            time.sleep(1)
