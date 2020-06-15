from JsonDB import JsonDB

class Foo:
    def __init__(self):
        self.db = JsonDB("Foo.json", {"param1": [1,2,3,4], "param2": {"a": 1, "b": 2}})
        self.params = self.db.getJSON()

    def changeParam1(self, value):
        self.params["param1"] = value

    def changeParam2(self, value):
        self.params["param2"] = value

foo = Foo()

foo.changeParam1([1,2,3])
foo.changeParam2(14)

# Salva no arquivo as alterações nos JSONs
JsonDB.flushAll()