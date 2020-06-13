import functools
import logging
import re

# Parser


class Token:
    re_element_tag = re.compile(r"^E\:\s([^\s]+)\s\(([^\)]+)\)")
    re_attribute = re.compile(r"^A:\s([^=]*)=([^$]+)")
    re_parentheses = re.compile(r"\([^)]*\)")

    def __init__(self, text):
        self._stripped = text.strip()
        self._bad = False

        if len(text) == 0:
            self._bad = True
        else:
            try:
                self._deep = len(text) - len(text.lstrip())
                self._type = self._stripped[0]
            except Exception as e:
                logging.warning(e)
                self._bad = True

    def as_element(self):
        g = Token.re_element_tag.match(self._stripped).groups()
        return g

    def as_attribute(self):
        g = Token.re_attribute.match(Token.remove_parentheses(self._stripped)).groups()
        return g

    @staticmethod
    def remove_parentheses(s):
        return Token.re_parentheses.sub("", s)

    def __str__(self):
        return "{}, {}, {}".format(self._deep, self._type, self._stripped)

    @property
    def type(self):
        return self._type

    @property
    def deep(self):
        return self._deep

    @property
    def raw(self):
        return self._stripped

    @property
    def bad(self):
        return self._bad


class ManifestAttribute:
    def __init__(self, element, token):
        self._element = element

        r = token.as_attribute()

        self._name = r[0].strip()
        self._value = r[1].strip()
        self._origin = token.raw

    def __str__(self):
        return "{}={}".format(self._name, self._value)

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value


class ManifestNamespace:
    def __init__(self, element, token):
        pass


class ManifestElement:
    def __init__(self, parent=None, token=None):

        self._namespaces: [ManifestNamespace] = []
        self._attributes: dict[str, ManifestAttribute] = {}
        self._elements: [ManifestElement] = []

        self._parent = parent

        if token is not None:
            e = token.as_element()
            self._name = e[0]
            self._at_line = e[1]
            self._deep = token.deep
            self._type = self._name
        else:
            self._name = '[ROOT]'
            self._type = '[ROOT]'
            self._deep = -1

    def __str__(self):
        intent = self._deep
        if intent < 0:
            intent = 0

        intent_str = " " * intent

        s = "{}<{}>".format(intent_str, self._name)

        for a in self._attributes:
            s += "\n{}[{}={}]".format(intent_str, str(a), str(self._attributes[a].value))

        for e in self._elements:
            s += "\n{}".format(str(e))

        return s

    def add_element(self, element):
        self._elements.append(element)

    def get_elements(self):
        return self._elements

    def add_attribute(self, attribute: ManifestAttribute):
        self._attributes[attribute.name] = attribute

    def get_attribute_value(self, key, default):
        r = self._attributes.get(key)
        if r is not None:
            return r.value
        else:
            return default

    def add_namespace(self, namespace):
        self._namespaces.append(namespace)

    @property
    def name(self):
        return self._name

    @property
    def deep(self):
        return self._deep


class Manifest(ManifestElement):

    def __init__(self, text):
        super().__init__()
        lines = text.split('\n')

        stack: [ManifestElement] = [self]

        for line in lines:
            token = Token(line)

            if token.bad:
                logging.debug("bad token {}".format(token.raw))
                continue

            if token.type == 'N':
                stack[-1].add_namespace(ManifestNamespace(stack[-1], token))
            elif token.type == 'E':
                element = ManifestElement(stack[-1], token)
                while stack[-1].deep >= element.deep:
                    stack.pop()
                stack[-1].add_element(element)
                stack.append(element)
            elif token.type == 'A':
                stack[-1].add_attribute(ManifestAttribute(stack[-1], token))
            else:
                logging.warning("unknown tag '{}'".format(token.raw))


