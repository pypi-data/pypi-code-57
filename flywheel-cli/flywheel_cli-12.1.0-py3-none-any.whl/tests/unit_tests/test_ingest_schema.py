from flywheel_cli.ingest import schemas as T


def test_ingest_status_is_terminal():
    # terminal ('finished', 'failed', 'aborted')
    assert T.IngestStatus.is_terminal('finished')
    assert T.IngestStatus.is_terminal('failed')
    assert T.IngestStatus.is_terminal('aborted')

    # not terminal
    assert not T.IngestStatus.is_terminal('created')
    assert not T.IngestStatus.is_terminal('scanning')
    assert not T.IngestStatus.is_terminal('resolving')
    assert not T.IngestStatus.is_terminal('in_review')
    assert not T.IngestStatus.is_terminal('preparing')
    assert not T.IngestStatus.is_terminal('uploading')
    assert not T.IngestStatus.is_terminal('finalizing')

def test_task_type_ingest_status():
    assert T.TaskType.ingest_status(T.TaskType.scan) == T.IngestStatus.scanning
    assert T.TaskType.ingest_status(T.TaskType.resolve) == T.IngestStatus.resolving
    assert T.TaskType.ingest_status(T.TaskType.prepare) == T.IngestStatus.preparing
    assert T.TaskType.ingest_status(T.TaskType.upload) == T.IngestStatus.uploading
    assert T.TaskType.ingest_status(T.TaskType.finalize) == T.IngestStatus.finalizing
