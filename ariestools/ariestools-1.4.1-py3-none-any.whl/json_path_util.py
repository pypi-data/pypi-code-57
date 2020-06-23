import enum


class Separator(enum.Enum):
    DOT = "."
    STAR = "*"
    L_STR = "|"


class JsonPath(object):
    __ROOT = "$"
    __SQUARE_L = "["
    __SQUARE_R = "]"

    def __init__(self, json=None, separator=Separator.DOT):
        self.json = json
        self.separator = separator.value

    def path(self, path: str, json=None):
        if json is None:
            json = self.json

        if json is None:
            raise SyntaxError("not set json param")

        if not path.startswith(self.__ROOT):
            raise SyntaxError("path: %s must start with '$'" % path)

        if path.count(self.__ROOT) != 1:
            raise SyntaxError("path: %s must contains one '$'" % path)

        for i in path.split(self.separator):
            if self.__ROOT in i:
                continue

            if self.__SQUARE_L in i:
                try:
                    json = self.__get(json, i.split(self.__SQUARE_L)[0])[
                        int(i[i.index(self.__SQUARE_L) + 1: i.index(self.__SQUARE_R)])]
                    continue
                except IndexError:
                    raise IndexError("list: %s index out of range, length: %d, index: %d" % (
                        self.__get(json, i.split(self.__SQUARE_L)[0]),
                        i.split(self.__SQUARE_L)[0].__len__(),
                        int(i[i.index(self.__SQUARE_L) + 1: i.index(self.__SQUARE_R)])))
                except Exception as e:
                    raise Exception(e)

            json = self.__get(json, i)

        return json

    @staticmethod
    def __get(json, key: str):
        if isinstance(json, dict):
            if key not in json.keys():
                raise Exception("json: %s have not key: %s" % (json, key))
            return json.get(key)

        if isinstance(json, list):
            return json

        raise Exception("Can't find key: %s in primary value: %s" % (key, json))


if __name__ == '__main__':
    _json_dict = {'k': 'v'}
    _jp1 = JsonPath(_json_dict)
    print(_jp1.path("$.k"))

    _json_list = [{'k': 'v'}]
    _jp2 = JsonPath(_json_list)
    print(_jp2.path("$.[0].k"))

    _json_complex = {'k': [{'k': 'v'}]}
    _jp3 = JsonPath(_json_complex)

    print(_jp3.path("$.k.[0].k"))
