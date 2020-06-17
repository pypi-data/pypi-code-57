from .sales_inv_utils import SalesInvBase
from datetime import datetime
from datetime import timedelta
import jmespath

from .item_week import ItemWeekCollection, ItemWeek
from .item_reserve import ItemReserve
from .reserve_summary import ReserveSummary
from .inventory_active_items import InventoryActiveItems, InventoryItems

'''
This will be the new converted class GrowWeek
'''
class GrowWeek(SalesInvBase):

    ext_fields = ['week_number','year','week_monday','soft_delete','parent_path','path']
    COLLECTION_NAME = 'application_data'
    
    """ Represents a Week where we can have reserve orders """
    #week_number = ndb.IntegerProperty(required=True)
    #year = ndb.IntegerProperty(required=True)
    #week_monday = ndb.DateProperty()

    def __init__(self, fsClient, **kwargs):
        self.soft_delete = kwargs.get('soft_delete',False)
        self.week_number = kwargs.get('week_number','') 
        self.year = kwargs.get('year','') 
        self.week_monday = kwargs.get('week_monday','') # Stored in ISO format

        self._inventoryItems = InventoryItems.getInstance()
        self._itemweek = {}
        self._reserves = []
        self._reserve_summaries = []

        super(GrowWeek, self).__init__(fsClient, **kwargs)
    
    def base_path(self):
        return GrowWeek.__basePath(self._fsClient)

    @classmethod
    def basePath(cls):
        return GrowWeek.__basePath(GrowWeek.get_client())

    @classmethod
    def __basePath(cls,inClient):
        return GrowWeek.COLLECTION_NAME+'/'+inClient.company+'/Sales_Inventory/Converted/GrowWeek'

    @classmethod
    def getInstance(cls,fsDocument):
        ref,snap = GrowWeek.getDocuments(fsDocument)
        docDict = snap.to_dict() if snap.exists else {}
        docDict['fs_docSnap'] = snap
        docDict['fs_docRef'] = ref
        return GrowWeek(GrowWeek.get_firestore_client(),**docDict)
    
    def get_itemweek_type(self,item_type):
        iw = self._itemweek.get(item_type,None)
        if iw is None:
            item_path = self.path+'/Items/'+item_type
            iw = ItemWeekCollection.getInstance(self._fsClient.document(item_path))
            if not iw.exists:
                iw.item_type = item_type
                iw.finish_week = self.id
                self._in_growWeekParent = self
                iw.update_ndb(True)
                self._itemweek[item_type] = iw
        return iw
    
    @classmethod
    def getGrowWeekInstance(cls, week_id):
        path = GrowWeek.basePath()+'/'+week_id
        return GrowWeek.getInstance(GrowWeek.get_firestore_client().document(path))

    @classmethod
    def get_active(cls):
        return GrowWeek.get_active_any(GrowWeek.get_firestore_client(), GrowWeek.basePath, GrowWeek)

    def get_growweek_dict(self):
        d = {'week_number': self.week_number,
             'year': self.year,
             '_id':self.id}
        return d

    @classmethod
    def get_9_weeks(cls, center_date):
        '''

        :param center_date: should be a date time
        :return: an array of 10 weeks 3 before center_date and 7 after
        '''
        #gw_center_date = GrowWeek.create_week(center_date)
        # Get 3 prior weeks
        days = [-3,-2,-1,0,1,2,3,4,5,6]
        gw_array = [GrowWeek.GetGrowWeekByDate(center_date + timedelta(days=(x*7))) for x in days]
        return gw_array


    def get_schema(self):
        schema = self.get_bq_schema()
        schema['fields'].append({'field_name':'week_number','field_type':'int','field_required':True})
        schema['fields'].append({'field_name':'year','field_type':'int','field_required':True})
        schema['fields'].append({'field_name':'week_monday','field_type':'date'})
        return schema

    def get_values_dict(self):
        return self.get_dict()

    @property
    def next_week(self):
        nxtWk = datetime.fromisoformat(self.week_monday) + timedelta(days=7)
        return GrowWeek.GetGrowWeekByDate(nxtWk)

    @property
    def prior_week(self):
        nxtWk = datetime.fromisoformat(self.week_monday) - timedelta(days=7)
        return GrowWeek.GetGrowWeekByDate(nxtWk)

    @property
    def reserves(self):
        '''
        This will be a list of ItemReserves... here is the format of a reserve
        the standard fields are still included... but removed them here for brevity
        {
            customer: {
                id: customer-79164,
                name: Test Customer,
                type: Legacy, ## Can be either legacy or item_tracking
                path: application_data/Color_Orchids/....
            },
            id: ProductReserve-459726,
            finish_week: 2019_49,
            num_reserved: 485,
            item: {
                id: Product-4791597, # Or in the future will be Cust_Plant_Item-2976,
                name: Bonita X Umbra,
                type: Legacy, ## can be either legacy or item_tracking
                path: application_data/Color_orchids/....
            },
            vase: {
               id: recipe_costing-487,
               name: Blue Vase,
               path: application_data/Color_Orchids/....
               },
            plants: [  # copied from ProductPlant or from now on from the Recipe
                {
                    plant: {
                        id: Plant-197111, ## in the future will be Recipe_Costing-4975
                        name: Bonita
                        type: Legacy, ## Can be either legacy or item_tracking
                        path: application_data/Color_Orchids/....
                    } ,
                    qty: 2   
                },
                {
                    plant: {
                        id: Plant-197411, ## in the future will be Recipe_Costing-4975
                        name: Mini Succulent,
                        type: Legacy, ## Can be either legacy or item_tracking
                        path: application_data/Color_Orchids/....
                    } ,
                    qty: 1
                }
            ]
        }
        '''
        if len(self._reserves) == 0:
            self._reserves = ItemReserve.get_reserves_for_week(self)
        return self._reserves

    def getSummary(self):
        summary = self._documentRef.collection("ReservesSummary").document('summary')
        return ReserveSummary.getInstance(summary)
    
    def get_reserve_reference(self):
        return self._documentRef.collection('Reserves').document(self._get_doc_id('Reserve')) 

    def create_reserve(self,customer_id, location_id, item_id, reserved, reserveDate=None):
        docRef = self.get_reserve_reference()
        return ItemReserve.create_reserve(docRef,customer_id,location_id,item_id,reserved,self.id,reserveDate)

    def update_reserve(self, reserve_id, customer_id, location_id, item_id, reserved, reserveDate=None):
        if reserveDate is not None:
            gw = GrowWeek.GetGrowWeekByDate(reserveDate)
        else:
            gw = self
        ir = ItemReserve.getItemReserveInstance(reserve_id)
        return ir.update_reserve(customer_id,location_id, item_id, reserved, gw, reserveDate)

    def update_item_info(self, reserve_id, item_id):
        ir = ItemReserve.getItemReserveInstance(reserve_id)
        return ir.refresh()


    @property
    def reserve_summaries(self):
        '''
        This will be a list of reserve summaries... here is the format of a reserve SUMMARY
        {
            customer: Test Customer,
            location: Greenville, SC,
            id: ProductReserve-459726,
            num_reserved: 485,
            item_name: Bonita X Umbra,
            item_id: Cust_Plant_Item-16533
            vase: Blue Style
            plants: [  {name: Bonita, qty: 2}, {name: Mini Succulent, qty: 1}]
        }
        
        What will be retuned is the summary of reserves... not the full reserves
        '''

        if len(self._reserve_summaries) == 0:
            summaryPath = self.path+'/ReservesSummary/summary'
            docRef = self._fsClient.document(summaryPath)
            snap = docRef.get()
            if snap.exists:
                self._reserve_summaries = snap.to_dict()['summary']   

        return self._reserve_summaries

    @classmethod
    def create_weeks(cls, start_date, end_date):
        while start_date.isocalendar()[2] != 1:
            start_date = start_date + timedelta(days=-1)

        while start_date <= end_date:
            GrowWeek.GetGrowWeekByDate(start_date)
            start_date = start_date + timedelta(days=7)

    @classmethod
    def create_doc_id(cls, year, wk_num):
        return str(year)+"_"+str(wk_num).zfill(2)

    @classmethod
    def GetGrowWeekByDate(cls, indate):
        '''Get the week... if it doesn't exist..create it'''
        while indate.isocalendar()[2] != 1:
            indate = indate + timedelta(days=-1)

        wknum = indate.isocalendar()[1]
        year = indate.isocalendar()[0]

        doc_id = GrowWeek.create_doc_id(year,wknum)
        path = GrowWeek.basePath()+'/'+doc_id
        gw = GrowWeek.getInstance(GrowWeek.get_firestore_client().document(path))
        if not gw.exists:
            gw.week_number = wknum
            gw.year = year
            gw.week_monday = indate
            gw.update_ndb()
        return gw

    @classmethod
    def _get_active_items(cls,item_type):
        return InventoryActiveItems.get_all(item_type)

    @classmethod
    def get_9_itemweek(cls, item_type, center_date):
        """
        Get 10 weeks total 9 around the date provided
        :param center_date:
        :return: array of ItemWeek
        """
        activeItems = GrowWeek._get_active_items(item_type)
        gws = GrowWeek.get_9_weeks(center_date)
        resp = {'data':[],"inv_items":[{'name':pl.name,'id':pl.id,'path':pl.path} for pl in list(activeItems.values())]}
        for gw in gws:
            gwd = gw.get_growweek_dict()
            gwd['inv_items'] = []
            for item in activeItems.keys():
                gwd['inv_items'].append(gw.get_or_create_itemweek(item_type,activeItems[item]).get_itemweek_dict())
            resp['data'].append(gwd)

        return resp

    def _getItemWeekCollection(self, item_type):
        itemWeekCollection = self._itemweek.get(item_type,None)
        if itemWeekCollection is None:
            itemWeekCollection = ItemWeekCollection.getOrCreateInstance(item_type,self)
            self._itemweek[item_type] = itemWeekCollection
        return itemWeekCollection
    
    def get_or_create_itemweek(self,item_type,itemObj):
        itemWeekCollection = self._getItemWeekCollection(item_type)
        return itemWeekCollection.create_itemweek_entry(itemObj,self)

    def chk_create_item(self, din, name, item, item_type):
        if name not in din.keys():
            din[name] = {'wanted':0,'actual':0,'forecast':0, 'reserved':0, 'notes':0}
            din[name]['item_key'] = item.id
            din[name]['week_key'] = self.id

    @classmethod
    def update_itemweek_supply(cls, item_type, weekId, supply_id, supplier, forecast, confirmation_num, cost):
        gw = GrowWeek.getGrowWeekInstance(weekId)
        itemWeekCollection = gw._getItemWeekCollection(item_type)
        supply = itemWeekCollection.get_supply().getSupplyById(supply_id)
        return supply.update(supplier, forecast, confirmation_num, cost)

    @classmethod
    def update_itemweek(cls, itemName, item_type, weekId, actual):
        resp = {'status':'success','msg':'PlantGrow Updated Successfully'}
        try:
            gwRef = GrowWeek.getGrowWeekInstance(weekId)
            itemWeekCollection = gwRef._getItemWeekCollection(item_type)
            iw = itemWeekCollection.get_itemweek(itemName)
            if iw.exists:
                #pg.want_qty = int(wanted)
                #
                # Disabling plant emails for time being
                #
                #if pg.actual > 0:
                #    pl = pg.plant.get()
                #    wk = pg.finish_week.get()
                #    msg = "The plant: {} for week {} ({}), had the actual number updated from {} to {}".format(pl.name, wk.week_number, wk.year, pg.actual, actual)
                #    EmailNotifications.send_email("actual_update", "Actual Has Been Updated", msg)
                iw.actual = int(actual)
                iw.update_ndb()
            else:
                resp = {'status':'failed','msg':'No record found to update'}
        except Exception as e:
            resp = {'status':'failed','msg': str(e)}
        return resp

    def week_summary(self,item_type):
        iws = []
        items = list(self._get_active_items(item_type).values())
        for item in items:
            if item.name != 'N/A':
                iws.append({'key': item.name, 'value': self.get_or_create_itemweek(item_type,item)})
        

        iwd = {}
        for pg in iws:
            name = pg['key']
            itemweek = pg['value']
            self.chk_create_item(iwd,name,itemweek,item_type)
            iwd[name]['actual'] = iwd[name]['actual'] + itemweek.actual
            iwd[name]['notes'] = len(itemweek.notes)
            iwd[name]['id'] = itemweek.id

            supps = itemweek.supply
            for supp in supps:
                iwd[name]['forecast'] = iwd[name]['forecast'] + supp.forecast
            '''
            This is what should get returned... 
            [
                {
                    "reserved": 360,
                    "qty": 1
                },
                {
                    "reserved": 800,
                    "qty": 1
                }
            ]
            '''
            rsvs = []
            item_key = ItemWeek.CleanItemType(item_type)+'s'
            item_ent = itemweek.clean_item_type
            #"[?vases[?vase == '3\" Designer']].{reserved: num_reserved, qty: vases[*].qty | [0]}"
            srch = '[?'+item_key+'[?'+item_ent+' == \''+name+'\']].{reserved: num_reserved, qty: '+item_key+'[*].qty | [0]}'
            rsvs = jmespath.search(srch, self.reserve_summaries)

            for rsv in rsvs:
                iwd[name]['reserved'] = iwd[name]['reserved'] + (rsv['qty'] * rsv['reserved'])


        for key in iwd.keys():
            iwd[key]['available'] = iwd[key]['forecast'] - iwd[key]['reserved']
            if iwd[key]['actual'] > 0:
                iwd[key]['available'] = iwd[key]['actual'] - iwd[key]['reserved']
        return iwd

    @classmethod
    def _split_item_id(cls,itemId):
        '''
        Item id:  2020_18-Singolo
        Item Type: Plants
        '''
        parts = itemId.split("-")
        week_id = parts[0]
        item_name = None
        if len(parts) > 1:
            item_name = parts[1]
        return item_name, week_id

    @classmethod
    def get_itemweek_by_id(cls,item_type, itemId):
        '''  Assuming that the PlantGrow Id is Week<->Plant Name
        2020_20-Bonita
        '''
        itemName, weekId = GrowWeek._split_item_id(itemId)
        if itemName is not None and weekId is not None:
            #return GrowWeek.get_plantgrow(plName,weekId)
            return GrowWeek.get_itemweek(item_type, itemName, weekId)
        raise Exception("Invalid plant grow id supplied: {}".format(itemId))

    @classmethod
    def get_itemweek(cls, argItemType, argItem, argWeek):
        gw = GrowWeek.getGrowWeekInstance(argWeek)
        iwc = gw._getItemWeekCollection(argItemType)
        iw = iwc.get_itemweek(argItem)
        return iw

    @classmethod
    def get_item_availability_now(cls,item_type, item_name):
        cal = datetime.now()

        gw = GrowWeek.GetGrowWeekByDate(cal)
        iwc = gw._getItemWeekCollection(item_type)
        iw = iwc.get_itemweek(item_name)
        avail = {"prior":0,"current":0,"next":0}
        if iw:
            avail['current'] = iw.availability()
            iwPrior = iw.prior
            if iwPrior:
                avail['prior'] = iwPrior.availability()
            iwNext = iw.next
            if iwNext:
                avail['next'] = iwNext.availability()
        return avail


    @classmethod
    def save_note(cls,note, item_type, item_key):
        iw = GrowWeek.get_itemweek_by_id(item_type,item_key)
        return iw.create_note(note)
