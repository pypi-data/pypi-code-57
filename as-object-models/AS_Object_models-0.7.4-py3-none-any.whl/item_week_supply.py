from .sales_inv_utils import SalesInvBase
from datetime import datetime
import jmespath

from . import GetInstance
from . import Supplier

class SupplyCollection(SalesInvBase):
    ext_fields = ['finish_week','item_type','supply','soft_delete','parent_path','path']
    COLLECTION_NAME = 'application_data'

    def __init__(self,fsClient, **kwargs):
        self.soft_delete = kwargs.get('soft_delete',False)
        self.item_type = kwargs.get('item_type','')
        self.supply = kwargs.get('supply',None)
        self.finish_week = kwargs.get('finish_week','')
        self._in_growWeekParent = kwargs.get('_growWeekParent',None)
        self._loaded_supply = {}
        super(SupplyCollection,self).__init__(fsClient, **kwargs)

        if self.supply is not None:
            supply_itemnames = self.supply.keys()
            for supplyname in supply_itemnames:
                supplies = self.supply[supplyname]
                for supply_entry in supplies:
                    supply_entry['_supplyCollection'] = self
                    supply_entry['_growWeekParent'] = self._growWeekParent
                    supply_entry['item_type'] = self.item_type
                    supply = ItemWeekSupply(self._fsClient,**supply_entry)
                    self._loaded_supply[supply.id] = supply

    def base_path(self):
        return self.parent_path+'/Supply'

    @property
    def id(self):
        return self.item_type

    @classmethod
    def getInstance(cls,docRef,gwParent):
        ref,snap = SupplyCollection.getDocuments(docRef)
        docDict = snap.to_dict() if snap.exists else {}
        docDict['fs_docSnap'] = snap
        docDict['fs_docRef'] = ref
        docDict['_growWeekParent'] = gwParent
        return SupplyCollection(SupplyCollection.get_firestore_client(),**docDict)

    @classmethod
    def getOrCreateInstance(cls,docRef,gwParent):
        col = cls.getInstance(docRef,gwParent)
        if not col.exists:
            col.update_ndb(True)
        return col

    @property
    def _growWeekParent(self):
        if self._in_growWeekParent is None:
            gwParDoc = self.get_firestore_client().document(self.parent_path)
            self._in_growWeekParent = GetInstance("GrowWeek",gwParDoc)
        return self._in_growWeekParent

    def getSupplyByItemName(self,item_name):
        return [supply for supply in list(self._loaded_supply.values()) if supply.item_name == item_name]

    def getSupplyById(self,supply_id):
        return self._loaded_supply.get(supply_id,None)

    def create_supply(self, item_name, supplier_id, inforecast,confirmation_num):
        supply_id = self._get_doc_id('Supply')
        supplier = SalesInvBase.GetByDNL(supplier_id,Supplier)
        supply_entry = {}
        supply_entry['_supplyCollection'] = self
        supply_entry['_growWeekParent'] = self._growWeekParent
        supply_entry['item_type'] = self.item_type
        supply_entry['item_name'] = item_name
        suppInfo = {'name': supplier.name,'id': supplier.id,'path': supplier.path}
        supply_entry['supplier'] = suppInfo
        supply_entry['forecast'] = int(inforecast)
        supply_entry['confirmation_num'] = confirmation_num
        supply_entry['id'] = supply_id
        supply = ItemWeekSupply(self._fsClient,**supply_entry)
        self._loaded_supply[supply.id] = supply
        supply._set_add_entries()
        supply._set_update_entries()
        self.update_ndb()
        return supply

    def delete_supply(self, supply_id):
        del self._loaded_supply[supply_id]
        self.update_ndb()

    def update_ndb(self, doCreate=False):
        self.supply = {}
        supply_ids = self._loaded_supply.keys()
        for supply_id in supply_ids:
            sup = self._loaded_supply[supply_id]
            supply_array = self.supply.get(sup.item_name,[])
            supply_array.append(sup.get_dict())
            self.supply[sup.item_name] = supply_array

        return super(SupplyCollection,self).update_ndb(doCreate)


