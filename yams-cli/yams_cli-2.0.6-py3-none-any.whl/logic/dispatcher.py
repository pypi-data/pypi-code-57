#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import json
import os
import sys
import time
import signal
import urllib
import re
import tempfile
import urllib.parse

from injector import inject
from requests import ConnectionError
from datetime import datetime
from yams_cli.logic.core.manager import Manager
from yams_cli.profile import Profile
from yams_cli.utils import generate_pretty_print, id_generator, configure_logging, str2bool, dispatcher_exception_safe, \
    get_directory

log = logging.getLogger('yams-cli.dispatcher')

DEFAULT_BUCKET_STATICS = "false"
DEFAULT_BUCKET_MAX_AGE = 259200  # 3 days


class Dispatcher(object):
    @inject
    def __init__(self, manager: Manager, profile: Profile):
        self._manager = manager
        self._profile = profile

    @property
    def tenant_id(self):
        return self._profile.get_profile_value('tenant_id')

    # ######################################################
    # TENANTS
    # ######################################################

    @dispatcher_exception_safe(Exception)
    def tenant_info(self, args):
        tenant = self._manager.get_tenant(self.tenant_id)
        self.show_result(tenant)
        return True

    @dispatcher_exception_safe(Exception)
    def tenant_list(self, args):
        result = self._manager.get_tenants()
        self.show_result(result)
        return True

    @dispatcher_exception_safe(Exception)
    def tenant_delete(self, args):
        self._manager.delete_tenant(self.tenant_id)
        log.info("Tenant successfully deleted")
        return True

    # ######################################################
    # DISTRIBUTIONS
    # ######################################################
    @dispatcher_exception_safe(Exception)
    def distribution_info(self, args):
        distribution_id = args['distribution_id']
        distribution_info = self._manager.get_distribution(self.tenant_id, distribution_id)
        self.show_result(distribution_info)
        return True

    @dispatcher_exception_safe(Exception)
    def distribution_list(self, args):
        result = self._manager.get_distributions(self.tenant_id)
        self.show_result(result)
        return True

    @dispatcher_exception_safe(Exception)
    def distribution_create(self, args):
        dns_name = args['dns_name']
        result = self._manager.create_distribution(self.tenant_id, dns_name)
        self.show_result(result)
        return True

    @dispatcher_exception_safe(Exception)
    def distribution_delete(self, args):
        distribution_id = args['distribution_id']
        self._manager.delete_distribution(self.tenant_id, distribution_id)
        log.info("Distribution is in process of being deleted")
        return True

    # ######################################################
    # DOMAINS
    # ######################################################
    @dispatcher_exception_safe(Exception)
    def domain_info(self, args):
        domain_id = args['domain_id']
        domain_info = self._manager.get_domain(self.tenant_id, domain_id)
        self.show_result(domain_info)
        return True

    @dispatcher_exception_safe(Exception)
    def domain_list(self, args):
        result = self._manager.get_domains(self.tenant_id)
        self.show_result(result)
        return True

    @dispatcher_exception_safe(Exception)
    def domain_create(self, args):
        domain_name = args['domain_name']
        domain_status = args['domain_status']
        result = self._manager.create_domain(self.tenant_id, domain_name, domain_status)
        self.show_result({
            "tenant_id": result.tenant_id,
            "domain_id": result.domain_id,
            "alias": result.alias
        })
        return True

    @dispatcher_exception_safe(Exception)
    def domain_delete(self, args):
        domain_id = args['domain_id']
        self._manager.delete_domain(self.tenant_id, domain_id)
        log.info("Domain successfully deleted")
        return True

    # ######################################################
    # RULES
    # ######################################################
    @dispatcher_exception_safe(Exception)
    def rule_list(self, args):
        domain_id = args['domain_id']
        result = self._manager.get_rules(self.tenant_id, domain_id)
        self.show_result(result)
        return True

    @dispatcher_exception_safe(Exception)
    def rule_info(self, args):
        domain_id = args['domain_id']
        rule_id = args['rule_id']
        result = self._manager.get_rule(self.tenant_id, domain_id, rule_id)
        self.show_result(result)
        return True

    @dispatcher_exception_safe(Exception)
    def rule_create(self, args):
        domain_id = args['domain_id']
        rule_json = self._get_json_or_none(args, 'rule_json')
        create_rule_result = self._manager.create_rule(self.tenant_id, domain_id, rule_json)
        # log.info("create rule: {}".format(create_rule_result))
        self.show_result({
            "tenant_id": create_rule_result.tenant_id,
            "domain_id": create_rule_result.domain_id,
            "rule_id": create_rule_result.rule_id,
            "alias": create_rule_result.alias
        })
        return True

    @dispatcher_exception_safe(Exception)
    def rule_delete(self, args):
        domain_id = args['domain_id']
        rule_id = args['rule_id']
        self._manager.delete_rule(self.tenant_id, domain_id, rule_id)
        log.info("Rule successfully deleted")
        return True

    @dispatcher_exception_safe(Exception)
    def rule_update(self, args):
        domain_id = args['domain_id']
        rule_id = args['rule_id']
        rule_json = self._get_json_or_none(args, 'rule_json')
        result = self._manager.update_rule(self.tenant_id, domain_id, rule_id, rule_json)
        self.show_result(result)
        return True

    # ######################################################
    # POLICIES
    # ######################################################
    @dispatcher_exception_safe(Exception)
    def policy_list(self, args):
        result = self._manager.get_policies(self.tenant_id)
        self.show_result(result)
        return True

    @dispatcher_exception_safe(Exception)
    def policy_info(self, args):
        policy_id = args['policy_id']
        result = self._manager.get_policy(self.tenant_id, policy_id)
        self.show_result(result)
        return True

    @dispatcher_exception_safe(Exception)
    def policy_create(self, args):
        policy_json = self._get_json_or_none(args, 'policy_json')
        create_policy_result = self._manager.create_policy(self.tenant_id, policy_json)
        self.show_result({
            "tenant_id": create_policy_result.tenant_id,
            "policy_id": create_policy_result.policy_id
        })
        return True

    @dispatcher_exception_safe(Exception)
    def policy_update(self, args):
        policy_json = self._get_json_or_none(args, 'policy_json')
        policy_id = args['policy_id']
        result = self._manager.update_policy(self.tenant_id, policy_id, policy_json)
        self.show_result(result)
        return True

    @dispatcher_exception_safe(Exception)
    def policy_delete(self, args):
        policy_id = args['policy_id']
        self._manager.delete_policy(self.tenant_id, policy_id)
        log.info("Policy successfully deleted")
        return True

    # ######################################################
    # ACCESS-KEYS
    # ######################################################
    @dispatcher_exception_safe(Exception)
    def accesskey_list(self, args):
        result = self._manager.get_access_keys(self.tenant_id)
        self.show_result(result)
        return True

    @dispatcher_exception_safe(Exception)
    def accesskey_info(self, args):
        accesskey_id = args['accesskey_id']
        result = self._manager.get_access_key(self.tenant_id, accesskey_id)
        self.show_result(result)
        return True

    @dispatcher_exception_safe(Exception)
    def accesskey_create(self, args):
        description = args.get('description')
        result = self._manager.create_access_key(self.tenant_id, description)
        self.show_result({
            "tenant_id": result.tenant_id,
            "access_key_id": result.access_key_id,
            "private_key": result.private_key
        })
        return True

    @dispatcher_exception_safe(Exception)
    def accesskey_provide(self, args):
        public_key = args['public_key']
        description = args.get('description')
        result = self._manager.provide_access_key(self.tenant_id, public_key, description)
        self.show_result({
            "tenant_id": result.tenant_id,
            "access_key_id": result.access_key_id
        })
        return True

    @dispatcher_exception_safe(Exception)
    def accesskey_update(self, args):
        accesskey_id = args['accesskey_id']
        description = args.get('description')
        active = None
        if args.get('enable'):
            active = True
        if args.get('disable'):
            active = False
        result = self._manager.update_access_key(self.tenant_id, accesskey_id, active, description)
        self.show_result(result)
        return True

    @dispatcher_exception_safe(Exception)
    def accesskey_delete(self, args):
        accesskey_id = args['accesskey_id']
        self._manager.delete_access_key(self.tenant_id, accesskey_id)
        log.info("AccessKey successfully deleted")
        return True

    # ######################################################
    # ATTACHED-POLICIES
    # ######################################################
    @dispatcher_exception_safe(Exception)
    def accesskey_list_policies(self, args):
        accesskey_id = args['accesskey_id']
        result = self._manager.get_attached_policies(self.tenant_id, accesskey_id)
        self.show_result(result)
        return True

    @dispatcher_exception_safe(Exception)
    def accesskey_attach_policy(self, args):
        accesskey_id = args['accesskey_id']
        policy_id = args['policy_id']
        result = self._manager.attach_policy(self.tenant_id, accesskey_id, policy_id)
        self.show_result(result)
        return True

    @dispatcher_exception_safe(Exception)
    def accesskey_detach_policy(self, args):
        accesskey_id = args['accesskey_id']
        policy_id = args['policy_id']
        result = self._manager.detach_policy(self.tenant_id, accesskey_id, policy_id)
        self.show_result(result)
        return True

    # ######################################################
    # WATERMARKS
    # ######################################################
    @dispatcher_exception_safe(Exception)
    def watermark_list(self, args):
        domain_id = args['domain_id']
        result = self._manager.list_watermarks(self.tenant_id, domain_id)
        self.show_result(result)
        return True

    @dispatcher_exception_safe(Exception)
    def watermark_fetch(self, args):
        domain_id = args['domain_id']
        watermark_id = args['watermark_id']
        filename = args.get('watermark_file')
        if filename is None:
            if args.get('store_file'):
                filename = '{}/{}'.format(tempfile.gettempdir(), watermark_id)

        result = self._manager.get_watermark(self.tenant_id, domain_id, watermark_id)
        if filename:
            with open(filename, 'wb') as f:
                f.write(result.content)
                log.info("Object file saved at {}".format(filename))
        return True

    @dispatcher_exception_safe(Exception)
    def watermark_create(self, args):
        watermark_file = args['watermark_file']
        alias = args.get('alias')

        if not os.path.exists(watermark_file):
            log.error("Given watermark file does not exist: {}".format(watermark_file))
            return False

        if os.path.isdir(watermark_file):
            log.error("Given watermark file is a directory: {}".format(watermark_file))
            return False

        domain_id = args['domain_id']
        log.info("Uploading watermark '{}' into domain '{}'".format(watermark_file, domain_id))
        with open(watermark_file, 'rb') as f:
            file_data = f.read()
        result = self._manager.create_watermark(self.tenant_id, domain_id, alias, file_data)
        self.show_result({
            "tenant_id": result.tenant_id,
            "domain_id": result.domain_id,
            "watermark_id": result.watermark_id
        })
        return True

    @dispatcher_exception_safe(Exception)
    def watermark_update(self, args):
        domain_id = args['domain_id']
        watermark_id = args['watermark_id']
        alias = args.get('alias')
        result = self._manager.update_watermark(self.tenant_id, domain_id, watermark_id, alias)
        self.show_result(result)
        return True

    @dispatcher_exception_safe(Exception)
    def watermark_delete(self, args):
        domain_id = args['domain_id']
        watermark_id = args['watermark_id']
        self._manager.delete_watermark(self.tenant_id, domain_id, watermark_id)
        log.info("Watermark successfully deleted")
        return True

    # ######################################################
    # METRICS
    # ######################################################
    @dispatcher_exception_safe(Exception)
    def metrics_list(self, args):
        domain_id = args.get('domain_id')
        bucket_id = args.get('bucket_id')
        result = self._manager.get_bucket_metric_names(self.tenant_id, domain_id, bucket_id)
        self.show_result(result)
        return True

    @dispatcher_exception_safe(Exception)
    def metrics_info(self, args):
        domain_id = args.get('domain_id')
        bucket_id = args.get('bucket_id')
        metric_name = args.get('metric_name')
        year_month = args['year_month']
        result = self._manager.get_bucket_metric(self.tenant_id, domain_id, bucket_id, metric_name, year_month)
        self.show_result(result)
        return True

    # ######################################################
    # BUCKETS
    # ######################################################
    @dispatcher_exception_safe(Exception)
    def bucket_list(self, args):
        domain_id = args['domain_id']
        result = self._manager.get_buckets(self.tenant_id, domain_id)
        self.show_result(result)
        return True

    @dispatcher_exception_safe(Exception)
    def bucket_info(self, args):
        domain_id = args['domain_id']
        bucket_id = args['bucket_id']
        self.show_result(self._manager.get_bucket(self.tenant_id, domain_id, bucket_id))
        return True

    @dispatcher_exception_safe(Exception)
    def bucket_create(self, args):
        domain_id = args['domain_id']
        bucket_name = args['bucket_name']
        bucket_region = args['bucket_region']

        bucket_statics = args.get('bucket_statics')
        if bucket_statics is None:
            bucket_statics = DEFAULT_BUCKET_STATICS
        bucket_statics = str2bool(bucket_statics)

        bucket_cache_max_age = args.get('bucket_cache_max_age')
        if bucket_cache_max_age is None:
            bucket_cache_max_age = DEFAULT_BUCKET_MAX_AGE

        result = self._manager.create_bucket(self.tenant_id, domain_id, bucket_name, bucket_region,
                                             bucket_statics, bucket_cache_max_age)
        self.show_result({
            "tenant_id": result.tenant_id,
            "domain_id": result.domain_id,
            "bucket_id": result.bucket_id,
            "alias": result.alias
        })
        return True

    @dispatcher_exception_safe(Exception)
    def bucket_update(self, args):
        domain_id = args['domain_id']
        bucket_id = args['bucket_id']
        bucket_name = args.get('bucket_name')
        bucket_cache_max_age = args.get('bucket_cache_max_age')

        bucket_statics = args.get('bucket_statics')
        if bucket_statics:
            bucket_statics = str2bool(bucket_statics)

        result = self._manager.update_bucket(self.tenant_id, domain_id, bucket_id, bucket_name,
                                             bucket_statics, bucket_cache_max_age)
        self.show_result(result)
        return True

    @dispatcher_exception_safe(Exception)
    def bucket_delete(self, args):
        domain_id = args['domain_id']
        bucket_id = args['bucket_id']
        self._manager.delete_bucket(self.tenant_id, domain_id, bucket_id)
        log.info("Bucket successfully deleted")
        return True

    # ######################################################
    # OBJECTS
    # ######################################################
    @dispatcher_exception_safe(Exception)
    def object_describe(self, args):
        domain_id = args['domain_id']
        bucket_id = args['bucket_id']
        object_id = args['object_id']

        print(self._manager.head_object(self.tenant_id, domain_id, bucket_id, object_id))
        return True

    @dispatcher_exception_safe(Exception)
    def object_fetch(self, args):
        domain_id = args['domain_id']
        bucket_id = args['bucket_id']
        object_id = args['object_id']
        filename = args.get('directory')
        if filename is None:
            filename = "{}".format(urllib.parse.unquote(object_id))
        else:
            filename += "/{}".format(urllib.parse.unquote(object_id))

        filename = re.sub(r"/+", "/", filename)

        if "/" in filename:
            directory = get_directory(filename)

            if not os.path.exists(directory):
                os.makedirs(directory)

        get_object_result = self._manager.get_object(self.tenant_id, domain_id, bucket_id, object_id)
        with open(filename, 'wb') as f:
            f.write(get_object_result.content)
            log.info("Object file saved at {}".format(filename))
        return True

    @dispatcher_exception_safe(Exception)
    def object_list(self, args):
        domain_id = args['domain_id']
        bucket_id = args['bucket_id']
        options = {}
        if args.get("show_recoverable"):
            options["show-recoverable"] = True

        if args.get('prefix'):
            options['prefix'] = args['prefix']

        if args.get('list_backup'):
            options['list-backup'] = True

        self.print_object_header(args)

        token = None
        while True:
            content = self._manager.list_objects(self.tenant_id, domain_id, bucket_id, options, token)

            token = content.get('continuation_token')
            objects = content.get('objects')

            for record in objects:
                self.print_object_record(record, args)

            if token is None:
                break

        return True

    @staticmethod
    def print_object_header(args):
        if args.get('with_headers'):
            line = "object_id"
            if args.get('long'):
                line = "size\tmd5\tlast_modified\tobject_id"

            if args.get('show_recoverable'):
                line += "\tdeleted"

            print(line)

    @staticmethod
    def print_object_record(record, args):
        line = record.get('object_id')
        if args.get('long'):
            ts = int(record.get('last_modified')/1000)
            date_formatted = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            line = "{}\t{}\t{}\t{}".format(record.get('size'), record.get('md5'), date_formatted,
                                           record.get('object_id'))

        if args.get('show_recoverable'):
            line += "\t{}".format(record.get('deleted'))

        print(line)

    @dispatcher_exception_safe(Exception)
    def object_push(self, args):
        file_or_directory = args['object']
        if not os.path.exists(file_or_directory):
            log.error("Given file or path does not exist: {}".format(file_or_directory))
            return False

        domain_id = args['domain_id']
        bucket_id = args['bucket_id']

        expiration = args.get('expiration')
        if os.path.isdir(file_or_directory):
            recursive = args.get('recursive')
            if not recursive:
                log.error("Object path {} is a directory but --recursive was not set".format(file_or_directory))
                return False

            files = os.listdir(file_or_directory)

            for idx, file_name_dir in enumerate(files):
                files[idx] = os.path.join(file_or_directory, file_name_dir)

            files = filter(os.path.isfile, files)
            idx = 0
            result = True
            for file_name in files:
                log.info("Uploading {} into {}".format(file_name, bucket_id))
                result &= self._object_push(domain_id, bucket_id, file_name, "image_{}".format(idx), expiration)
                log.info("Uploaded {} into {}".format(file_name, bucket_id))
                idx += 1
            return result
        else:
            object_name = args['object_name']
            return self._object_push(domain_id, bucket_id, file_or_directory, object_name, expiration)

    def _object_push(self, domain_id, bucket_id, file_path, object_name=None, expiration=None):
        log.debug("Filename: {}".format(file_path))
        with open(file_path, 'rb') as f:
            file_data = f.read()
        result = self._manager.put_object(self.tenant_id, domain_id, bucket_id, object_name, file_data, expiration)

        self.show_result({
            "tenant_id": result.tenant_id,
            "domain_id": result.domain_id,
            "bucket_id": result.bucket_id,
            "object_id": result.object_id
        })
        return True

    @dispatcher_exception_safe(Exception)
    def object_remove(self, args):
        domain_id = args['domain_id']
        bucket_id = args['bucket_id']
        object_id = args['object_id']
        force = args.get('force', False)

        self._manager.delete_object(self.tenant_id, domain_id, bucket_id, object_id, force)
        return True

    # @dispatcher_exception_safe(Exception)
    def object_restore(self, args):
        domain_id = args['domain_id']
        bucket_id = args['bucket_id']
        object_id = args['object_id']

        self._manager.delete_delete_marker(self.tenant_id, domain_id, bucket_id, object_id)
        return True


    # ######################################################
    # OBJECTS METADATA
    # ######################################################
    @dispatcher_exception_safe(Exception)
    def object_metadata_info(self, args):
        domain_id = args['domain_id']
        bucket_id = args['bucket_id']
        object_id = args['object_id']

        self.show_result(self._manager.get_object_metadata(self.tenant_id, domain_id, bucket_id, object_id))
        return True

    def object_metadata_update(self, args):
        domain_id = args['domain_id']
        bucket_id = args['bucket_id']
        object_id = args['object_id']
        expiration = args.get('expiration')
        self._manager.update_object_metadata(self.tenant_id, domain_id, bucket_id, object_id, expiration)
        return True
    # ######################################################
    # PROCESSING
    # ######################################################
    @dispatcher_exception_safe(Exception)
    def processing_start(self, args):
        domain_id = args['domain_id']
        bucket_id = args['bucket_id']
        object_id = args['object_id']
        models = args['models'].split(',')

        self.show_result(self._manager.processing_start(self.tenant_id, domain_id, bucket_id, object_id, models))
        return True
    # ######################################################
    # IMAGES
    # ######################################################
    @dispatcher_exception_safe(Exception)
    def image_fetch(self, args):
        domain_id = args['domain_id']
        bucket_id = args['bucket_id']
        object_id = args['object_id']
        rule_id = args.get('rule_id')
        rule_json = args.get('rule_json')

        if rule_id:
            return self._manager.fetch_object(self.tenant_id, domain_id, bucket_id, object_id, rule_id)
        elif rule_json:
            rule_json = json.loads(rule_json)
            return self._manager.fetch_object_with_rule(self.tenant_id, domain_id, bucket_id, object_id, rule_json)
        else:
            log.warn("When fetching an image, --rule-id or --rule-json must be provided")
            return False

    # ######################################################
    # DOCUMENTS
    # ######################################################
    @dispatcher_exception_safe(Exception)
    def document_fetch(self, args):
        domain_id = args['domain_id']
        bucket_id = args['bucket_id']
        object_id = args['object_id']
        rule_id = args.get('rule_id')
        rule_json = args.get('rule_json')

        if rule_id:
            return self._manager.fetch_document(self.tenant_id, domain_id, bucket_id, object_id, rule_id)
        elif rule_json:
            rule_json = json.loads(rule_json)
            return self._manager.fetch_document_with_rule(self.tenant_id, domain_id, bucket_id, object_id, rule_json)
        else:
            log.warn("When fetching a document, --rule-id or --rule-json must be provided")
            return False

    # ######################################################
    # STATICS
    # ######################################################
    @dispatcher_exception_safe(Exception)
    def static_fetch(self, args):
        domain_id = args['domain_id']
        bucket_id = args['bucket_id']
        object_id = args['object_id']
        return self._manager.fetch_static_object(self.tenant_id, domain_id, bucket_id, object_id)

    # ######################################################
    # CONFIGURE
    # ######################################################
    def configure(self, args):
        """ Helper to create and configure credentials file.
        :param args:
        :return:
        """

        signal.signal(signal.SIGINT, self._signal_handler)

        # create credentials file if it doesn't exist
        created = self._profile.create_credentials_file_if_needed()
        tenant_id = input('[>] YAMS Tenant ID [{}]: '.format(self._profile.get_profile_value_or_none('tenant_id')))
        access_key_id = input("[>] YAMS Access Key ID [{}]: ".format(
            '****' if self._profile.get_profile_value_or_none('access_key_id') else "None"))
        private_secret_key = input("[>] YAMS Private Key [{}]: ".format(
            '****' if self._profile.get_profile_value_or_none('private_secret_key') else "None"))

        # once profile data recollected, create in profile file if it doesn't exist
        self._profile.create_profile(tenant_id, access_key_id, private_secret_key)

        print("[!] Profile file {} successfully!".format("created" if created else "updated"))
        return True

    # ######################################################
    # WIZARD
    # ######################################################
    def wizard(self, args):
        """ Wizard to easily create Domains, Buckets and test Objects upload and download. Using the management API.
        :param args:
        :return:
        """

        configure_logging('error')

        wizard_values = {
            'tenant_id': self.tenant_id,
            'domain_id': None,
            'bucket_id': None,
        }

        signal.signal(signal.SIGINT, self._signal_handler)

        if self._wizard_domains(wizard_values):
            if self._wizard_buckets(wizard_values):
                self._wizard_test_bucket(wizard_values)

        # wait 2 seconds before exiting wizard
        time.sleep(2)
        self._show_goodbye()
        return True

    def _wizard_domains(self, wizard_values):
        """ Shows the console to list, select or create a domain.
        :param wizard_values: dictionary. Selected tenant data.
        :return:
        """
        tenant_id = wizard_values['tenant_id']

        while True:
            try:
                response_get_domains = self._manager.get_domains(tenant_id)
            except ConnectionError:
                sys.exit(-1)
            except Exception as e:
                print("[E] Error retrieving the domains list. Aborting.")
                return False

            domains_list = self._wizard_show_domain_list(response_get_domains)
            create_condition = len(domains_list)
            exit_condition = create_condition + 1

            while True:
                option = input("> Choose option to select a Domain or perform an action: ")
                if option.isdigit():
                    optint = int(option)
                    if optint == create_condition:
                        domain_info = self._wizard_get_domain_info_from_input(tenant_id)
                        self._wizard_create_domain(domain_info)
                    elif optint == exit_condition:
                        self._show_goodbye()
                    else:
                        if optint > len(domains_list) or optint < 0:
                            print("Select domain out of range")
                            continue
                        wizard_values['domain_id'] = domains_list[optint]['id']
                        print("[I] Selected domain '{}' ('{}')".format(domains_list[optint]['name'],
                                                                       wizard_values['domain_id']))
                        return True
                    break

    def _wizard_show_domain_list(self, response_get_domains):
        domains_list = list(filter(lambda x: x['status'] == 'active', response_get_domains))
        # show list of domains and actions
        if len(domains_list) > 0:
            print("Select one of the existing domains to work with: ")
            for idx, domain in enumerate(domains_list):
                print("   {}. {} ({})".format(idx, domain['name'], domain['id']))
        else:
            print("No domain found.")

        self._show_extra_options(len(domains_list))

        return domains_list

    def _wizard_get_domain_info_from_input(self, tenant_id):
        domain_name = input("Write domain name: ")
        return {"tenant_id": tenant_id, "name": domain_name}

    def _wizard_create_domain(self, domain_info):
        try:
            created_domain = self._manager.create_domain(domain_info['tenant_id'], domain_info["name"], 'active')
        except Exception as e:
            print("[E] Error creating domain {}".format(e))
            sys.exit(-1)
        print("[I] Domain created successfully at 'tenants/{}/domains/{}'".format(
            created_domain.tenant_id, created_domain.domain_id))

        return created_domain

    def _wizard_buckets(self, wizard_values):
        """ Shows the console to list, select or create a bucket.
        :param wizard_values: dictionary. Selected tenant and domain data.
        :return:
        """
        tenant_id = wizard_values['tenant_id']
        domain_id = wizard_values['domain_id']

        while True:
            try:
                get_buckets_result = self._manager.get_buckets(tenant_id, domain_id)
            except Exception as e:
                print("[E] Error retrieving the buckets list. Aborting. {}".format(e))
                return False

            buckets_list = self._wizard_show_buckets(wizard_values['domain_id'], get_buckets_result)

            while True:
                option = input("[?] Choose which bucket to test or an extra action: ")
                if option.isdigit():
                    optint = int(option)
                    if optint == len(buckets_list):
                        bucket_info = self._wizard_get_bucket_info_from_input(tenant_id, domain_id)
                        self._wizard_create_bucket(bucket_info)
                    elif optint == len(buckets_list) + 1:
                        self._show_goodbye()
                    else:
                        wizard_values['bucket_id'] = buckets_list[optint]['bucket_id']
                        print("[I] Selected bucket '{}' ('{}')".format(
                            ",".join(x for x in buckets_list[optint]['aliases']), wizard_values['bucket_id']))
                        return True
                    break

    def _wizard_show_buckets(self, domain_id, get_buckets_result):
        # store only 'active' domains
        buckets_list = list(filter(lambda x: x['status'] == 'active', get_buckets_result))
        if len(buckets_list) > 0:
            print("Test one of the existing buckets for the domain '{}':".format(domain_id))
            # show list of domains
            for idx, bucket in enumerate(buckets_list):
                print("   {}. {} ({})".format(idx, ",".join(x for x in bucket['aliases']), bucket['bucket_id']))
        else:
            print("No bucket found.")

        # show actions
        self._show_extra_options(len(buckets_list))

        return buckets_list

    def _wizard_get_bucket_info_from_input(self, tenant_id, domain_id):
        bucket_name = input("Write bucket name: ")
        return {
            "tenant_id": tenant_id,
            "domain_id": domain_id,
            "name": bucket_name,
            "region": 'eu-west-1',
            "allow_statics": False,
            "cache_max_age": 3
        }

    def _wizard_create_bucket(self, bucket_info):
        try:
            create_bucket = self._manager.create_bucket(bucket_info['tenant_id'],
                                                        bucket_info['domain_id'],
                                                        bucket_info["name"],
                                                        bucket_info["region"],
                                                        bucket_info["allow_statics"],
                                                        bucket_info["cache_max_age"])

        except Exception as e:
            log.error("[E] Error creating bucket {}".format(e))
            sys.exit(-1)

        log.info("[I] bucket created successfully at '{}/{}/{}'"
                     .format(create_bucket.tenant_id, create_bucket.domain_id, create_bucket.bucket_id))
        return create_bucket

    def _wizard_test_bucket(self, wizard_values):
        """ Performs a test in the recently created bucket.
        Upload a plain .txt file, ownloads it and removes it.
        :param wizard_values: dictionary. Selected tenant, domain and bucket data.
        :return:
        """
        rand_name = "test-file-{}.txt".format(id_generator())
        object_content = "This is the plain text test file content. It's a trap!"
        print("[I] Trying to upload object: {} to bucket: {}".format(rand_name, wizard_values["bucket_id"]))
        try:
            self._manager.put_object(wizard_values['tenant_id'], wizard_values['domain_id'],
                                     wizard_values['bucket_id'],
                                     rand_name, object_content, None)
        except Exception as e:
            print("[E] Error putting object: {}".format(e))
            sys.exit(-1)

        print("[I] Created object '{}' into the bucket".format(rand_name))
        try:
            get_object_result = self._manager.get_object(wizard_values['tenant_id'],
                                                         wizard_values['domain_id'],
                                                         wizard_values['bucket_id'], rand_name)
        except Exception as e:
            print("[E] Error getting object '{}': {}".format(rand_name, e))
            sys.exit(-1)

        if get_object_result.content != object_content:
            print("[E] The fetched content doesn't match the sent one: \"{}\"".format(object_content))
            sys.exit(-1)

        print("[I] Fetched object '{}' with content: {}".format(rand_name, get_object_result.content))

        try:
            self._manager.delete_object(wizard_values['tenant_id'], wizard_values['domain_id'],
                                        wizard_values['bucket_id'], rand_name, False)
        except Exception as e:
            print("[E] Error deleting object '{}':".format(rand_name))
            sys.exit(-1)

        print("[I] Deleted object '{}'".format(rand_name))

        print("[I] Bucket tested successfully. Thanks for using the CLI wizard mode!")

    @staticmethod
    def _signal_handler(signum, frame):
        print("\n[I] Captured ^C signal. Aborting.")
        Dispatcher._show_goodbye()

    @staticmethod
    def show_result(result):
        try:
            print(generate_pretty_print(result))
        except ValueError:
            log.info("Content is binary and is not shown here")
            # raising a value error con content is because it's downloading a binary
            pass

    @staticmethod
    def _show_extra_options(starting_idx):
        if starting_idx == 0:
            print("Allowed actions:")
        else:
            print("Or:")
        print("   {}. Create new one".format(starting_idx))
        print("   {}. Exit".format(starting_idx + 1))

    @staticmethod
    def _show_goodbye():
        print('')
        print(' .d8888b.                         888 888                         888')
        print('d88P  Y88b                        888 888                         888')
        print('888    888                        888 888                         888')
        print('888         .d88b.   .d88b.   .d88888 88888b.  888  888  .d88b.   888')
        print('888  88888 d88""88b d88""88b d88" 888 888 "88b 888  888 d8P  Y8b  888')
        print('888    888 888  888 888  888 888  888 888  888 888  888 88888888  Y8P')
        print('Y88b  d88P Y88..88P Y88..88P Y88b 888 888 d88P Y88b 888 Y8b.       " ')
        print(' "Y8888P88  "Y88P"   "Y88P"   "Y88888 88888P"   "Y88888  "Y8888   888')
        print('                                                    888              ')
        print('                                               Y8b d88P              ')
        print('                                                "Y88P"               ')

        sys.exit(0)

    # ######################################################
    # UTILS
    # ######################################################
    @staticmethod
    def _get_json_or_none(args, param):
        if not args.get(param):
            return None
        return json.loads(args[param])
