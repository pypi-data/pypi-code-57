from pathlib import Path
from typing import Dict

from jinja2 import Template

from forge_template.util.file_util import read_file, write_file


def render(content: Dict[str, str], template_path: Path, output_path: Path):
    template = Template(read_file(template_path))
    rendered = template.render(**content)
    write_file(output_path, rendered)
