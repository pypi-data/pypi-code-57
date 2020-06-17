from . import GetInstance,CallClassMethod
from .utils import FireStoreBase
import logging
'''
This is to generate a unique number with the storage class as a prefix
This class should only have 1 entry per storage class at max
'''
class DataNumber(FireStoreBase):

    COLLECTION_NAME = 'data_number_sync'
    ext_fields = ['data_storage_type','number']
    logger = logging.getLogger("DataNumber")

    def __init__(self, fsClient, **kwargs):
        self.data_storage_type = kwargs.get('data_storage_type','') #ndb.KeyProperty(kind=DataStorageType, required=True)
        self.number = kwargs.get('number','') #ndb.IntegerProperty(default=100, required=True)
        super(DataNumber, self).__init__(fsClient, **kwargs)

    def base_path(self):
        return DataNumber.__basePath(self._fsClient)

    @classmethod
    def basePath(cls):
        return DataNumber.__basePath(DataNumber.get_client())

    @classmethod
    def __basePath(cls,inClient):
        return DataNumber.COLLECTION_NAME+'/'+inClient.company+'/'+inClient.application

    @classmethod
    def getInstance(cls,fsDocument):
        ref,snap = cls.getDocuments(fsDocument)
        docDict = snap.to_dict()
        docDict['fs_docSnap'] = snap
        docDict['fs_docRef'] = ref
        return cls(cls.get_firestore_client(),**docDict)

    @classmethod
    def createInstance(cls,storeName,dst=None):
        clt = DataNumber.get_client()
        dnRef = clt.fsClient.document(DataNumber.__basePath(clt)+'/'+storeName)
        if dnRef.get().exists:
            return DataNumber.getInstance(dnRef)

        data = {}
        data['data_storage_type'] = dst.path if dst else 'No Storage Type'
        data['number'] = 99
        data['fs_docRef'] = dnRef
        dn = DataNumber(clt,**data)
        dn.update_ndb(True)
        return dn

    @classmethod
    def get_type_number(cls,storeName):
        dst = CallClassMethod('DataStorageType','get_dataStorageType',storeName) #DataStorageType.get_dataStorageType(storeName)

        dn = DataNumber.createInstance(storeName,dst)

        dn.number = dn.number + 1
        dn.update_ndb()

        return storeName+"-"+str(dn.number)

'''
Saving storage blobs by the unique DataNumber for easy retrieval
'''
class DataNumberLookup(object):

    COLLECTION_NAME = 'data_number_lookup'
    logger = logging.getLogger("DataNumberLookup")

    @classmethod
    def basePath(cls):
        return DataNumberLookup.__basePath(DataNumber.get_client())

    @classmethod
    def __basePath(cls,inClient):
        return DataNumberLookup.COLLECTION_NAME+'/'+inClient.company #+'/'+inClient.application

    @classmethod
    def store_data_number(cls, dn, storeBlobKey):
        raise Exception("Method not implemented: 'store_data_number', use method store_data_number_sbPath")

    @classmethod
    def _get_collection_type(cls, dnl):
        if dnl:
            parts = dnl.split("-")
            if len(parts) > 1:
                return "DNL_"+parts[0]
        return DataNumber.get_client().application

    @classmethod
    def store_data_number_sbPath(cls,dn,sb_path):
        colName = DataNumberLookup._get_collection_type(dn)
        dnlRef = DataNumber.get_firestore_client().document(DataNumberLookup.basePath()+'/'+colName+'/'+dn)
        dnlRef.set({'path':sb_path})

    @classmethod
    def create_dnl(cls, docRef):
        dnl = docRef.id
        path = docRef.path
        DataNumberLookup.store_data_number_sbPath(dnl,path)

    @classmethod
    def remove_dnl(cls,dnl):
        if dnl == '' or dnl is None:
            return False

        colName = DataNumberLookup._get_collection_type(dnl)
        dnlRef = DataNumber.get_firestore_client().document(DataNumberLookup.basePath()+'/'+colName+'/'+dnl)
        try:
            dnlRef.delete()
            return True
        except Exception:
            return False

    @classmethod
    def get_path_for_dnl(cls,dn):
        return cls._get_path_for_dnl(DataNumber.get_firestore_client(),dn)

    @classmethod
    def _get_path_for_dnl(cls,fsClient, dn):
        if dn == '' or dn is None:
            return None
        
        colName = DataNumberLookup._get_collection_type(dn)
        dnlRef = fsClient.document(DataNumberLookup.basePath()+'/'+colName+'/'+dn)
        snap = dnlRef.get()
        if snap.exists:
            return snap.get('path')
        return None

    @classmethod
    def delete_obj_by_dnl(cls,dnl):
        '''
        We'll use the datanumberlookup concept to load and clean up the DNL and the object
        '''
        resp = "success"
        try:
            colName = DataNumberLookup._get_collection_type(dnl)
            dnlRef = DataNumber.get_firestore_client().document(DataNumberLookup.basePath()+'/'+colName+'/'+dnl)
            snap = dnlRef.get()
            if snap.exists:
                docRef = DataNumber.get_firestore_client().document(snap.get('path'))
                docRef.delete() 
                dnlRef.delete()
        except Exception as e:
            resp = str(e)
        
        return resp


    @classmethod
    def get_obj_by_dnl(cls,dnl,clzz):
        return DataNumberLookup._get_obj_by_dnl(DataNumber.get_firestore_client(),dnl,clzz)

    @classmethod
    def _get_obj_by_dnl(cls,fsClient,dnl,clzz):
        '''
        We'll use the datanumberlookup concept to load, with the expectation that every python object
        that represents a record in firestore has a "getInstance" method
        '''
        colName = DataNumberLookup._get_collection_type(dnl)
        dnlRef = fsClient.document(DataNumberLookup.basePath()+'/'+colName+'/'+dnl)
        snap = dnlRef.get()
        if snap.exists:
            docRef = fsClient.document(snap.get('path'))
            try:
                return clzz.getInstance(docRef)
            except Exception:
                cls.logger.error("Could not instantiate {}.. returning None".format(str(clzz)))
                return None
        else:
            cls.logger.error("Document not found for {}... returning None".format(dnl))
            return None

    @classmethod
    def get_doc_children(cls, dnl, collName):
        docPath = DataNumberLookup.get_path_for_dnl(dnl)
        if docPath is not None:
            colPath = docPath+"/"+collName
            colRef = DataNumber.get_firestore_client().collection(colPath)
            docRefs = colRef.list_documents()
            return docRefs
        
        return []


    @classmethod
    def get_storeblob(cls, dataNumber):
        colName = DataNumberLookup._get_collection_type(dataNumber)
        dnlRef = DataNumber.get_firestore_client().document(DataNumberLookup.basePath()+'/'+colName+'/'+dataNumber)
        dnl = dnlRef.get()
        if dnl.exists:
            doc = DataNumber.get_firestore_client().document(dnlRef.get('path'))
            return GetInstance('StorageBlob',doc)
        return None