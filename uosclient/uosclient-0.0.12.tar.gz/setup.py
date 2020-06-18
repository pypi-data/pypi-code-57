#!/usr/bin/env python3

"""Setup script"""

from setuptools import setup, find_packages

setup(
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['test']),
    use_scm_version=True,
    python_requires='>=3.7',
    setup_requires=[
        'setuptools_scm',
    ],
    install_requires=([
        'netaddr',
        'osc_lib',
        'passlib',
        'python-designateclient',
        'python-openstackclient',
    ]),
    entry_points={
        'openstack.common': [
            'uos_network_create=uosclient.network:CreateNetwork',
            'uos_network_delete=uosclient.network:DeleteNetwork',
            'uos_project_create=uosclient.project:CreateProject',
            'uos_project_delete=uosclient.project:DeleteProject',
            'uos_routing_port_create=uosclient.port:CreateRoutingPort',
            'uos_routing_port_delete=uosclient.port:DeleteRoutingPort',
            'uos_security_groups_fix=uosclient.secgroup:FixSecurityGroups',
            'uos_user_create=uosclient.user:CreateUser',
            'uos_user_delete=uosclient.user:DeleteUser',
        ],
    },
)
