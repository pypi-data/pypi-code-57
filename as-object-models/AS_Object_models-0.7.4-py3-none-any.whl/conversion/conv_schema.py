import datetime,json,logging
from google.cloud import firestore
from google.cloud.firestore import DocumentReference, DocumentSnapshot
from google.cloud.datastore.key import Key
from google.cloud import datastore

import re

advanced_pattern = re.compile(r"((?P<field_name>[^\[\]\?\s=<>!]+)\s*(?P<comparison>[=<>!]+)\s*[\'\`](?P<field_value>[^\[\]\?=<>!]+)[\'\`](\s*(?P<operator>[&|]+)\s*)*)")
class SchemaConversion:
    def __init__(self, datastore_project, firestore_project):
        self.ds_client = datastore.Client(project=datastore_project)
        self.db = firestore.Client(project=firestore_project)
        self.company = 'Color_Orchids'
        self.application = 'Customer_Tracking'
        self.base_coll = self.db.collection('data_schemas')
        self.option_fields = {}
        self.base_doc = self.base_coll.document(self.company)
        base_data = {'CompanyName': 'Color Orchids', 'ApplicationName': [
            'Customer Tracking', 'Sales Inventory']}
        self.base_doc.set(base_data)
        logging.info('loading from datastore...')
        self.ds_dict = self.__get_datastore_dict()
        logging.info('loading the firestore')
        self.__load_firestore()
        logging.info('Converstion of Schema complete')

    def run_validation(self):
        qry = self.db.collection_group('storage_fields').where(
            'parent_container', '==', 'data_schemas/Color_Orchids/Customer_Tracking/address')
        ee = qry.stream()
        entities = [e for e in ee]
        assert len(entities) == 6
        assert self.db.document(entities[0].to_dict()['parent_container']).get().to_dict()[
            'storage_name'] == 'address'

    def get_op_fields(self):
        return self.option_fields

    def parse_jmespath(self,jmespath_str):
        '''
        Regex is awesome... having named capture groups!!! seriously!!
        '''
        match_arr = []
        matches = advanced_pattern.finditer(jmespath_str)
        for _, match in enumerate(matches, start=1):
            m_dict = {'field':match.group('field_name'),'compare':match.group('comparison'),'value':match.group('field_value'),'operator':match.group('operator')}
            match_arr.append(m_dict)

        return None if len(match_arr) == 0 else match_arr[0]['value'] 

    def __load_firestore(self):
        dst_ref = self.base_doc.collection(self.application)
        for ds_entry in self.ds_dict:
            fields = [x for x in ds_entry.keys() if x != 'storage_fields']
            st_name = ds_entry['storage_name']
            dstdoc_ref = dst_ref.document(st_name)
            logging.info('loading... '+st_name)
            doc = {}
            for field in fields:
                doc[field] = ds_entry[field]
                if st_name == 'item_order' and field == 'extends':
                    doc['field'] = 'cust_plant_item'

            # dstdoc_ref.set(doc)
            doc['storage_fields'] = {}
            #sf_ref = dstdoc_ref.collection('storage_fields')
            for field in ds_entry['storage_fields']:
                field['parent_container'] = 'data_schemas/' + \
                    self.company+'/'+self.application+'/'+st_name
                fldName = field['field_name']
                field['is_collection'] = False
                if fldName == 'addresses':
                    fldName = st_name+"_"+fldName
                    field['field_name'] = fldName
                if field['field_type'] == 'group':
                    field['is_collection'] = True
                #sfdoc_ref = sf_ref.document(fldName)
                # sfdoc_ref.set(field)

                if field['is_option_filled'] or str(field['is_option_filled']).lower() == 'true':
                    #print("option field: "+field['field_name'])
                    #print("option container: "+field['option_container'])
                    self.option_fields[field['field_name']]= self.parse_jmespath(field['option_container'])
                    
                doc['storage_fields'][fldName] = field
            dstdoc_ref.set(doc)

    def __get_datastore_dict(self):
        qry_ds = self.ds_client.query(kind='DataStorageType')
        dsi = qry_ds.fetch()
        entities = [e for e in dsi]
        dst_dict = [self.__to_dict(e) for e in entities]
        for dEntry in dst_dict:
            dEntry['storage_fields'] = self.__get_storage_fields(dEntry)
        return dst_dict

    def __get_storage_fields(self, entity):
        sfqry = self.ds_client.query(kind="StorageField")
        keyParts = entity['ds_id'].split('_')
        dstkey = self.ds_client.key(keyParts[0], int(keyParts[1]))
        sfqry.add_filter('parent_container', '=', dstkey)
        entries = sfqry.fetch()
        entities = [self.__to_dict(e) for e in entries]
        return entities

    def __to_dict(self, entity, storage_blob=False):
        keys = list(entity)
        l = list(set(entity.key.flat_path))
        l = [str(x) for x in l if type(x) == int]
        idVal = entity.kind+'_'+'_'.join(l)
        ret_dict = {'ds_id': idVal}
        for key in keys:
            value = entity[key]
            if storage_blob == True and key == 'data':
                d = json.loads(entity[key])
                ret_dict.update(d)
            elif type(entity[key]) == datastore.key.Key:
                l = list(set(entity[key].flat_path))
                l = [entity[key].kind] + [str(x) for x in l if type(x) == int]
                ret_dict[key] = '_'.join(l)
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
