"""
Copyright (c) 2020, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

PAGE_PARAM = "page"
PER_PAGE_PARAM = "per_page"
DEFAULT_PER_PAGE_PARAM = 10


def get_pagination_query_params(page, per_page: int) -> dict:
    # Returns the query params object to request a pagination.
    return {PAGE_PARAM: page, PER_PAGE_PARAM: per_page}


def get_uri(base_path: str, paths: []) -> str:
    # Joins the base path and paths array and adds the query values to return a new uri.
    items = [base_path, *paths]
    return "/".join([(u.strip("/") if index + 1 < len(items) else u.lstrip("/")) for index, u in enumerate(items)])


def concat_fqid(company_id: str, id: str) -> str:
    # Concatenates a company bcid and a uuid into a fully qualified id.
    return "{}-{}".format(company_id, id)
