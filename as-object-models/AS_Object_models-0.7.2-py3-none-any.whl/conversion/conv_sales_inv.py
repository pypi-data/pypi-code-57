from abc import ABCMeta, abstractmethod
import datetime
import json
import copy
import traceback
import logging
import pprint
import os
import concurrent.futures
import time

import jmespath

from google.cloud import firestore
from google.cloud.firestore import DocumentReference, DocumentSnapshot
from google.cloud.datastore.key import Key
from google.cloud import datastore

from .map_sales_reserves import MapSalesReserves
from .. import StorageBlob,DataNumber,DataNumberLookup, ItemWeek

class BatchWrite(object):

    MAX_WRITES = 400

    def __init__(self, fsBatch):
        self.batch = fsBatch
        self.write_count = 0
        self._block = False

    def delete(self, fsDoc):
        while self._block:
            time.sleep(0.5)
        self.batch.delete(fsDoc)
        self.write_count += 1
        if self.write_count >= BatchWrite.MAX_WRITES:
            self.commit()

    def create(self, fsDoc, data):
        while self._block:
            time.sleep(0.5)
        self.batch.set(fsDoc, data)
        self.write_count += 1
        if self.write_count >= BatchWrite.MAX_WRITES:
            self.commit()

    def set(self, fsDoc, data):
        while self._block:
            time.sleep(0.5)
        self.batch.set(fsDoc, data)
        self.write_count += 1
        if self.write_count >= BatchWrite.MAX_WRITES:
            self.commit()

    def commit(self):
        self._block = True
        self.batch.commit()
        self.write_count = 0
        self._block = False



