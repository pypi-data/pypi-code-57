#!/usr/bin/env python3

# internal:
from fdroid_mirror_monitor.utils import get_logger, Generic
from fdroid_mirror_monitor.mirror import Mirror

# stdlib
import time

# external:
from fdroidserver import common, index, exception


class Repo(Generic):
    '''
    Repo
    '''

    instances = []
    log = get_logger(__name__)

    def __init__(
        self,
        address,
        fingerprint=None,
        rsync_pw=None,
        timeout=60,
        headers={'User-Agent': 'https://gitlab.com/marzzzello/mirror-monitor'},
    ):
        '''
        :param address: main repo addres
        :param fingerprint: repo fingerprint (often part of url address?fingerprint=ABCDEF1234567890)
        :param rsync_pw: optional rsync password
        :param timeout: timeout for various requests
        :param headers: http headers for various requests
        '''
        self.instances.append(self)

        self.url = address
        self.fingerprint = fingerprint
        self.rsync_pw = rsync_pw
        self.timeout = timeout
        self.headers = headers

        self.init_protocols()
        self.main_mirror = Mirror(self.url, rsync_pw=rsync_pw, timeout=timeout, headers=headers)
        self.integrated_mirrors = []
        self.additional_mirrors = []
        self.errors = {}

    def get_all(self, tries=1):
        '''
        - get index version
        - get index
        - get infos from index
        :param tries: if get fails retry after waiting period again
        :return: success True/False
        '''

        for t in range(tries):
            success = self.get_index_version()
            if success is False:
                if t + 1 < tries:
                    self.log.info(
                        'Trying again to get index version in %s seconds (%d/%d)' % (self.timeout, t + 2, tries)
                    )
                    time.sleep(self.timeout)
                else:
                    self.log.error('Failed to get index version')
                    return False
            else:
                break

        for t in range(tries):
            success = self.get_index()
            if success is False:
                if t + 1 < tries:
                    self.log.info('Trying again to get index in %s seconds (%d/%d)' % (self.timeout, t + 2, tries))
                    time.sleep(self.timeout)
                else:
                    self.log.error('Failed to get index')
                    return False
            else:
                break

        self.get_infos_from_index(minimal=False)
        return True

    def set_additional_mirrors(self, additional_mirrors):
        '''
        Set additional mirrors. Filter out self.main_mirror and self.integrated_mirrors

        :param additional_mirrors: list of Mirror objects
        '''
        for mirror_obj in additional_mirrors:
            if type(mirror_obj) != Mirror:
                self.log.error('additional_mirrors must be a list of Mirror objects (got %s)' % type(mirror_obj).__name__)
                return

            if mirror_obj == self.main_mirror:
                continue

            for integrated_mirror in self.integrated_mirrors:
                if mirror_obj == integrated_mirror:
                    continue

            self.additional_mirrors.append(mirror_obj)

    def get_index_version(self):
        '''
        Check for index files index-v1.jar and index.jar
        prefer index-v1.jar
        output to self.index_file
        :return: success: True/False
        '''
        current = 'index-v1.jar'
        legacy = 'index.jar'

        urls = [self.url]

        for mirror in self.integrated_mirrors:
            urls.append(mirror.url)
        for mirror in self.additional_mirrors:
            urls.append(mirror.url)

        for url in urls:
            self.log.info('Checking repo index version from %s...' % url)
            current_url = url + current
            legacy_url = url + legacy
            try:
                if self.check_file(current_url) is True:
                    self.index_file = current
                    self.log.debug('Index version is %s', current)
                    return True
            except Exception as e:
                self.log.debug('%s: %s' % (url, str(e)))
                current_exception = str(e)

            try:
                if self.check_file(legacy_url) is True:
                    self.index_file = legacy
                    self.log.debug('Index version is %s', legacy)
                    return True
                else:
                    # both legacy and current returned 404
                    self.index_file = None
                    self.log.error('Could not find an index file')
                    self.errors['index_version'] = 'Could not find an index file'
                    return False
            except Exception as e:
                self.log.debug('%s: %s' % (url, str(e)))
                if urls.index(url) < len(urls) - 1:
                    self.log.info('Trying different mirror...')
                else:
                    self.index_file = None
                    # maybe use e.response.status_code
                    err = 'Could not get index version: %s; %s' % (str(e), current_exception)
                    self.log.error(err)
                    self.errors['index_version'] = err
                    return False

    def get_index(self):
        '''
        Downloads self.index_file from main mirror.\n
        If main mirror times out try other mirrors.\n
        If self.fingerprint is set it gets verified.\n
        The index is saved under self.index\n
        :return: success: True/False
        '''
        config = dict()
        config['jarsigner'] = 'jarsigner'
        common.config = config
        index.config = config

        urls = [self.url]

        for mirror in self.integrated_mirrors:
            urls.append(mirror.url)
        for mirror in self.additional_mirrors:
            urls.append(mirror.url)

        for url in urls:
            self.log.info('Getting repo index from %s/%s...' % (url.rstrip('/'), self.index_file))
            if self.index_file == 'index.jar':
                self.index = None
                err = 'Legacy index not supported (yet)'
                self.log.error(err)
                self.errors['get_index'] = err
                return False

            try:
                if self.fingerprint is not None:
                    self.index, _ = index.download_repo_index(
                        url.rstrip('/') + '?fingerprint=' + self.fingerprint, timeout=self.timeout
                    )
                else:
                    self.index, _ = index.download_repo_index(
                        url.rstrip('/'), verify_fingerprint=False, timeout=self.timeout
                    )
            except exception.VerificationException as e:
                self.index = None
                self.log.debug('%s: %s' % (e.value, e.detail))
                err = 'Could not verify fingerprint %s' % self.fingerprint
                self.log.error(err)
                self.errors['get_index'] = err
                self.fingerprint = None
                return False
            except Exception as e:
                self.log.debug('%s: %s' % (url, str(e)))
                if urls.index(url) < len(urls) - 1:
                    self.log.info('Trying different mirror...')
                else:
                    self.index = None
                    err = 'Could not download index for %s' % self.url
                    self.log.error(err)
                    self.errors['get_index'] = err
                    return False
            else:
                return True

    # TODO: maybe extract additional info from pubkey
    def get_infos_from_index(self, minimal=False):
        '''
        :minimal: if set to True, don't calculate sizes and number of apps/packages

        verify address and fingerprint

        add:
        - description
        - icon
        - maxage
        - integrated_mirrors
        - name
        - pubkey
        - timestamp
        - version

        - size_all_packages
        - size_current_packages
        - num_all_packages
        - num_current_packages
        - num_apps
        '''
        repo = self.index['repo']

        if self.url != repo['address'] and self.url != repo['address'] + '/':
            self.log.error('Address missmatch %s, %s' % (self.url, repo['address']))
            self.errors['address'] = 'missmatch %s, %s' % (self.url, repo['address'])

        if self.fingerprint is None:
            self.fingerprint = repo['fingerprint']
        else:
            if self.fingerprint != repo['fingerprint']:
                self.log.error('Fingerprint missmatch %s, %s' % (self.fingerprint, repo['fingerprint']))
                self.errors['fingerprint'] = 'missmatch %s, %s' % (self.fingerprint, repo['fingerprint'])
                self.fingerprint = repo['fingerprint']

        self.description = repo['description']
        self.icon = repo['icon']
        try:
            self.maxage = repo['maxage']
        except KeyError:
            pass
        try:
            for integrated_mirror in repo['mirrors']:
                self.integrated_mirrors.append(Mirror(integrated_mirror, timeout=self.timeout, headers=self.headers))
        except KeyError:
            pass
        self.name = repo['name']
        self.pubkey = repo['pubkey']
        self.timestamp = repo['timestamp']
        self.version = repo['version']

        if minimal is False:
            size_outdated = 0
            size_current = 0
            num_current_packages = 0
            num_outdated_packages = 0

            # there are apps that have multiple packages per versionName (for different hardware platforms)
            # size_current calculates the sum of all package sizes with the current versionName
            for package_name in self.index['packages']:
                i = 0
                current_version = 0
                for packages in self.index['packages'][package_name]:

                    # get current version from latest package:
                    if i == 0:
                        current_version = packages['versionName']
                        size_current += packages['size']
                        num_current_packages += 1
                    else:
                        older_version = packages['versionName']

                        if older_version == current_version:
                            size_current += packages['size']
                            num_current_packages += 1
                        else:
                            size_outdated += packages['size']
                            num_outdated_packages += 1

                    i += 1

            self.size_all_packages = size_current + size_outdated
            self.size_current_packages = size_current

            self.num_all_packages = num_current_packages + num_outdated_packages
            self.num_current_packages = num_current_packages

            self.num_apps = len(self.index['apps'])
