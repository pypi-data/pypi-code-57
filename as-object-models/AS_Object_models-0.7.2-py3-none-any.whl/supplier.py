from .utils import FireStoreBase

class Supplier(FireStoreBase):

    ext_fields = ['name','soft_delete','parent_path','path']
    COLLECTION_NAME = 'application_data'

    """ Represents the supplier of plants """
    #name = ndb.StringProperty(required=True)
    def __init__(self, fsClient, **kwargs):
        self.soft_delete = kwargs.get('soft_delete',False)
        self.name = kwargs.get('name','') 
        super(Supplier, self).__init__(fsClient, **kwargs)
    
    def base_path(self):
        return Supplier.__basePath(self._fsClient)

    @classmethod
    def basePath(cls):
        return Supplier.__basePath(Supplier.get_client())

    @classmethod
    def __basePath(cls,inClient):
        return Supplier.COLLECTION_NAME+'/'+inClient.company+'/Customer_Tracking/StorageBlob/Supplier'

    @classmethod
    def getInstance(cls,fsDocument):
        ref,snap = Supplier.getDocuments(fsDocument)
        docDict = snap.to_dict() if snap.exists else {}
        docDict['fs_docSnap'] = snap
        docDict['fs_docRef'] = ref
        return Supplier(Supplier.get_firestore_client(),**docDict)

    @classmethod
    def get_active(cls):
        #return NDBBase.get_active('Supplier')
        return Supplier.get_active_any(Supplier.get_firestore_client(), Supplier.basePath(), Supplier)

    def get_schema(self):
        schema = self.get_bq_schema()
        schema['fields'].append({'field_name':'name','field_type':'string','field_required':True})
        return schema

    def get_values_dict(self):
        values = self.get_dict()
        values['name'] = self.name
        return values

    def plantgrow(self):
        #return PlantGrow.query(PlantGrow.supplier == self.key)
        raise Exception("propert plantgrow not implemented")

    @classmethod
    def dev_get_create(cls):
        #suppliers = Supplier.query().fetch()
        col = Supplier.get_firestore_client().collection(Supplier.__basePath)
        docRefs = col.list_documents()
        suppliers = [Supplier.getInstance(x) for x in docRefs]
        if not suppliers:
            d = {'name':'Test Supplier'}
            s = Supplier(Supplier.get_firestore_client(),**d)
            s.update_ndb()