class BaseSalesInv(metaclass=ABCMeta):

    BASE_PATH = 'application_data/Color_Orchids/Sales_Inventory'

    def __init__(self, fs_project=None, ds_project=None):
        if fs_project:
            self.fsProject = fs_project
        else:
            self.fsProject = os.environ.get('FS_PROJECT', 'backend-firestore-test')
        
        self.fsClient = firestore.Client(self.fsProject)

        if ds_project:
            self.dsProject = ds_project
        else:
            self.dsProject = os.environ.get('DS_PROJECT', 'sales-inv-colororchids')
            
        self.dsClient = datastore.Client(self.dsProject)

        self.fsBase = self.base_path()
        self._entities = None
        self._filter_deletes = True
        self._post_process = False
        self.NUM_WORKERS = os.environ.get("NUM_WORKERS_SEED",30)
        self._threading = False

    def get_next_dnl(cls,inName):
        dn = DataNumber.createInstance(inName)

        dn.number = dn.number + 1
        dn.update_ndb()

        return inName+"-"+str(dn.number)

    def delete_producer(self, item):
        logging.info("Delete Producer: Starting..")
        deletes = []
        def _inner_deleteCollection(colRefs):
            for colRef in colRefs:
                docRefs = colRef.list_documents()
                for docRef in docRefs:
                    _inner_deleteCollection(docRef.collections())
                    deletes.append({'ref':docRef,'batch':item['batch']})

        _inner_deleteCollection([self.fsClient.collection(item['collection'])])
                    
        logging.info("Delete Producer: ending")
        return deletes

    def delete_consumer(self, item):
        try:
            batch = item['batch']
            batch.delete(item['ref'])
            
        except Exception:
            logging.error("trouble with rec: ")
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(item['ref'].path)

 
    def load_consumer(self, entity):
        rec = entity['entry']
        batch = entity['batch']
        key = entity['key']
        collection = self.fsClient.collection(entity.get('collection','')) 

        docRef = None
        if rec.get('path',None) is None:
            docRef = collection.document(key)
        else:
            docRef = self.fsClient.document(rec['path'])
            collection = docRef.parent

        try:
            rec['path'] = docRef.path
            rec['parent_path'] = collection.parent.path+'/'+collection.id
            snap = docRef.get()
            if snap and snap.exists:
                batch.set(docRef, rec)
            else:
                batch.create(docRef, rec)
            
            self._post_fs_processing(docRef)
        except Exception as e:
            logging.error("trouble with rec: ")
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(rec)
            traceback.print_exc()
            raise e

    def threaded_load_fs(self, batch):
        self._threading = True
        to_process = []
        for key in self._entities.keys():
            rec = self._entities[key]
            path = self.base_path() if rec.get('parent_path',None) is None else rec['parent_path']
            newEntity = {'batch':batch,'collection': path, 'entry': rec,'key': key}
            to_process.append(newEntity)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.NUM_WORKERS) as executor:
            executor.map(self.load_consumer,to_process)

        batch.commit()
        self._threading = False

    def threaded_delete_fs(self, batch):
        self._threading = True
        deletes = self.delete_producer({'collection': self.base_path(),'batch':batch})
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.NUM_WORKERS) as executor:
            executor.map(self.delete_consumer, deletes)

        batch.commit()
        self._threading = False

    def _create_path(self):
        start = self.BASE_PATH
        mid = '/Legacy/' if self.is_legacy else '/Converted/'
        return start+mid+self.the_kind

    @abstractmethod
    def base_path(self):
        pass

    @property
    @abstractmethod
    def is_legacy(self):
        pass

    @property
    @abstractmethod
    def the_kind(self):
        pass

    def add_entity(self,entity):
        if self._entities is None:
            self._entities = {}
        self._entities[entity['id']] = entity

    def pull_all_firestore(self):
        colRef = self.fsClient.collection(self.base_path())
        docRefs = colRef.list_documents()
        ents = [self._load_to_entities(ref) for ref in docRefs]
        self._entities = {x['id']:x for x in ents}

    def pull_firestore(self,entry_id):
        if self._entities is None:
            self._entities = {}
        docRef = self.fsClient.document(self.base_path()+"/"+entry_id)
        snap = docRef.get()
        if snap.exists:
            entryDict = snap.to_dict()
            eId = entryDict.get('ds_id',entryDict.get('id',None))
            if not eId:
                eId = docRef.id
            
            if self._entities is None:
                self._entities = {}

            self._entities[eId] = entryDict
            return entryDict
        return None

    def _load_to_entities(self, docRef):
        snap = docRef.get()
        retDict = {}
        if snap.exists:
            retDict = snap.to_dict()
            eId = retDict.get('ds_id',retDict.get('id',None))
            if not eId:
                eId = docRef.id
        return retDict

    def getEntry(self, entry_id):
        if self._entities and self._entities.get(entry_id, None):
            return self._entities[entry_id]
        else:
            return self.pull_firestore(entry_id)
        return None

    def delete_fs(self):
        logging.info("Creating 'Delete' Batch... "+self.the_kind)
        batch = BatchWrite(self.fsClient.batch())
        colRefs = self.fsClient.collection(self.base_path())
        self._deleteCollection([colRefs], batch)
        batch.commit()
        logging.info("Batch Delete.. Complete.. "+self.the_kind)


    def _deleteCollection(self, colRefs, batch):
        for colRef in colRefs:
            docRefs = colRef.list_documents()
            for docRef in docRefs:
                self._deleteCollection(docRef.collections(), batch)
                batch.delete(docRef)


    def load_fs(self, skipDelete=False):
        batch = BatchWrite(self.fsClient.batch())
        if self._post_process:
            DataNumber.createInstance(self.the_kind)

        if not self._entities:
            self._entities = {x['id']: x for x in self.get_sr_entities()}

        if not skipDelete:
            self.threaded_delete_fs(batch)
        
        while self._threading:
            logging.info("Waiting on Deletes...")
            time.sleep(0.5)
        
        batch.commit()

        logging.info('starting firestore batch load... '+self.the_kind)
        
        self.threaded_load_fs(batch)

        while self._threading:
            logging.info("Waiting on Loads...")
            time.sleep(0.5)

        batch.commit()
        logging.info('Load complete.. '+self.the_kind)

    def load_fs_linear(self, skipDelete=False):
        if self._post_process:
            DataNumber.createInstance(self.the_kind)

        if not self._entities:
            self._entities = {x['id']: x for x in self.get_sr_entities()}

        if not skipDelete:
            self.delete_fs()
        logging.info('starting firestore batch load... '+self.the_kind)
        batch = BatchWrite(self.fsClient.batch())
        col = self.fsClient.collection(self.base_path())
        self._process_fs_documents(col, self._entities, batch)
        batch.commit()
        logging.info('Load complete.. '+self.the_kind)

    def _process_fs_documents(self, collection, entities, batch):
        keys = entities.keys()
        for key in keys:
            self._process_one_entity(collection, key, entities[key], batch)

    def load_one_fs_document(self,entity):
        path = self.base_path() if entity.get('parent_path',None) is None else entity['parent_path']
        collection = self.fsClient.collection(path)
        batch = BatchWrite(self.fsClient.batch())
        self._process_one_entity(collection,entity['id'],entity,batch)
        batch.commit()
        return entity.get('path',None)

    def _process_one_entity(self, collection, key, rec, batch):
        docRef = None
        if rec.get('path',None) is None:
            docRef = collection.document(key)
        else:
            docRef = self.fsClient.document(rec['path'])
            collection = docRef.parent

        try:
            rec['path'] = docRef.path
            rec['parent_path'] = collection.parent.path+'/'+collection.id
            snap = docRef.get()
            if snap and snap.exists:
                batch.set(docRef, rec)
            else:
                batch.create(docRef, rec)
            
            self._post_fs_processing(docRef)
        except Exception as e:
            logging.error("trouble with rec: ")
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(rec)
            raise e
    
    def _post_fs_processing(self,docRef):
        if self._post_process:
            dnl = docRef.id
            path = docRef.path
            DataNumberLookup.store_data_number_sbPath(dnl,path)

    def get_ds_key(self,ds_id):
        parts = ds_id.split("-")
        if len(parts) > 1:
            return self.dsClient.key(parts[0],int(parts[1]))
        return None

    def get_ds_entry(self, ds_id,loadToEntities=False):
        dsKey = self.get_ds_key(ds_id)
        entity = self._to_dict(self.dsClient.get(dsKey))
        if loadToEntities:
            if self._entities is None:
                self._entities = {}
            self._entities[entity['id']] = entity
        return entity

    def get_sr_entities(self):
        qry_ds = self.dsClient.query(kind=self.the_kind)
        dsi = qry_ds.fetch()
        entities = [e for e in dsi]
        dst_dict = [self._to_dict(e) for e in entities]
        if self._filter_deletes:
            return [x for x in dst_dict if not x.get('soft_delete',False)]
        return dst_dict

    def _to_dict(self, entity):
        keys = list(entity)
        l = list(set(entity.key.flat_path))
        l = [str(x) for x in l if type(x) == int]
        idVal = entity.kind+'-'+'-'.join(l)
        ret_dict = {'id': idVal}
        for key in keys:
            value = entity[key]
            if key == '-- nothing --':
                logging.info(entity[key])
                d = json.loads(entity[key])
                ret_dict[key] = d
            elif key == 'data':
                d = json.loads(entity[key])
                ret_dict.update(d)
            elif type(entity[key]) == datastore.key.Key:
                l = list(set(entity[key].flat_path))
                l = [str(x) for x in l if type(x) == int]
                idVal = entity[key].kind+'-'+'-'.join(l)
                ret_dict[key] = idVal
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


