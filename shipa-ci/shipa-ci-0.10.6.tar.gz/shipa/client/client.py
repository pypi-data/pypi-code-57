import json
import requests

from schematics.exceptions import ValidationError, DataError
from shipa.client.types import AddNodeRequest, UpdatePoolRequest, AddPoolRequest, AddAppRequest, DeployAppRequest, \
    MoveAppRequest, RemovePoolRequest, AddClusterRequest
from shipa.commands.constant import KUBERNETES_PROVISIONER
from shipa.utils import RepositoryFolder, parse_step_interval

CONST_TEST_TOKEN = "test-token"
CONST_TEST_SERVER = "test-server"


class ShipaException(Exception):
    pass


class ShipaClient(object):

    def __init__(self, server, client, email=None, password=None, token=None, verbose=False):
        self.server = server
        if not server.startswith('http'):
            self.urlbase = 'http://{0}'.format(server)
        else:
            self.urlbase = server

        self.email = email
        self.password = password
        self.token = token
        self.verbose = verbose
        self.http = client

        if token is not None:
            self.headers = {"Authorization": "bearer " + self.token}
            self.json_headers = {"Authorization": "bearer " + self.token, 'Content-Type': 'application/json',
                                 'Accept': 'application/json'}

    def print_response(self, response):
        if self.verbose:
            print(response.text)
            print(response.status_code)

    def auth(self):
        if self.email is None or self.password is None:
            raise ShipaException('Please, provide email and password')

        url = '{0}/users/{1}/tokens'.format(self.urlbase, self.email)
        params = {'password': self.password}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        try:
            r = self.http.post(url, params=params, headers=headers)
            self.print_response(r)

            if r.status_code != 200:
                raise ShipaException('Invalid token or user/password ({0})'.format(r.text))

            self.token = r.json()['token']
            self.headers = {"Authorization": "bearer " + self.token}
            self.json_headers = {"Authorization": "bearer " + self.token, 'Content-Type': 'application/json',
                                 'Accept': 'application/json'}

        except requests.ConnectionError:
            raise ShipaException("Shipa server connection error")

    def app_deploy(self, appname, directory='.', steps=1, step_interval='1s', step_weight=300):
        files = None
        try:
            url = '{0}/apps/{1}/deploy'.format(self.urlbase, appname)

            if self.server is not CONST_TEST_SERVER:
                folder = RepositoryFolder(directory, verbose=self.verbose)
                file = folder.create_tarfile()
                files = {'file': file}

            request = DeployAppRequest({'steps': steps, 'step_interval': parse_step_interval(step_interval),
                                        'step_weight': step_weight})
            request.validate()

            r = self.http.post(url, files=files, headers=self.headers, data=request.to_primitive())
            self.print_response(r)
            if r.text is None:
                raise ShipaException(r.text)

            ok = any(line.strip() == "OK" for line in r.text.split('\n'))

            if ok is False:
                raise ShipaException(r.text)

        except requests.ConnectionError as e:
            raise ShipaException(e)
        except ValidationError as e:
            raise ShipaException(e)
        except DataError as e:
            raise ShipaException(e)

    def app_create(self, appname, team, pool, platform=None, description=None, dependency_files=tuple(), tags=tuple(),
                   plan=None, router=None, router_opts=dict()):
        try:
            url = '{0}/apps'.format(self.urlbase)

            request = AddAppRequest({'name': appname, 'platform': platform, 'plan': plan, 'teamOwner': team,
                                     'description': description, 'pool': pool, 'router': router,
                                     'dependency_files': dependency_files, 'tags': tags,
                                     'router_opts': router_opts})
            request.validate()

            r = self.http.post(url, headers=self.json_headers, data=json.dumps(request.to_primitive()))
            self.print_response(r)
            if r.status_code != 201:
                raise ShipaException(r.text)

            out = json.loads(r.text)
            if out['status'] != 'success':
                raise ShipaException(out['status'])

            print('App {0} has been created!'.format(appname))
            print('Use app-info to check the status of the app and its units')
            if out['repository_url'] is not None:
                print('Your repository for {0} project is {1}'.format(appname, out['repository_url']))

        except requests.ConnectionError as e:
            raise ShipaException(e)
        except ValidationError as e:
            raise ShipaException(e)
        except DataError as e:
            raise ShipaException(e)

    def app_remove(self, appname):
        try:
            url = '{0}/apps/{1}'.format(self.urlbase, appname)

            r = self.http.delete(url, headers=self.headers)
            self.print_response(r)
            if r.status_code != 200:
                raise ShipaException(r.text)

            responses = r.text.split('\n')
            for response in responses:
                if response.find("Message") < 0:
                    continue
                out = json.loads(response)
                print(out['Message'].replace('\n', ''))

        except requests.ConnectionError as e:
            raise ShipaException(e)
        except AttributeError:
            print('Done removing application.')

    def autoscale_check(self):
        try:
            print('running autoscale checks')
            url = '{0}/node/autoscale/run'.format(self.urlbase)

            r = self.http.post(url, headers=self.headers)
            self.print_response(r)
            if r.text is None:
                raise ShipaException(r.text)

            if "Node Autoscaler available only" in r.text:
                raise ShipaException(r.text)

            responses = r.text.split('\n')
            for response in responses:
                if response.find("Message") < 0:
                    continue
                out = json.loads(response)
                print(out['Message'].replace('\n', ''))

        except requests.ConnectionError as e:
            raise ShipaException(e)

    def app_move(self, appname, pool):
        url = '{0}/apps/{1}/move'.format(self.urlbase, appname)

        try:
            request = MoveAppRequest({'pool': pool})
            request.validate()

            r = self.http.post(url, headers=self.headers, data=request.to_primitive())
            self.print_response(r)
            if r.text is None:
                raise ShipaException(r.text)

            ok = any(line.strip() == "OK" for line in r.text.split('\n'))
            if ok is False:
                raise ShipaException(r.text.replace('\n\n', ''))

        except requests.ConnectionError as e:
            raise ShipaException(e)
        except ValidationError as e:
            raise ShipaException(e)
        except DataError as e:
            raise ShipaException(e)

    def pool_add(self, pool, default=False, public=False, accept_drivers=tuple(), app_quota_limit=None,
                 provisioner=None, plan=None, kubernetes_namespace=None):

        try:
            url = '{0}/pools'.format(self.urlbase)

            request = AddPoolRequest({'name': pool, 'public': public, 'default': default,
                                      'provisioner': provisioner, 'plan': plan, 'accept_drivers': accept_drivers,
                                      'kubernetes_namespace': kubernetes_namespace, 'app_quota_limit': app_quota_limit})
            request.validate()

            r = self.http.post(url, headers=self.headers, data=request.to_primitive())
            self.print_response(r)
            if r.status_code != 201:
                raise ShipaException(r.text)

        except requests.ConnectionError as e:
            raise ShipaException(e)
        except ValidationError as e:
            raise ShipaException(e)
        except DataError as e:
            raise ShipaException(e)

    def pool_remove(self, pool):

        try:
            url = '{0}/pools/{1}'.format(self.urlbase, pool)

            r = self.http.delete(url, headers=self.headers)
            self.print_response(r)
            if r.status_code != 200:
                raise ShipaException(r.text)

        except requests.ConnectionError as e:
            raise ShipaException(e)

    def pool_update(self, pool, default=False, public=False, accept_drivers=tuple(), app_quota_limit=None, plan=None):
        try:
            url = '{0}/pools/{1}'.format(self.urlbase, pool)
            request = UpdatePoolRequest({'public': public, 'default': default, 'plan': plan,
                                         'app_quota_limit': app_quota_limit, 'accept_drivers': accept_drivers})
            request.validate()

            r = self.http.put(url, headers=self.headers, data=request.to_primitive())
            self.print_response(r)
            if r.status_code != 200:
                raise ShipaException(r.text)

        except requests.ConnectionError as e:
            raise ShipaException(e)
        except ValidationError as e:
            raise ShipaException(e)
        except DataError as e:
            raise ShipaException(e)

    def file_read(self, path=None):
        try:
            if path is not None:
                with open(path, "r") as f:
                    return f.read()
            return None
        except IOError as e:
            raise ShipaException(e)

    def node_add(self, pools=tuple(), iaas=None, iaasid=None, address=None, template=None, driver=None,
                 cacert=None, clientcert=None, clientkey=None, register=False):

        try:
            url = '{0}/node'.format(self.urlbase)

            request = AddNodeRequest({'register': register, 'pool': pools[0], 'alternative_pools': pools[1:],
                                      'client_key': self.file_read(clientkey),
                                      'client_cert': self.file_read(clientcert), 'ca_cert': self.file_read(cacert),
                                      'meta_data': {'driver': driver, 'address': address, 'iaas': iaas,
                                                    'iaas_id': iaasid, 'template': template}})
            request.validate()

            r = self.http.post(url, headers=self.json_headers, data=json.dumps(request.to_primitive()))
            self.print_response(r)
            if r.status_code != 201:
                raise ShipaException(r.text)

        except requests.ConnectionError as e:
            raise ShipaException(e)
        except ValidationError as e:
            raise ShipaException(e)
        except DataError as e:
            raise ShipaException(e)

    def node_remove(self, address, no_rebalance=False, destroy=False):
        try:
            url = '{0}/node'.format(self.urlbase, address)

            request = RemovePoolRequest({'address': address, 'destroy': destroy, 'no_rebalance': no_rebalance})
            request.validate()

            r = self.http.delete(url, headers=self.headers, params=request.to_primitive())
            self.print_response(r)
            if r.status_code != 200:
                raise ShipaException(r.text)

        except requests.ConnectionError as e:
            raise ShipaException(e)
        except ValidationError as e:
            raise ShipaException(e)
        except DataError as e:
            raise ShipaException(e)

    def cluster_add(self, name, address=tuple(), default=None, pools=tuple(), teams=tuple(), token=None,
                    ingress_service=None, ingress_ip=None, ingress_port=0, ca_cert=None,
                    client_cert=None, client_key=None, provisioner=KUBERNETES_PROVISIONER,
                    custom_data=dict()):

        try:
            url = '{0}/provisioner/clusters'.format(self.urlbase)

            request = AddClusterRequest({'name': name, 'address': address, 'default': default, 'teams': teams,
                                         'token': token, 'ingress_service': ingress_service, 'ingress_ip': ingress_ip,
                                         'ingress_port': ingress_port, 'ca_cert': ca_cert, 'pools': pools,
                                         'client_cert': client_cert, 'client_key': client_key,
                                         'provisioner': provisioner, 'custom_data': custom_data})
            request.validate()

            r = self.http.post(url, headers=self.json_headers, data=json.dumps(request.to_primitive()))
            self.print_response(r)
            if r.status_code != 201:
                raise ShipaException(r.text)

        except requests.ConnectionError as e:
            raise ShipaException(e)
        except ValidationError as e:
            raise ShipaException(e)
        except DataError as e:
            raise ShipaException(e)

    def cluster_remove(self, name):
        try:
            url = '{0}/provisioner/clusters/{1}'.format(self.urlbase, name)

            r = self.http.delete(url, headers=self.headers)
            self.print_response(r)
            if r.status_code != 200:
                raise ShipaException(r.text)

        except requests.ConnectionError as e:
            raise ShipaException(e)
