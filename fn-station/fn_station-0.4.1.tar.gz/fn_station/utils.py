import traceback


def format_exception(e):
    return "".join(traceback.format_exception_only(type(e), e)).rstrip()


def slugify(string):
    return string.lower().replace(" ", "_")


# This is apparently harder than it should be
# https://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
def row_to_dict(row):
    result = row.__dict__.copy()
    result.pop("_sa_instance_state")
    return result


def rows_to_dicts(rows):
    return [row_to_dict(row) for row in rows]