class DS_Plants(BaseSalesInv):
    def __init__(self, fs_project=None, ds_project=None, load=True):
        super(DS_Plants, self).__init__(fs_project, ds_project)
        if load:
            self._entities = {x['id']: x for x in self.get_sr_entities()}
            self.load_fs()

    def base_path(self):
        return self._create_path()

    @property
    def is_legacy(self):
        return True

    @property
    def the_kind(self):
        return 'Plant'


class DS_Supplier(BaseSalesInv):
    def __init__(self, fs_project=None, ds_project=None, load=True):
        super(DS_Supplier, self).__init__(fs_project, ds_project)
        self._post_process = True
        if load:
            self._entities = {x['id']: x for x in self.get_sr_entities()}
            self.load_fs()

    def base_path(self):
        return 'application_data/Color_Orchids/Customer_Tracking/StorageBlob/'+self.the_kind

    @property
    def is_legacy(self):
        return True

    @property
    def the_kind(self):
        return 'Supplier'


class DS_Customer(BaseSalesInv):
    def __init__(self, fs_project=None, ds_project=None, load=True):
        super(DS_Customer, self).__init__(fs_project, ds_project)
        if load:
            self._entities = {x['id']: x for x in self.get_sr_entities()}
            self.load_fs()

    def base_path(self):
        return self._create_path()

    @property
    def is_legacy(self):
        return True

    @property
    def the_kind(self):
        return 'Customer'


class DS_Product(BaseSalesInv):
    def __init__(self, fs_project=None, ds_project=None, load=True):
        super(DS_Product, self).__init__(fs_project, ds_project)
        self._filter_deletes = False
        if load:
            self._entities = {x['id']: x for x in self.get_sr_entities()}
            self.load_fs()

    def base_path(self):
        return self._create_path()

    @property
    def is_legacy(self):
        return True

    @property
    def the_kind(self):
        return 'Product'


class DS_EmailNotifications(BaseSalesInv):
    def __init__(self, fs_project=None, ds_project=None, load=True):
        super(DS_EmailNotifications, self).__init__(fs_project, ds_project)
        self._post_process = True
        if load:
            self._entities = {x['id']: x for x in self.get_sr_entities()}
            self.load_fs()

    def base_path(self):
        return self._create_path()

    @property
    def is_legacy(self):
        return False

    @property
    def the_kind(self):
        return 'EmailNotifications'


