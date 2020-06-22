#!/usr/bin/python3
import click
import jinja2
import logging
import subprocess
import os
import shutil
import sys
import xmlrpc.client
import yaml

logging.basicConfig()
logger = logging.getLogger('main')

config = yaml.safe_load(open('manage.yml').read())

################### MARKET FUNCTIONS  #######################################

BRANCHES = ['10.0', '11.0', '12.0', '13.0']


def get_current_branch():
    # Returns the current branch of app.
    branches = subprocess.check_output(
        'cd {} && git branch'.format(config['addons_dir']),
        shell=True).decode()
    current = [k.strip('* ') for k in branches.split('\n') if '*' in k]
    return current[0]


def set_branch(branch):
    # Returns the current branch of app.
    subprocess.check_output(
        'cd {} && git checkout {}'.format(config['addons_dir'], branch),
        shell=True).decode()


def checkout_branch(branch):
    subprocess.check_output(
        'cd {} && git checkout {}'.format(config['addons_dir'], branch),
        shell=True)


@click.group()
def main():
    pass


@click.command()
@click.option('-b', '--branch')
def push(branch):
    current_branch = get_current_branch()
    for b in BRANCHES if not branch else [branch]:
        try:
            subprocess.check_output(
                'cd {} && git checkout {} && git push'.format(
                    config['addons_dir'], b), shell=True)
        except subprocess.CalledProcessError as e:
            click.echo(e.output)
    subprocess.check_output(
        'cd {} && git checkout {}'.format(
            config['addons_dir'], current_branch), shell=True)


main.add_command(push)


@click.command()
@click.option('-b', '--branch')
def pull(branch):
    current_branch = get_current_branch()
    for b in BRANCHES if not branch else [branch]:
        try:
            subprocess.check_output(
                'cd {} && git checkout {} && git pull'.format(
                    config['addons_dir'], b), shell=True)
        except subprocess.CalledProcessError as e:
            click.echo(e.output)
    subprocess.check_output(
        'cd {} && git checkout {}'.format(
            config['addons_dir'], current_branch), shell=True)


main.add_command(pull)

@click.command()
@click.argument('commit', required=True)
@click.argument('branches', nargs=-1)
def cherry(commit, branches):
    current_branch = get_current_branch()
    print('Current branch: ', current_branch)
    if not branches or branches == ('all',):
        branches = BRANCHES
        branches.remove(current_branch)
    for b in branches:
        checkout_branch(b)
        try:
            subprocess.check_output(
                'cd {} && git cherry-pick {}'.format(
                    config['addons_dir'], commit), shell=True)
        except subprocess.CalledProcessError as e:
            click.echo(e.output)
            break
    # Return back
    checkout_branch(current_branch)


main.add_command(cherry)


@click.command()
@click.argument('apps', nargs=-1)
@click.pass_context
def publish(ctx, apps):    
    current_branch = get_current_branch()
    if not apps:
        apps = config['market_apps']
    for version in config['versions']:
        # Change addon version
        subprocess.check_output(
            "cd {} && git checkout {}".format(config['addons_dir'], version),
            shell=True, universal_newlines=True)
        # Change market version
        subprocess.check_output(
            "cd {} && git checkout {}".format(config['market_dir'], version),
            shell=True, universal_newlines=True)
        for app in config['market_apps']:
            # Remove old files
            market_app_dir = os.path.join(config['market_dir'], app)
            if os.path.isdir(market_app_dir):
                print('Removing old ', app)
                shutil.rmtree(market_app_dir)
            os.mkdir(market_app_dir)
            # Copy files
            print('Copy ', app)
            files = subprocess.check_output(
                "cd {} && git ls-files {}".format(
                    config['addons_dir'], app),
                shell=True).decode().split()
            for file in files:
                subprocess.check_output(
                    'rsync -v -l -R {}/{} {}/'.format(
                        config['addons_dir'], file, market_app_dir),
                    shell=True)
            print('Re-adding app ', app)
            subprocess.check_call(
                'cd {} && git add {} '.format(config['market_dir'], app),
                shell=True)
        # Commit market changes
        status = subprocess.check_output(
            'cd {} && git status'.format(config['market_dir']),
            shell=True).decode().strip()
        if 'nothing to commit' not in status:
            print('Commiting changes.')
            subprocess.check_call(
                'git commit -a -m "Apps updated."', shell=True)
            subprocess.check_call('git push', shell=True)
        else:
            print('Nothing changed.')
    # Restore
    checkout_branch(current_branch)

main.add_command(publish)


@click.command()
@click.argument('app')
def unpublish(app):
    branches = get_branches(os.path.join(config['market_dir'], app))
    current_branch = get_current_branch(config['market_dir'])
    print('Current branch ', current_branch)
    print('Market branches: ', branches)
    os.chdir(config['market_dir'])
    for branch in branches:
        print('Switching branch: ', branch)
        subprocess.check_output('git checkout {}'.format(branch),
                                shell=True)
        print('Removing app ', app)
        #shutil.rmtree(app)
        subprocess.check_output(
            'git commit {app} -m "Removed {app}"'.format(app=app), shell=True)

    set_branch(config['market_dir'], current_branch)


main.add_command(unpublish)


@click.command()
@click.argument('apps', nargs=-1)
def describe_addons(apps):
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('docs/addons_description'),
        extensions=['jinja2.ext.debug'],
        trim_blocks=True, lstrip_blocks=True)
    data = yaml.safe_load(
        open('docs/addons_description/modules.yml').read())
    if not apps:
        apps = list(data.keys())
    click.echo('Doing addons: {}'.format(apps))
    for app in apps:
        template = jinja_env.get_template('index.j2.html')
        res = template.render(data=data, module=data[app])
        open(
            'addons/{}/static/description/index.html'.format(app),
            'w').write(res)

main.add_command(describe_addons)



if __name__ == '__main__':
    main()
