import subprocess
from lb_dev.commands.copyright.check_copyright_comment.check_copyright_comment import check_copyright
from lb_utils.log_utils import set_up_logging


def main():
    current_commit_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
    result = check_copyright(current_commit_sha)

    exit(result)

if __name__ == "__main__":
    main()
    