class DS_GrowWeek(BaseSalesInv):
    def __init__(self, fs_project=None, ds_project=None, load=True):
        super(DS_GrowWeek, self).__init__(fs_project, ds_project)
        print("FS PROJECT: "+fs_project)
        print("DS PROJECT: "+ds_project)
        print("Loading... "+str(load))
        self._conv_entities = None
        if load:
            self.run_load()

    def run_load(self):
        srEntities = self.get_sr_entities()
        for x in srEntities:
            x['ds_id'] = x['id']
            x['id'] = str(x['year'])+'_'+str(x['week_number']).zfill(2)

        self._entities = {x['id']: x for x in srEntities}
        self._conv_entities = {x['ds_id']: x for x in srEntities}
        self.load_fs()

    def base_path(self):
        return self._create_path()

    def getConvEntry(self, inId):
        convEntry = None if self._conv_entities is None else self._conv_entities.get(inId, None)
        return convEntry

    def _create_new_key_from_ds(self,dsEntry):
        year = dsEntry['year']
        wkNum = str(dsEntry['week_number']).zfill(2)
        _id = str(year)+"_"+wkNum
        return _id

    def get_entry_path(self,entry):
        if entry['path'] is None:
            path = self.base_path+'/'+entry['id']
            entry['path']  = path
        return entry['path']

    def getEntry(self,inId):
        convLook = True if len(inId.split("-")) > 1 else False
        entry = None
        if not convLook:
            entry = None if self._entities is None else self._entities.get(inId,None)

            if entry is None:
                entry = super(DS_GrowWeek,self).getEntry(inId)
            
        else:
            entry = self.getConvEntry(inId)
            if entry is None:
                entry = self.get_ds_entry(inId,True)
                _id = self._create_new_key_from_ds(entry)

                fs_entry = super(DS_GrowWeek,self).getEntry(_id)
                if fs_entry is None:
                    entry['id'] = _id
                    entry['ds_id'] = inId
                    self.load_one_fs_document(entry)

                    if self._conv_entities is None:
                        self._conv_entities = {}

                    self._conv_entities[inId] = entry
                    self.add_entity(entry)
                else:
                    entry = fs_entry
        
        return entry

    @property
    def is_legacy(self):
        return False

    @property
    def the_kind(self):
        return 'GrowWeek'


class DS_PlantGrow(BaseSalesInv):
    def __init__(self, fs_project=None, ds_project=None, growWeeks=None, plants=None, load=True):
        super(DS_PlantGrow, self).__init__(fs_project, ds_project)
        self.growWeeks = growWeeks if growWeeks is not None else DS_GrowWeek(load=False)
        self.plants = plants if plants is not None else DS_Plants(load=False)
        self.gw_dict = {}
        self._pg_entities = {}
        if load:
            self.run_load()
            #self.legacy_load()
            self.load_fs()

    def load_fs(self):
        super(DS_PlantGrow,self).load_fs(True)
    #    logging.info("Pulling out PlantGrow to update GrowWeek")
    #    for gw_id in self.gw_dict.keys():
    #        gwPg = self.gw_dict[gw_id]
    #        gw_entry = self.growWeeks.getEntry(gw_id)
    #        docRef = self.fsClient.document(gw_entry['path'])
    #        gwDict = docRef.get().to_dict()
    #        gwDict['plantgrow'] =  gwPg
    #        docRef.set(gwDict)

    def run_load(self):
        srEntities = self.get_sr_entities()
        self._entities = {x['id']: x for x in srEntities}
        self._update_entries()
        #self._conv_entities = {x['plant']['name']: x for x in list(self._entities.values())}
    
    def legacy_load(self):
        if self._entities is None:
            self._entities = {x['id']: x for x in self.get_sr_entities()}

        super(DS_PlantGrow, self).load_fs()

    def base_path(self):
        return self._create_path()

    @property
    def is_legacy(self):
        return True

    @property
    def the_kind(self):
        return 'PlantGrow'
    
    def getEntry(self,inId):
        convLook = True if len(inId.split("-")) > 1 else False
        #entry = super(DS_PlantGrow,self).getEntry(inId)
        entry = self._pg_entities.get(inId,None)
        if convLook and entry is None:
            entry = self.get_ds_entry(inId,True)
            if entry is not None:
                entry = self._process_entry(inId,entry)
                #self.add_entity(entry)
        
        return entry


    def _update_entries(self):
        logging.info("Starting to update the PlantGrow entries")
        temp = {}
        for k,v in self._entities.items():
            self._process_entry(k,v,temp_entities=temp)
        self._entities = temp
        logging.info("Completed update for PlantGrow")

    def _process_entry(self,entry_key, entry_value,temp_entities=None):
        if temp_entities is None:
            temp_entities = self._entities

        self._pg_entities[entry_key] = {'old':copy.deepcopy(entry_value),'new':None}
        entity = self._update_entry(entry_value)
        doc_id = entity['finish_week'] + "-"+entity['id']
        entry = temp_entities.get(doc_id,None)
        if entry is None:
            entry = {}
            entry['soft_delete'] = False
            entry['item_type'] = 'Plants'
            entry['items'] = {}
            entry['finish_week'] = entity['finish_week']
            path_base = 'application_data/Color_Orchids/Sales_Inventory/Converted/GrowWeek'
            parent_path = path_base+'/'+entity['finish_week']+'/Items'
            path = parent_path + '/Plants'
            entry['path'] = path
            entry['parent_path'] = parent_path
        entry['items'][entity['item_name']] = entity
        self._pg_entities[entry_key]['new'] = entity
        temp_entities[doc_id] = entry
        return entry

    def _update_entry(self, entry):
        plt_id = entry['plant']
        plt_entry = self.plants.getEntry(plt_id)
        entry['id'] = 'Plants'
        entry['item_type'] = 'Plants'
        entry['item_name'] = ItemWeek.CleanItemName(plt_entry['name'])
        entry['name'] = plt_entry['name']
        entry['item'] = {'name': plt_entry['name'],
                          'id': plt_id, 'path': plt_entry['path']}
        cg = entry.get('color_groupings', '{"all":"'+str(entry['actual'])+'"}')
        entry['color_groupings'] = json.loads(cg)
        gw_id = entry['finish_week']
        gw_entry = self.growWeeks.getEntry(gw_id)
        entry['finish_week'] = gw_entry['id']
        return entry


