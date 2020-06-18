from setuptools import setup, find_packages


setup(
    name='lhcb-copyright-plugins',
    version='0.0.1',
    packages=find_packages(),
    entry_points='''
        [lb_dev.plugins]
        create-license-file=create_license_file.create_license_file:create_license_file_command
        check-for-license=check_for_license_file.check_for_license:check_for_license_command
    '''
)