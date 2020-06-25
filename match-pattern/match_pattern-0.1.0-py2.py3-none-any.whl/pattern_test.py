import os
import pytest
from match_pattern.pattern import Pattern


def test_match_regex():
    pattern = r"re::.*abcde.*"
    assert Pattern.test(pattern, "____abcde___"), "Invalid positive match on regex pattern"
    assert not Pattern.test(pattern, "____abcd___"), "Invalid negative match on regex pattern"


def test_match_wildcard():
    pattern = r"*abcde*"
    assert Pattern.test(pattern, "____abcde___"), "Invalid positive match on regex pattern"
    assert not Pattern.test(pattern, "____abcd___"), "Invalid negative match on regex pattern"


def test_pattern_str():
    ptrn = Pattern(["ab*", r"re::cb.d"])
    assert str(ptrn) == "re::" + r"^ab.*$|cb.d"


def test_multi_pattern():
    ptrn = Pattern(["ab*", r"re::cb.d"])
    assert ptrn.test("abcd"), "Invalid positive match pattern 1"
    assert ptrn.test("cbkd"), "Invalid positive match pattern 2"
    assert not ptrn.test("cbkkd"), "Invalid negative match pattern 2"


def test_multi_glob_pattern():
    ptrn = Pattern("ab*|cb?d")
    assert ptrn.test("abcd"), "Invalid positive match pattern 1"
    assert ptrn.test("cbkd"), "Invalid positive match pattern 2"
    assert not ptrn.test("cbkkd"), "Invalid negative match pattern 2"


def test_multi_glob_with_pattern_object():
    ptrn = Pattern(["ab*|cbke", Pattern(r"re::cb.d")])
    assert ptrn.test("abcd"), "Invalid positive match pattern 1"
    assert ptrn.test("cbkd"), "Invalid positive match pattern 2"
    assert ptrn.test("cbke"), "Invalid positive match pattern 3"
    assert not ptrn.test("cbkkd"), "Invalid negative match pattern 2"


def test_pattern_replace_glob():
    assert Pattern.replace("ab", "cd", "abcd") == "cdcd"


def test_pattern_replace():
    assert Pattern("re::(lama)").replace("kka", "the lama of nothing") == "the kka of nothing"


def test_pattern_format():
    assert Pattern.format("the {{SOME_VALUE}} is true", SOME_VALUE="lama") == "the lama is true"
    assert (
        Pattern.format(
            "the [[SOME_VALUE}] is true", custom_start_pattern="[[", custom_end_pattern="}]", SOME_VALUE="lama",
        )
        == "the lama is true"
    )


def test_pattern_format_default():
    to_format = "{{msg}}"
    assert Pattern.format(to_format, msg="ok") == "ok"


def test_pattern_format_custom():
    to_format = "{{msg}}"
    assert Pattern.format(to_format, msg="ok") == "ok"
    to_format = "[[msg]]"
    assert Pattern.format(to_format, custom_start_pattern="[[", custom_end_pattern="]]", msg="ok") == "ok"


def test_pattern_scan_path():
    pattern = Pattern("*_test.py")
    src_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    assert os.path.join(src_path, "match_pattern", "pattern_test.py") in pattern.scan_path(src_path)


if __name__ == "__main__":
    pytest.main(["-x", __file__])