class DS_PlantGrowNotes(BaseSalesInv):
    def __init__(self, fs_project=None, ds_project=None, pltGrow=None,load=True):
        super(DS_PlantGrowNotes, self).__init__(fs_project, ds_project)
        self.plantGrow = pltGrow if pltGrow is not None else DS_PlantGrow(load=False)
        self._post_process = True
        self._note_entities = {}
        if load:
            self.run_load()
            #self.legacy_load()
            self.load_fs()

    def load_fs(self):
        super(DS_PlantGrowNotes,self).load_fs(True)

    def getEntry(self,inId):
        entry = super(DS_PlantGrowNotes,self).getEntry(inId)
        if entry is None:
            entry = self.get_ds_entry(inId,True)
            if entry is not None:
                entry = self._update_entry(entry)
                self.add_entity(entry)
            
        return entry
    
    def run_load(self):
        self._entities = {x['id']: x for x in self.get_sr_entities()}
        self._update_entries()
    
    def legacy_load(self):
        if self._entities is None:
            self._entities = {x['id']: x for x in self.get_sr_entities()}

        super(DS_PlantGrowNotes, self).load_fs()

    def base_path(self):
        return self._create_path()

    @property
    def is_legacy(self):
        return True

    @property
    def the_kind(self):
        return 'PlantGrowNotes'

    def _update_entries(self):
        # _ = {k: self._update_entry(v) }
        temp = {}
        for k, v in self._entities.items():
            self._process_entry(k,v,temp_entities=temp)

        self._entities = temp

    def _process_entry(self,entry_key, entry_value,temp_entities=None):
        if temp_entities is None:
            temp_entities = self._entities

        self._note_entities[entry_key] = {'old':copy.deepcopy(entry_value),'new':None}
        entity = self._update_entry(entry_value)
        doc_id = entity['finish_week'] + "-"+entity['id']
        entry = temp_entities.get(doc_id,None)
        if entry is None:
            entry = {}
            entry['soft_delete'] = False
            entry['item_type'] = 'Plants'
            entry['notes'] = {}
            entry['finish_week'] = entity['finish_week']
            path_base = 'application_data/Color_Orchids/Sales_Inventory/Converted/GrowWeek'
            parent_path = path_base+'/'+entity['finish_week']+'/Notes'
            path = parent_path + '/Plants'
            entry['path'] = path
            entry['parent_path'] = parent_path
        notes_array = entry['notes'].get(entity['item_name'],[])
        notes_array.append(entity)
        entry['notes'][entity['item_name']] = notes_array
        self._note_entities[entry_key]['new'] = entity
        temp_entities[doc_id] = entry
        return entry

    def _update_entry(self, entry):
        if entry:
            pg_id = entry['plant_grow']
            pg_entry = self.plantGrow.getEntry(pg_id)
            entry['id'] = self.get_next_dnl('Notes')
            entry['item_name'] = pg_entry['new']['item_name']
            entry['item_type'] = 'Plants'
            entry['finish_week'] = pg_entry['new']['finish_week']
        return entry


