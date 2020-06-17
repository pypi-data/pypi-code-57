"""atoti Types."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AtotiType:
    """atoti Type.

    Attributes:
        java_type: The name of the associated Java literal type.
        nullable: Whether the objects of this type can be ``None``.
            Elements within array types cannot be ``None`` and must share the same scalar type.
    """

    java_type: str
    nullable: bool


def local_date(java_format: str):
    """Create a date type with the given Java date format."""
    return AtotiType(f"LocalDate[{java_format}]", True)


def local_date_time(java_format: str):
    """Create a datetime type with the given Java datetime format."""
    return AtotiType(f"LocalDateTime[{java_format}]", True)


BOOLEAN = AtotiType("boolean", False)
STRING = AtotiType("string", True)
INT = AtotiType("int", False)
INT_NULLABLE = AtotiType("int", True)
INT_ARRAY = AtotiType("int[]", True)
LONG = AtotiType("long", False)
LONG_NULLABLE = AtotiType("long", True)
LONG_ARRAY = AtotiType("long[]", True)
FLOAT = AtotiType("float", False)
FLOAT_NULLABLE = AtotiType("float", True)
FLOAT_ARRAY = AtotiType("float[]", True)
DOUBLE = AtotiType("double", False)
DOUBLE_NULLABLE = AtotiType("double", True)
DOUBLE_ARRAY = AtotiType("double[]", True)
LOCAL_DATE = local_date("yyyy-MM-dd")
LOCAL_DATE_TIME = local_date_time("yyyy-MM-dd'T'HH:mm:ss")
DOUBLE_PYTHON_LIST = AtotiType("atoti_list_double[][,]", True)
LONG_PYTHON_LIST = AtotiType("atoti_list_long[][,]", True)
INT_PYTHON_LIST = AtotiType("atoti_list_int[][,]", True)
DOUBLE_NUMPY_ARRAY = AtotiType("atoti_numpy_double[][ ]", True)
LONG_NUMPY_ARRAY = AtotiType("atoti_numpy_long[][ ]", True)
INT_NUMPY_ARRAY = AtotiType("atoti_numpy_int[][ ]", True)
