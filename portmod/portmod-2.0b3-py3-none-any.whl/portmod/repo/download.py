# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from typing import AbstractSet, Dict, Iterable, List, Optional

import os
import urllib
import urllib.request
import urllib.error
import urllib.parse
import requests
import logging
from base64 import b64decode, b16encode
from progressbar import ProgressBar, Percentage, Bar, ETA, FileTransferSpeed

from portmod.repo.util import get_hash
from portmod.globals import env
from ..config import get_config
from ..pybuild import FullPybuild, Pybuild, Source, HashAlg, MD5
from ..repos import get_repo
from .metadata import get_license_groups, get_repo_root
from .usestr import use_reduce
from .use import get_use


class RemoteHashError(Exception):
    """Exception indicating an unexpected download file"""


class LocalHashError(Exception):
    """Exception indicating an unexpected download file"""


def parse_arrow(sourcelist: Iterable[str]) -> List[Source]:
    """
    Turns a list of urls using arrow notation into a list of
    Source objects
    """
    result: List[Source] = []
    arrow = False
    for value in sourcelist:
        if arrow:
            result[-1] = Source(result[-1].url, value)
            arrow = False
        elif value == "->":
            arrow = True
        else:
            url = urllib.parse.urlparse(value)
            result.append(Source(value, os.path.basename(url.path)))
    return result


def get_filename(basename: str) -> str:
    """
    Returns the location of the local cached version of the source file
    corresponding to the given name. The file may or may not exist.
    @return the cache location of the given source name
    """
    return os.path.join(env.DOWNLOAD_DIR, basename)


def mirrorable(mod: Pybuild, enabled_use: Optional[AbstractSet[str]] = None) -> bool:
    """
    Retuerns whether or not a mod can be mirrored
    """
    # FIXME: Determine which sources have use requirements
    # that don't enable mirror or fetch
    if "mirror" not in mod.RESTRICT and "fetch" not in mod.RESTRICT:
        redis: Iterable[str]
        if mod.INSTALLED:
            redis = get_license_groups(get_repo(mod.REPO).location).get(
                "REDISTRIBUTABLE", []
            )
        else:
            redis = get_license_groups(get_repo_root(mod.FILE)).get(
                "REDISTRIBUTABLE", []
            )

        def is_license_redis(group):
            if not group:
                # No license is considered equivalent to all-rights-reserved
                return False
            if isinstance(group, str):
                return group in redis
            if group[0] == "||":
                return any(is_license_redis(li) for li in group)

            return all(is_license_redis(li) for li in group)

        if enabled_use and is_license_redis(
            use_reduce(mod.LICENSE, enabled_use, opconvert=True)
        ):
            return True
        if not enabled_use and is_license_redis(
            use_reduce(mod.LICENSE, opconvert=True, matchall=True)
        ):
            return True

    return False


def fetchable(mod: FullPybuild) -> List[Source]:
    """
    Returns the list of fetchable sources associated with a mod
    A source can be fetched if it is mirrorable,
    or if it has a URI
    """
    if "fetch" in mod.RESTRICT:
        return []

    use, _ = get_use(mod)
    if "mirror" not in mod.RESTRICT and mirrorable(mod, use):
        return mod.get_default_sources()

    can_fetch = []
    for source in mod.get_default_sources():
        parsedurl = urllib.parse.urlparse(source.url)
        if parsedurl.scheme:
            can_fetch.append(source)

    return can_fetch


def download(
    url: str,
    dest_name: str,
    *,
    size: Optional[int] = None,
    hashes: Dict[HashAlg, str] = {},
):
    """
    Downloads the given url to the path specified by dest_name
    Raises exceptions as defined by urllib.request.urlretrieve
    """
    print("Fetching {}".format(url))

    os.makedirs(env.DOWNLOAD_DIR, exist_ok=True)

    req = requests.get(url, stream=True)
    req.raise_for_status()

    if "Content-Length" in req.headers:
        remote_size = int(req.headers["Content-Length"].strip())
    else:
        remote_size = None

    precheck = False
    if "X-Goog-Hash" in req.headers:
        remote_hashes = {
            remote_hash.split("=", maxsplit=1)[0]: remote_hash.split("=", maxsplit=1)[1]
            for remote_hash in req.headers["X-Goog-Hash"].split(", ")
        }
        if "md5" in remote_hashes and MD5 in hashes:
            value = remote_hashes["md5"]
            hexvalue = b16encode(b64decode(value)).decode("utf-8").lower()
            precheck = True
            if hashes[MD5] != hexvalue:
                raise RemoteHashError(
                    f"Local hash is {hashes[MD5]}, but remote hash is {hexvalue}!"
                )

    numbytes = 0
    bar = ProgressBar(
        widgets=[Percentage(), " ", Bar(), " ", ETA(), " ", FileTransferSpeed()],
        redirect_stdout=True,
        max_value=remote_size or size,
    ).start()
    with open(get_filename(dest_name), mode="wb") as file:
        for buf in req.iter_content(1024):
            if buf:
                file.write(buf)
                numbytes += len(buf)
                bar.update(numbytes)
    bar.finish()

    # Skip post check if we did a pre-check using a local hash
    if not precheck and "X-Goog-Hash" in req.headers and "md5" in remote_hashes:
        localhash = get_hash(get_filename(dest_name), (MD5.func,))[0]
        remotehash = b16encode(b64decode(remote_hashes["md5"])).decode("utf-8").lower()
        if localhash != remotehash:
            # Try again
            return download(url, dest_name, size=size, hashes=hashes)