class DS_PlantGrowSupply(BaseSalesInv):
    def __init__(self, fs_project=None, ds_project=None, pltGrow=None, supps=None, load=True):
        super(DS_PlantGrowSupply, self).__init__(fs_project, ds_project)
        self.plantGrow = pltGrow if pltGrow is not None else DS_PlantGrow(load=False)
        self.suppliers = supps if supps is not None else DS_Supplier(load=False)
        self._post_process = True

        self._supp_entities = {}
        if load:
            self.run_load()
            #self.legacy_load()
            self.load_fs()

    def load_fs(self):
        super(DS_PlantGrowSupply,self).load_fs(True)

    def getEntry(self,inId):
        entry = super(DS_PlantGrowSupply,self).getEntry(inId)
        if entry is None:
            entry = self.get_ds_entry(inId,True)
            if entry is not None:
                entry = self._update_entry(entry)
                self.add_entity(entry)
            
        return entry

    def run_load(self):
        self._entities = {x['id']: x for x in self.get_sr_entities()}
        self._update_entries()

    def legacy_load(self):
        if self._entities is None:
            self._entities = {x['id']: x for x in self.get_sr_entities()}

        super(DS_PlantGrowSupply, self).load_fs()

    def base_path(self):
        return self._create_path()

    @property
    def is_legacy(self):
        return True

    @property
    def the_kind(self):
        return 'PlantGrowSupply'

    #def _update_entries(self):
    #    self._entities = {k: self._update_entry(
    #        v) for k, v in self._entities.items()}

    def _update_entries(self):
        temp = {}
        for k, v in self._entities.items():
            self._process_entry(k,v,temp_entities=temp)

        self._entities = temp

    def _process_entry(self,entry_key, entry_value,temp_entities=None):
        if temp_entities is None:
            temp_entities = self._entities

        self._supp_entities[entry_key] = {'old':copy.deepcopy(entry_value),'new':None}
        entity = self._update_entry(entry_value)
        doc_id = entity['finish_week'] + "-"+entity['id']
        entry = temp_entities.get(doc_id,None)
        if entry is None:
            entry = {}
            entry['soft_delete'] = False
            entry['item_type'] = 'Plants'
            entry['supply'] = {}
            entry['finish_week'] = entity['finish_week']
            path_base = 'application_data/Color_Orchids/Sales_Inventory/Converted/GrowWeek'
            parent_path = path_base+'/'+entity['finish_week']+'/Supply'
            path = parent_path + '/Plants'
            entry['path'] = path
            entry['parent_path'] = parent_path
        supply_array = entry['supply'].get(entity['item_name'],[])
        supply_array.append(entity)
        entry['supply'][entity['item_name']] = supply_array
        self._supp_entities[entry_key]['new'] = entity
        temp_entities[doc_id] = entry
        return entry

    def _update_entry(self, entry):
        if entry:
            pg_id = entry['plantgrow']
            supplier = self.suppliers.getEntry(entry['supplier'])
            entry['supplier'] = {'name': supplier['name'],'id': entry['supplier'],'path': supplier['path'], 'type': 'Legacy'} #supplier['name']
            pg_entry = self.plantGrow.getEntry(pg_id)['new']
            entry['item_name'] = pg_entry['item_name']
            entry['item_type'] = pg_entry['item_type']
            entry['id'] = self.get_next_dnl('Supply')
            entry['finish_week'] = pg_entry['finish_week']
            del entry['plantgrow']
        return entry


class DS_ProductPlant(BaseSalesInv):
    def __init__(self, fs_project=None, ds_project=None, prods=None, plts=None,load=True):
        super(DS_ProductPlant, self).__init__(fs_project, ds_project)
        self.products = prods if prods is not None else DS_Product(load=False)
        self.plants = plts if plts is not None else DS_Plants(load=False)
        if load:
            self.run_load()
            self.legacy_load()

    def load_fs(self):
        super(DS_ProductPlant,self).load_fs(True)

    def getEntry(self,inId):
        entry = super(DS_ProductPlant,self).getEntry(inId)
        if entry is None:
            entry = self.get_ds_entry(inId,True)
            if entry is not None:
                entry = self._update_entry(entry)
                self.add_entity(entry)
        return entry
 
    def run_load(self):
        self._entities = {x['id']: x for x in self.get_sr_entities()}
        self._update_entries()

    def legacy_load(self):
        if self._entities is None:
            self._entities = {x['id']: x for x in self.get_sr_entities()}

        super(DS_ProductPlant, self).load_fs()

    def base_path(self):
        return self._create_path()

    @property
    def is_legacy(self):
        return True

    @property
    def the_kind(self):
        return 'ProductPlant'

    def _update_entries(self):
        self._entities = {k: self._update_entry(
            v) for k, v in self._entities.items()}

    def _update_entry(self, entry):
        plt_id = entry['plant']
        plt_entry = self.plants.getEntry(plt_id)
        entry['plant'] = {'name': plt_entry['name'], 'id': plt_id,
                          'path': plt_entry['path'], 'type': 'Legacy'}
        prd_id = entry['product']
        prd_entry = self.products.getEntry(prd_id)
        if prd_entry:
            entry['product'] = {'name': prd_entry['name'],
                                'id': prd_id, 'path': prd_entry['path'], 'type': 'Legacy'}
        else:
            logging.info("cant't find... "+prd_id)
            entry['product'] = {'name': 'Unknown Product: ' +
                                prd_id, 'id': None, 'path': None, 'type': 'Not Found'}
        return entry


