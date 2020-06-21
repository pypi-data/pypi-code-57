import yaml


def get_password():
    variables = yaml.load(open(
        'inventory/group_vars/gitlab/gitlab.yml'))
    return variables['gitlab_password']
