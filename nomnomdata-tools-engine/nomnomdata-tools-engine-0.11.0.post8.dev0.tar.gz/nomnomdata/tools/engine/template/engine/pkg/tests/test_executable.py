from ..executable import an_action


def test_an_action():
    an_action({"integer_parameters": 1, "string_parameters": "some_string"})
