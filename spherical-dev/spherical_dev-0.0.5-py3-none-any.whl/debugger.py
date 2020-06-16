import os
import pathlib

import IPython


class Debugger:
    quitting = True

    def reset(self):
        pass

    def interaction(self, frame, traceback):
        print(os.linesep)
        testname = None
        while traceback.tb_next is not None:
            traceback = traceback.tb_next
            if testname is None:
                if traceback.tb_frame.f_code.co_filename.startswith(os.getcwd()):
                    print(traceback.tb_frame.f_code.co_name)
                    print(os.linesep)
        filename = traceback.tb_frame.f_code.co_filename
        func = traceback.tb_frame.f_code.co_name
        lineno = traceback.tb_lineno
        file_lines = pathlib.Path(filename).read_text().splitlines()
        print(f'> {filename}({lineno}){func}()')
        print(file_lines[lineno - 1])
        print(os.linesep)
        IPython.start_ipython(argv=[], user_ns=traceback.tb_frame.f_locals)
