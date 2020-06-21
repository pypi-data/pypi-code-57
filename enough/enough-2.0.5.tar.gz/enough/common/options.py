import os

from enough import settings


def set_options(parser):
    parser.add_argument('--driver', default='openstack')
    parser.add_argument('--inventory', action='append')
    o = parser.add_argument_group(title='OpenStack',
                                  description='Only when --driver=openstack')
    o.add_argument(
        '--clouds',
        default=os.environ.get('OS_CLIENT_CONFIG_FILE',
                               f'{settings.CONFIG_DIR}/inventory/group_vars/all/clouds.yml'),
        help='Path to the clouds.yml file')
    return parser
