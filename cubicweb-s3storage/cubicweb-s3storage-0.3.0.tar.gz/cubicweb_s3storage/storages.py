# copyright 2018 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of CubicWeb.
#
# CubicWeb is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# CubicWeb is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with CubicWeb.  If not, see <http://www.gnu.org/licenses/>.

"""custom storages for S3"""

import uuid
from logging import getLogger

from six import PY3
import os
import boto3

from cubicweb import Binary, set_log_methods
from cubicweb.server.sources.storages import Storage
from cubicweb.server.edition import EditedEntity


class S3Storage(Storage):
    is_source_callback = True

    def __init__(self, bucket):
        self.s3cnx = self._s3_client()
        self.bucket = bucket

    @classmethod
    def _s3_client(cls):
        endpoint_url = os.environ.get('AWS_S3_ENDPOINT_URL')
        if endpoint_url:
            cls.debug('Using custom S3 endpoint url {}'.format(endpoint_url))
        return boto3.client('s3',
                            endpoint_url=endpoint_url)

    def callback(self, source, cnx, value):
        """see docstring for prototype, which vary according to is_source_callback
        """
        key = source.binary_to_str(value).decode()
        try:
            return Binary(self.s3cnx.get_object(
                Bucket=self.bucket, Key=key)['Body'].read())
        except Exception as ex:
            source.critical("can't retrive S3 object %s: %s", value, ex)
            return None

    def entity_added(self, entity, attr):
        """an entity using this storage for attr has been added"""
        binary = entity.cw_edited.pop(attr)
        if binary is not None:
            key = self.get_s3_key(entity, attr)
            # bytes storage used to store S3's object key
            binary_obj = Binary(key.encode())
            entity.cw_edited.edited_attribute(attr, binary_obj)
            # required workaround for boto3 bug
            # https://github.com/boto/s3transfer/issues/80
            # .read() is required since Binary can't wrap itself
            buffer = Binary(binary.read())
            self.debug('Upload object to S3')
            # upload_fileobj should make automagically a multipart upload if
            # needed
            self.s3cnx.upload_fileobj(buffer, self.bucket, key)
            buffer.close()
            self.info('Uploaded object %s.%s to S3', entity.eid, attr)
        return binary

    def entity_updated(self, entity, attr):
        """an entity using this storage for attr has been updatded"""
        return self.entity_added(entity, attr)

    def entity_deleted(self, entity, attr):
        """an entity using this storage for attr has been deleted"""
        if entity._cw.repo.config['s3-auto-delete']:
            key = self.get_s3_key(entity, attr)
            self.info('Deleting object %s.%s (%s/%s) from S3',
                      entity.eid, attr, self.bucket, key)
            resp = self.s3cnx.delete_object(Bucket=self.bucket, Key=key)
            if resp.get('ResponseMetadata', {}).get('HTTPStatusCode') >= 300:
                self.error('S3 object deletion FAILED: %s', resp)
            else:
                self.debug('S3 object deletion OK: %s', resp)

    def migrate_entity(self, entity, attribute):
        """migrate an entity attribute to the storage"""
        entity.cw_edited = EditedEntity(entity, **entity.cw_attr_cache)
        binary = self.entity_added(entity, attribute)
        if binary is not None:
            cnx = entity._cw
            source = cnx.repo.system_source
            attrs = source.preprocess_entity(entity)
            sql = source.sqlgen.update('cw_' + entity.cw_etype, attrs,
                                       ['cw_eid'])
            source.doexec(cnx, sql, attrs)
        entity.cw_edited = None

    def get_s3_key(self, entity, attr):
        """
        Return the S3 key of the S3 object storing the content of attribute
        attr of the entity.

        If the given entity already has a key (eg. at entity creation time),
        a new  key is generated.

        """
        try:
            rset = entity._cw.execute(
                'Any stkey(D) WHERE X eid %s, X %s D' %
                (entity.eid, attr))
        except NotImplementedError:
            # may occur when called from migrate_entity, ie. when the storage
            # has not yet been installed
            rset = None
        if rset and rset.rows[0][0]:
            key = rset.rows[0][0].getvalue()
            if PY3:
                key = key.decode()
            return key
        return self.new_s3_key(entity, attr)

    def new_s3_key(self, entity, attr):
        """Generate a new key for given entity attr.

        This implemenation just return a random UUID"""
        return str(uuid.uuid1())


set_log_methods(S3Storage,
                getLogger('cube.s3storage.storages.s3storage'))
