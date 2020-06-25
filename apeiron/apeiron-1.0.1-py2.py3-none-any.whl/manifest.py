import json
import uuid
from functools import partial
from hashlib import sha1
from itertools import chain, filterfalse, tee, groupby
from multiprocessing import Pool
from multiprocessing import cpu_count
from pathlib import Path
from shutil import copy
from shutil import rmtree
from tempfile import NamedTemporaryFile
from typing import Optional, Dict, Union, List, Any, Iterable, Tuple

import click
import yaml
from pydantic import ValidationError

from apeiron import constants as c
from apeiron import models as m
from apeiron.config import cfg
from apeiron.exceptions import ManifestError
from apeiron.packer import pack


SplittedFiles = Tuple[List[Path], Dict[str, List[Path]]]


def validate_manifest_fs(package_id: str, manifest: m.RichManifest) -> bool:
    consistent = manifest.name == package_id
    if not consistent:
        click.echo(click.style(
            f"Inconsistent {manifest.__class__.__name__}! "
            f"Internal id equals «{manifest.name}», but resides in «{package_id}»!",
            fg='red',
            bold=True
        ))
    return consistent


def load_target_manifest(package_id: str) -> Optional[m.TargetManifest]:
    path: Path = Path(cfg.packages_dir) / package_id / c.TARGET_MANIFEST_INDEX

    if not path.exists():
        return None

    try:
        manifest = m.TargetManifest(**json.load(path.open()))
    except ValidationError as e:
        click.echo(click.style(f"Broken TargetManifest, id: «{package_id}». Reason: {str(e)}", fg='red'))
        return None
    else:
        return validate_manifest_fs(package_id, manifest) and manifest or None


def _validate_task(path: Path, task: m.Task) -> bool:
    return (path / task.location).exists()


def validate_target_manifest(manifest: m.TargetManifest) -> bool:
    path: Path = Path(cfg.packages_dir) / manifest.name / manifest.objectsLocation

    if not path.exists():
        return False

    with Pool(processes=cfg.parallelism or cpu_count()) as pool:
        return all(pool.imap_unordered(partial(_validate_task, path), manifest.tasks))


def delete_target_manifest(manifest: m.TargetManifest):
    path: Path = Path(cfg.packages_dir) / manifest.name
    rmtree(path.as_posix())


def load_source_manifest(package_id: str) -> Optional[m.SourceManifest]:
    path: Path = Path(cfg.sources_dir) / package_id / c.SOURCE_MANIFEST_INDEX

    if not path.exists():
        return None

    try:
        manifest = m.SourceManifest(**yaml.load(path.open(), Loader=yaml.SafeLoader))
    except ValidationError as e:
        click.echo(click.style(f"Broken SourceManifest, id: «{package_id}». Reason: {str(e)}", fg='red'))
        return None
    else:
        return validate_manifest_fs(package_id, manifest) and manifest or None


def delete_source_manifest(manifest: m.SourceManifest):
    path: Path = Path(cfg.sources_dir) / manifest.name
    rmtree(path.as_posix())


def _get_base_data(destination: str, path: Path) -> Dict[str, Union[str, int]]:
    with path.open(mode='rb') as file:
        data: bytes = file.read()
        digest: str = sha1(data).hexdigest()
        return dict(
            hash=digest,
            location="{}/{}/{}".format(digest[0:2], digest[2:4], digest),
            to=destination,
            size=len(data)
        )


def _generate_task(
    user_files: m.PatternTestable,
    features: Dict[str, m.PatternTestable],
    base_dir: Path,
    path: Path,
) -> m.TargetTask:
    destination: str = path.relative_to(base_dir).as_posix()
    base_data = _get_base_data(destination, path)
    affected_features: List[str] = [
        name
        for name, feature_pattern
        in features.items()
        if destination in feature_pattern
    ]

    if affected_features:
        return m.FeatureTask(
            when={"if": "requireAny", "features": affected_features},
            **base_data
        )
    elif destination in user_files:
        return m.UserFileTask(**base_data)
    else:
        return m.Task(**base_data)


