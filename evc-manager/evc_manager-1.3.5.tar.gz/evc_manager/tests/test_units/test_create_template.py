""" Test module for CurrentConfig Class """


import unittest
from ...libs.core.create_template_files import create_template


class TestCreateTemplatesAdd(unittest.TestCase):
    """ Test if the output of create_template is correct """

    def setUp(self):
        self.output = create_template("1.0", "add")

    def test_template_action_add_correct_version(self):
        """ check version """
        assert self.output["version"] == "1.0"

    def test_template_action_add_correct_action(self):
        """ check add action"""
        assert self.output["action"] == "add"

    def test_template_action_add_correct_evcs(self):
        """ check add correct evcs"""
        assert isinstance(self.output["evcs"], list)
        assert len(self.output["evcs"]) == 1

    def test_template_action_add_correct_evcs_each(self):
        """ check each evc """
        for evc in self.output["evcs"]:
            assert isinstance(evc, dict)
            assert "name" in evc
            assert evc["name"] == "evc_name"
            assert "unis" in evc
            assert isinstance(evc["unis"], list)
            assert len(evc["unis"]) == 2
            for uni in evc["unis"]:
                assert isinstance(uni, dict)
                assert "device" in uni
                assert "interface_name" in uni
                assert "tag" in uni
                assert "type" in uni["tag"]
                assert "value" in uni["tag"]
                assert uni["tag"]["type"] == "vlan"
                assert uni["tag"]["value"] == "vlan_id"


class TestCreateTemplatesAddRange(unittest.TestCase):
    """ Test if the output of create_template is correct """

    def setUp(self):
        self.output = create_template("1.0", "add_range")

    def test_template_action_add_range_correct_action(self):
        """ check add_range"""
        assert self.output["action"] == "add_range"

    def test_template_action_add_range_correct_evcs(self):
        """ check add_range evcs vlan range """
        for evc in self.output["evcs"]:
            for uni in evc["unis"]:
                assert isinstance(uni, dict)
                assert "tag" in uni
                assert "type" in uni["tag"]
                assert "value" in uni["tag"]
                assert uni["tag"]["type"] == "vlan"
                assert uni["tag"]["value"] == "[first_vlan_id, last_vlan_id]"


class TestCreateTemplatesDelete(unittest.TestCase):
    """ Test if the output of create_template is correct """

    def setUp(self):
        self.output = create_template("1.0", "delete")

    def test_template_action_add_range_correct_action(self):
        """ check add_range"""
        assert self.output["action"] == "delete"


class TestCreateTemplatesMove(unittest.TestCase):
    """ Test if the output of create_template is correct """

    def setUp(self):
        self.output = create_template("1.0", "move")

    def test_template_action_add_range_correct_action(self):
        """ check add_range"""
        assert self.output["action"] == "move"


class TestCreateTemplatesChange(unittest.TestCase):
    """ Test if the output of create_template is correct """

    def setUp(self):
        self.output = create_template("1.0", "change")

    def test_template_action_add_range_correct_action(self):
        """ check add_range"""
        assert self.output["action"] == "change"
