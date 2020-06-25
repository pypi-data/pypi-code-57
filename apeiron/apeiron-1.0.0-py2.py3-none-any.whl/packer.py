from pathlib import Path
from typing import Iterable
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

import click

from apeiron.config import cfg


def pack(base_path: Path, content: Iterable[Path], out_path: Path):
    mode = ZIP_DEFLATED
    with ZipFile(out_path, 'w', mode) as zf:  # the only place where os.PathLike is supported -_-
        for path in sorted(content):
            assert path.is_file()
            arc_path = path.relative_to(base_path).as_posix()  # the ZipInfo constructor can't do os.PathLike
            data = path.read_bytes()
            info = ZipInfo(arc_path)  # mtime is "0 since epoch" by default
            zf.writestr(info, data, mode)  # can't just write() since it fetches mtime from the disk
            if cfg.debug:
                click.echo(click.style(f"Packed: {out_path.as_posix()} ← {path.as_posix()}", dim=True))
