import logging
from jinja2 import Environment, PackageLoader, select_autoescape

from .config import ConfigField

class Generator:
    def __init__(self, manifest):
        self.__config = manifest.defaults()
        self.__fields = manifest.fields()
        self.__fields.append(ConfigField('name', 'Project name'))

    def init(self, name=None):
        logging.info('Initializing project...')
        if name is not None:
            self.__config.update({'name': name})
        self.__config_prompt()

    def generate(self, module):
        logging.info('Generating project...')
        env = Environment(
            loader=PackageLoader(module)
        )
        for template_name in env.list_templates():
            template = env.get_template(template_name)
            with open(template_name.replace('.jinja',''), 'w') as f:
                f.write(template.render(self.__config))

    def __config_prompt(self):
        logging.debug('Prompt empty config...')
        for field in self.__fields:
            if field.name not in self.__config:
                self.__config[field.name] = input(f'{field.prompt}: ')
