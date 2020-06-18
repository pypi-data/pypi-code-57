from abc import ABC, abstractmethod


class AbstractBigtableRowMatcher(ABC):

    @abstractmethod
    def matches(self, key: str, column_family: str, qualifier: str, value: str) -> bool:
        pass


class BigtableRowMatcher(AbstractBigtableRowMatcher):
    def __init__(self, key_prefix: str, column_family: str, qualifier: str, value: str) -> None:
        self.__expected_key_prefix = key_prefix
        self.__expected_column_family = column_family
        self.__expected_qualifier = qualifier
        self.__expected_value = value

    def matches(self, key: str, column_family: str, qualifier: str, value: str) -> bool:
        return self.__expected_key_prefix in key and column_family == self.__expected_column_family and qualifier == self.__expected_qualifier and value == self.__expected_value
