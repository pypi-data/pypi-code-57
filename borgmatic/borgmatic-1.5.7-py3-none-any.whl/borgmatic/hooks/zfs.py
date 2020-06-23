from snapshot import get_path_and_all_parents


def create_snapshot(source_directory, log_prefix, dry_run):
    try:
        zfs_name = next(
            zfs_name
            for path in get_path_and_all_parents(source_directory)
            for zfs_name in (path_to_zfs_name(path),)
            if zfs_name
        )
    except StopIteration:
        logger.debug(
            '{}: Skipping ZFS snapshot for {}; not a ZFS dataset'.format(
                log_prefix, source_directory
            )
        )
        return

    dry_run_label = ' (dry run; not actually snapshotting anything)' if dry_run else ''
    # TODO: How to generate a unique snapshot name? borgmatic-HASHOFCONFIGPATH-HASHOFSOURCEPATH?
    # TODO: hashlib.blake2b(value.encode('utf-8'), digest_size=10).hexdigest()
    snapshot_name = 'borgmatic-{}-{}'.format()
    logger.info(
        '{}: Creating ZFS snapshot for {} ({}){}'.format(
            log_prefix, source_directory, snapshot_name, dry_run_label
        )
    )

    # TODO: How to destroy stale snapshots?
    # TODO: What about ushare and remapping paths to make restore easier?


def remove_snapshot():
    pass
