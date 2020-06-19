# -*- coding: utf-8 -*-
# Adapted code provided by the sphinx-dev community [0] to produce a plugin to
# provide the last updated date for each file in YYYY-mm-dd format instead of a
# single date for the entire project.
# [0]: https://groups.google.com/forum/#!topic/sphinx-dev/6G8TWtIVN14

from datetime import datetime
import os
import subprocess


def _get_last_updated(app, pagename):
    """
    Pull the date from a git log call that represents the date a file was last
    updated.
    """
    last_updated = None
    src_file = app.builder.env.doc2path(pagename)
    if os.path.exists(src_file):
        try:
            last_updated_t = subprocess.check_output(
            [
                'git', 'log', '-n1', '--format=%ad', '--date=unix',
                '--', src_file,
            ]
            ).decode('utf-8').strip()
            last_updated = datetime.fromtimestamp(int(last_updated_t))
        except (ValueError, subprocess.CalledProcessError):
            pass
    return last_updated


def html_page_context(app, pagename, templatename, context, doctree):
    context['last_updated'] = _get_last_updated(app, pagename)


def setup(app):
    app.connect('html-page-context', html_page_context)
    return {
        'version': '1.0.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True
    }
