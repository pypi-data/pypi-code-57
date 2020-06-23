import requests


def graphql_query(query_url: str, payload: dict):
    """
    Graphql 查询
    :param query_url:
    :param payload:
    :return:
    """
    res = requests.post(
        url=query_url,
        json=payload,
        headers={'content-type': 'application/json'}
    )

    res.raise_for_status()

    return res.json()
