import json


class PubsubMessage:

    def __init__(self, message_as_string):
        self.__message_as_string = message_as_string
        self.__load_as_json()

    def get_data(self):
        return self.__data

    def __str__(self):
        return self.__message_as_string

    def is_json(self):
        return self.__data is not None

    def has_key(self, key):
        return isinstance(self.__data, dict) and self.__data.has_key(key)

    def get(self, key, default=None):
        if not isinstance(self.__data, dict):
            return None

        if key in self.__data:
            return self.__data[key]
        else:
            return default

    def __getitem__(self, key):
        return isinstance(self.__data, dict) and self.__data[key]

    def __len__(self):
        if isinstance(self.__data, dict):
            return len(self.__data)
        else:
            return None

    def __load_as_json(self):
        try:
            self.__data = json.loads(self.__message_as_string)
        except:
            self.__data = None