def _generate_bundle_task(
    features: Dict[str, m.PatternTestable],
    base_dir: Path,
    bundle_pair: Tuple[str, List[Path]]
) -> m.TargetTask:
    bundle_dir, bundle_content = bundle_pair
    archive_base_dir = base_dir / bundle_dir

    with NamedTemporaryFile(suffix=".zip") as temp_archive:
        archive_path = Path(temp_archive.name)
        pack(archive_base_dir, bundle_content, archive_path)
        destination: str = Path(bundle_dir).with_suffix(".zip").as_posix()
        base_data = _get_base_data(destination, archive_path)

    affected_features: List[str] = [
        name
        for name, feature_pattern
        in features.items()
        if destination in feature_pattern
    ]

    if affected_features:
        return m.FeatureTask(
            when={"if": "requireAny", "features": affected_features},
            bundle=bundle_dir,
            **base_data
        )
    return m.Task(bundle=bundle_dir, **base_data)


def partition(pred, iterable):
    t1, t2 = tee(iterable)
    return filterfalse(pred, t1), filter(pred, t2)


def _fnmatch_pattern_from_dir(dir_name: str) -> str:
    return f"{dir_name}/**"


def _is_in_bundle(compressed_pattern: m.PatternTestable, base_dir: Path, path: Path) -> bool:
    destination: str = path.relative_to(base_dir).as_posix()
    return destination in compressed_pattern


def _bundle_grouper(bundles_patterns: Dict[str, m.PatternTestable], base_dir: Path, path: Path) -> str:
    return [bundle for bundle, pattern in bundles_patterns.items() if _is_in_bundle(pattern, base_dir, path)][0]


def group_bundles(bundles_content: Iterable[Path], bundles: List[str], base_path: Path):
    bundles_patterns = {bundle_path: m.PatternTestable([_fnmatch_pattern_from_dir(bundle_path)]) for bundle_path in bundles}
    groups = groupby(bundles_content, partial(_bundle_grouper, bundles_patterns, base_path))
    return {bundle: list(paths) for bundle, paths in groups}


def build_target_manifest(source: m.SourceManifest) -> m.TargetManifest:
    user_files: m.PatternTestable = m.PatternTestable(source.userFiles.include)
    path: Path = Path(cfg.sources_dir) / source.name / source.objectsLocation

    features: Dict[str, m.PatternTestable] = {
        f.properties.name: m.PatternTestable(f.files.include)
        for f
        in source.features
    }
    bundle_pattern: m.PatternTestable = m.PatternTestable(map(_fnmatch_pattern_from_dir, source.bundles))
    bundle_splitter = partial(_is_in_bundle, bundle_pattern, path)

    raw_files: List[Path] = [path for path in path.glob('**/*') if path.is_file()]
    plain_files, all_bundle_files = partition(bundle_splitter, raw_files)
    bundle_files: Dict[str, List[Path]] = group_bundles(all_bundle_files, source.bundles, path)
    target_features: List[m.FeatureProperties] = [f.properties for f in source.features]
    common_values: Dict[str, Any] = source.dict(include=m.RichManifest.construct().fields)

    plain_processor = partial(_generate_task, user_files, features, path)
    bundle_processor = partial(_generate_bundle_task, features, path)

    with Pool(processes=cfg.parallelism or cpu_count()) as pool:
        plain_tasks: Iterable[m.TargetTask] = pool.map(plain_processor, plain_files)
        bundle_tasks: Iterable[m.TargetTask] = pool.map(bundle_processor, bundle_files.items())

    tasks: List[m.TargetTask] = list(chain(plain_tasks, bundle_tasks))
    return m.TargetManifest(features=target_features, tasks=tasks, **common_values)


def cleanup_target_location(manifest_name: str, objects_dir: str, strict: bool):
    base_path: Path = Path(cfg.packages_dir) / manifest_name

    if strict and base_path.exists():
        raise ManifestError(f"Base path {base_path} for modpack {manifest_name} already exists!")

    try:
        rmtree(base_path.as_posix())
    except FileNotFoundError as e:
        click.echo(click.style(f"Target {base_path.as_posix()} doesn't exist, suppressing…", fg="yellow", bold=True))
    except IOError as e:
        raise ManifestError(f"Can't clean target dir: {str(e)}") from e
    else:
        click.echo(f"Removed {click.style(base_path.as_posix(), bold=True)} (due to disabled strict mode)")

    try:
        base_path.mkdir()
        (base_path / objects_dir).mkdir()
    except IOError as e:
        raise ManifestError(f"Can't create target directory: {str(e)}") from e
    else:
        click.echo(f"Created empty directory: {click.style(base_path.as_posix(), bold=True)}")


