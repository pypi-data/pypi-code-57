import logging
import os
from subprocess import check_output

log = logging.getLogger(__name__)


class GitUtils:
    @staticmethod
    def get_all_files_tracked_in_repo(reference):

        log.info('getting all files where copyright is applicable')
        log.debug('reference: {}'.format(reference))
        if reference is None:
            files_in_repo = (path.decode() for path in check_output(
                ['git', 'ls-files', '-z']).rstrip(b'\x00').split(b'\x00'))
        else:
            prefix_len = len(
                check_output(['git', 'rev-parse', '--show-prefix']).strip())
            files_in_repo = (path[prefix_len:].decode()
                             for path in check_output([
                                 'git', 'diff', '--name-only', '--no-renames',
                                 '--diff-filter=MA', '-z', reference +
                                 '...', '.'
                             ]).rstrip(b'\x00').split(b'\x00'))

        return files_in_repo

    @staticmethod
    def get_git_root(path):
        from subprocess import Popen, PIPE
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        p = Popen(['git', 'rev-parse', '--show-toplevel'],
                  cwd=path,
                  stdout=PIPE,
                  stderr=PIPE)
        out, _ = p.communicate()
        if p.returncode == 0:
            return out.strip()
        else:
            return None
