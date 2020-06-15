"""Test runner"""
from scruf import compare


def run_test(test, exec_result):
    """run a test against a result

    Parameters
    ----------
    test : scruf.test.Test
    exec_result : scruf.execute.Result

    Returns
    -------
    list of dict
        a list of the test result for each test line. Each dict contains keys:
            "result_line": str
                The line from the `exec_result` that was compared
            "result_source": str
                The source of the `"result_line"`, one of "stdout" or "stderr"
            "test_line": str
                The line from the `test` that was compared
            "comparison_result": bool
            "comparison_type": scruf.compare.ComparisonTypes
                The type of comparison made

    Raises
    ------
    scruf.compare.RegexError
        If the test contains a regex comparison with an invalid regex
    scruf.execute.OutOfLinesError
        If there are more lines in the test than the `exec_result`
    """
    summary = []

    for line in test.result_lines:
        comparison_details = compare.get_comparison_details(line)

        comparison_type = comparison_details["type"]
        comparison_content = comparison_details["content"]
        comparison_source = comparison_details["source"]

        result_content = _get_result_content(
            exec_result, comparison_type, comparison_source
        )
        comparison = compare.get_comparer(comparison_type)(
            comparison_content, result_content
        )
        summary.append(
            {
                "result_line": result_content,
                "result_source": comparison_source,
                "test_line": comparison_content,
                "comparison_result": comparison,
                "comparison_type": comparison_type,
            }
        )
    return summary


def get_printable_failures(comparison):
    """Get a printable representation of a failed comparison

    Parameters
    ----------
    comparison : dict
        As returned `run_test`

    Returns
    -------
    str
    """

    comparison_type = comparison["comparison_type"]

    return {
        compare.ComparisonTypes.BASIC: _basic_comparison_failure_lines,
        compare.ComparisonTypes.ESCAPE: _basic_comparison_failure_lines,
        compare.ComparisonTypes.NO_EOL: _no_eol_comparison_failure_lines,
        compare.ComparisonTypes.REGEX: _regex_comparison_failure_lines,
        compare.ComparisonTypes.RETURNCODE: _returncode_comparison_failure_lines,
    }[comparison_type](comparison["test_line"], comparison["result_line"])


def _format_content(content):
    formatted_content = repr(content)

    if content[-1] != "\n":
        formatted_content += " (no eol)"
    return formatted_content


def _basic_comparison_failure_lines(comparison_content, result_content):
    return [
        "got: " + _format_content(result_content),
        "expected: " + _format_content(comparison_content),
    ]


def _no_eol_comparison_failure_lines(comparison_content, result_content):
    return _basic_comparison_failure_lines(
        comparison_content.rstrip("\r\n"), result_content
    )


def _regex_comparison_failure_lines(comparison_content, result_content):
    return [
        "got: " + _format_content(result_content),
        "Does not match: '{}'".format(comparison_content),
    ]


def _returncode_comparison_failure_lines(expected_returncode, got_returncode):
    return [
        "got return code: {} != {}".format(
            str(got_returncode), str(expected_returncode)
        )
    ]


def _get_result_content(result, comparison_type, source):
    if comparison_type == compare.ComparisonTypes.RETURNCODE:
        return result.returncode
    else:
        return result.next_line(source)