def save_target_manifest(manifest: m.TargetManifest):
    base_path: Path = Path(cfg.packages_dir) / manifest.name
    index_path: Path = base_path / c.TARGET_MANIFEST_INDEX

    try:
        json.dump(manifest.dict(), index_path.open("w", encoding="utf-8"), indent=2, ensure_ascii=False)
    except (IOError, ValueError, TypeError, json.decoder.JSONDecodeError) as e:
        raise ManifestError(f"Can't write target index: {str(e)}") from e
    else:
        click.echo(f"Wrote target index at: {click.style(index_path.as_posix(), bold=True)}")


def _save_target_task(
    source_base_path: Path,
    target_base_path: Path,
    task: Union[m.Task, m.UserFileTask, m.FeatureTask]
) -> bool:

    target: Path = target_base_path / task.location
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        if task.bundle is not None:
            archive_dir = source_base_path / task.bundle
            archive_content = [path for path in archive_dir.glob('**/*') if path.is_file()]
            pack(archive_dir, archive_content, target)
        else:
            copy(
                (source_base_path / task.to).as_posix(),
                (target_base_path / task.location).as_posix()
            )
    except IOError:
        return False
    else:
        return True
    finally:
        if cfg.debug:
            click.echo(click.style(f"Copying: {task.location} ← {task.to}", dim=True))


def save_target_content(source_manifest: m.SourceManifest, target_manifest: m.TargetManifest):
    source_path: Path = Path(cfg.sources_dir) / source_manifest.name / source_manifest.objectsLocation
    target_path: Path = Path(cfg.packages_dir) / target_manifest.name / target_manifest.objectsLocation

    with Pool(processes=cfg.parallelism or cpu_count()) as pool:
        tasks: Iterable[bool] = pool.map(
            partial(_save_target_task, source_path, target_path),
            target_manifest.tasks
        )
        result = all(tasks)

    if result:
        click.echo(click.style(f"Deployed {len(target_manifest.tasks)} files"))
    else:
        raise ManifestError("Error happened while copying target files")


def get_manifest_index_path() -> Path:
    return Path(cfg.packages_dir) / cfg.modpack_index


def get_enabled_manifests() -> m.ManifestIndex:
    return m.ManifestIndex(**json.load(get_manifest_index_path().open()))


def save_manifests(modpack_index: m.ManifestIndex):
    with get_manifest_index_path().open('w') as file_handler:
        json.dump(modpack_index.dict(), file_handler, ensure_ascii=False, indent=2)


def get_manifest_info(
    source_manifest: Optional[m.SourceManifest],
    target_manifest: Optional[m.TargetManifest]
) -> m.ManifestInfo:
    if source_manifest is not None:
        location = Path(source_manifest.name) / c.TARGET_MANIFEST_INDEX
        name = source_manifest.name
        title = source_manifest.title
        version = source_manifest.version
    elif target_manifest is not None:
        location = Path(target_manifest.name) / c.TARGET_MANIFEST_INDEX
        name = target_manifest.name
        title = target_manifest.title
        version = target_manifest.version
    else:
        name = "unknown_" + uuid.uuid4().hex
        title = "unknown_" + uuid.uuid4().hex
        version = "0.0"
        location = Path("/tmp") / uuid.uuid4().hex

    return m.ManifestInfo(
        name=name,
        title=title,
        version=version,
        location=location.as_posix(),
    )


def bootstrap_source_manifest(manifest: m.SourceManifest) -> Path:
    base_path: Path = Path(cfg.sources_dir) / manifest.name

    if base_path.exists():
        raise ManifestError(f"Base path {base_path} for modpack {manifest.name} already exists!")

    base_path.mkdir()
    (base_path / manifest.objectsLocation).mkdir()

    index_path: Path = base_path / c.SOURCE_MANIFEST_INDEX

    yaml.dump(
        manifest.dict(),
        index_path.open("w", encoding="utf-8"),
        encoding="utf-8",
        indent=2,
    )

    return index_path
