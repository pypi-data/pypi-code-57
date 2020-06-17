import datetime
import json
import logging
from google.cloud import firestore
from google.cloud.datastore.key import Key
from google.cloud import datastore

from .. import DataNumberLookup

class MiscConversion:
    def __init__(self, datastore_project, firestore_project):
        self.ds_client = datastore.Client(project=datastore_project)
        self.db = firestore.Client(project=firestore_project)

        self.company = 'Color_Orchids'
        self.applicationCT = 'Customer_Tracking'
        self.applicationAPI = 'Data_API'
        self.base_colls = ['reporting_config', 'application_data',
                           'data_number_sync', 'application_data', 'data_number_lookup']

        self.base_data = {'CompanyName': 'Color Orchids', 'ApplicationName': [
            'Customer Tracking', 'Sales Inventory', 'Data API']}

        for c in self.base_colls:
            coll = self.db.collection(c)
            doc = coll.document(self.company)
            doc.set(self.base_data)

        logging.info('loading from datastore...')
        self.ds_dict = {}
        misc_conv = ['ReportingConfig', 'ApiUser', 'ImageNumber', 'Image']

        self.misc_rename = {'ReportingConfig': 'reporting_config/'+self.company+'/'+self.applicationCT,
                            'ApiUser': 'application_data/'+self.company+'/'+self.applicationAPI,
                            'ImageNumber': 'data_number_sync/'+self.company+'/'+self.applicationCT,
                            'Image': 'application_data/'+self.company+'/'+self.applicationCT+'/StorageBlob/Image',
                            'DataNumberLookup': 'data_number_lookup/'+self.company}

        self.doc_name = {'ReportingConfig': 'name', 'ApiUser': 'userName',
                         'ImageNumber': 'name', 'Image': 'image_number', 'DataNumberLookup': 'datanumber'}
        for name in misc_conv:
            self.ds_dict[name] = self.__get_datastore_dict(name)

        logging.info('loading the firestore')
        for name in misc_conv:
            logging.info(name)
            logging.info(".....starting load for: "+name)
            self.__load_firestore(name)
            logging.info(".....Completed Load for: "+name)
        logging.info('Converstion of Misc Complete')

    def get_ds_dict(self):
        return self.ds_dict

    def __load_firestore(self, name):
        firestore_name = self.misc_rename[name]
        #firestore_name = firestore_name + '/' + self.applicationAPI if name == 'ApiUser' else self.applicationCT
        logging.info(firestore_name)
        col_ref = self.db.collection(firestore_name)
        for ds_entry in self.ds_dict[name]:
            doc_id = ds_entry[self.doc_name[name]]
            dstdoc_ref = col_ref.document(doc_id)
            dstdoc_ref.set(ds_entry)
            if name == 'Image':
                path = dstdoc_ref.path
                colName = DataNumberLookup._get_collection_type(doc_id)
                dnl = self.db.collection('data_number_lookup/'+self.company+'/'+colName)
                dnldoc_ref = dnl.document(doc_id)
                dnldoc_ref.set({'path': path})

    def __get_datastore_dict(self, name):
        qry_ds = self.ds_client.query(kind=name)
        dsi = qry_ds.fetch()
        entities = [e for e in dsi]
        dst_dict = [self.__to_dict(e) for e in entities]
        return dst_dict

    def __get_data_storage_type(self, key):
        dsType = self.ds_client.get(key)
        dst = self.__to_dict(dsType)
        return {'data_storage_type': 'data_storage_type/'+dst['storage_name'], 'storage_name': dst['storage_name']}

    def __to_dict(self, entity):
        keys = list(entity)
        l = list(set(entity.key.flat_path))
        l = [str(x) for x in l if type(x) == int]
        idVal = entity.kind+'_'+'_'.join(l)
        ret_dict = {'ds_id': idVal}
        for key in keys:
            value = entity[key]
            if key == '-- nothing --':
                prlogging.infoint(entity[key])
                d = json.loads(entity[key])
                ret_dict[key] = d
            elif type(entity[key]) == datastore.key.Key and key == 'dTypeKey':
                ret_dict.update(self.__get_data_storage_type(entity[key]))
            elif type(entity[key]) == datastore.entity.Entity:
                l = list(entity[key])
                l.sort()
                if l == ['auth_domain', 'email', 'user_id']:
                    value = entity[key]['email']
                    ret_dict[key] = value
            elif type(entity[key]) == datetime.datetime:
                value = entity[key].isoformat()
                ret_dict[key] = value
            else:
                ret_dict[key] = value

        return ret_dict
