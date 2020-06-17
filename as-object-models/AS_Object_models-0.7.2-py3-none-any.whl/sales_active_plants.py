from .sales_inv_utils import SalesInvBase
from .utils import FSObjSummary
from datetime import datetime
import jmespath

from . import GetInstance
from . import DataNumber, DataNumberLookup

'''
In order to make the production view screen return relatively quickly.. I needed a way to identify when a new plant was entered that needed tracked
... 

This adds an extra step for the user, that they have to add it as a "recipe plant"... and also add it here to configure it to be tracked.

However, this also allows more control on how plants in a recipe are tracked... by turning some off (cleaning up the view) or remapping on the fly
'''
class SalesActivePlants(SalesInvBase):
    """ This is the class represents all plants that are available during a specific week """

    ext_fields = ['plants', 'soft_delete','parent_path','path']
    COLLECTION_NAME = 'application_data'
    
    def __init__(self, fsClient, **kwargs):
        self.soft_delete = kwargs.get('soft_delete',False)
        self.plants = kwargs.get('plants',{})
    
        super(SalesActivePlants, self).__init__(fsClient, **kwargs)

    def base_path(self):
        return SalesActivePlants.__basePath(self._fsClient)

    @classmethod
    def basePath(cls):
        return SalesActivePlants.__basePath(SalesActivePlants.get_client())

    @classmethod
    def __basePath(cls,inClient):
        return SalesActivePlants.COLLECTION_NAME+'/'+inClient.company+'/Sales_Inventory/Converted/SalesActivePlants'


    @classmethod
    def getInstance(cls,fsDocument):
        ref,snap = SalesActivePlants.getDocuments(fsDocument)
        docDict = snap.to_dict() if snap.exists else {}
        docDict['fs_docSnap'] = snap
        docDict['fs_docRef'] = ref
        return SalesActivePlants(SalesActivePlants.get_firestore_client(),**docDict)
  
    def get_schema(self):
        schema = self.get_bq_schema()
        return schema

    def get_values_dict(self):
        values = self.get_dict()
        return values

    @classmethod
    def display_recipe_plants(cls):
        recipePlants = SalesActivePlants.get_active_recipe_plants(fldKey='data_number_lookup')
        productionViewPlants = SalesActivePlants.get_all_dict()
        entries = {}
        for rp in list(recipePlants.values()):
            pvp = productionViewPlants.get(rp.data_number_lookup,None)
            if pvp:
                pvp['tracked'] = True
                pvp['plant_id'] = pvp['id']
                pvp['plant_path'] = pvp['path']
                pvp['plant_name'] = pvp['name']
                entries[pvp['id']] = pvp
            else:
                d = {'plant_name':rp.name}
                d['plant_id'] = rp.id
                d['plant_path'] = rp.path
                d['tracked'] = False
                entries[d['plant_id']] = d
            
        return entries


    @classmethod
    def get_active_recipe_plants(cls,fldKey='name'):
        path = 'application_data/Color_Orchids/Customer_Tracking/StorageBlob/recipe_costing'
        colRef = SalesActivePlants.get_firestore_client().collection(path)
        q = colRef.where('item_type','==','Plants')
        q = q.where('status','==','Active')
        snaps = q.stream()
        plts = {x.get(fldKey):SalesActivePlants.GetStorageBlobInstance(x) for x in snaps if x.get('name') != 'N/A'}
        return plts

    @classmethod
    def remove_plant(cls,activePlantId):
        sap = SalesActivePlants.get_entry()
        entry = sap.plants.get(activePlantId,None)
        if entry is not None:
            del sap.plants[activePlantId]
        sap.update_ndb()
        return {'status':'success','msg':'Deleted Successfully', 'didDelete':True}

    @classmethod
    def add_plant_by_id(cls, plant_id):
        recipe_plant = SalesActivePlants.GetSBObjByDNL(plant_id)
        return SalesActivePlants.add_plant(recipe_plant)

    @classmethod
    def add_plant_by_name(cls, plant_name):
        plts = SalesActivePlants.get_active_recipe_plants()
        recipePlant = plts.get(plant_name,None)
        if recipePlant is not None:
            return SalesActivePlants.add_plant(recipePlant)
        
        return None

    @classmethod
    def _setup_entry(self):
        _id = SalesActivePlants.GetNextDNL('SalesActivePlants')
        doc_path = SalesActivePlants.basePath()+"/"+_id
        sap = SalesActivePlants.getInstance(SalesActivePlants.get_firestore_client().document(doc_path))
        sap.update_ndb()
        return sap

    @classmethod
    def add_plant(cls, recipe_plant):
        sap = cls.get_entry()
        plantD = sap.plants.get('recipe_plant.id',{})
        plantD['id'] = recipe_plant.id
        plantD['name'] = recipe_plant.name
        plantD['path'] = recipe_plant.path
        sap.plants[recipe_plant.id] = plantD
        
        sap.update_ndb()
        return sap

    @classmethod
    def get_entry(cls):
        col = SalesActivePlants.get_firestore_client().collection(SalesActivePlants.basePath())
        docRefs = col.list_documents()
        activePlants = [SalesActivePlants.getInstance(x) for x in docRefs]
        if len(activePlants) > 0:
            if len(activePlants) > 1:
                raise Exception("There are too many SalesActivePlants items!!!")
            else:
                return activePlants[0]
        return cls._setup_entry()
    
    @classmethod
    def get_all(cls):
        aps = SalesActivePlants.get_entry()
        objDict = {}
        for key in aps.plants.keys():
            objDict[key] = FSObjSummary(**aps.plants[key])
        
        return objDict
    
    @classmethod
    def get_all_dict(cls):
        aps = SalesActivePlants.get_entry()
        return aps.plants
