import click
from injector import singleton, inject
from zunzun import AppRegister
from zunzun.apps.maker.commands.base_command import BaseCommand


@singleton
class model_createCommand(BaseCommand):
    @inject
    def __init__(self, app_register: AppRegister):
        super().__init__("model_create")
        self.app_register = app_register
        self.add_argument("name")
        self.add_option(
            "--app", default="app", help='By default the principal app is named "app"'
        )
        self.add_option(
            "--create-repository",
            default=True,
            help="Create the repository of the model.",
        )

    def handle(self, name, app, create_repository):
        name = name.capitalize()
        app = self.app_register.get(app)
        model_dir = app.get_config("orm.model_dir", "model")
        repositories_dir = app.get_config("orm.repositories_dir", "repositories")
        model = app.get_or_create_module(model_dir)
        file, name, _ = self._create_file(model, name)
        self._write_text(file, self._template_model, name=name)
        self._import_init_module(model.__file__, name, name)
        click.echo(file)
        repositories = app.get_or_create_module(repositories_dir)
        file, name, _ = self._create_file(repositories, name)
        self._write_text(
            file,
            self._template_repository,
            name=name,
            model_path=app.get_module_name(model_dir),
        )
        self._import_init_module(repositories.__file__, name, name)
        click.echo(file)

    _template_model = """from zunzun import orm
from sqlalchemy import Column, Integer


class {name}(orm.BaseModel):
    __tablename__ = "{name}"
    id = Column(Integer, primary_key=True)
"""

    _template_repository = """from injector import singleton
from zunzun import orm
from {model_path} import {name}


@singleton
class {name}Repository(orm.BaseRepository):
    def new(self, **kwargs):
        return {name}(**kwargs)
"""
