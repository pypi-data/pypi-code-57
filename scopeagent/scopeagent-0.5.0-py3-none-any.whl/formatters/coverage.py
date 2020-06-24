from scopeagent.tracer.util import generate_id, TRACE_ID_LENGTH


def format_coverage(coverage):
    files = []

    for file_reporter in coverage._get_file_reporters():
        analysis = coverage._analyze(file_reporter)
        if analysis.numbers.n_statements == 0 or len(analysis.executed) == 0:
            continue

        boundaries = []

        for fileline in sorted(analysis.executed):
            boundaries += [[fileline, 1, 1], [fileline + 1, 0, -1]]

        files.append({'filename': file_reporter.filename, 'boundaries': boundaries})

    return {
        'type': 'com.undefinedlabs.uccf',
        'uuid': '{0:032x}'.format(generate_id(TRACE_ID_LENGTH)),
        'files': files,
        'version': '0.2.0',
    }
