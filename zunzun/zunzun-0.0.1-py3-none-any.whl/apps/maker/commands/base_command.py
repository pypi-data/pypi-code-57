from zunzun import Command, CommandException
from pathlib import Path


class FileExistsException(CommandException):
    pass


class BaseCommand(Command):
    def _create_file(self, module, name: str, extencion: str = "py"):
        if name.find(".") > -1:
            before, resource_name = name.rsplit(".", 1)
            resource_path = [] if before.find(".") == -1 else before.split(".")
        else:
            resource_path = []
            resource_name = name
        folder = str(Path(module.__file__).parent)
        for item in resource_path:
            folder = f"{folder}/{item}"
            path = Path(folder)
            if not path.is_dir():
                path.mkdir()
        resource_file = f"{folder}/{resource_name.lower()}.{extencion}"
        path = Path(resource_file)
        if path.is_file():
            raise FileExistsException(f'The file "{resource_file}", exists yet.')
        path.touch()
        return resource_file, resource_name, ".".join(resource_path)

    def _write_text(self, file, template, **kwargs):
        path = Path(file)
        path.write_text(template.format(**kwargs))

    def _append_text(self, file_name, template, **kwargs):
        file = Path(file_name)
        self._write_text(
            file_name, template, before=file.read_text().strip(), **kwargs,
        )

    def _import_init_module(self, file, name, class_name):
        self._append_text(
            file, self._init_template, name=name.lower(), class_name=class_name,
        )

    _init_template = """{before}
from .{name} import {class_name}  # noqa
"""
