from typing import Any, Dict, Optional

from termcolor import colored

from . import api


def delete(
    model_name: str, api_key: Optional[str] = None, silent: bool = False
) -> Dict[str, Any]:
    """
    Delete a model from your model zoo.

    Before calling this function, the model must be in a STOPPED or STOPPING
    state.

    .. warning::

        This operation is irreversible. If you might need to start this model
        in the future and want to save costs by shutting it down, consider
        using :py:func:`modelzoo.stop`.

    Args:
        model_name: String name of the model.
        api_key:
            Optional API key that, if provided, will override the API key
            available to the environment.
        silent:
            Boolean that disables the confirmation prompt when deleting a
            model. Defaults to False.

    Returns:
        Dictionary of model metadata.
    """
    if not silent:
        answer = input(
            colored(
                "You are about to irreversibly delete '{}' from Model Zoo. "
                "Would you like to proceed [Y/N]? ".format(model_name)
            )
        ).lower()
        if answer not in ("y", "yes"):
            print(colored("Operation aborted", "red"))
            return

    api.call(method="DELETE", path="models/{}".format(model_name), api_key=api_key)
    print("✅ Deleted '{}'".format(model_name))
