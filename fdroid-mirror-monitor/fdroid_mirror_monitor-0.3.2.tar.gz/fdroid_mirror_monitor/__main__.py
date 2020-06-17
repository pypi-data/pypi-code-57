#!/usr/bin/env python3

from fdroid_mirror_monitor.main import main
from fdroid_mirror_monitor.utils import get_logger

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log = get_logger(__name__)
        log.info('Exiting...')
        exit()
    except Exception as e:
        log = get_logger(__name__)
        log.fatal(e)
        raise
        exit(1)
