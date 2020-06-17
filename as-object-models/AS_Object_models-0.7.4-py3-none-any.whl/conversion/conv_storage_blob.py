import datetime
import json, logging
import pandas as pd
from google.cloud import firestore
from google.cloud.datastore.key import Key
from google.cloud import datastore

from .. import DataNumberLookup

class StorageBlobConversion:
    def __init__(self, datastore_project, firestore_project, fld_option):
        self.ds_client = datastore.Client(project=datastore_project)
        self.db = firestore.Client(project=firestore_project)
        self.plt_cols = self.get_plant_entries()
        self._get_conv_sheets()
        self.field_option = fld_option
        self.option_lookup = {
            '6213387679694848': 'recipe_costing-179', 
            '6241863581302784': 'recipe_costing-204',
            "5072267952259072": "recipe_costing-288",
            "5923467320885248": "recipe_costing-149",
            "5763950356463616": "recipe_costing-287",
            "6046866798018560": "recipe_costing-148"}

        '''
        It will look like this
        {
            <field_name>:{
                <field_value>: <dnl|value>,
                ...
            },
            ...
        }

        '''
        self.value_lookup = {}
            
        self.base_coll = 'application_data'
        self.company = 'Color_Orchids'
        self.application = 'Customer_Tracking'
        self.sb_path = self.base_coll+'/'+self.company + \
            '/'+self.application+'/StorageBlob/'
        self.key_lookup = {}
        self.__conv_list = ['options', 'recipe_costing',
                            'customer', 'admin_items', 'test_image', 'invoice_email']
        logging.info('loading from datastore...')
        self.ds_dict = self.__start_load()
        logging.info('Converstion of StorageBlob complete')
    
    def get_plant_entries(self):
        plt_cols = ['Poinsettia'
        ,'Bonita'
        ,'Singolo'
        ,'Mini Bromeliad'
        ,'3" Pothos'
        ,'3" ZZ'
        ,'2.5" Kalanchoe'
        ,'4" Frosty Fern'
        ,'4" Mini Rose'
        ,'3" Neantha Bella Palm'
        ,'2.5" Haworthia'
        ,'Grande'
        ,'Succulent'
        ,'ZZ'
        ,'Bromeliad'
        ,'4" Frosty Fern'
        ,'2.5" Frosty Fern'
        ,'Bellini'
        ,'Mini Succulent'
        ,'Ivy'
        ,'Anthurium'
        ,'4" Spathiphyllum'
        ,'Belita']
        return plt_cols

    def _create_plt_entries(self,row):
        plt_entries = []
        for plant in self.plt_cols:
            qty = row[plant]
            if qty > 0:
                plt_entries.append({'plant':plant,'qty':qty})
        return plt_entries

    def _get_conv_sheets(self):
        df = pd.read_excel('as_models/scripts/item_plants_revised.xlsx',sheet_name='CustomerPlantItem')
        df['plants_new'] = df.apply(self._create_plt_entries,axis=1)
        df = df[['data_number_lookup','plants_new']]
        df.rename(columns={'plants_new':'Plants'},inplace=True)
        df = df.set_index('data_number_lookup')
        self._conv_cpi_plts = df.to_dict('index')

        dfm = pd.read_excel('as_models/scripts/item_plants_revised.xlsx',sheet_name='Master')
        dfm['plants_new'] = dfm.apply(self._create_plt_entries,axis=1)
        dfm = dfm[['data_number_lookup','plants_new','CO_Item_Num']]
        dfm.rename(columns={'plants_new':'Plants'},inplace=True)
        dfm = dfm.set_index('data_number_lookup')
        mUpdate = dfm.to_dict('index')
        for dnl in mUpdate.keys():
            self._conv_cpi_plts[dnl] = mUpdate[dnl]

        dfc = pd.read_excel('as_models/scripts/item_conv revised.xlsx',sheet_name='CustomerPlantItem')
        dfc = dfc[['data_number_lookup','CO_Item_Num']]
        dfc = dfc.set_index('data_number_lookup')
        cin = dfc.to_dict('index')
        for dnl in cin.keys():
            entry = self._conv_cpi_plts.get(dnl,{})
            entry['CO_Item_Num'] = cin[dnl]['CO_Item_Num']
            self._conv_cpi_plts[dnl] = entry

    def __get_types(self):
        coll = self.db.collection('data_schemas')
        ds = coll.stream()
        l = [x.get('storage_name') for x in ds]
        return l

    def __create_data_number_lookup(self, firestore_path, entry):
        dnl_path, dnl, fsp = self.__get_dnl(firestore_path, entry)
        dnl_ref = self.db.collection(dnl_path).document(dnl)

        dnl_ref.set({'path': fsp})
        return dnl

    def __get_dnl(self, firestore_path, entry):
        dnl = entry['data_number_lookup']
        colName = DataNumberLookup._get_collection_type(dnl)

        dns_path = 'data_number_sync/'+self.company+'/'+self.application
        dnl_path = 'data_number_lookup/'+self.company+'/'+colName

        if not dnl or dnl == "null":
            dn_ref = self.db.collection(dns_path).document(entry['data_type'])
            doc = dn_ref.get()
            num = 100
            if doc.exists:
                num = doc.get('number')
                #name = doc.get('storage_name')
                num = num+1
                dn_ref.update({'number': num})
            else:
                dn = {'added_by': 'jasonbowles@analyticssupply.com',
                      'data_storage_type': 'data_storage_type/'+entry['data_type'],
                      'ds_id': 'added_on_conversion',
                      'dw_sync_status': 'to_update',
                      'number': num,
                      'soft_delete': False,
                      'storage_name': entry['data_type'],
                      'timestamp': datetime.datetime.now().isoformat(),
                      'up_timestamp': datetime.datetime.now().isoformat(),
                      'updated_by': 'jasonbowles@analyticssupply.com'}
                dn_ref.set(dn)
            dnl = entry['data_type']+'-'+str(num)
            colName = DataNumberLookup._get_collection_type(dnl)
            dnl_path = 'data_number_lookup/'+self.company+'/'+colName
            firestore_path = firestore_path+"/"+dnl
        else:
            firestore_path = firestore_path+"/"+dnl

        return dnl_path, dnl, firestore_path

    def get_ds_dict(self):
        return self.ds_dict

    def __get_schema(self, data_type):
        schema_path = 'data_schemas/'+self.company+'/'+self.application+'/'+data_type
        dt_docRef = self.db.document(schema_path)
        dt_doc = dt_docRef.get()
        dt_dict = dt_doc.to_dict()
        # print(dt_dict)
        fields = list(dt_dict['storage_fields'].values())
        field_d = {'fields': {}, 'collections': {}}
        for field in fields:
            # print(field)
            field_d['fields'][field['field_name']] = field
            if field['is_collection']:
                field_d['collections'][field['group_name']] = field
        return field_d

    def __start_load(self):
        ''' This is where we'll get started with the load for each entry '''
        for ent in self.__conv_list:
            entries = self.__get_datastore_dict(ent)
            logging.info('loading:... '+ent)
            for entry in entries:
                #print('loading... '+str(entry)+"... ")
                path = self.__load_firestore(entry)
                self.__process_children(entry, path)
            logging.info('finished loading... '+ent)
        return True

    def __process_children(self, entry, path):
        ''' starts the recursion part '''
        fields = self.__get_schema(entry['data_type'])
        sbkey = self.key_lookup[entry['ds_id']]
        kids = self.__get_children(sbkey)
        for kid in kids:
            kid_field = fields['collections'][kid['data_type']]
            kid_path = path+'/'+kid_field['field_name']
            kid_doc = self.__load_firestore(kid, kid_path)
            self.__process_children(kid, kid_doc)

    def __get_children(self, sbkey):
        qry_a = self.ds_client.query(kind='StorageBlob', ancestor=sbkey)
        ss = qry_a.fetch()
        ents = [s for s in ss if s.key != sbkey and s.key.parent == sbkey]
        child_dicts = [self.__to_dict(ent) for ent in ents]
        return child_dicts

    def __get_image_data(self,image_dnl):
        imageCol = DataNumberLookup._get_collection_type(image_dnl)
        docRef = self.db.document('data_number_lookup/Color_Orchids/'+imageCol+'/'+image_dnl)
        docSnap = docRef.get()
        if docSnap.exists:
            path = docSnap.get('path')
            image_info = self.db.document(path).get()
            if image_info.exists:
                img_dict = image_info.to_dict()
                return {'image_id': img_dict['image_number'],'image_url':img_dict['image_url']}
            
            return None
        return None

    def __convert_images(self, entry, image_field_nm):
        image_field = entry.get(image_field_nm,None)
        if image_field:
            new_image_list = []
            if isinstance(image_field,str):
                if image_field.startswith('image-'):
                    imgD = self.__get_image_data(image_field)
                    if imgD:
                        new_image_list.append(imgD)
            if isinstance(image_field, list): 
                for i in image_field:
                    if i.startswith('image-'):
                        imgD = self.__get_image_data(i)
                        if imgD:
                            new_image_list.append(imgD)
            entry[image_field_nm] = new_image_list

    def __load_firestore(self, entry, parent_document=None):
        sb_path = self.sb_path+entry['data_type']
        if parent_document:
            sb_path = parent_document

        dnl = self.__create_data_number_lookup(sb_path, entry)

        #
        # Update the way we store images
        #
        if entry['data_type'] in ['recipe_costing','plant_image','item_order','cust_plant_item']:
            field_nm  = 'image' if entry['data_type'] == 'recipe_costing' else 'plant_image'
            self.__convert_images(entry,field_nm)
            
        #
        #  Fixing the lookup problem for recipe costing
        #
        if entry['data_type'] in ['recipe_costing', 'options']:
            _id = entry['ds_id'].split("_")[1]
            key = self.option_lookup.get(_id, None)
            if _id:
                self.option_lookup[_id] = dnl

            if entry['data_type'] == 'recipe_costing':
                field_name = entry['item_type']
                value = entry['name']
                valDict = self.value_lookup.get(field_name,{})
                valDict[value] = dnl
                self.value_lookup[field_name] = valDict

            if entry['data_type'] == 'options':
                field_name = entry['option_name']
                value = entry['option_value']
                valDict = self.value_lookup.get(field_name,{})
                valDict[value] = dnl
                self.value_lookup[field_name] = valDict
        else:
            if entry['data_type'] in ['plant_item', 'item_order', 'cust_plant_item']:
                self.process_plant_item(entry)

        entry['data_number_lookup'] = dnl

        path = sb_path
        if parent_document:
            path = parent_document

        col_ref = self.db.collection(path)
        dstdoc_ref = col_ref.document(dnl)
        dstdoc_ref.set(entry)
        #print("firestore Loaded...")
        return path+'/'+dnl

    def process_plant_item(self, entry):
        keys = entry.keys()
        for key in keys:
            value = entry[key]
            isList = False
            values = []
            newValues = []
            if not isinstance(value,list):
                values.append(value)
            else:
                values = value
                isList = True

            if key != 'Plants' and key != 'CO_Item_Num':
                newValues = self.__convert_dnl_entry(values,key)
            else:
                if key == 'Plants':
                    newValues = self.__convert_xslx_plants(entry)
                else:
                    newValues = self.__convert_xslx_co_item_num(entry)

            if not isList:
                value = newValues[0]

            entry[key] = value
    
    def __convert_xslx_co_item_num(self,entry):
        dnl = entry['data_number_lookup']
        convEntry = self._conv_cpi_plts.get(dnl,{'Plants':None,'CO_Item_Num':None})
        if convEntry.get('CO_Item_Num',None) is None:
            return [entry['CO_Item_Num']]
        else:
            return [convEntry['CO_Item_Num']]
    
    def __convert_xslx_plants(self,entry):
        dnl = entry['data_number_lookup']
        newValues = []
        convEntry = self._conv_cpi_plts.get(dnl,{'Plants':None,'CO_Item_Num':None})
        if convEntry.get('Plants',None) is None:
            oldPlts = entry['Plants']
            oldPlts = oldPlts if isinstance(oldPlts,list) else [oldPlts]
            plts = self.__convert_dnl_entry(oldPlts,'Plants')
            for plt in plts:
                newValues.append({'plant':plt,'qty':1})
        else:
            for convPlt in convEntry['Plants']:
                plName = convPlt['plant']
                qty = convPlt['qty']
                plDNL = self.value_lookup.get('Plants',{}).get(plName,None)
                if plDNL is not None:
                    plName = plDNL+'|'+plName
                newValues.append({'plant':plName,'qty':qty})
        return newValues

    def __convert_dnl_entry(self,values,key):
        newValues = []
        for val in values:
            if isinstance(val, str) and val.find('|') > 0 and key != 'key_fields':
                parts = val.split("|")
                op_dnl = self.option_lookup.get(parts[0], None)
                if op_dnl is None:
                    #print("Going to look up by value... ")
                    opField = self.field_option.get(key,None)
                    if opField:
                        op_dnl = self.value_lookup.get(opField,None)
                        if op_dnl is None:
                            logging.info("failed to look up by value... "+key)
                            val = parts[1]
                        else:
                            op_dnl = op_dnl.get(parts[1],None)
                            if op_dnl:
                                val = op_dnl+"|"+parts[1]
                            else:
                                logging.info("Field found... but value not.. :(.. "+key+", with value: "+parts[1])
                                val = parts[1]
                    else:
                        logging.info("failed to look up by value... "+key)
                        val = parts[1]
                    #raise Exception("Could not find lookup value for: "+value)
                else:
                    val = op_dnl+'|'+parts[1]
            newValues.append(val)
        return newValues

    def __get_datastore_dict(self, filter_type):
        qry_ds = self.ds_client.query(kind='StorageBlob')
        qry_ds.add_filter('data_type', '=', filter_type)
        dsi = qry_ds.fetch()
        entities = [e for e in dsi]
        dst_dict = [self.__to_dict(e) for e in entities]
        return dst_dict

    def __get_data_storage_type(self, key):
        dsType = self.ds_client.get(key)
        dst = self.__to_dict(dsType)
        schema_path = 'data_schemas/'+self.company + \
            '/'+self.application+'/'+dst['storage_name']
        return {'schema': schema_path, 'storage_name': dst['storage_name']}

    def __to_dict(self, entity):
        keys = list(entity)
        l = list(set(entity.key.flat_path))
        _id = entity.key.id
        l = [str(x) for x in l if type(x) == int]
        idVal = entity.kind+'_'+'_'.join(l)
        ret_dict = {'ds_id': idVal}

        if entity['data_type'] == 'options' or entity['data_type'] == 'recipe_costing':
            self.option_lookup[str(_id)] = '--to-fill--'

        self.key_lookup[idVal] = entity.key
        for key in keys:
            value = entity[key]
            if key == '-- nothing --':
                d = json.loads(entity[key])
                ret_dict[key] = d
            elif key == 'data':
                d = json.loads(entity[key])
                ret_dict.update(d)
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
