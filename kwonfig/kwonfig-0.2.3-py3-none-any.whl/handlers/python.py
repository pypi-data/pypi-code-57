from . import Handler


class PythonHandler(Handler):
    suffix = 'py'

    @classmethod
    def load(cls, fp) -> Handler.Data:
        content = fp.read()

        data = {}
        exec(content, data)

        return data
