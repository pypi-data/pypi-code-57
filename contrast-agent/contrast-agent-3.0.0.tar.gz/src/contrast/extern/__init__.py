# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Contains dependencies of the agent that we have chosen to vendor

Vendoring dependencies can make life easier on both ourselves and our
customers. Some customers have fairly constrained environments which can make
it difficult for them to install our dependencies. By vendoring, we reduce the
burden for them. Vendoring also allows ourselves to use specific, known stable
versions of dependencies without worrying about conflicts in customer
environments. This can be especially useful for common packages that are
expected to already exist in most environments (e.g. `six`).

The code under this directory should be ignored when linting and when
calculating test coverage since it is technically out of our control. In
general we should not make changes to the code in this directory other than to
introduce a different version of a particular package.

Packages included:
    - backports.functools_lru_cache-1.5
    - isort-5.0.0 (dev)
    - ruamel.yaml-0.16.10
    - WebOb-1.8.6
    - six-1.14.0
    - wrapt-1.12.1
    - pathlib2-2.3.5 (Python 2.7 only)
    - scandir-1.10.0 (required for pathlib2)
"""