class Reserve_Summary(BaseSalesInv):
    def __init__(self, fs_project=None, ds_project=None, reserves=None):
        super(Reserve_Summary, self).__init__(fs_project, ds_project)
        self.growWeek = DS_GrowWeek(fs_project, ds_project,load=False)
        if reserves is None:
            raise Exception("Can't create a summary of nothing... send in some reserves")
        self.reserves = reserves
        #self._post_process = True
        self.run_load()
        
    
    def base_path(self):
        return self._create_path()

    @property
    def is_legacy(self):
        return True

    def run_load(self):
        self._create_reserve_summary()
        self.load_fs()

    @property
    def the_kind(self):
        return 'ReservesSummary'

    def _create_reserve_summary(self):
        '''
        Step 1:  Get a list of all finish_weeks... Create an array of all reserves.. use jmespath to get out the finish_weeks in array
        Step 2:  Convert the array to a set
        Step 3:  Iterate the unique list of finish weeks
        Step 4:  During each iteration use jmespath again to pull out ust the reserves for that finish week
        Step 5:  Create the summary from those
        Step 6:  Load that as an entity, adding GrowWeek as the parent path
        '''
        logging.info("Summarizing Reserves... ")
        base = "[*].{id: id, customer: customer.name, location: location.name, num_reserved: num_reserved, item_name: item.name, item_id: item.id "
        plants = "plants: plants[*].{plant: plant.name,qty:qty}"
        vases = "vases: vases[*].{vase: vase.name, qty: qty}"
        jPath = base+","+plants+","+vases+"}"
        reserves_array = list(self.reserves._entities.values())
        growWeeks = jmespath.search("[*].finish_week",reserves_array)
        growWeeks = list(set(growWeeks))
        for growWeek in growWeeks:
            gw = self.growWeek.getEntry(growWeek)
            legReserves = jmespath.search("[?finish_week == '"+growWeek+"']",reserves_array)
            summReserves = copy.deepcopy(jmespath.search(jPath, legReserves))
            self._update_entry({'summary':summReserves},gw)

    
    def _update_entry(self,entry,gw):
        entry['id'] = gw['id']
        entry['parent_path'] = gw['path']+'/ReservesSummary'
        entry['path'] = entry['parent_path']+'/summary'
        self.add_entity(entry)
        return entry


