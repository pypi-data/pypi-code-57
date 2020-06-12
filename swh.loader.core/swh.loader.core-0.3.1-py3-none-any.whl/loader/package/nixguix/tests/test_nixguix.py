# Copyright (C) 2020 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import os
import json
import logging

import pytest

from json.decoder import JSONDecodeError
from typing import Dict, Optional, Tuple

from unittest.mock import patch

from swh.model.model import Snapshot
from swh.loader.package.archive.loader import ArchiveLoader
from swh.loader.package.nixguix.loader import (
    NixGuixLoader,
    retrieve_sources,
    clean_sources,
)

from swh.loader.package.tests.common import get_stats, check_snapshot
from swh.loader.package.utils import download
from swh.model.hashutil import hash_to_bytes, hash_to_hex
from swh.storage.exc import HashCollision

sources_url = "https://nix-community.github.io/nixpkgs-swh/sources.json"


def test_retrieve_sources(swh_config, requests_mock_datadir):
    j = retrieve_sources(sources_url)
    assert "sources" in j.keys()
    assert len(j["sources"]) == 2


def test_retrieve_non_existing(swh_config, requests_mock_datadir):
    with pytest.raises(ValueError):
        NixGuixLoader("https://non-existing-url")


def test_retrieve_non_json(swh_config, requests_mock_datadir):
    with pytest.raises(JSONDecodeError):
        NixGuixLoader("https://example.com/file.txt")


def test_clean_sources_invalid_schema(swh_config, requests_mock_datadir):
    sources = {}
    with pytest.raises(ValueError, match="sources structure invalid, missing: .*"):
        clean_sources(sources)


def test_clean_sources_invalid_version(swh_config, requests_mock_datadir):
    sources = {"version": 2, "sources": [], "revision": "my-revision"}

    with pytest.raises(
        ValueError, match="sources structure version .* is not supported"
    ):
        clean_sources(sources)


def test_clean_sources_invalid_sources(swh_config, requests_mock_datadir):
    sources = {
        "version": 1,
        "sources": [
            # Valid source
            {"type": "url", "urls": ["my-url"], "integrity": "my-integrity"},
            # integrity is missing
            {"type": "url", "urls": ["my-url"],},
            # urls is not a list
            {"type": "url", "urls": "my-url", "integrity": "my-integrity"},
            # type is not url
            {"type": "git", "urls": ["my-url"], "integrity": "my-integrity"},
        ],
        "revision": "my-revision",
    }
    clean = clean_sources(sources)

    assert len(clean["sources"]) == 1


def check_snapshot_revisions_ok(snapshot, storage):
    """Ensure the snapshot revisions are structurally as expected

    """
    revision_ids = []
    for name, branch in snapshot["branches"].items():
        if name == b"evaluation":
            continue  # skipping that particular branch
        if branch["target_type"] == "revision":
            revision_ids.append(branch["target"])

    revisions = storage.revision_get(revision_ids)
    for rev in revisions:
        metadata = rev["metadata"]
        raw = metadata["extrinsic"]["raw"]
        assert "url" in raw
        assert "integrity" in raw


def test_loader_one_visit(swh_config, requests_mock_datadir):
    loader = NixGuixLoader(sources_url)
    res = loader.load()
    assert res["status"] == "eventful"

    stats = get_stats(loader.storage)
    assert {
        "content": 1,
        "directory": 3,
        "origin": 1,
        "origin_visit": 1,
        "person": 1,
        "release": 0,
        "revision": 1,
        "skipped_content": 0,
        "snapshot": 1,
    } == stats

    origin_visit = loader.storage.origin_visit_get_latest(sources_url)
    # The visit is partial because urls pointing to non tarball file
    # are not handled yet
    assert origin_visit["status"] == "partial"
    assert origin_visit["type"] == "nixguix"


def test_uncompress_failure(swh_config, requests_mock_datadir):
    """Non tarball files are currently not supported and the uncompress
    function fails on such kind of files.

    However, even in this case of failure (because of the url
    https://example.com/file.txt), a snapshot and a visit has to be
    created (with a status partial since all files are not archived).

    """
    loader = NixGuixLoader(sources_url)
    loader_status = loader.load()

    urls = [s["urls"][0] for s in loader.sources]
    assert "https://example.com/file.txt" in urls
    assert loader_status["status"] == "eventful"

    origin_visit = loader.storage.origin_visit_get_latest(sources_url)
    # The visit is partial because urls pointing to non tarball files
    # are not handled yet
    assert origin_visit["status"] == "partial"