# Wrappers
class Attribute:
    def __init__(self, name, default):
        self._name = name
        self._default = default

    def __call__(self, fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            data: ManifestElement = args[0].data
            return fn(args[0], data.get_attribute_value(self._name, self._default))

        return decorated


class Wrapper:
    def __init__(self, data: ManifestElement):
        self._data = data

    @property
    def data(self):
        return self._data

    @property
    @Attribute("android:name", "Unknown")
    def name(self, value):
        return value


class ManifestWrapper(Wrapper):

    def __init__(self, manifest: ManifestElement):

        for e in manifest.get_elements():
            if e.name == 'manifest':
                self._manifest = e

        if self._manifest is None:
            logging.error("no manifest tag")
            return

        super().__init__(self._manifest)

        self._use_features = []
        self._application = None

        for e in self.data.get_elements():
            if e.name == 'use_feature':
                self._use_features.append(UseFeature(e))
            elif e.name == 'application':
                if self._application is not None:
                    logging.warning("multi application in manifest")
                self._application = Application(e)

    @property
    def use_features(self):
        return self._use_features

    @property
    def application(self):
        return self._application


class UseFeature(Wrapper):
    def __init__(self, data: ManifestElement):
        super().__init__(data)


class Application(Wrapper):
    def __init__(self, data: ManifestElement):
        super().__init__(data)
        self._meta = []
        self._activities = []
        self._receivers = []
        self._services = []
        self._providers = []
        self._launchActivity = None

        for e in data.get_elements():
            if e.name == 'meta-data':
                self._meta.append(Meta(e))
            elif e.name == 'activity':
                activity = Activity(e)
                self._activities.append(activity)
                if activity.is_launch_activity:
                    if self._launchActivity is not None:
                        logging.warning("multi launchActivity {}", activity.name)
                    self._launchActivity = activity
            elif e.name == 'receiver':
                self._receivers.append(Receiver(e))
            elif e.name == 'service':
                self._services.append(Service(e))
            elif e.name == 'provider':
                self._providers.append(Provider(e))

    @property
    @Attribute("android:debuggable", 0x0)
    def debuggable(self, value):
        return not int(value, 16) == 0

    @property
    @Attribute("android:largeHeap", 0x0)
    def largeHeap(self, value):
        return not int(value, 16) == 0

    @property
    def activities(self):
        return self._activities

    @property
    def services(self):
        return self._services

    @property
    def metas(self):
        return self._meta

    @property
    def receivers(self):
        return self._receivers

    @property
    def providers(self):
        return self._providers


class Activity(Wrapper):
    def __init__(self, data: ManifestElement):
        super().__init__(data)

        self._intent_filter: IntentFilter = None
        self._meta: [Meta] = []

        for e in self.data.get_elements():
            if e.name == 'intent-filter':
                if self._intent_filter is not None:
                    logging.warning("multi intent-filter, activity: {}".format(self.name))
                self._intent_filter = IntentFilter(e)
            elif e.name == 'meta-data':
                self._meta.append(Meta(e))

    @property
    def is_launch_activity(self):
        return self._intent_filter is not None and self._intent_filter.is_launch

    @property
    @Attribute("android:name", "Unknown")
    def name(self, value):
        return value[1:-1]


class Service(Wrapper):
    def __init__(self, data: ManifestElement):
        super().__init__(data)

    @property
    @Attribute("android:name", "Unknown")
    def name(self, value):
        return value[1:-1]


class Receiver(Wrapper):
    def __init__(self, data: ManifestElement):
        super().__init__(data)

    @property
    @Attribute("android:name", "Unknown")
    def name(self, value):
        return value[1:-1]


class Provider(Wrapper):
    def __init__(self, data: ManifestElement):
        super().__init__(data)

    @property
    @Attribute("android:name", "Unknown")
    def name(self, value):
        return value[1:-1]


class Meta(Wrapper):
    def __init__(self, data: ManifestElement):
        super().__init__(data)

    @property
    @Attribute("android:name", None)
    def name(self, value):
        return value[1:-1]

    @property
    @Attribute("android:value", None)
    def value(self, value):
        return value


class IntentFilter(Wrapper):
    def __init__(self, data: ManifestElement):
        super().__init__(data)

        self._action: Action = None
        self._categories: [Category] = []

        for e in self.data.get_elements():
            if e.name == 'action':
                if self._action is not None:
                    logging.warning("multi action, activity: {}".format(self.name))
                self._action = Action(e)
            elif e.name == 'category':
                self._categories.append(Category(e))

    @property
    def is_launch(self):

        has_launch_cate = False

        for c in self._categories:
            if c.name == Category.LAUNCHER:
                has_launch_cate = True
                break

        return self._action.name == Action.MAIN and has_launch_cate


class Action(Wrapper):
    MAIN = "android.intent.action.MAIN"

    def __init__(self, data: ManifestElement):
        super().__init__(data)

    @property
    @Attribute("android:name", None)
    def name(self, value):
        return value

    @property
    @Attribute("android:name", "Unknown")
    def name(self, value):
        return value[1:-1]


class Category(Wrapper):
    LAUNCHER = "android.intent.category.LAUNCHER"

    def __init__(self, data: ManifestElement):
        super().__init__(data)

    @property
    @Attribute("android:name", None)
    def name(self, value):
        return value

    @property
    @Attribute("android:name", "Unknown")
    def name(self, value):
        return value[1:-1]
