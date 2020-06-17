from .sales_inv_utils import SalesInvBase
from .utils import FSObjSummary
from datetime import datetime
import jmespath

from . import GetInstance
from . import DataNumber, DataNumberLookup

'''
In order to make the production view screen return relatively quickly.. I needed a way to identify when a new vase was entered that needed tracked
... 

This adds an extra step for the user, that they have to add it as a "recipe vase"... and also add it here to configure it to be tracked.

However, this also allows more control on how vases in a recipe are tracked... by turning some off (cleaning up the view) or remapping on the fly
'''
class SalesActiveVases(SalesInvBase):
    """ This is the class represents all vases that are available during a specific week """

    ext_fields = ['vases', 'soft_delete','parent_path','path']
    COLLECTION_NAME = 'application_data'
    
    def __init__(self, fsClient, **kwargs):
        self.soft_delete = kwargs.get('soft_delete',False)
        self.vases = kwargs.get('vases',{})
    
        super(SalesActiveVases, self).__init__(fsClient, **kwargs)

    def base_path(self):
        return SalesActiveVases.__basePath(self._fsClient)

    @classmethod
    def basePath(cls):
        return SalesActiveVases.__basePath(SalesActiveVases.get_client())

    @classmethod
    def __basePath(cls,inClient):
        return SalesActiveVases.COLLECTION_NAME+'/'+inClient.company+'/Sales_Inventory/Converted/SalesActiveVases'


    @classmethod
    def getInstance(cls,fsDocument):
        ref,snap = SalesActiveVases.getDocuments(fsDocument)
        docDict = snap.to_dict() if snap.exists else {}
        docDict['fs_docSnap'] = snap
        docDict['fs_docRef'] = ref
        return SalesActiveVases(SalesActiveVases.get_firestore_client(),**docDict)
  
    def get_schema(self):
        schema = self.get_bq_schema()
        return schema

    def get_values_dict(self):
        values = self.get_dict()
        return values

    @classmethod
    def display_recipe_vases(cls):
        recipeVases = SalesActiveVases.get_active_recipe_vases(fldKey='data_number_lookup')
        productionViewVases = SalesActiveVases.get_all_dict()
        entries = {}
        for rp in list(recipeVases.values()):
            pvp = productionViewVases.get(rp.data_number_lookup,None)
            if pvp:
                pvp['tracked'] = True
                pvp['vase_id'] = pvp['id']
                pvp['vase_path'] = pvp['path']
                pvp['vase_name'] = pvp['name']
                entries[pvp['id']] = pvp
            else:
                d = {'vase_name':rp.name}
                d['vase_id'] = rp.id
                d['vase_path'] = rp.path
                d['tracked'] = False
                entries[d['vase_id']] = d
            
        return entries


    @classmethod
    def get_active_recipe_vases(cls,fldKey='name'):
        path = 'application_data/Color_Orchids/Customer_Tracking/StorageBlob/recipe_costing'
        colRef = SalesActiveVases.get_firestore_client().collection(path)
        q = colRef.where('item_type','==','Vase')
        q = q.where('status','==','Active')
        snaps = q.stream()
        plts = {x.get(fldKey):SalesActiveVases.GetStorageBlobInstance(x) for x in snaps if x.get('name') != 'N/A'}
        return plts

    @classmethod
    def remove_vase(cls,activeVaseId):
        sap = SalesActiveVases.get_entry()
        entry = sap.vases.get(activeVaseId,None)
        if entry is not None:
            del sap.vases[activeVaseId]
        sap.update_ndb()
        return {'status':'success','msg':'Deleted Successfully', 'didDelete':True}

    @classmethod
    def add_vase_by_id(cls, vase_id):
        recipe_vase = SalesActiveVases.GetSBObjByDNL(vase_id)
        return SalesActiveVases.add_vase(recipe_vase)

    @classmethod
    def add_vase_by_name(cls, vase_name):
        plts = SalesActiveVases.get_active_recipe_vases()
        recipeVase = plts.get(vase_name,None)
        if recipeVase is not None:
            return SalesActiveVases.add_vase(recipeVase)
        
        return None

    @classmethod
    def _setup_entry(self):
        _id = SalesActiveVases.GetNextDNL('SalesActiveVases')
        doc_path = SalesActiveVases.basePath()+"/"+_id
        sap = SalesActiveVases.getInstance(SalesActiveVases.get_firestore_client().document(doc_path))
        sap.update_ndb()
        return sap

    @classmethod
    def add_vase(cls, recipe_vase):
        sap = cls.get_entry()
        vaseD = sap.vases.get('recipe_vase.id',{})
        vaseD['id'] = recipe_vase.id
        vaseD['name'] = recipe_vase.name
        vaseD['path'] = recipe_vase.path
        sap.vases[recipe_vase.id] = vaseD
        
        sap.update_ndb()
        return sap

    @classmethod
    def get_entry(cls):
        col = SalesActiveVases.get_firestore_client().collection(SalesActiveVases.basePath())
        docRefs = col.list_documents()
        activeVases = [SalesActiveVases.getInstance(x) for x in docRefs]
        if len(activeVases) > 0:
            if len(activeVases) > 1:
                raise Exception("There are too many SalesActiveVases items!!!")
            else:
                return activeVases[0]
        return cls._setup_entry()
    
    @classmethod
    def get_all(cls):
        aps = SalesActiveVases.get_entry()
        objDict = {}
        for key in aps.vases.keys():
            objDict[key] = FSObjSummary(**aps.vases[key])
        
        return objDict
    
    @classmethod
    def get_all_dict(cls):
        aps = SalesActiveVases.get_entry()
        return aps.vases
