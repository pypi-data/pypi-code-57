#!/usr/bin/env python3

ROOT_COL_INDEX = ord('A')


def char_to_index(colchar):
  ind = ord(colchar.upper()) - ROOT_COL_INDEX + 1
  if ind < 1 or 26 < ind:
    raise TypeError("The character is an invalid column name")
  return ind


def lookup_number_of_colname(col_name):
  if not isinstance(col_name, str):
    raise TypeError("The name of a column must be a string")

  len_col_name = len(col_name)
  if len_col_name == 1:
    return char_to_index(col_name) - 1
  if len_col_name == 2:
    n_1 = char_to_index(col_name[0])
    n_2 = char_to_index(col_name[1])
    return n_1 * 26 + n_2 - 1
  if len_col_name == 3:
    n_1 = char_to_index(col_name[0])
    n_2 = char_to_index(col_name[1])
    n_3 = char_to_index(col_name[2])
    return n_1 * 26 * 26 + n_2 * 26 + n_3 - 1

  raise TypeError("The number exceeds the maximum columns")


def lookup_colname_by_number(col_index):
  if col_index < 0:
    raise TypeError("The number of a column must be not negative")

  if col_index < 26:
    return chr(ROOT_COL_INDEX + col_index)

  if col_index < 26 + 26*26:
    sum = col_index - 26
    n_1 = sum // 26
    n_2 = sum - (26*n_1)
    return chr(ROOT_COL_INDEX + n_1) + chr(ROOT_COL_INDEX + n_2)

  if col_index < 26 + 26*26 + 26*26*26:
    sum = col_index - (26 + 26*26)
    n_1 = sum // 26 // 26
    sum = sum - (26*26*n_1)
    n_2 = sum // 26
    n_3 = sum - (26*n_2)
    return chr(ROOT_COL_INDEX + n_1) + chr(ROOT_COL_INDEX + n_2) + chr(ROOT_COL_INDEX + n_3)

  # 26 + 26*26 + 26*26*26 ~ 18278
  raise TypeError("The number exceeds the maximum columns")


def lookup_fieldname_from_mappings(colname, mappings=dict()):
  if mappings is not None and colname in mappings:
    return mappings[colname]
  return colname


def pick_object_fields(obj, field_names=[]):
  if len(field_names) == 0:
    return obj
  return {k: v for k, v in obj.items() if k in field_names}
