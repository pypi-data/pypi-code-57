#!/usr/bin/env python3

# stdlibs:
from datetime import datetime, timezone
from importlib.metadata import metadata
from os import makedirs, path, getenv

# external:
from jinja2 import Environment, FileSystemLoader
from json2html import json2html


def create_html(status, dir, history=None):
    '''
    Create html on current status.

    :param status: dict
    :param dir: output directory of html
    :param repo_name: headline 1
    '''
    # generate html from template with jinja
    template_dir = path.join(path.dirname(__file__), path.pardir, 'templates')
    template_dir = path.abspath(template_dir)

    # variables:
    sourceurl = getenv('CI_PROJECT_URL', metadata(__package__)['Home-Page'])
    # timestamp to date string
    last_check = datetime.fromtimestamp(status['last_check'], tz=timezone.utc).strftime("%F %H:%M %Z")

    makedirs(dir, exist_ok=True)
    env = Environment(loader=FileSystemLoader(template_dir))
    env.trim_blocks = True
    env.lstrip_blocks = True

    # render mirror details subpages
    # detaildir = dir + '/mirrors'
    template = env.get_template('details.html')
    for mirror in status['mirrors']:
        table = json2html.convert(json=mirror)
        # makedirs(detaildir + mirror[name], exist_ok=True)
        with open(path.join(dir, mirror['name'] + '.html'), 'w') as f:
            f.write(template.render(mirror=mirror, table=table, ref_name=getenv('CI_COMMIT_REF_NAME')))

    # render index.html
    template = env.get_template('index.html')
    index = template.render(sourceurl=sourceurl, status=status, last_check=last_check)
    with open(path.join(dir, 'index.html'), 'w') as fp:
        fp.write(index)
