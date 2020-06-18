from pyOptional import Optional
from subprocess import Popen, PIPE, CalledProcessError


class ShellUtils:
    @staticmethod
    def run_in_shell(cmd, input=None):
        '''
        Return the formatted version of the given file.
        '''

        import logging
        logging.debug('calling %r', cmd)
        p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        if input:
            out, err = p.communicate(input)
            result = out.decode()
        else:
            result = None
        if p.returncode:
            raise CalledProcessError(p.returncode, cmd, err)
        return result

    @staticmethod
    def find_command(names):
        from whichcraft import which
        try:
            return next(path for path in (which(name) for name in names)
                        if path)
        except StopIteration:
            return None
