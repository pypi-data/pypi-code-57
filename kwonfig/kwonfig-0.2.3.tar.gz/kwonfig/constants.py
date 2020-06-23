def is_supported(name: str, package=None) -> bool:
    import importlib

    module = None

    try:
        module = importlib.import_module(name, package)
    except ImportError:
        pass

    return module is not None


HJSON_SUPPORTED = is_supported('hsjon')
INI_SUPPORTED = is_supported('ini')
JSON5_SUPPORTED = is_supported('json5')
YAML_SUPPORTED = is_supported('.yaml', 'ruamel')
TOML_SUPPORTED = is_supported('qtoml')

PYDANTIC_SUPPORTED = is_supported('pydantic')
