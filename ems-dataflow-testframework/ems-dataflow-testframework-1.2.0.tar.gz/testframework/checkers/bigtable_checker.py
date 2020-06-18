from google.cloud.bigtable.table import Table
from tenacity import retry, stop_after_attempt, retry_if_exception_type, wait_fixed

from testframework.checkers.bigtable_matchers import AbstractBigtableRowMatcher
from testframework.checkers.checker_message import CheckerMessage

WAIT_BETWEEN_RETRIES_IN_SECONDS = 2.
RETRY_ATTEMPTS = 30


class BigtableChecker:

    def __init__(self, bt_table: Table) -> None:
        self.__table = bt_table
        self.ENCODING = "utf-8"

    def has_row_for(self, checker_message: CheckerMessage, max_attempts: int = RETRY_ATTEMPTS, wait_seconds: float = WAIT_BETWEEN_RETRIES_IN_SECONDS) -> bool:
        @retry(stop=stop_after_attempt(max_attempts), wait=wait_fixed(wait_seconds), retry=retry_if_exception_type(TimeoutError))
        def _has_row_for() -> bool:
            bt_key = checker_message.get_bigtable_key()
            is_found = self.__table.read_row(bt_key.encode(self.ENCODING)) is not None
            if is_found is False:
                raise TimeoutError("Bigtable row not found!")

            return is_found

        return _has_row_for()

    def has_single_row_in_scan_matching(self, bt_key_prefix: str, matcher: AbstractBigtableRowMatcher, max_attempts: int = RETRY_ATTEMPTS,
                                        wait_seconds: float = WAIT_BETWEEN_RETRIES_IN_SECONDS) -> bool:
        @retry(stop=stop_after_attempt(max_attempts), wait=wait_fixed(wait_seconds), retry=retry_if_exception_type(TimeoutError))
        def _has_single_row_in_scan_matching() -> bool:
            end_key = self.__get_bt_end_key(bt_key_prefix)
            scan = self.__table.read_rows(start_key=bt_key_prefix.encode(self.ENCODING), end_key=end_key.encode(self.ENCODING))
            count = 0
            for row_data in scan:
                decoded_key = row_data.row_key.decode(self.ENCODING)
                for column_family, qualifiers in row_data.cells.items():
                    for qualifier, values in qualifiers.items():
                        for value in values:
                            if matcher.matches(decoded_key, column_family, qualifier.decode(self.ENCODING), value.value.decode(self.ENCODING)):
                                count += 1
            if count == 0:
                raise TimeoutError("Bigtable row not found!")

            return count == 1

        return _has_single_row_in_scan_matching()

    @staticmethod
    def __get_bt_end_key(bt_key_prefix: str):
        with_last_char_incremented = bt_key_prefix[:-1] + chr(ord(bt_key_prefix[-1]) + 1)
        return with_last_char_incremented

    def has_single_row_in_scan_for(self, checker_message: CheckerMessage, max_attempts: int = RETRY_ATTEMPTS, wait_seconds: float = WAIT_BETWEEN_RETRIES_IN_SECONDS) -> bool:
        @retry(stop=stop_after_attempt(max_attempts), wait=wait_fixed(wait_seconds), retry=retry_if_exception_type(TimeoutError))
        def _has_single_row_in_scan_for() -> bool:
            bt_key_prefix = checker_message.get_bigtable_key()
            end_key = self.__get_bt_end_key(bt_key_prefix)
            scan = self.__table.read_rows(start_key=bt_key_prefix.encode(self.ENCODING), end_key=end_key.encode(self.ENCODING))
            # scan.consume_all()
            result = []
            for row in scan:
                decoded_key = row.row_key.decode(self.ENCODING)
                result.append(decoded_key)

            num_rows = len(result)

            if num_rows == 1:
                return True
            elif num_rows > 1:
                return False
            elif num_rows == 0:
                raise TimeoutError("Bigtable row not found!")

        return _has_single_row_in_scan_for()
