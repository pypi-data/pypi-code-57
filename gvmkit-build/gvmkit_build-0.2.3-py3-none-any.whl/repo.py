from typing_extensions import Final
import requests
import io
from alive_progress import alive_bar
import hashlib


_DEFAULT_REPO_URL: Final = "http://34.244.4.185:8000"


def upload_image(file_obj: io.FileIO, file_name: str):

    file_size = file_obj.seek(0, io.SEEK_END)
    hasher = hashlib.sha3_224()
    assert file_obj.seek(0, io.SEEK_SET) == 0

    def chunks(bar, chunk_size=1024 * 1024):
        chunk = file_obj.read(chunk_size)
        while chunk:
            hasher.update(chunk)
            yield chunk
            bar(incr=len(chunk))
            chunk = file_obj.read(chunk_size)

    with alive_bar(file_size, title="upload image") as bar:
        resp = requests.put(f"{_DEFAULT_REPO_URL}/upload/{file_name}", data=chunks(bar))
        image_url = f"{_DEFAULT_REPO_URL}/{file_name}"
        hash_hex = hasher.hexdigest()
        requests.put(
            f"{_DEFAULT_REPO_URL}/upload/image.{hash_hex}.link",
            data=image_url.encode("utf-8"),
        )
    print(f"success. hash link {hash_hex}")
