from .JsonEnum import JsonEnum

class DataType(JsonEnum):
    Unclassified = "unclassified"
    String = "string"
    Int64 = "int64"
    Double = "double"
    DateTime = "dateTime"
    DateTimeOffset = "dateTimeOffset"
    Decimal = "decimal"
    Boolean = "boolean"
    Guid = "guid"
    Json = "json"