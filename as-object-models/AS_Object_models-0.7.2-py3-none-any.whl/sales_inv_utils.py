from .utils import FireStoreBase

from .quick_storage import QuickStorage
from .storage_blob import StorageBlob
from .data_number import DataNumber, DataNumberLookup

class SalesInvBase(FireStoreBase):

    def _get_sb_by_dnl(self,inId):
        return StorageBlob.get_by_dnl(inId)
    
    def _get_sb_instance_by_path(self,path):
        return SalesInvBase.GetSBObj(path)

    def _get_doc_id(self, storeName):
        return SalesInvBase.GetNextDNL(storeName)

    def _insert_dnl(self, docRef):
        DataNumberLookup.create_dnl(docRef)

    def _delete_by_dnl(self,dnl):
        return DataNumberLookup.delete_obj_by_dnl(dnl)

    @classmethod
    def GetSBObj(self,path):
        return StorageBlob.getInstanceByPath(path)
    
    @classmethod
    def GetSB(self,docRef):
        return StorageBlob.getInstance(docRef)

    @classmethod
    def GetSBObjByDNL(self,dnl):
        return SalesInvBase.GetByDNL(dnl,StorageBlob)


    @classmethod
    def AddDNL(cls,dnl, path):
        return DataNumberLookup.store_data_number_sbPath(dnl,path)
        
    @classmethod
    def GetNextDNL(cls,inName):
        dn = DataNumber.createInstance(inName)

        dn.number = dn.number + 1
        dn.update_ndb()

        return inName+"-"+str(dn.number)

    @classmethod
    def DeleteByDNL(cls,dnl):
        return DataNumberLookup.delete_obj_by_dnl(dnl)

    @classmethod
    def GetActive(cls,collectionName, clzz):
        cg = SalesInvBase.get_firestore_client().collection_group(collectionName)
        q = cg.where('soft_delete','!=','true')
        objArr = []
        for snap in q.stream():
            if clzz:
                clsObj = clzz.getInstance(snap)
                objArr.append(clsObj)
            else:
                d = snap.to_dict()
                d['id'] = snap.id
                objArr.append(d)
        
        return objArr


    @classmethod
    def GetByDNL(cls,dnl,clzz):
        return DataNumberLookup.get_obj_by_dnl(dnl,clzz)

    def _get_cust_info(self,customer):
        return {'id':customer.id,
        'name':customer.customer_name,
        'path':customer.path,
        'type':'Item_Tracking'}

    def _get_item_info(self,item):
        return {'id':item.id,
        'name':item.Product_Name,
        'path':item.path,
        'type':'Item_Tracking'}

    def _get_loc_info(self,location):
        return {'id':location.id,
        'name':location.location_name,
        'path':location.path,
        'type':'Item_Tracking'}

    def _get_sb_instance(self,fsDoc):
        return SalesInvBase.getInstanceAny(StorageBlob,fsDoc)

    @classmethod
    def GetStorageBlobInstance(cls,fsDoc):
        return SalesInvBase.getInstanceAny(StorageBlob,fsDoc)

    def _get_recipe_costing_item(self, item_type, item_name):
        path = 'application_data/Color_Orchids/Customer_Tracking/StorageBlob/recipe_costing'
        colRef = self._fsClient.collection(path)
        q = colRef.where('item_type','==',item_type)
        #q = q.where('status','==','Active')
        q = q.where('name','==',item_name)
        snaps = q.stream()
        items = [{'name':x.get('name'),'id':x.id,'path':x.reference.path,'type':'recipe_costing'} for x in snaps]
        return None if len(items) == 0 else items[0]

    def _get_item_recipe(self, item_type, recipe_entry):
        parts = recipe_entry.split("|")
        if len(parts) == 1:
            return self._get_recipe_costing_item(item_type, parts[0])

        itemDNL = parts[0]
        itemName = parts[1]
        itemInfo = StorageBlob.get_by_dnl(itemDNL)
        if itemInfo is None:
            itemInfo = self._get_recipe_costing_item(item_type, itemName)
        else:
            itemInfo = {'name':itemInfo.name,'id':itemInfo.id,'path':itemInfo.path,'type':'recipe_costing'}

        return itemInfo