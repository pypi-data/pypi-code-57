# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
from os.path import dirname

from azureml.automl.core._shared_package_legacy_import import _import_all_legacy_submodules


def _handle_legacy_shared_package_imports():
    # Note: the code in the 'shared' package is used directly by some AutoML components that live in the
    # Jasmine repo. This shared package used to be importable under different namespaces.
    # For the sake of backwards compatibility (not breaking legacy code still using these imports),
    # we redirect legacy aliases to the 'shared' module they intend to reference.
    legacy_aliases = set([
        "automl.client.core.runtime",
        "azureml.automl.runtime._vendor.automl.client.core.runtime",
    ])

    # Find azureml package's init file.
    # (Legacy stub package imports will be redirected to the top-level azureml stub package.)
    azureml_init_file_path = os.path.join(dirname(dirname(dirname(__file__))), "__init__.py")

    from . import shared

    _import_all_legacy_submodules(
        legacy_aliases,
        azureml_init_file_path,
        shared
    )
