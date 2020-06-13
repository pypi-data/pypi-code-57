import os
import yapl

## Setup Dump
def dump_setup(auto=False, files=[]):
    if auto:
        # to be implemeted
        pass

    else:
        if len(files) == 0:
            raise Exception('No file provided')
        else:
            #zip -r -q source_code archive/ *.c *.h
            _files = " ".join(files)
            os.system('zip -r -q backup_{} {}'.format(yapl.config.EXPERIMENT_NAME, _files))