def test_loader_incremental(swh_config, requests_mock_datadir):
    """Ensure a second visit do not download artifact already
    downloaded by the previous visit.

    """
    loader = NixGuixLoader(sources_url)
    load_status = loader.load()

    loader.load()
    expected_snapshot_id = "0c5881c74283793ebe9a09a105a9381e41380383"
    assert load_status == {"status": "eventful", "snapshot_id": expected_snapshot_id}
    expected_branches = {
        "evaluation": {
            "target": "cc4e04c26672dd74e5fd0fecb78b435fb55368f7",
            "target_type": "revision",
        },
        "https://github.com/owner-1/repository-1/revision-1.tgz": {
            "target": "488ad4e7b8e2511258725063cf43a2b897c503b4",
            "target_type": "revision",
        },
    }
    expected_snapshot = {
        "id": expected_snapshot_id,
        "branches": expected_branches,
    }
    snapshot = check_snapshot(expected_snapshot, storage=loader.storage)
    check_snapshot_revisions_ok(snapshot, loader.storage)

    urls = [
        m.url
        for m in requests_mock_datadir.request_history
        if m.url == ("https://github.com/owner-1/repository-1/revision-1.tgz")
    ]
    # The artifact
    # 'https://github.com/owner-1/repository-1/revision-1.tgz' is only
    # visited one time
    assert len(urls) == 1


def test_loader_two_visits(swh_config, requests_mock_datadir_visits):
    """To ensure there is only one origin, but two visits, two revisions
    and two snapshots are created.

    The first visit creates a snapshot containing one tarball. The
    second visit creates a snapshot containing the same tarball and
    another tarball.

    """
    loader = NixGuixLoader(sources_url)
    load_status = loader.load()
    expected_snapshot_id = "0c5881c74283793ebe9a09a105a9381e41380383"
    assert load_status == {"status": "eventful", "snapshot_id": expected_snapshot_id}

    expected_branches = {
        "evaluation": {
            "target": "cc4e04c26672dd74e5fd0fecb78b435fb55368f7",
            "target_type": "revision",
        },
        "https://github.com/owner-1/repository-1/revision-1.tgz": {
            "target": "488ad4e7b8e2511258725063cf43a2b897c503b4",
            "target_type": "revision",
        },
    }

    expected_snapshot = {
        "id": expected_snapshot_id,
        "branches": expected_branches,
    }
    snapshot = check_snapshot(expected_snapshot, storage=loader.storage)
    check_snapshot_revisions_ok(snapshot, loader.storage)

    stats = get_stats(loader.storage)
    assert {
        "content": 1,
        "directory": 3,
        "origin": 1,
        "origin_visit": 1,
        "person": 1,
        "release": 0,
        "revision": 1,
        "skipped_content": 0,
        "snapshot": 1,
    } == stats

    loader = NixGuixLoader(sources_url)
    load_status = loader.load()
    expected_snapshot_id = "b0bfa75cbd0cc90aac3b9e95fb0f59c731176d97"
    assert load_status == {"status": "eventful", "snapshot_id": expected_snapshot_id}

    # This ensures visits are incremental. Indeed, if we request a
    # second time an url, because of the requests_mock_datadir_visits
    # fixture, the file has to end with `_visit1`.
    expected_branches = {
        "evaluation": {
            "target": "602140776b2ce6c9159bcf52ada73a297c063d5e",
            "target_type": "revision",
        },
        "https://github.com/owner-1/repository-1/revision-1.tgz": {
            "target": "488ad4e7b8e2511258725063cf43a2b897c503b4",
            "target_type": "revision",
        },
        "https://github.com/owner-2/repository-1/revision-1.tgz": {
            "target": "85e0bad74e33e390aaeb74f139853ae3863ee544",
            "target_type": "revision",
        },
    }

    expected_snapshot = {
        "id": expected_snapshot_id,
        "branches": expected_branches,
    }
    snapshot = check_snapshot(expected_snapshot, storage=loader.storage)
    check_snapshot_revisions_ok(snapshot, loader.storage)

    stats = get_stats(loader.storage)
    assert {
        "content": 2,
        "directory": 5,
        "origin": 1,
        "origin_visit": 2,
        "person": 1,
        "release": 0,
        "revision": 2,
        "skipped_content": 0,
        "snapshot": 2,
    } == stats