class ItemWeekSupply(SalesInvBase):
    """ This is the class represents all plants that are available during a specific week """

    ext_fields = ['id','supplier','item_name','item_type','forecast','confirmation_num','cost','soft_delete']
    COLLECTION_NAME = 'application_data'
    
    def __init__(self, fsClient, **kwargs):
        self.soft_delete = kwargs.get('soft_delete',False)
        self.supplier = kwargs.get('supplier',{}) 
        self.forecast = kwargs.get('forecast',0) 
        self.supply_id = kwargs.get('id',ItemWeekSupply.GetNextDNL('Supply'))
        self.item_name = kwargs.get('item_name','')
        self.item_type = kwargs.get('item_type','')
        self.cost = kwargs.get('cost','')
        self.confirmation_num = kwargs.get('confirmation_num','') 
        self._growWeekParent = kwargs.get('_growWeekParent',None)
        self._supplyCollection = kwargs.get('_supplyCollection',None)
        super(ItemWeekSupply, self).__init__(fsClient, **kwargs)

    def base_path(self):
        return self._supplyCollection.path
    
    @classmethod
    def get_active(cls):
        return SalesInvBase.GetActive('ItemWeekSupply',ItemWeekSupply)

    @property
    def id(self):
        return self.supply_id

    
    @property
    def path(self):
        return self._supplyCollection.path

    @property
    def parent_path(self):
        return self._supplyCollection.parent_path

    def get_schema(self):
        schema = self.get_bq_schema()
        return schema

    def get_values_dict(self):
        values = self.get_dict()
        return values

    def get_forecast(self):
        if self.forecast:
            return self.forecast
        return 0

    def update(self,argSupplier, argForecast=0, argConfirmation=None, argCost=0):
        #pgs = SalesInvBase.GetByDNL(argId,ItemWeekSupply) #.get_by_id(int(argId))
        if self.supplier['id'] != argSupplier:
            supplier = SalesInvBase.GetByDNL(argSupplier,Supplier)
            suppInfo = {'name': supplier.name,'id': supplier.id,'path': supplier.path}
            self.supplier = suppInfo

        self.forecast = int(argForecast)
        self.confirmation_num = str(argConfirmation)
        self.cost = int(argCost)
        return self.update_ndb()

    def get_itemweeksupply_dict(self):
        pgs = {}
        pgs['id'] = self.id
        pgs['supplier_name'] = self.supplier.get('name','none')
        pgs['supplier_id'] = self.supplier.get('id','none')
        pgs['forecast'] = self.forecast
        pgs['itemweek'] = self.item_name
        pgs['confirmation_num'] = self.confirmation_num
        return pgs

    def get_supply2(self):
        pgsdb = {}
        pgsdb['_id'] = self.id
        pgsdb['supplier'] = self.supplier.get('name','none')
        pgsdb['supplier_id'] = self.supplier.get('id','none')
        pgsdb['forecast'] = self.forecast
        pgsdb['week_id'] = self._growWeekParent.id
        pgsdb['add_date'] = self.timestamp
        pgsdb['item'] = self.item
        #pg = self._growWeekParent.plantgrow.get(self.plantgrow,None)
        #pgsdb['plant_id'] = pg.plant_id if pg is not None else 'none'
        pgsdb['soft_delete'] = "Y" if self.soft_delete and (True == self.soft_delete) else "N"
        return pgsdb

    def update_ndb(self,doCreate=True):
        if doCreate:
            self._set_add_entries()
        self._set_update_entries()
        self._supplyCollection._loaded_supply[self.id] = self
        return self._supplyCollection.update_ndb(doCreate)

    def delete_resp(self):
        if self._supplyCollection._loaded_supply.get(self.id,None) is not None:
            del self._supplyCollection._loaded_supply[self.id]
        
        self._supplyCollection.update_ndb()