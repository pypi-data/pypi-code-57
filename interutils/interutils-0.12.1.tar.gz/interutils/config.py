import json
import typing
from pathlib import PosixPath
from .interactive import pr


class DictConfig(dict):
    def __init__(self, conf_path: PosixPath,
                 default_config: dict, quiet=False):
        super(DictConfig, self).__init__()
        self.conf_path = conf_path

        if data := self.load():
            self.update(data)
        else:
            if not quiet:
                pr('Recreated config!', '!')
            self.update(default_config)
            self.save()

    def load(self) -> (typing.Dict[str, str], bool):
        try:
            with self.conf_path.open() as f:
                return json.load(f)
        except FileNotFoundError:
            return False
        except json.JSONDecodeError:
            return False

    def save(self) -> None:
        with self.conf_path.open('w') as f:
            json.dump(self, f)
