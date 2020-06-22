from .Base import Base
from .JsonEnum import JsonEnum
from .utils import String
from .SchemaEntry import SchemaEntry
from .FileFormatSettings import FileFormatSettings
from collections import OrderedDict


class CsvQuoteStyle(JsonEnum):
    Csv = "QuoteStyle.Csv"
    None_ = "QuoteStyle.None"


class CsvStyle(JsonEnum):
    QuoteAlways = "CsvStyle.QuoteAlways"
    QuoteAfterDelimiter = "CsvStyle.QuoteAfterDelimiter"


class CsvFormatSettings(FileFormatSettings):
    def __init__(self, schema=[]):
        self.schema = schema + [
            SchemaEntry("columnHeaders", bool),
            SchemaEntry("delimiter", String),
            SchemaEntry("quoteStyle", CsvQuoteStyle),
            SchemaEntry("csvStyle", CsvStyle)
        ]
        super().__init__(self.schema)

    def toJson(self):
        result = OrderedDict()
        result["$type"] = "CsvFormatSettings"
        entity = super().toJson()
        for k, v in entity.items():
            result[k] = v
        return result