def test_resolve_revision_from(swh_config, requests_mock_datadir):
    loader = NixGuixLoader(sources_url)

    known_artifacts = {
        "id1": {"extrinsic": {"raw": {"url": "url1", "integrity": "integrity1"}}},
        "id2": {"extrinsic": {"raw": {"url": "url2", "integrity": "integrity2"}}},
    }

    metadata = {"url": "url1", "integrity": "integrity1"}
    assert loader.resolve_revision_from(known_artifacts, metadata) == "id1"
    metadata = {"url": "url3", "integrity": "integrity3"}
    assert loader.resolve_revision_from(known_artifacts, metadata) == None  # noqa


def test_evaluation_branch(swh_config, requests_mock_datadir):
    loader = NixGuixLoader(sources_url)
    res = loader.load()
    assert res["status"] == "eventful"

    expected_branches = {
        "https://github.com/owner-1/repository-1/revision-1.tgz": {
            "target": "488ad4e7b8e2511258725063cf43a2b897c503b4",
            "target_type": "revision",
        },
        "evaluation": {
            "target": "cc4e04c26672dd74e5fd0fecb78b435fb55368f7",
            "target_type": "revision",
        },
    }

    expected_snapshot = {
        "id": "0c5881c74283793ebe9a09a105a9381e41380383",
        "branches": expected_branches,
    }

    snapshot = check_snapshot(expected_snapshot, storage=loader.storage)
    check_snapshot_revisions_ok(snapshot, loader.storage)


def test_eoferror(swh_config, requests_mock_datadir):
    """Load a truncated archive which is invalid to make the uncompress
    function raising the exception EOFError. We then check if a
    snapshot is created, meaning this error is well managed.

    """
    sources = (
        "https://nix-community.github.io/nixpkgs-swh/sources-EOFError.json"  # noqa
    )
    loader = NixGuixLoader(sources)
    loader.load()

    expected_branches = {
        "evaluation": {
            "target": "cc4e04c26672dd74e5fd0fecb78b435fb55368f7",
            "target_type": "revision",
        },
    }
    expected_snapshot = {
        "id": "4257fa2350168c6bfec726a06452ea27a2c0cb33",
        "branches": expected_branches,
    }

    snapshot = check_snapshot(expected_snapshot, storage=loader.storage)
    check_snapshot_revisions_ok(snapshot, loader.storage)


def fake_download(
    url: str,
    dest: str,
    hashes: Dict = {},
    filename: Optional[str] = None,
    auth: Optional[Tuple[str, str]] = None,
) -> Tuple[str, Dict]:
    """Fake download which raises HashCollision (for the sake of test simpliciy,
    let's accept that makes sense)

    For tests purpose only.

    """
    if url == "https://example.com/file.txt":
        # instead of failing because it's a file not dealt with by the nix guix
        # loader, make it raise a hash collision
        raise HashCollision("sha1", "f92d74e3874587aaf443d1db961d4e26dde13e9c", [])
    return download(url, dest, hashes, filename, auth)


def test_raise_exception(swh_config, requests_mock_datadir, mocker):
    mock_download = mocker.patch("swh.loader.package.loader.download")
    mock_download.side_effect = fake_download

    loader = NixGuixLoader(sources_url)
    res = loader.load()

    expected_snapshot_id = "0c5881c74283793ebe9a09a105a9381e41380383"
    assert res == {
        "status": "eventful",
        "snapshot_id": expected_snapshot_id,
    }

    expected_branches = {
        "https://github.com/owner-1/repository-1/revision-1.tgz": {
            "target": "488ad4e7b8e2511258725063cf43a2b897c503b4",
            "target_type": "revision",
        },
        "evaluation": {
            "target": "cc4e04c26672dd74e5fd0fecb78b435fb55368f7",
            "target_type": "revision",
        },
    }
    expected_snapshot = {
        "id": expected_snapshot_id,
        "branches": expected_branches,
    }

    snapshot = check_snapshot(expected_snapshot, storage=loader.storage)
    check_snapshot_revisions_ok(snapshot, loader.storage)

    assert len(mock_download.mock_calls) == 2

    origin_visit = loader.storage.origin_visit_get_latest(sources_url)

    # The visit is partial because some hash collision were detected
    assert origin_visit["status"] == "partial"
    assert origin_visit["type"] == "nixguix"


