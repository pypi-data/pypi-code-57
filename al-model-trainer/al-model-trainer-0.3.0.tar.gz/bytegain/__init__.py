__path__ = __import__('pkgutil').extend_path(__path__, __name__)

try:
    # This is tricky! We want to pick up the version from python-common when bytegain package is also present.
    from .__version__ import __version__
except ImportError:
    pass
