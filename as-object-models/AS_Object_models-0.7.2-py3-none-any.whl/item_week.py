from .sales_inv_utils import SalesInvBase
from datetime import datetime
import jmespath

from .item_week_notes import ItemWeekNotes, NotesCollection
from .item_week_supply import ItemWeekSupply, SupplyCollection
from .supplier import Supplier
from . import GetInstance

class ItemWeekCollection(SalesInvBase):
    ext_fields = ['items','item_type','finish_week','soft_delete','parent_path','path']
    COLLECTION_NAME = 'application_data'

    IWS = "Supply"
    IWN = "Notes"

    def __init__(self,fsClient, **kwargs):
        self.soft_delete = kwargs.get('soft_delete',False)
        self.items = kwargs.get('items',None)
        self.item_type = kwargs.get('item_type','')
        self.finish_week = kwargs.get('finish_week','')
        self._in_growWeekParent = kwargs.get('_growWeekParent',None)
        self._loaded_items = {}

        super(ItemWeekCollection,self).__init__(fsClient, **kwargs)

        if self.exists:
            self.post_create_activities()
    
    def post_create_activities(self):
        self._notes_collection = NotesCollection.getOrCreateInstance(self._fsClient.document(self.notes_path),self._in_growWeekParent)
        self._supply_collection = SupplyCollection.getOrCreateInstance(self._fsClient.document(self.supply_path),self._in_growWeekParent)

        if self.items is not None:
            item_names = self.items.keys()
            for item_name in item_names:
                item_dict = self.items[item_name]
                item_dict['_itemCollection'] = self
                item_dict['_notesCollection'] = self._notes_collection
                item_dict['_supplyCollection'] = self._supply_collection
                item_dict['_growWeekParent'] = self._growWeekParent
                self._loaded_items[item_name] = ItemWeek(self._fsClient,**item_dict)

        
    def base_path(self):
        return self.parent_path+'/Items'

    @property
    def id(self):
        return self.item_type

    @property
    def notes_path(self):
        return self._growWeekParent.path+'/'+self.IWN+'/'+self.item_type
    
    @property
    def supply_path(self):
        return self._growWeekParent.path+'/'+self.IWS+'/'+self.item_type

    @classmethod
    def getInstance(cls,docRef,gwParent):
        ref,snap = ItemWeekCollection.getDocuments(docRef)
        docDict = snap.to_dict() if snap.exists else {}
        docDict['fs_docSnap'] = snap
        docDict['fs_docRef'] = ref
        docDict['_growWeekParent'] = gwParent
        return ItemWeekCollection(ItemWeekCollection.get_firestore_client(),**docDict)

    @classmethod
    def getOrCreateInstance(cls,item_type,gwParent):
        iwc = cls.getInstance(gwParent._fsClient.document(gwParent.path+'/Items/'+item_type),gwParent)
        if not iwc.exists:
            iwc.item_type = item_type
            iwc.finish_week = gwParent.id
            iwc.update_ndb(True)
            iwc.post_create_activities()
        return iwc


    @property
    def _growWeekParent(self):
        if self._in_growWeekParent is None:
            gwParDoc = self.get_firestore_client().document(self.parent_path)
            self._in_growWeekParent = GetInstance("GrowWeek",gwParDoc)
        return self._in_growWeekParent

    def create_itemweek_entry(self, item, gwPar):
        ''' Input is going to be recipe item '''
        cleanName = ItemWeek.CleanItemName(item.name)
        iw = self._loaded_items.get(cleanName,None)
        if iw is None:
            item_dict = {}
            itemObj = self._get_sb_instance_by_path(item.path)
            item_dict['item'] = {'name':itemObj.name,'id':itemObj.id,'path':itemObj.path}
            item_dict['name'] = itemObj.name
            item_dict['item_type'] = self.item_type
            item_dict['finish_week'] = self.finish_week
            item_dict['actual'] = 0
            item_dict['want_qty'] = 0
            item_dict['color_groupings'] = {}
            item_dict['groupings'] = {}
            item_dict['_growWeekParent'] = gwPar
            item_dict['_itemCollection'] = self
            item_dict['_notesCollection'] = self._notes_collection
            item_dict['_supplyCollection'] = self._supply_collection
            iw = ItemWeek(self._fsClient,**item_dict)
            iw.update_ndb()
        return iw

    def get_itemweek(self,itemName):
        cleanName = ItemWeek.CleanItemName(itemName)
        return self._loaded_items.get(cleanName,None)

    def get_supply(self):
        return self._supply_collection

    def get_notes(self):
        return self._notes_collection

    def update_ndb(self, doCreate=False):
        if self.items is None:
            self.items = {}

        item_names = self._loaded_items.keys()
        for item_name in item_names:
            self.items[item_name] = self._loaded_items[item_name].get_dict()

        super(ItemWeekCollection,self).update_ndb(doCreate)


