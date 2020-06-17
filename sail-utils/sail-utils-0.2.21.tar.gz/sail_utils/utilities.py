# -*- coding: utf-8 -*-
"""
package utilities module
"""

import shutil
from pathlib import Path
from ffmpy import FFmpeg


def _merge(start_epoch: int,
           end_epoch: int,
           merged_file: str,
           used_files: list):
    used_files = [Path(file) for file in used_files]
    file_list_name = Path(f"tmp/{start_epoch}_{end_epoch}.txt")
    if not file_list_name.exists():
        with open(file_list_name, 'w') as f_handle:
            for file in used_files:
                f_handle.write(f"file '{file.name}'\n")

    for file in used_files:
        file_name = file.name
        dst_file = Path('tmp') / file_name
        if not dst_file.exists():
            shutil.copy(file, dst_file)

    if not Path(merged_file).exists():
        ff_cmd = FFmpeg(global_options=['-f', 'concat'],
                        inputs={file_list_name.as_posix(): ['-safe', '0']},
                        outputs={merged_file: ['-c', 'copy']})
        ff_cmd.run()
