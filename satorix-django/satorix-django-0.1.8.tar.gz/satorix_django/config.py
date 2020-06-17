import filecmp
import os
import shutil
import difflib
import tempfile


PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.getcwd()


def go():
    verify_location()
    print("Creating Satorix hosting configuration...\n")
    runtime()
    requirements()
    app_module = input("Please enter your application’s module name: ")
    passenger_wsgi(app_module)
    edit_settings(app_module)
    copy_file(package_path('install/.gitlab-ci.yml'),
              app_path('.gitlab-ci.yml'))
    copy_file(package_path('install/Procfile'),
              app_path('Procfile'))
    copy_file(package_path('install/.buildpacks'),
              app_path('.buildpacks'))
    copy_file(package_path('install/.ruby-version'),
              app_path('.ruby-version'))
    copy_file(package_path('install/Gemfile'),
              app_path('Gemfile'))
    copy_file(package_path('install/Gemfile.lock'),
              app_path('Gemfile.lock'))
    copy_file(package_path('install/public/Passengerfile.json'),
              app_path('public/Passengerfile.json'))
    copy_file(package_path('install/config/passenger_standalone/nginx.conf.erb'),
              app_path('config/passenger_standalone/nginx.conf.erb'))
    copy_file(package_path('install/config/passenger_standalone/includes/django_asset_pipeline.erb'),
              app_path('config/passenger_standalone/includes/django_asset_pipeline.erb'))
    copy_file(package_path('install/config/passenger_standalone/includes/page_level_redirects.erb'),
              app_path('config/passenger_standalone/includes/page_level_redirects.erb'))
    copy_file(package_path('install/config/passenger_standalone/includes/proxy_configuration.erb'),
              app_path('config/passenger_standalone/includes/proxy_configuration.erb'))
    copy_file(package_path('install/config/passenger_standalone/includes/authentication.erb'),
              app_path('config/passenger_standalone/includes/authentication.erb'))


def app_path(path):
    # Prefix the given path with the app directory path
    return os.path.join(APP_DIR, path)


def copy_file(src, dst):
    if not os.path.exists(src):
        raise ValueError("Source file does not exist: {}".format(src))

    # Create a folder for dst if one does not already exist
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))

    # If the configuration file exists and is not the same show the user a diff
    if os.path.exists(dst):
        if filecmp.cmp(src, dst):
            print("Configuration file {} already installed".format(dst))
        else:
            print("\n{} already exists, showing diff:".format(dst))
            show_diff(src, dst)

    # If there is no configuration file copy to destination
    if not os.path.exists(dst):
        print("Writing configuration file: {}".format(dst))
        shutil.copyfile(src, dst)


def edit_settings(app_module):
    setup_path = app_path("public/{}/settings.py".format(app_module))
    backup_path = app_path("public/{}/settings.py-satorix-save".format(app_module))

    if os.path.exists(setup_path):
        print("Adding 'satorix_django' settings to "
              "'{}'".format(setup_path))
        with tempfile.TemporaryDirectory() as tempdir:
            out_path = os.path.join(tempdir, 'settings.py')
            with open(setup_path) as i, open(out_path, 'w') as o:
                for line in i:
                    if line.startswith('import os'):
                        line = 'import os\nimport satorix_django\n'
                    o.write(line)
            with open(out_path, "a") as file_object:
                file_object.write('\n# Settings for satorix hosting\n'
                                  'satorix_django.settings(locals())\n')
            os.rename(setup_path, backup_path)
            copy_file(out_path, setup_path)
    else:
        raise ValueError("File '{}' does not exist: ".format(setup_path))


def passenger_wsgi(app_module):
    print("In order for Passenger to run your application, we create a "
          "'passenger_wsgi.py' file within your site's 'public/' directory.")

    with tempfile.TemporaryDirectory() as tempdir:
        out_path = os.path.join(tempdir, 'passenger_wsgi.py')
        wsgi_path = app_path('public/passenger_wsgi.py')
        with open(out_path, "w") as o:
            print("import {}.wsgi\n"
                  "application = {}.wsgi.application".format(app_module, app_module), file=o)
        copy_file(out_path, wsgi_path)


def package_path(path):
    # Prefix the given path with this package location
    return os.path.join(PACKAGE_DIR, path)


def requirements():
    requirements_file = app_path('requirements.txt')

    if not os.path.exists(requirements_file):
        print("Please edit the 'requirements.txt' in the root of your "
              "application directory with the Python package dependencies "
              "required for your application.\n")
        copy_file(package_path('install/requirements.txt'),
                  app_path('requirements.txt'))
    else:
        try:
            requirements_text = open(requirements_file)
            print("Verify your Python package dependencies from "
                  "'requirements.txt' are correct and update if needed...\n"
                  "Current 'requirements.txt' packages:\n"
                  "{}".format(requirements_text.read()))
            print("Make sure to add the 'satorix-django' package to the above "
                  "list if it is missing.\n")
        finally:
            requirements_text.close()


def runtime():
    runtime_file = app_path('runtime.txt')

    if not os.path.exists(runtime_file):
        print("Please create a 'runtime.txt' in the root of your application "
              "directory with the Python version required for your"
              " application.\n")
    else:
        try:
            runtime_text = open(runtime_file)
            print("Verify your Python version from 'runtime.txt' is correct "
                  "and update if needed...\n"
                  "Current 'runtime.txt' version:\n"
                  "{}".format(runtime_text.read()))
        finally:
            runtime_text.close()


def show_diff(src, dst):
    with open(src) as src_file, open(dst) as dst_file:
        src_text = src_file.readlines()
        dst_text = dst_file.readlines()
        diff_text = difflib.unified_diff(dst_text, src_text,
                                         fromfile=dst,
                                         tofile=os.path.basename(src))
        print(''.join(list(diff_text)))
        print('\n')


def verify_location():
    if not os.path.exists(app_path('public')):
        raise RuntimeError("Configuration must be run from base directory with"
                           " your application code located in a 'public/' "
                           "sub-directory.")
