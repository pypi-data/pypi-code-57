import os

from configurations import Configuration, values

def getlist(path):
    return list(filter(
        None,map(lambda s:s.strip(),open(path).read().splitlines() if path else [])
    ))

class TemplatesConfiguration(Configuration):
    BASE_DIR = os.getcwd()
    TEMPLATES_BACKEND = values.Value('django.template.backends.django.DjangoTemplates')
    TEMPLATES_DIRS = values.ListValue([])
    TEMPLATES_APP_DIRS = values.BooleanValue(True)
    TEMPLATES_OPTIONS = {}
    TEMPLATES_CONTEXT_PROCESSORS = values.ListValue([])
    TEMPLATES_CONTEXT_PROCESSORS_FILE = values.Value(None)
    TEMPLATES_LOADERS = values.ListValue([])

    @classmethod
    def setup(cls):
        super(TemplatesConfiguration, cls).setup()
        path = os.path.join(cls.BASE_DIR,"templates")
        if not cls.TEMPLATES_DIRS and os.path.exists(path):
            cls.TEMPLATES_DIRS = [path]
        cls.TEMPLATES_CONTEXT_PROCESSORS = getlist(cls.TEMPLATES_CONTEXT_PROCESSORS_FILE)
        if not cls.TEMPLATES_OPTIONS:
            cls.TEMPLATES_OPTIONS = {
                'context_processors': cls.TEMPLATES_CONTEXT_PROCESSORS
            }
            if cls.TEMPLATES_LOADERS:
                cls.TEMPLATES_OPTIONS['loaders'] = cls.TEMPLATES_LOADERS
        if cls.TEMPLATES_LOADERS:
            cls.TEMPLATES_APP_DIRS = False
        if not hasattr(cls,'TEMPLATES') or not cls.TEMPLATES:
            cls.TEMPLATES = [{}]
        if 'BACKEND' not in cls.TEMPLATES[0]:
            cls.TEMPLATES[0]['BACKEND'] = cls.TEMPLATES_BACKEND
        if 'DIRS' not in cls.TEMPLATES[0]:
            cls.TEMPLATES[0]['DIRS'] = cls.TEMPLATES_DIRS
        if 'APP_DIRS' not in cls.TEMPLATES[0]:
            cls.TEMPLATES[0]['APP_DIRS'] = cls.TEMPLATES_APP_DIRS
        if 'OPTIONS' not in cls.TEMPLATES[0]:
            cls.TEMPLATES[0]['OPTIONS'] = cls.TEMPLATES_OPTIONS
        if cls.TEMPLATES_CONTEXT_PROCESSORS and 'context_processors' not in cls.TEMPLATES[0]['OPTIONS']:
            cls.TEMPLATES[0]['OPTIONS']['context_processors'] = cls.TEMPLATES_CONTEXT_PROCESSORS
        if cls.TEMPLATES_LOADERS and 'loaders' not in cls.TEMPLATES[0]['OPTIONS']:
            cls.TEMPLATES[0]['OPTIONS']['loaders'] = cls.TEMPLATES_LOADERS

