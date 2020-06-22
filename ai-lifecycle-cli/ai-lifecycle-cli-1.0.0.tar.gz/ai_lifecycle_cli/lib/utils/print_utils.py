#  © Copyright IBM Corporation 2020.

import time
import datetime
import string
import textwrap


def print_resource_lists(tables, table_headers, values):
    """
    Print out series of tables with listed rows (for now can handle exactly two columns)

    :param tables: list of tables names
    :param table_headers: list of column names (same for each table)
    :param values: dict with keys equal to items in 'tables' variable, and values equal to rows
    :return: printed out series of tables on stdout
    """
    for table in tables:
        if len(values.get(table, [])) > 0:
            table_name = string.capwords(table.replace("wml", "").replace("_", " "))
            print("#" * 20 + "\n" + "#" * 3 + " {}".format(table_name) + "\n" + "#" * 20 + "\n")
            print(" {:40}".format(table_headers[0]) + "|" + " {:56}".format(table_headers[1]))
            print("-" * 99)

            for value in values.get(table, []):
                printable_id = value[table_headers[0].lower()]
                printable_name = textwrap.shorten(value[table_headers[1].lower()], width=52, placeholder="...")
                print(" {:40}".format(printable_id) + "|" + " {:56}".format(printable_name))
            print("\n")