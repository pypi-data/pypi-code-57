from flywheel_cli.ingest import errors
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.scanners.abstract import AbstractScanner

from .conftest import DummyWalker


class DummyScanner(AbstractScanner):
    def _scan(self, subdir):
        pass


def test_iter_files_filter_zero_byte_files():
    scanner = DummyScanner(
        None, None, None, DummyWalker([("zero.txt", 0), ("non-zero.txt", 1)])
    )

    files = list(scanner.iter_files("/subdir"))

    assert len(files) == 1
    assert files[0].name == "non-zero.txt"
    assert len(scanner.file_errors) == 1
    assert isinstance(scanner.file_errors[0], T.Error)
    assert scanner.file_errors[0].code == errors.ZeroByteFile.code
    assert scanner.file_errors[0].message == errors.ZeroByteFile.message
    assert scanner.file_errors[0].filepath == "/subdir/zero.txt"
