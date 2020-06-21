import requests
import tqdm
from pathlib import Path
import zipfile

from molnet.utils import md5
from molnet.molnet_config import molnet_config


def download(dataset, dest='/tmp'):
    task_config = molnet_config[dataset]
    fpath = Path(dest) / task_config.fname
    if not (fpath.is_file() and md5(fpath) == task_config.hash):
        r = requests.get(task_config.url, stream=True)
        total_size = int(r.headers.get('content-length', 0))
        block = 100  # 100KB
        with open(fpath, 'wb') as f:
            with tqdm.tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                for data in r.iter_content(block * 1024):
                    f.write(data)
                    pbar.update(len(data))
    else:
        print("Dataset file already downloaded.")
    if fpath.suffix == '.zip':
        if not (fpath.parent / fpath.stem).is_dir():
            with zipfile.ZipFile(fpath, 'r') as zip_ref:
                zip_ref.extractall(fpath.parent / fpath.stem)
        else:
            print("Dataset file already unzipped")
    return fpath


