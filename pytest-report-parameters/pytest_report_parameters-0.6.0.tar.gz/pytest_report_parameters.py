"""Plugin for adding test parameters to junit report."""

import pytest


def get_unicode_str(obj):
    """Make sure obj is a unicode string."""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, bytes):
        return obj.decode("utf-8", errors="ignore")
    return str(obj)


def extract_parameters(item):
    """Extract names and values of all the fixtures that the test has.

    Args:
        item: py.test test item
    Returns:
        :py:class:`dict` with fixtures and their values.

    """
    try:
        return item.callspec.params.copy()  # protect against accidential manipulation of the spec
    except AttributeError:
        # Some of the test items do not have callspec, so fall back
        # This can cause some problems if the fixtures are used in the guards in this case, but
        # that will tell use where is the problem and we can then find it out properly.
        return {}


@pytest.mark.tryfirst
# pylint: disable=protected-access
def pytest_collection_modifyitems(session, config, items):
    # prevent on slave nodes (xdist)
    if hasattr(config, "slaveinput"):
        return

    # collect tests metadata
    if config.pluginmanager.hasplugin("pytest_polarion_collect"):
        config.hook.pytest_collect_polarion_metadata(session=session, items=items)

    node_map = {
        item.nodeid: {
            "params": extract_parameters(item),
            "id": getattr(item, "_testcase_data", {}).get("id"),
        }
        for item in items
    }

    config.pluginmanager.register(AddPropertiesToJunitPlugin(node_map=node_map))


class AddPropertiesToJunitPlugin:
    def __init__(self, node_map):
        self.node_map = node_map
        self._ff = False

    @pytest.mark.tryfirst
    def pytest_runtest_logreport(self, report):
        """Add the parameters and ids to the junit report as a property."""
        if report.when != "teardown":
            return

        node_record = self.node_map.get(report.nodeid) or {}

        test_id = node_record.get("id")
        if test_id:
            report.user_properties.append(("polarion-testcase-id", get_unicode_str(test_id)))

        test_params = node_record.get("params") or {}
        for param, value in test_params.items():
            report.user_properties.append(
                ("polarion-parameter-{}".format(param), get_unicode_str(value))
            )
