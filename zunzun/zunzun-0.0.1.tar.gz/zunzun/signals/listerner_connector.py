from zunzun.import_string import import_string
from injector import Injector, inject


class ListenerConnector:
    @inject
    def __init__(self, injector: Injector, *args, **kwargs):
        self.injector = injector

    def connect(self, signal_type, listener_type):
        signal, listener = self._get_signal_listener(signal_type, listener_type)
        args = self._get_args_connect(listener)
        signal.connect(listener, **args)

    def _get_signal_listener(self, signal_type, listener_type):
        if isinstance(signal_type, str):
            signal_type = import_string(signal_type)
        if isinstance(listener_type, str):
            listener_type = import_string(listener_type)
        signal = self._create_object(signal_type)
        listener = self._create_object(listener_type)
        return signal, listener

    def _get_args_connect(self, listener):
        if not hasattr(listener, "connect_args"):
            return dict()
        connect_args = getattr(listener, "connect_args")
        return connect_args()

    def _create_object(self, cls):
        return self.injector.get(cls)