def test_load_nixguix_one_common_artifact_from_other_loader(
    swh_config, datadir, requests_mock_datadir_visits, caplog
):
    """Misformatted revision should be caught and logged, then loading continues

    """
    caplog.set_level(logging.ERROR, "swh.loader.package.nixguix.loader")

    # 1. first ingest with for example the archive loader
    gnu_url = "https://ftp.gnu.org/gnu/8sync/"
    release = "0.1.0"
    artifact_url = f"https://ftp.gnu.org/gnu/8sync/8sync-{release}.tar.gz"
    gnu_artifacts = [
        {
            "time": 944729610,
            "url": artifact_url,
            "length": 221837,
            "filename": f"8sync-{release}.tar.gz",
            "version": release,
        }
    ]
    archive_loader = ArchiveLoader(url=gnu_url, artifacts=gnu_artifacts)
    actual_load_status = archive_loader.load()
    expected_snapshot_id = "c419397fd912039825ebdbea378bc6283f006bf5"
    assert actual_load_status["status"] == "eventful"
    assert actual_load_status["snapshot_id"] == expected_snapshot_id  # noqa

    gnu_snapshot = archive_loader.storage.snapshot_get(
        hash_to_bytes(expected_snapshot_id)
    )

    first_revision = gnu_snapshot["branches"][f"releases/{release}".encode("utf-8")]

    # 2. Then ingest with the nixguix loader which lists the same artifact within its
    # sources.json

    # ensure test setup is ok
    data_sources = os.path.join(
        datadir, "https_nix-community.github.io", "nixpkgs-swh_sources_special.json"
    )
    all_sources = json.loads(open(data_sources).read())
    found = False
    for source in all_sources["sources"]:
        if source["urls"][0] == artifact_url:
            found = True
            assert (
                found is True
            ), f"test setup error: {artifact_url} must be in {data_sources}"

    # first visit with a snapshot, ok
    sources_url = "https://nix-community.github.io/nixpkgs-swh/sources_special.json"
    loader = NixGuixLoader(sources_url)
    actual_load_status2 = loader.load()
    assert actual_load_status2["status"] == "eventful"

    snapshot_id = actual_load_status2["snapshot_id"]
    snapshot = loader.storage.snapshot_get(hash_to_bytes(snapshot_id))
    snapshot.pop("next_branch")  # snapshot_get endpoint detail to drop

    # simulate a snapshot already seen with a revision with the wrong metadata structure
    # This revision should be skipped, thus making the artifact being ingested again.
    with patch(
        "swh.loader.package.loader.PackageLoader.last_snapshot"
    ) as last_snapshot:
        # mutate the snapshot to target a revision with the wrong metadata structure
        # snapshot["branches"][artifact_url.encode("utf-8")] = first_revision
        old_revision = next(loader.storage.revision_get([first_revision["target"]]))
        # assert that revision is not in the right format
        assert old_revision["metadata"]["extrinsic"]["raw"].get("integrity", {}) == {}

        # mutate snapshot to create a clash
        snapshot["branches"][artifact_url.encode("utf-8")] = {
            "target_type": "revision",
            "target": old_revision["id"],
        }

        # modify snapshot to actually change revision metadata structure so we simulate
        # a revision written by somebody else (structure different)
        last_snapshot.return_value = Snapshot.from_dict(snapshot)

        loader = NixGuixLoader(sources_url)
        actual_load_status3 = loader.load()
        assert last_snapshot.called
        assert actual_load_status3["status"] == "eventful"

        new_snapshot_id = "32ff641e510aceefc3a6d0dcbf208b2854d2e965"
        assert actual_load_status3["snapshot_id"] == new_snapshot_id

        last_snapshot = loader.storage.snapshot_get(hash_to_bytes(new_snapshot_id))
        new_revision_branch = last_snapshot["branches"][artifact_url.encode("utf-8")]
        assert new_revision_branch["target_type"] == "revision"

        new_revision = next(
            loader.storage.revision_get([new_revision_branch["target"]])
        )

        # the new revision has the correct structure,  so it got ingested alright by the
        # new run
        assert new_revision["metadata"]["extrinsic"]["raw"]["integrity"] is not None

        nb_detections = 0
        actual_detection: Dict
        for record in caplog.records:
            logtext = record.getMessage()
            if "Unexpected metadata revision structure detected:" in logtext:
                nb_detections += 1
                actual_detection = record.args["context"]

        assert actual_detection
        # as many calls as there are sources listed in the sources.json
        assert nb_detections == len(all_sources["sources"])

        assert actual_detection == {
            "revision": hash_to_hex(old_revision["id"]),
            "reason": "'integrity'",
            "known_artifact": old_revision["metadata"],
        }
