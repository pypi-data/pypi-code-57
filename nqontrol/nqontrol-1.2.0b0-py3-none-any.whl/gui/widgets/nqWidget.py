from abc import ABCMeta, abstractmethod


class NQWidget:
    """Abstract class of UI components. In order to organize the Dash system and make features more modular, object structures are used for complex subsections of the interface. Callback functions and all user interaction to the backend are defined in the :obj:`controller` module. Callbacks are performed by the app (which is a Flask server that gets passed to gunicorn).
    Components also implement two default class functions/properties: `layout`, which returns the HTML layout in Dash syntax (sometimes, the layout has to be handled as part of initialization, when the layout needs more syntactic functionality), and `setCallbacks()``, which initializes all callbacks in startup. Dash usually requires the layout to be defined before the callbacks, as such, all calls to layout have to be made first. The `nqontrolUI` class starts a chain of calls to `setCallbacks()`, the majority of which are set in the `UIDevice` class.

    """

    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def layout(self):
        pass

    @abstractmethod
    def setCallbacks(self):
        pass
