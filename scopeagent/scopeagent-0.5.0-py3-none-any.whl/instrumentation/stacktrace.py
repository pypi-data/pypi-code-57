import inspect
import six


def get_stacktrace():
    if six.PY2:
        return {
            'frames': [
                {'file': filename, 'line': lineno, 'name': function}
                for _, filename, lineno, function, _, _ in inspect.stack()
            ]
        }
    return {
        'frames': [{'file': frame.filename, 'line': frame.lineno, 'name': frame.function} for frame in inspect.stack()]
    }
