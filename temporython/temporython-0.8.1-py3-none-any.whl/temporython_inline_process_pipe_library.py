#### BEGIN temporython_inline_process_pipe_library ###########################################
import sys

def pipe_main(LineProcessorClass):
    try:
        # preprocessing, setup ----
        processor = LineProcessorClass()

        # process each line from stdin ----
        line, line_number = 'dummy', 0
        while (line != ''):  # line will be empty only when EOF is reached.
            line, line_number = sys.stdin.readline(), line_number+1
            processor.process_line('-', line_number, line)

        # run post processing ----
        processor.post_process()

    except KeyboardInterrupt:
        sys.exit(1)
#### END temporython_inline_process_pipe_library #############################################
