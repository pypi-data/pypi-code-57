# You're creating an ORM. Look at what's already there
# BaseModel
from typing import List, Union, Dict, Any
from pydantic import BaseModel

class Foo(BaseModel):
    data: Dict[str, Union[str, bool, int, float, Dict[str, Any]]] = {}
    size: float = None

    def field_keys(self) -> List[str]:
        return list(self.fields.keys())

    def create_query(self):
        print(self.field_keys())
        print("Hello World")


Foo().create_query()
