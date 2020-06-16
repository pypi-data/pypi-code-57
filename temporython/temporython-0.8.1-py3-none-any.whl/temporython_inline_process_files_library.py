
#### BEGIN temporython_inline_process_files_library ###########################################
import sys

def process_files_in_argv(process_line=None, process_file=None):
    """
    inlined version of process_files_in_argv() from the temporython library.
    """
    # TODO: use argparse?
    input_filenames = sys.argv[1:]
    if not input_filenames:
        input_filenames = ['-']  # stdin

    process_files(input_filenames, process_line=process_line, process_file=process_file)


def process_files(filenames, process_line=None, process_file=None):
    """
    inlined version of process_files() from the temporython library.
    """
    if (process_line and process_file) or (not process_line and not process_file):
        raise ValueError('must provide exactly one of `process_line` or `process_file` callback. ')

    for input_filename in filenames:
        if input_filename == '-':
            input_file = sys.stdin
        else:
            input_file = open(input_filename, 'r')
        if process_line:
            # process each line of input ----
            line, line_number = 'dummy', 0
            while (line != ''):  # line will be empty only when EOF is reached.
                line, line_number = sys.stdin.readline(), line_number+1
                process_line(input_filename, line_number, line)
            #except EOFError:
            if input_file != sys.stdin:
                input_file.close()
        else:  # process file
            contents = input_file.read()
            process_file(input_filename, contents)
            if input_file != sys.stdin:
                input_file.close()

def main(ProcessorClass):
    """
    inlined version of main() from the temporython library.
    assumes that class implements these methods:
        * process_line(filename, line_number, line)
        * post_process()
    """
    try:
        processor = ProcessorClass()
        kwargs = {
            'process_line': getattr(processor, 'process_line', None),
            'process_file': getattr(processor, 'process_file', None)
        }
        process_files_in_argv(**kwargs)
        processor.post_process()
    except KeyboardInterrupt:
        sys.exit(1)

#### END temporython_inline_process_files_library #############################################
