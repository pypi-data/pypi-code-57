"""Fortran linter"""
import os
import argparse
from flinter.formatting import parse_format_line, init_format_rules


__all__ = ["fmt_analysis"]


def fmt_analysis(lines):
    """Start the linter of file FILENAME."""
    file_stats = dict()
    all_errors = dict()
    file_stats["modifs"] = 0
    file_stats["errors"] = 0
    file_stats["total_lines"] = 0

    format_rules = init_format_rules()
    for i, line in enumerate(lines, 1):

        if line.strip().startswith("!>"):  #  Doxygen pragma
            continue
        if line.strip().startswith("!!"):  #  Doxygen pragma
            continue
        if line.strip() == "":  # . Blank line
            continue

        file_stats["total_lines"] += 1
        line_stats, line_errors = parse_format_line(line, i, format_rules)
        file_stats["errors"] += line_stats["errors"]
        file_stats["modifs"] += line_stats["modifs"]
        for key in line_errors:
            if key in all_errors:
                all_errors[key] += line_errors[key]
            else:
                all_errors[key] = line_errors[key]
    rate = (float(file_stats["errors"]) / file_stats["total_lines"]) * 10
    rate = 10.0 - rate
    print(50 * "-")
    print("Your code has been rated %2.2f/10" % rate)
    print("\n\n")

    for key in all_errors:
        print(format_rules[key]["message"], len(all_errors[key]))
    # print(all_errors.keys())
    return rate
