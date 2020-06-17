__version__ = VERSION = (0, 2, 1)

import warnings

from django.db.models import options


# Django doesn't support adding third-party fields to model class Meta.
# So lets also allow them to safely exist on models even if app is missing
class SafeOptionalMetaMeta(type):

    def __new__(cls, name, bases, dct):
         for name in list(dct.keys()):
             if name.startswith('__'):
                 continue
             if name not in options.DEFAULT_NAMES:
                 warnings.warn('Discarding unsupported {}'.format(name),
                               stacklevel=2)
                 del dct[name]

         return super().__new__(cls, name, bases, dct)


class SafeOptionalMeta(metaclass=SafeOptionalMetaMeta):
      pass
