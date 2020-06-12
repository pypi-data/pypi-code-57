from flask import jsonify


class Json:
    def to_json(self):
        return jsonify(self.__dict__)


class SuccessMessage(Json):
    def __init__(self, message, **kwargs):
        self.ok = True
        self.message = message
        for key in kwargs:
            self.__dict__[key] = kwargs[key]


class ErrorMessage(Json):
    def __init__(self, message):
        self.ok = False
        self.message = message