class DS_ProductReserve(BaseSalesInv):
    def __init__(self, fs_project=None, ds_project=None, prods=None, custs=None, prod_plts=None, gws=None,load=True):
        super(DS_ProductReserve, self).__init__(fs_project, ds_project)
        self.products = prods if prods is not None else DS_Product(load=False)
        self.customers = custs if custs is not None else DS_Customer(load=False)
        self.msr = MapSalesReserves(None,ds_project,fs_project)
        self._post_process = True
        self._copies = {}

        if prod_plts is not None:
            self.product_plants = list(prod_plts._entities.values())
        else:
            logging.info('loading product plants')
            pp = DS_ProductPlant(load=False)
            pp.pull_all_firestore()
            self.product_plants = list(pp._entities.values())
            logging.info('product plants loaded ...')

        self.growWeeks = gws if gws is not None else DS_GrowWeek(load=False)

        if load:
            self.run_load()
            #self.legacy_load()

    def run_load(self):
        self._entities = {x['id']: x for x in self.get_sr_entities()}
        self._update_entries()
        self.load_fs()

    def legacy_load(self):
        if self._entities is None:
            self._entities = {x['id']: x for x in self.get_sr_entities()}

        super(DS_ProductReserve, self).load_fs()

    def base_path(self):
        return self._create_path()

    @property
    def is_legacy(self):
        return True

    @property
    def the_kind(self):
        return 'ProductReserve'

    def load_fs(self):
        super(DS_ProductReserve,self).load_fs(True)

    def getEntry(self,inId):
        entry = super(DS_ProductReserve,self).getEntry(inId)
        if entry is None:
            entry = self.get_ds_entry(inId,True)
            if entry is not None:
                entry = self._update_entry(entry)
                self.add_entity(entry)
        elif entry['path'].find('Legacy') > 0:
            entry = self._update_entry(entry)
        return entry

    def _update_entries(self):
        upEntries = [self._update_entry(entry) for entry in list(self._entities.values())]
        self._entities = {x['id']: x for x in upEntries if x is not None}
            
    def _check_update_converstion(self, entry):
        _id = entry['id']
        cust = entry['customer']['id']
        prod = entry['item']['id']

        if prod is None:
            del self._entities[_id]
            return None

        conv_map = jmespath.search("[?sales_cust_id == '"+cust+"' && sales_prod_id == '"+prod+"'] | [0]",self.msr.conversion_data)
        if conv_map:
            remove = self._do_convert_entry(entry,conv_map)
            if remove:
                del self._entities[_id]
                return None
        return entry
    
    def _do_convert_entry(self,entry,convInfo):
        #print('Converting reserve: {}, with action: {}'.format(entry['id'],convInfo['action']))
        if convInfo['action'] == 'delete':
            return True

        convCustomer = convInfo['match_customer']
        convLocation = convInfo['match_location']
        convItem = convInfo['match_item']['item']

        entry['customer']['name'] = convCustomer['customer_name']
        entry['customer']['id'] = convCustomer['data_number_lookup']
        entry['customer']['path'] = convCustomer['path']
        entry['customer']['type'] = "Item_Tracking"

        entry['location']['name'] = convLocation['location_name']
        entry['location']['id'] = convLocation['data_number_lookup']
        entry['location']['path'] = convLocation['path']
        entry['location']['type'] = "Item_Tracking"

        if convInfo['action'] == 'convert':
            name = convItem['Product_Name']
            dnl = convItem['data_number_lookup']
            path = convItem['path']
            if convInfo['match_item']['copy']:
                '''
                making sure we don't copy something over and over and over and over and over and over and over again
                '''
                copyKey = entry['customer']['id']+"|"+entry['location']['id']
                if self._copies.get(copyKey,{}).get(dnl,None) is None:
                    conversions = self._copies.get(copyKey,{})
                    sb = StorageBlob.create_blob_parent_fromPath('cust_plant_item',convItem,convLocation['path'],'items')
                    name = sb.Product_Name
                    dnl = sb.data_number_lookup
                    path = sb.path
                    conversions[convItem['data_number_lookup']] = sb.data_number_lookup
                    self._copies[copyKey] = conversions
                else:
                    dnl = self._copies[copyKey][convItem['data_number_lookup']]

            entry['item']['name'] = name
            entry['item']['id'] = dnl
            entry['item']['path'] = path
            entry['item']['type'] = "Item_Tracking"

            convPlts = convItem['Plants']
            plants = []
            for plt in convPlts:
                parts = plt.split("|")
                path = 'application_data/Color_Orchids/Customer_Tracking/StorageBlob/recipe_costing/'+parts[0]
                pntEntry = {'plant':{'id': parts[0], 'name': parts[1],'path':path,'type':'recipe_costing'},'qty':1} 
                plants.append(pntEntry)
            entry['plants'] = plants
            
            convVase = convItem['Vase_Style']
            vases = []
            if convVase is not None and len(convVase.split("|")) > 1:
                parts = convVase.split("|")
                path = 'application_data/Color_Orchids/Customer_Tracking/StorageBlob/recipe_costing/'+parts[0]
                vseEntry = {'vase':{'id': parts[0], 'name': parts[1],'path':path,'type':'recipe_costing'},'qty':1}
                vases.append(vseEntry)

            entry['vases'] = vases
            
        return False

    def _update_entry(self, entry):
        cust_id = entry['customer']
        cust_entry = self.customers.getEntry(cust_id)
        entry['location'] = {'name':'','id':'','path':'','type':''}
        if cust_entry:
            entry['customer'] = {'name': cust_entry['customer_name'],
                                 'id': cust_id, 'path': cust_entry['path'], 'type': 'Legacy'}
        else:
            logging.info("Can't find customer... "+cust_id)
            entry['customer'] = {'name': 'Unknown Customer: ' +
                                 cust_id, 'id': None, 'path': None, 'type': 'Not Found'}

        prd_id = entry['product']
        prd_entry = self.products.getEntry(prd_id)
        if prd_entry:
            entry['item'] = {'name': prd_entry['name'], 'id': prd_id,
                             'path': prd_entry['path'], 'type': 'Legacy'}
        else:
            logging.info("Can't find Product... "+prd_id)
            entry['item'] = {'name': 'Unknown Product: '+prd_id,
                             'id': None, 'path': None, 'type': 'Not Found'}

        del entry['product']
        #entry['product_plants'] = jmespath.search("[?product.id == '"+prd_id+"']",self.product_plants)
        prdPlts = jmespath.search("[?product.id == '"+prd_id+"']", self.product_plants)
        plants = []
        for prdPlt in prdPlts:
            plant = {'plant': prdPlt['plant'], 'qty': prdPlt['qty']}
            plants.append(plant)

        entry['plants'] = plants

        gw_id = entry['finish_week']
        gw_entry = self.growWeeks.getEntry(gw_id)

        entry['finish_week'] = gw_entry['id']
        entry['parent_path'] = gw_entry['path'] +'/Reserves'
        entry['path'] = entry['parent_path'] +'/'+entry['id']
        entry = self._check_update_converstion(entry)
        return entry
