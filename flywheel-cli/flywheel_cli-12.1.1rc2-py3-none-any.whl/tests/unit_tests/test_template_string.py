import pytest

from flywheel_cli import importers
from flywheel_cli.util import METADATA_EXPR


group_pattern = "(?P<group>{})".format(METADATA_EXPR["string-id"])
project_pattern = "(?P<project>{})".format(METADATA_EXPR["default"])
subject_pattern = "(?P<subject>{})".format(METADATA_EXPR["default"])
session_pattern = "(?P<session>{})".format(METADATA_EXPR["default"])


def test_compile_regex():
    # No special replacement
    result = importers.compile_regex("dicom")
    assert result.pattern == "dicom"

    # Replace group/project
    result = importers.compile_regex("{group}-{project._id}")
    expected = "(?P<group>{})-(?P<project__2e___id>{})".format(
        METADATA_EXPR["string-id"], METADATA_EXPR["default"]
    )
    assert result.pattern == expected

    # Don't replace a normal regex
    result = importers.compile_regex("[a-f]{3}")
    assert result.pattern == "[a-f]{3}"

    # Ignore backslashes
    result = importers.compile_regex(r"\w+")
    assert result.pattern == r"\w+"

    # Escaped groupings
    result = importers.compile_regex(r"\{foo\}")
    assert result.pattern == r"\{foo\}"

    # Fix groups
    result = importers.compile_regex(r"(?P<project._id>\w+)")
    assert result.pattern == r"(?P<project__2e___id>\w+)"


def test_parse_template_string():
    result = importers.parse_template_string("{group}")

    assert result
    assert result.template.pattern == group_pattern
    assert result.packfile_type is None
    assert result.next_node == importers.TERMINAL_NODE

    result = importers.parse_template_string("{group}:{project}")

    assert result
    assert result.template.pattern == group_pattern
    assert result.packfile_type is None

    result = result.next_node
    assert result
    assert result.template.pattern == project_pattern
    assert result.packfile_type is None
    assert result.next_node == importers.TERMINAL_NODE

    result = importers.parse_template_string(
        r"{group}:{project}:(?P<session>[a-zA-Z0-9]+)-(?P<subject>\d+):scans,packfile_type=pv5"
    )

    assert result
    assert result.template.pattern == group_pattern
    assert result.packfile_type is None

    result = result.next_node
    assert result
    assert result.template.pattern == project_pattern
    assert result.packfile_type is None

    result = result.next_node
    assert result
    assert result.template.pattern == r"(?P<session>[a-zA-Z0-9]+)-(?P<subject>\d+)"
    assert result.packfile_type is None

    result = result.next_node
    assert result
    assert result.template.pattern == "scans"
    assert result.packfile_type == "pv5"
    assert result.next_node == importers.TERMINAL_NODE

    with pytest.raises(ValueError):
        result = importers.parse_template_string("{foo.bar}")

    with pytest.raises(ValueError):
        result = importers.parse_template_string("{group.label.foo}")

    result = importers.parse_template_string("{subject.info.AdmissionID}")
    assert result


def test_parse_template_list():
    tmpl = [
        "{group}",
        {"pattern": "{project}"},
        {"pattern": r"(?P<session>[a-zA-Z0-9]+)-(?P<subject>\d+)"},
        {
            "select": [
                {"pattern": "scans", "packfile_type": "dicom"},
                "stim",
                "associated",
                {"pattern": "Trash", "ignore": True},
            ]
        },
    ]

    result = importers.parse_template_list(tmpl)

    assert result
    assert result.template.pattern == group_pattern
    assert result.packfile_type is None

    result = result.next_node
    assert result
    assert result.template.pattern == project_pattern
    assert result.packfile_type is None

    result = result.next_node
    assert result
    assert result.template.pattern == r"(?P<session>[a-zA-Z0-9]+)-(?P<subject>\d+)"
    assert result.packfile_type is None

    result = result.next_node
    assert result

    assert isinstance(result, importers.CompositeNode)
    assert len(result.children) == 4

    child = result.children[0]
    assert child.template.pattern == "scans"
    assert child.packfile_type == "dicom"
    assert child.next_node == importers.TERMINAL_NODE

    child = result.children[1]
    assert child
    assert child.template.pattern == "stim"
    assert child.packfile_type is None
    assert not child.ignore

    child = result.children[2]
    assert child
    assert child.template.pattern == "associated"
    assert child.packfile_type is None
    assert not child.ignore

    child = result.children[3]
    assert child
    assert child.template.pattern == "Trash"
    assert child.packfile_type is None
    assert child.ignore
