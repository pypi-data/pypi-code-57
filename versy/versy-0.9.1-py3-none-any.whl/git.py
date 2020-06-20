import subprocess

SUB = {'stderr': subprocess.DEVNULL, 'encoding': 'utf8'}
CMD = 'git log --pretty=format:%s HEAD~{end}..HEAD~{begin}'


def get_commits(version, cwd, max_commits=256, commit_block=2):
    commits = []

    begin = 0
    end = commit_block
    while True:
        cmd = CMD.format(begin=begin, end=end)
        try:
            out = subprocess.check_output(cmd.split(), cwd=cwd, **SUB)
        except subprocess.CalledProcessError:
            return []

        for line in out.splitlines():
            if line:
                if version in line:
                    return commits
                if len(commits) >= max_commits:
                    return []
                commits.append(line)

        begin += commit_block
        end += commit_block

    return commits


def check_clean_workspace():
    try:
        subprocess.check_output('git diff-index --quiet HEAD --'.split())
    except subprocess.CalledProcessError:
        raise ValueError('Cannot create new version with changes in workspace')


def commit(files, message, dry_run, verbose):
    for cmd in (
        ('git', 'add') + tuple(str(f) for f in files),
        ('git', 'commit', '-m', message),
    ):
        if verbose or dry_run:
            print('$', *cmd)
        if not dry_run:
            if verbose:
                subprocess.run(cmd).check_returncode()
            else:
                subprocess.check_output(cmd)


if __name__ == '__main__':
    import sys

    for line in get_commits(sys.argv[1], '.'):
        print(line)
