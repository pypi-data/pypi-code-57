from lb_dev_formatting.commands.format import format_files
from lb_utils.git_utils import GitUtils
from lb_utils.log_utils import set_up_logging
from lb_dev_formatting import constants

import logging

log = logging.getLogger(__name__)

def format():
    set_up_logging(10)
    files = GitUtils.get_all_files_tracked_in_repo(None)
    return format_files(files, constants.CLANG_FORMAT_VERSION, '0.29.0', True, None, False, None)