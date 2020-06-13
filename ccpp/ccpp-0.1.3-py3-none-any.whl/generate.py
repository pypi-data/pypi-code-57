import os
import re

from cookiecutter.main import cookiecutter


def get_context(repo):
    context = dict(
        user=os.popen("git config --global user.name").read(),
        email=os.popen("git config --global user.email").read(),
        repo=repo,
        repo_src=re.sub('[- ]', '_', repo),
    )
    return context


def get_tmpl_path():
    module_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(module_dir, 'ccpp-tmpl')


def generate_tmpl(repo):
    extra_context = get_context(repo)
    tmpl_path = get_tmpl_path()
    # https: // cookiecutter.readthedocs.io/en/latest/advanced/suppressing_prompts.html
    cookiecutter(tmpl_path, extra_context=extra_context, no_input=True, overwrite_if_exists=True)