import datetime
import json
import logging
from google.cloud import firestore
from google.cloud.datastore.key import Key
from google.cloud import datastore

from .. import DataNumberLookup


class DataNumbernConversion:
    def __init__(self, datastore_project, firestore_project):
        self.ds_client = datastore.Client(project=datastore_project)
        self.db = firestore.Client(project=firestore_project)
        self.base_coll = 'data_number_sync'
        self.company = 'Color_Orchids'
        self.application = 'Customer_Tracking'

        logging.info('loading from datastore...')
        self.ds_dict = self.__get_datastore_dict()
        logging.info('loading the firestore')
        self.__load_firestore()
        logging.info('Converstion of DataNumber complete')

    def get_ds_dict(self):
        return self.ds_dict

    def __load_firestore(self):
        col_ref = self.db.collection(self.base_coll+'/'+self.company+'/'+self.application)
        for ds_entry in self.ds_dict:
            logging.info('loading... '+ds_entry['storage_name'])
            doc_id = ds_entry['storage_name']
            dstdoc_ref = col_ref.document(doc_id)
            dstdoc_ref.set(ds_entry)

    def __get_datastore_dict(self):
        qry_ds = self.ds_client.query(kind='DataNumber')
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
                logging.info(entity[key])
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
