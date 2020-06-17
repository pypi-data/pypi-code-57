import pytest
from repofinder.query import QueryBuilder


def test_query_all():
    params = {
        "language": "python",
        "created": {"lt": "2020-10-10", "gt": "2020-09-09"},
        "pushed": {"lt": "2020-10-10", "gt": "2020-09-09"},
        "forks": {"lt": 100, "gt": 50},
        "stars": {"lt": 100, "gt": 50},
    }

    assert QueryBuilder(**params).build() == (
        "https://api.github.com/search/repositories?q=language:python"
        "+created:>2020-09-09"
        "+created:<2020-10-10"
        "+pushed:>2020-09-09"
        "+pushed:<2020-10-10"
        "+stars:>50"
        "+stars:<100"
        "+forks:>50"
        "+forks:<100")
