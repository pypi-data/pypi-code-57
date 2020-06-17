from datetime import datetime


class QueryBuilder:
    """ Class responsible for build URL like:
    https://api.github.com/search/repositories?q=stars:%3E=10000+language:go&sort=stars&order=desc
    """
    BASE_URL = "https://api.github.com/search/repositories"

    def __init__(self, **kwargs):
        self.language = kwargs.get("language", "")
        self.created = kwargs.get("created", {}) or {}
        self.pushed = kwargs.get("pushed", {}) or {}
        self.stars = kwargs.get("stars", {}) or {}
        self.forks = kwargs.get("forks", {}) or {}

    def build(self) -> str:
        def get_params() -> str:
            created = self.translate_lt_gt("created")
            pushed = self.translate_lt_gt("pushed")
            stars = self.translate_lt_gt("stars")
            forks = self.translate_lt_gt("forks")
            return f"{self._language()}{created}{pushed}{stars}{forks}"

        return f"{self.BASE_URL}?q={get_params()}"

    def translate_lt_gt(self, item: str) -> str:
        if item not in self.__dict__:
            return ""

        prefix = ""
        gt = self.__dict__[item].get('gt')
        lt = self.__dict__[item].get('lt')

        if gt:
            prefix += f"+{item}:>{gt}"

        if lt:
            prefix += f"+{item}:<{lt}"

        return prefix

    def _language(self):
        return f"language:{self.language}" if self.language else ""