class ItemWeek(SalesInvBase):
    """ This is the class represents all plants that are available during a specific week """

    ext_fields = ['item','name','item_name','item_type','finish_week','actual','want_qty','color_groupings','groupings','soft_delete','parent_path','path']
    COLLECTION_NAME = 'application_data'
    
    def __init__(self, fsClient, **kwargs):
        self.soft_delete = kwargs.get('soft_delete',False)
        self.name = kwargs.get('name','')
        self.item_type = kwargs.get('item_type',None)
        self._collection_parent = kwargs.get('_itemCollection',None)
        self._notesCollection = kwargs.get('_notesCollection',None)
        self._supplyCollection = kwargs.get('_supplyCollection',None)
        self.item = kwargs.get('item',{}) 
        self.finish_week = kwargs.get('finish_week','')
        self.actual = kwargs.get('actual','')
        self.want_qty = kwargs.get('want_qty','')
        self.color_groupings = kwargs.get('color_groupings','')
        self.groupings = kwargs.get('groupings',{})
        self._in_growWeekParent = kwargs.get('_growWeekParent',None)
        self._supplies = None
        self._notes = None
        super(ItemWeek, self).__init__(fsClient, **kwargs)
        
    
    def base_path(self):
        return self.parent_path+'/Items'

    @property
    def id(self):
        return self.finish_week+"-"+self.item_name

    @property
    def item_name(self):
        return ItemWeek.CleanItemName(self.item.get('name','NoItemName'))

    @property
    def get_lookup_entry(self):
        return {'key': self.item_name, 'value': self.item.get('name','NoItemName')}
    
    @property
    def item_id(self):
        return self.item.get('id',"NoItemId")

    @property
    def item_path(self):
        return self.item.get('path',"NoItemPath")

    @property
    def _growWeekParent(self):
        if self._in_growWeekParent is None:
            gwParDoc = self.get_firestore_client().document(self.parent_path)
            self._in_growWeekParent = GetInstance("GrowWeek",gwParDoc)
        return self._in_growWeekParent

    @classmethod
    def getInstance(cls,docDict):
        return ItemWeek(ItemWeek.get_firestore_client(),**docDict)

    @property
    def path(self):
        return self._collection_parent.path

    @property
    def parent_path(self):
        return self._collection_parent.parent_path

    def update_ndb(self,doCreate=True):
        self._collection_parent._loaded_items[self.item_name] = self
        return self._collection_parent.update_ndb(doCreate)

    def delete_resp(self):
        if self._collection_parent._loaded_items.get(self.item_name,None) is not None:
            del self._collection_parent._loaded_items[self.item_name]
        
        self._collection_parent.update_ndb()

    @classmethod
    def CleanItemName(cls,inName):
        return inName.replace("'","").replace('"','').replace(' ','').replace(".","")

    @property
    def notes(self):
        if self._notes is None:
            notes = self._notesCollection.getNotesByItemName(self.item_name)
            self._notes = notes
        return self._notes

    @property
    def notes_dict(self):
        return [note.get_dict() for note in self.notes]

    @property
    def supply(self):
        if self._supplies is None:
            supplies = self._supplyCollection.getSupplyByItemName(self.item_name)
            self._supplies = supplies
        return self._supplies

    def create_note(self, note):
        return self._notesCollection.create_note(self.item_name, note)

    def delete_note(self, note_id):
        return self._notesCollection.delete_note(note_id)
        
    def create_supply(self,supplier_id, inForecast, confirmation_num):
        return self._supplyCollection.create_supply(self.item_name,supplier_id,inForecast,confirmation_num)

    def get_itemweek_dict(self):
        d = {'name': self.item['name'],
             'finish_week': self._growWeekParent.get_growweek_dict(),
             'actual': self.actual,
             'want_qty': self.want_qty,
             'color_groupings': self.color_groupings,
             'groupings': self.groupings,
             '_id':self.id}

        return d

    def update_groupings(self, grouping, reset=False):
        """
        TODO
        """
        total_qnt = 0
        vals = False
        for key in grouping.keys():
            vals = True
            qnt = grouping[key]
            total_qnt = total_qnt + int(qnt)

        if vals or reset:
            self.actual = total_qnt

        self.grouping = grouping
        self.update_ndb()
        return True


    def update_color_grouping(self, color_grouping, reset=False):
        """
        The color grouping object should be a dict where the keys are colors and a quantity
        This function will add the json object and then go through and count the numbers and update the actual quantity
        :param color_grouping:
        :return:
        """
        total_qnt = 0
        vals = False
        for key in color_grouping.keys():
            vals = True
            qnt = color_grouping[key]
            total_qnt = total_qnt + int(qnt)

        if vals or reset:
            self.actual = total_qnt

        self.color_groupings = color_grouping
        self.update_ndb()
        return True

    def get_schema(self):
        schema = self.get_bq_schema()
        return schema

    def get_values_dict(self):
        return self.get_dict()

    @property
    def next(self):
        return ItemWeek.get_or_create(self.item_type, self.item, self._growWeekParent.next_week)

    @property
    def prior(self):
        return ItemWeek.get_or_create(self.item_type, self.item, self._growWeekParent.prior_week)

    @property
    def forecasts(self):
        fcast = 0
        for supp in self.supply:
            fcast = fcast + supp.get_forecast()
        return fcast

    @property
    def reserves(self):
        """Pulling this information through the _growWeekParent"""
        return self._growWeekParent.getSummary().getItemReserves(self.item_type, self.item_name)

    def get_total_reserved(self):
        return self._growWeekParent.getSummary().getReserveAmtByItem(self.item_type, self.item_name)

    @classmethod
    def get_or_create(cls,itemType, itemInfo, growWeek):
        itemObj = ItemWeek.GetSBObj(itemInfo['path'])
        return growWeek.get_or_create_itemweek(itemType,itemObj)

    @classmethod
    def CleanItemType(cls,item_type):
        lower = item_type.lower()
        if (lower.endswith('s')):
            return lower[:-1]
        return lower
    
    @property
    def clean_item_type(self):
        return ItemWeek.CleanItemType(self.item_type)

    def iw_summary(self):
        ps = {}
        ps['_id'] = self.id
        ps['item'] = self.item['name']
        ps['lookup_name'] = self.item_name
        ps['item_id'] = self.item['id']
        ps['week_id'] = self.finish_week
        ps['actual'] = self.actual
        ps['forecast'] = self.forecasts
        ps['num_reserved'] = self.get_total_reserved()
        return ps

    def availability(self):
        rsvs = self.get_total_reserved()
        fcast = self.forecasts
        if self.actual > 0:
            return self.actual - rsvs

        return fcast - rsvs