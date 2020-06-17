from .sales_inv_utils import SalesInvBase
from .utils import FSObjSummary
from datetime import datetime
import jmespath

from . import GetInstance
from . import DataNumber, DataNumberLookup
from .item_week import ItemWeek

'''
In order to make the production view screen return relatively quickly.. I needed a way to identify when a new item was entered and needed tracked
... 

This adds an extra step for the user, that they have to add it as a "recipe item"... and also add it here to configure it to be tracked.

However, this also allows more control on how items in a recipe are tracked... by turning some off (cleaning up the view) or remapping on the fly
'''
class InventoryActiveItems(SalesInvBase):
    """ This is the class represents all items that are available during a specific week """

    ext_fields = ['item_type', 'items','soft_delete','parent_path','path']
    COLLECTION_NAME = 'application_data'
    
    def __init__(self, fsClient, **kwargs):
        self.soft_delete = kwargs.get('soft_delete',False)
        self.item_type = kwargs.get('item_type','')
        self.items = kwargs.get('items',{})
    
        super(InventoryActiveItems, self).__init__(fsClient, **kwargs)

    def base_path(self):
        return InventoryActiveItems.__basePath(self._fsClient)

    @classmethod
    def basePath(cls):
        return InventoryActiveItems.__basePath(InventoryActiveItems.get_client())

    @classmethod
    def __basePath(cls,inClient):
        return InventoryActiveItems.COLLECTION_NAME+'/'+inClient.company+'/Sales_Inventory/Converted/InventoryActiveItems'


    @classmethod
    def getInstance(cls,fsDocument):
        ref,snap = InventoryActiveItems.getDocuments(fsDocument)
        docDict = snap.to_dict() if snap.exists else {}
        docDict['fs_docSnap'] = snap
        docDict['fs_docRef'] = ref
        return InventoryActiveItems(InventoryActiveItems.get_firestore_client(),**docDict)
  
    def get_schema(self):
        schema = self.get_bq_schema()
        return schema

    def get_values_dict(self):
        values = self.get_dict()
        return values

    @classmethod
    def __clean_item_type(cls,item_type):
        return ItemWeek.CleanItemType(item_type)

    @classmethod
    def display_recipe_items(cls,item_type):
        recipeItems = InventoryActiveItems.get_active_recipe_items(item_type,fldKey='data_number_lookup')
        productionViewItems = InventoryActiveItems.get_all_dict(item_type)
        entries = {}
        prefix = cls.__clean_item_type(item_type)
        for rp in list(recipeItems.values()):
            pvp = productionViewItems.get(rp.data_number_lookup,None)
            if pvp:
                pvp['tracked'] = True
                pvp[prefix+'_id'] = pvp['id']
                pvp[prefix+'_path'] = pvp['path']
                pvp[prefix+'_name'] = pvp['name']
                entries[pvp['id']] = pvp
            else:
                d = {prefix+'_name':rp.name}
                d[prefix+'_id'] = rp.id
                d[prefix+'_path'] = rp.path
                d['tracked'] = False
                entries[d[prefix+'_id']] = d
            
        return entries


    @classmethod
    def get_active_recipe_items(cls,item_type, fldKey='name'):
        path = 'application_data/Color_Orchids/Customer_Tracking/StorageBlob/recipe_costing'
        colRef = InventoryActiveItems.get_firestore_client().collection(path)
        q = colRef.where('item_type','==',item_type)
        q = q.where('status','==','Active')
        snaps = q.stream()
        plts = {x.get(fldKey):InventoryActiveItems.GetStorageBlobInstance(x) for x in snaps if x.get('name') != 'N/A'}
        return plts

    @classmethod
    def remove_item(cls,activeItemId):
        recipeItem = InventoryActiveItems.GetSBObjByDNL(activeItemId)
        sap = InventoryActiveItems.get_entry(recipeItem.item_type)
        entry = sap.items.get(activeItemId,None)
        if entry is not None:
            del sap.items[activeItemId]
        sap.update_ndb()
        return {'status':'success','msg':'Deleted Successfully', 'didDelete':True}

    @classmethod
    def add_item_by_id(cls, recipe_id):
        recipeItem = InventoryActiveItems.GetSBObjByDNL(recipe_id)
        return InventoryActiveItems.add_item(recipeItem)

    @classmethod
    def add_item_by_name(cls, item_type, name):
        items = InventoryActiveItems.get_active_recipe_items(item_type)
        recipeItem = items.get(name,None)
        if recipeItem is not None:
            return InventoryActiveItems.add_item(recipeItem)
        
        return None

    @classmethod
    def _setup_entry(self,item_type):
        doc_path = InventoryActiveItems.basePath()+"/"+item_type
        sap = InventoryActiveItems.getInstance(InventoryActiveItems.get_firestore_client().document(doc_path))
        sap.item_type = item_type
        sap.update_ndb()
        return sap

    @classmethod
    def add_item(cls, recipe_entry):
        sap = cls.get_entry(recipe_entry.item_type)
        itemD = sap.items.get(recipe_entry.id,{})
        itemD['id'] = recipe_entry.id
        itemD['name'] = recipe_entry.name
        itemD['path'] = recipe_entry.path
        sap.items[recipe_entry.id] = itemD
        
        sap.update_ndb()
        return sap

    @classmethod
    def get_entry(cls, item_type):
        docRef = InventoryActiveItems.get_firestore_client().document(InventoryActiveItems.basePath()+'/'+item_type)
        activeItem = InventoryActiveItems.getInstance(docRef)
        if activeItem.exists:
            return activeItem
        return cls._setup_entry(item_type)
    
    @classmethod
    def get_all(cls,item_type):
        aps = InventoryActiveItems.get_entry(item_type)
        objDict = {}
        for key in aps.items.keys():
            objDict[key] = FSObjSummary(**aps.items[key])
        
        return objDict
    
    @classmethod
    def get_all_dict(cls,item_type):
        aps = InventoryActiveItems.get_entry(item_type)
        return aps.items


class InventoryItems(SalesInvBase):
    """ This is the class represents all items that are available during a specific week """

    ext_fields = ['tracked_items','soft_delete','parent_path','path']
    COLLECTION_NAME = 'application_data'
    
    def __init__(self, fsClient, **kwargs):
        self.soft_delete = kwargs.get('soft_delete',False)
        self.tracked_items = kwargs.get('tracked_items',[])
        super(InventoryItems, self).__init__(fsClient, **kwargs)

    def base_path(self):
        return InventoryItems.__basePath(self._fsClient)

    @classmethod
    def basePath(cls):
        return InventoryItems.__basePath(InventoryItems.get_client())

    @classmethod
    def __basePath(cls,inClient):
        return InventoryItems.COLLECTION_NAME+'/'+inClient.company+'/Sales_Inventory/Converted/InventoryItems'


    @classmethod
    def getInstance(cls):
        fsDocument = InventoryItems.get_firestore_client().document(cls.basePath()+'/InventoryItems')
        ref,snap = InventoryItems.getDocuments(fsDocument)
        docDict = snap.to_dict() if snap.exists else {}
        docDict['fs_docSnap'] = snap
        docDict['fs_docRef'] = ref
        ii = InventoryItems(InventoryItems.get_firestore_client(),**docDict)
        if not ii.exists:
            ii.update_ndb(True)
        return ii
  