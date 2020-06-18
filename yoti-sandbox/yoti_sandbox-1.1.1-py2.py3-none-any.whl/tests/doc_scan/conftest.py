from os.path import join, dirname, abspath

import pytest

from yoti_python_sandbox.doc_scan.client import DocScanSandboxClient

YOTI_CLIENT_SDK_ID = "someSdkId"
FIXTURES_DIR = join(dirname(abspath(__file__)), "fixtures")
PEM_FILE_PATH = join(FIXTURES_DIR, "sdk-test.pem")


@pytest.fixture(scope="module")
def doc_scan_sandbox_client():
    """
    :rtype: DocScanSandboxClient
    """
    return DocScanSandboxClient(YOTI_CLIENT_SDK_ID, PEM_FILE_PATH)
