"""
Some reporting functions, e.g. to print a report based on a job result
"""
from . import shellescape


def print_job_result(job_file, print_func=print, verbose=False):
    from fastr.abc.serializable import load
    from fastr.helpers.iohelpers import load_json
    from pprint import pprint

    job = load(job_file)
    try:
        info_store = load_json(job.extrainfofile)
    except FileNotFoundError:
        info_store = {}

    print_func('\n\n===== JOB {} ====='.format(job.id))
    if hasattr(job, 'network_id'):
        print_func('Network: {}'.format(job.network_id))
    if hasattr(job, 'run_id'):
        print_func('Run: {}'.format(job.run_id))

    print_func('Node: {}'.format(job.node_id))
    print_func('Sample index: {}'.format(job.sample_index))
    print_func('Sample id: {}'.format(job.sample_id))
    print_func('Status: {}'.format(job.status))
    print_func('Timestamp: {}'.format(job.timestamp))
    print_func('Job file: {}'.format(job.logfile))

    if hasattr(job, 'errors'):
        errors = job.errors
    elif 'errors' in info_store and isinstance(info_store['errors'], list):
        errors = info_store['errors']
    else:
        errors = []

    print_func('\n----- ERRORS -----')
    for job_error in errors:
        print_func('- {e[0]}: {e[1]} ({e[2]}:{e[3]})'.format(e=job_error))
    print_func('------------------')

    if 'process' in info_store:
        command = info_store['process'].get('command', None)
        if command is not None:
            print_func('\nCommand:')
            print_func('List representation: {}\n'.format(command))
            printable_command = []
            for item in command:
                printable_command.append(shellescape.quote_argument(item))
            print_func('String representation: {}\n'.format(' '.join(printable_command)))
    else:
        print_func('\nNo process information:')
        print_func('Cannot find process information in Job information, processing probably got killed.')
        print_func('If there are no other errors, this is often a result of too high memory use or')
        print_func('exceeding some other type of resource limit.')

    print_func('\nOutput data:')
    pprint(job.output_data)

    print_func('\nStatus history:')
    for timestamp, status in job.status_list:
        print_func('{}: {}'.format(timestamp, status))

    if 'process' in info_store:
        if 'stdout' in info_store['process']:
            print_func('\n----- STDOUT -----')
            print_func(info_store['process']['stdout'])
            print_func('------------------')

        if 'stderr' in info_store['process']:
            print_func('\n----- STDERR -----')
            print_func(info_store['process']['stderr'])
            print_func('------------------')

    if verbose and job.stdoutfile.exists():
        print_func('\n------ FASTR JOB STDOUT -----')
        print_func(job.stdoutfile.read_text())
        print_func('-----------------------------')

    if verbose and job.stderrfile.exists():
        print_func('\n------ FASTR JOB STDERR -----')
        print_func(job.stderrfile.read_text())
        print_func('-----------------------------')
