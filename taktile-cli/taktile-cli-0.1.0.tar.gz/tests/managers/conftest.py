import shutil

import pytest

from tktl.core.managers.project import ProjectManager


@pytest.fixture(scope="function")
def create_proj():
    ProjectManager.init(".", "sample_project")
    yield
    shutil.rmtree("sample_project")
