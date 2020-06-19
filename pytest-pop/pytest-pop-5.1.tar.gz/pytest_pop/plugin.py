# -*- coding: utf-8 -*-
import _pytest.python as pythtest
import mock
import os
import pop.hub
import pytest
import sys
import logging
from typing import Any, Dict, List

log = logging.getLogger("pytest_pop.plugin")


def pytest_sessionstart(session: pytest.Session):
    CODE_DIR = session.config.invocation_dir
    TPATH_DIR = os.path.join(CODE_DIR, "tpath")
    if CODE_DIR in sys.path:
        sys.path.remove(CODE_DIR)
    sys.path.insert(0, CODE_DIR)
    if TPATH_DIR in sys.path:
        sys.path.remove(TPATH_DIR)
    sys.path.insert(0, TPATH_DIR)


@pytest.fixture(autouse=True, scope="session")
def hub():
    """
    Create a base hub that is scoped for session, you should redefine it in your own conftest.py
    to be scoped for modules or functions
    """
    hub = pop.hub.Hub()

    # Set up the rudimentary logger
    hub.pop.sub.add(dyne_name="log")

    # This will create the loop used for pytest-asyncio
    hub.pop.loop.create()

    yield hub

    # Hub cleanup
    hub.pop.Loop.close()


@pytest.fixture
def event_loop(hub):
    yield hub.pop.Loop


@pytest.fixture(autouse=True, scope="function")
def mock_hub(hub):
    # swap out some core mocked functions for real ones
    mock_hub = hub.pop.testing.mock_hub()
    for func in dir(hub.log):
        if not func.startswith("_"):
            setattr(mock_hub.log, func, getattr(hub.log, func))
    for loaded in hub.pop._loaded:
        sub = getattr(hub.pop, loaded)
        for func in sub._funcs:
            setattr(getattr(mock_hub.pop, loaded), func, getattr(sub, func))
    yield mock_hub


@pytest.fixture
def acct_subs() -> List[str]:
    log.error("Override the 'acct_subs' fixture in your own conftest.py")
    return []


@pytest.fixture
def acct_profile() -> str:
    log.error("Override the 'acct_profile' fixture in your own conftest.py")
    return ""


@pytest.fixture
@pytest.mark.asyncio
async def ctx(hub, acct_subs: List[str], acct_profile: str) -> Dict[str, Any]:
    """
    Set up the context for idem-cloud executions
    :param acct_subs: The output of an overridden fixture of the same name
    :param acct_profile: The output of an overridden fixture of the same name
    """
    ctx = {
        "run_name": "test",
        "test": False,
        "acct": {},
    }

    old_opts = hub.OPT

    if acct_subs and acct_profile:
        if not (
            hasattr(hub, "acct") and (hasattr(hub, "states") or hasattr(hub, "exec"))
        ):
            log.debug("Creating a temporary hub to generate ctx")
            # Use a fresh hub, they didn't supply a unique one
            hub = pop.hub.Hub()
            # Add the bare minimum for acct
            for dyne in ("acct", "exec"):
                hub.pop.sub.add(dyne_name=dyne)

        if not (
            hub.OPT.get("acct")
            and hub.OPT.acct.get("acct_file")
            and hub.OPT.acct.get("acct_key")
        ):
            # Get the account information from environment variables
            log.debug("Loading temporary config from idem and acct")
            with mock.patch("sys.argv", ["pytest_pop"]):
                hub.pop.config.load(["idem", "acct"], "idem", parse_cli=False)

        # Add the profile to the account
        hub.acct.init.unlock(hub.OPT.acct.acct_file, hub.OPT.acct.acct_key)
        ctx["acct"] = await hub.acct.init.gather(acct_subs, acct_profile)

    hub.OPT = old_opts

    yield ctx


def pytest_runtest_protocol(item: pythtest.Function, nextitem: pythtest.Function):
    """
    implements the runtest_setup/call/teardown protocol for
    the given test item, including capturing exceptions and calling
    reporting hooks.
    """
    log.debug(f">>>>> START >>>>> {item.name}")


def pytest_runtest_teardown(item: pythtest.Function):
    """
    called after ``pytest_runtest_call``
    """
    log.debug(f"<<<<< END <<<<<<< {item.name}")


@pytest.fixture(scope="session", autouse=True)
def os_sleep_secs():
    if "CI_RUN" in os.environ:
        return 1.75
    return 0.5