def check_hash(filename: str, hashes: Dict[HashAlg, str], raise_ex=False) -> bool:
    """
    Returns true if and only if the sha512sum of the given file
    matches the given checksum
    """
    results = get_hash(filename, tuple([h.func for h in sorted(hashes)]))
    for halg, result in zip(sorted(hashes), results):
        if hashes[halg] != result:
            if raise_ex:
                raise LocalHashError(
                    f'{filename} should have {halg.name} of "{hashes[halg]}", '
                    f"but instead it is {result}"
                )
            return False
    return True


def get_download(name: str, hashes: Optional[Dict[HashAlg, str]]) -> Optional[str]:
    """
    Determines if the given file is in the cache.
    The file must match both name and checksum
    @return path to donloaded file
    """
    if os.path.exists(get_filename(name)) and (
        hashes is None or check_hash(get_filename(name), hashes)
    ):
        return get_filename(name)

    # If a file with spaces otherwise matches, remove the spaces
    if os.path.exists(env.DOWNLOAD_DIR):
        for file in os.listdir(env.DOWNLOAD_DIR):
            src = get_filename(file)
            if file.replace(" ", "_") == name:
                try:
                    if hashes is None or check_hash(src, hashes, raise_ex=True):
                        dest = get_filename(name)
                        os.rename(src, dest)
                        return dest
                except LocalHashError as e:
                    logging.warning(
                        f'Filename "{file}" matches source "{name}", '
                        f"but the hash doesn't match\n{e}"
                    )

    return None


def is_downloaded(mod: FullPybuild) -> bool:
    """
    Returns true if the mod's sources are all present in the cache
    """
    for source in mod.get_default_sources():
        cached = get_download(source.name, source.hashes)
        if cached is None:
            return False
    return True


def download_and_check(url: str, source: Source, *, try_again: bool = True) -> str:
    download(url, source.name, size=source.size, hashes=source.hashes)
    filename = get_filename(source.name)

    try:
        check_hash(filename, source.hashes, raise_ex=True)
    except LocalHashError as e:
        if try_again:  # Try again once if download fails
            logging.error(e)
            print(f"Retrying Download of {url}...")
            download_and_check(url, source, try_again=False)
        else:
            raise


def download_source(mod, source: Source, check: bool = True) -> str:
    """
    Downloads the given source file.
    @return the path to the downloaded source file
    """
    if check:
        cached = get_download(source.name, source.hashes)
    else:
        cached = get_download(source.name, None)
    fetch = "fetch" not in mod.get_restrict()
    mirror = (
        "mirror" not in mod.get_restrict()
        and "fetch" not in mod.get_restrict()
        and mirrorable(mod)
    )

    if cached:
        # Download is in cache. Nothing to do.
        return cached
    elif not fetch:
        # Mod cannot be fetched and is not already in cache. abort.
        raise Exception(
            f"Source {source} could not be found in the cache and cannot be fetched"
        )
    else:
        parsedurl = urllib.parse.urlparse(source.url)

        # Download archive
        filename = get_filename(source.name)

        if mirror:
            PORTMOD_MIRRORS = get_config()["PORTMOD_MIRRORS"].split()
            for mirror_url in PORTMOD_MIRRORS:
                try:
                    url = urllib.parse.urljoin(mirror_url, source.name)

                    if check:
                        download_and_check(url, source)
                    else:
                        download(
                            url, source.name, size=source.size, hashes=source.hashes
                        )

                    return filename
                except requests.exceptions.HTTPError as err:
                    if parsedurl.scheme:
                        logging.info(f"{err}")
                    else:  # If there is no original source, warn instead of info
                        logging.warning(f"{err}")

        if parsedurl.scheme != "":
            if check:
                download_and_check(source.url, source)
            else:
                download(
                    source.url, source.name, size=source.size, hashes=source.hashes
                )

            return filename

        raise Exception(
            f"Source {source} could not be found in the cache and cannot be fetched"
        )


def download_mod(mod: FullPybuild, matchall=False) -> List[Source]:
    """
    Downloads missing sources for the given mod in its current USE configuration
    @return A list of paths of the sources for the mod
    """
    download_list = []
    if matchall:
        sources = mod.get_sources(matchall=True)
    else:
        sources = mod.get_default_sources()

    for source in sources:
        download_source(mod, source)

        download_list.append(source)

    return download_list
