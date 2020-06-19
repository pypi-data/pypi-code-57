from looqbox.objects.looq_object import LooqObject
import json
from collections import OrderedDict

class ObjQuery(LooqObject):

    def __init__(self, query):
        super().__init__()
        self.query = query

    @property
    def to_json_structure(self):

        json_content = OrderedDict(
            {
                "objectType": "query",
                "query": self.query
            }
        )

        # Transforming in JSON
        list_json = json.dumps(json_content, indent=1)

        return list_json
