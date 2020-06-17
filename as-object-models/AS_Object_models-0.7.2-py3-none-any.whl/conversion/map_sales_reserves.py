from google.cloud import datastore
from google.cloud import firestore

import jmespath,json,sys, os,logging

from .utils import progress
'''
The decision was made to convert all reserves from the Sales inventory to the Item Tracking data
.. this was effective for all reserves starting the 13th week of 2020.

This is pulled from a spreadsheet.  We'll add logic in the converstion to make sure that this is the case.

We may not upate... but it will show up in the mapping data..
'''
class MapSalesReserves(object):
    def __init__(self, convData=None, datastore_project=None, firestore_project=None, load=False):
        self.filename = 'as_models/scripts/converted_sales_inv.json'
        self.conversion_data = convData
        if firestore_project:
            self.fs_project = firestore_project
        else:
            self.fs_project = os.environ.get('FS_PROJECT', 'backend-firestore-test')

        if datastore_project:
            self.ds_project = datastore_project
        else:
            self.ds_project = os.environ.get('DS_PROJECT', 'sales-inv-colororchids')
  
        self.db = firestore.Client(project=self.fs_project)
        self.messages = []
        self.customers = self.get_customers()
        self.items = {}
        self.location_matches = {}
        if load and convData is not None:     
            self.run_mapping()
        else:
            with open(self.filename) as json_file:
                self.conversion_data = json.load(json_file)
                 
    def addMsg(self,msg):
        self.messages.append(msg)

    def get_conversion_data(self):
        return self.conversion_data

    def get_dict(self, docRef):
        snap = docRef.get()
        d = snap.to_dict()
        d['path'] = docRef.path
        return d

    def get_customers(self):
        col = self.db.collection('application_data/Color_Orchids/Customer_Tracking/StorageBlob/customer')
        docRefs = col.list_documents()
        return [self.get_dict(x) for x in docRefs]
    
    def run_mapping(self):
        self.load_master()
        total = len(self.conversion_data)
        for i in range(total):
            x = self.conversion_data[i]
            progress(i, total, status="Running through customer: "+x['item_cust_name'])
            x['match_customer'] = self.find_conv_entry(self.customers,x)
            x['pull_customer'] = self.find_conv_entry(self.customers,x,True)
            x['match_location'] = self.find_loc_entry(x)
            x['pull_location'] = self.find_loc_entry(x,True)
            x['match_item'] = self.find_item(x)

    def load_master(self):
        docRefs = self.db.collection('application_data/Color_Orchids/Customer_Tracking/StorageBlob/admin_items/admin_items-100/master_items').list_documents()
        master_items = [self.get_dict(x) for x in docRefs]
        self.items['Master'] = master_items

    def find_conv_entry(self, srchData, convData, pull=False):
        entry = 'pull_cust_name' if pull else 'item_cust_name'
        name = convData[entry]
        if name == "" or name == "Master":
            return {}
        entry = jmespath.search("[?customer_name == `"+name+"`] | [0]",srchData)
        if entry:
            return entry
        self.addMsg("No Match Found: "+name)
        return {}

    def find_loc_entry(self, convData,pull=False):
        entry = 'pull_loc_name' if pull else 'item_loc_name'
        custEntry = 'pull_cust_name' if pull else 'item_cust_name'
        name = convData[entry]
        custName = convData[custEntry]
        if name == "":
            return {}

        custPath = convData['pull_customer']['path'] if pull else convData['match_customer']['path']
        locations = self.location_matches.get(custPath,[])
        if len(locations) == 0:
            docRefs = self.db.document(custPath).collection('locations').list_documents()
            locations = [self.get_dict(x) for x in docRefs]
            self.location_matches[custPath] = locations
        entry = jmespath.search("[?location_name == `"+name+"`] | [0]",locations)
        if entry:
            return entry
        self.addMsg("No match found: Customer: "+custName+", location: "+name)
        return {}

    def find_item(self, convData):
        msg = ''
        if convData['action'] != 'convert':
            msg = "Doing nothing for action: "+convData['action']
            return {'found':False,'copy':False,'item':None,'msg':msg}

        location_path = ""
        copy_to_loc = False
        if convData['pull_cust_name'] != "":
            copy_to_loc = True
            if convData['pull_cust_name'] == 'Master':
                location_path = 'Master'
            else:
                location_path = convData['pull_location']['path']
        else:
            location_path = convData['match_location'].get('path',None)
            if not location_path:
                msg = "No LOCATION Entered: Customer: "+convData['match_customer']['customer_name']+", Product Name: "+convData['item_prod_name']
                self.addMsg(msg)
                return {'found':False,'copy':copy_to_loc,'item':None,'msg':msg}

        locItems = self.items.get(location_path,None)
        name = convData['item_prod_name']

        if not locItems:
             docRefs = self.db.document(location_path).collection('items').list_documents()
             locItems = [self.get_dict(x) for x in docRefs]
             self.items[location_path]= locItems

        entry = jmespath.search("[?Product_Name == '"+name+"'] | [0]",locItems)
        if entry:
             return {'found':True,'copy':copy_to_loc,'item':entry,'msg':''}
  
        msg = "No match found: Customer: "+convData['match_customer']['customer_name']+", Product Name: "+name+", location: "+location_path
        self.addMsg(msg)
        return {'found':False,'copy':copy_to_loc,'item':None,'msg':msg}

compare_map = [{'sales_cust_id':"Customer-5722646637445120",'sales_prod_id':"Product-5746858777378816",'item_cust_name':"Ahold",'item_loc_name':"Giant Carlisle",'item_prod_name':'Bellini','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5722646637445120",'sales_prod_id':"Product-5723698166235136",'item_cust_name':"Ahold",'item_loc_name':"Giant Carlisle",'item_prod_name':'Belita X Diamond','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5722646637445120",'sales_prod_id':"Product-5689866524295168",'item_cust_name':"Ahold",'item_loc_name':"Giant Carlisle",'item_prod_name':'Bellini','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5701508221894656",'sales_prod_id':"Product-6004703976488960",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Brea Whse, CA. ",'item_prod_name':'Succulent X Strawberry','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5741109967847424",'sales_prod_id':"Product-6291327008374784",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Denver Co",'item_prod_name':'Grande Designer Vase','action':'convert','pull_cust_name':"Jewel-OSCO",'pull_loc_name':"Franklin, IL"}
,{'sales_cust_id':"Customer-5741109967847424",'sales_prod_id':"Product-6109752308269056",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Denver Co",'item_prod_name':'belitaUmbra','action':'convert','pull_cust_name':"Albertson's Safeway",'pull_loc_name':"Roanoke TX"}
,{'sales_cust_id':"Customer-5741109967847424",'sales_prod_id':"Product-5691814547816448",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Denver Co",'item_prod_name':'DL 2x5 Duopot Orchid Garden ','action':'convert','pull_cust_name':"Jewel-OSCO",'pull_loc_name':"Franklin, IL"}
,{'sales_cust_id':"Customer-5741109967847424",'sales_prod_id':"Product-5661512844705792",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Denver Co",'item_prod_name':'bonitaOrb','action':'convert','pull_cust_name':"Albertson's Safeway",'pull_loc_name':"Denver PA"}
,{'sales_cust_id':"Customer-5741109967847424",'sales_prod_id':"Product-5749816936103936",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Denver Co",'item_prod_name':'Bonita X GP','action':'delete','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5741109967847424",'sales_prod_id':"Product-5768033574322176",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Denver Co",'item_prod_name':'Singolo X Lace','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5741109967847424",'sales_prod_id':"Product-6207305246834688",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Denver Co",'item_prod_name':'Yuma X Cake','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5741109967847424",'sales_prod_id':"Product-5752849686331392",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Denver Co",'item_prod_name':'5" Debi Lilly White Orchid','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5741109967847424",'sales_prod_id':"Product-5118732057706496",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Denver Co",'item_prod_name':'DL Oversize Orchid','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5741109967847424",'sales_prod_id':"Product-5160612308975616",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Denver Co",'item_prod_name':'bonitaDesigner','action':'convert','pull_cust_name':"United Texas",'pull_loc_name':"Texas"}
,{'sales_cust_id':"Customer-5741109967847424",'sales_prod_id':"Product-5761901967441920",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Denver Co",'item_prod_name':'Bonita Orchid Garden','action':'convert','pull_cust_name':"Albertson's Safeway",'pull_loc_name':"Roanoke TX"}
,{'sales_cust_id':"Customer-5741109967847424",'sales_prod_id':"Product-5636497101291520",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Denver Co",'item_prod_name':'Yuma X Lunar','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5741109967847424",'sales_prod_id':"Product-5658565461147648",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Denver Co",'item_prod_name':'Bonita X Charcoal','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5741109967847424",'sales_prod_id':"Product-5199268369399808",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Denver Co",'item_prod_name':'Singolo X Lace','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5741109967847424",'sales_prod_id':"Product-5151071655690240",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Denver Co",'item_prod_name':'Yuma X Lunar','action':'convert','pull_cust_name':"Albertson's Safeway",'pull_loc_name':"Roanoke TX"}
,{'sales_cust_id':"Customer-5741109967847424",'sales_prod_id':"Product-5665322749132800",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Denver Co",'item_prod_name':'Singolo X Lace','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5741109967847424",'sales_prod_id':"Product-5666464430292992",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Denver Co",'item_prod_name':'Bellini X Deco','action':'convert','pull_cust_name':"Albertson's Safeway",'pull_loc_name':"Roanoke TX"}
,{'sales_cust_id':"Customer-5741109967847424",'sales_prod_id':"Product-5753938796085248",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Denver Co",'item_prod_name':'Belita X Forest','action':'convert','pull_cust_name':"United Texas",'pull_loc_name':"Texas"}
,{'sales_cust_id':"Customer-5741109967847424",'sales_prod_id':"Product-5661719162519552",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Denver Co",'item_prod_name':'Singolo X Lace','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5741109967847424",'sales_prod_id':"Product-6324773739036672",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Denver Co",'item_prod_name':'Grande Designer Vase','action':'convert','pull_cust_name':"United Texas",'pull_loc_name':"Texas"}
,{'sales_cust_id':"Customer-5668241552703488",'sales_prod_id':"Product-5126916570873856",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Portland OR",'item_prod_name':'Debi Lilly 3X2 Duo Case 9','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5668241552703488",'sales_prod_id':"Product-5118732057706496",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Portland OR",'item_prod_name':'Grande GP','action':'delete','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5668241552703488",'sales_prod_id':"Product-5766477923745792",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Portland OR",'item_prod_name':'Sweetheart X Designer','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5668241552703488",'sales_prod_id':"Product-5689866524295168",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Portland OR",'item_prod_name':'Mixed Mini Designer','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5668241552703488",'sales_prod_id':"Product-5749816936103936",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Portland OR",'item_prod_name':'Bonita X GP','action':'delete','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5668241552703488",'sales_prod_id':"Product-5768782094008320",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Portland OR",'item_prod_name':'Cairo','action':'convert','pull_cust_name':"Albertson's Safeway",'pull_loc_name':"Roanoke TX"}
,{'sales_cust_id':"Customer-5668241552703488",'sales_prod_id':"Product-5663487359451136",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Portland OR",'item_prod_name':'DL Stone Cylinder Bonita','action':'convert','pull_cust_name':"Albertson's Safeway",'pull_loc_name':"Roanoke TX"}
,{'sales_cust_id':"Customer-5668241552703488",'sales_prod_id':"Product-5723698166235136",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Portland OR",'item_prod_name':'Belita GP','action':'delete','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5668241552703488",'sales_prod_id':"Product-5718601709387776",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Portland OR",'item_prod_name':'DL Paris Bonita','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5668241552703488",'sales_prod_id':"Product-5953769044967424",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Portland OR",'item_prod_name':'Mixed Mini Designer','action':'convert','pull_cust_name':"Albertson's Safeway",'pull_loc_name':"Roanoke TX"}
,{'sales_cust_id':"Customer-5668241552703488",'sales_prod_id':"Product-5640029049192448",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Portland OR",'item_prod_name':'Mixed Mini Designer','action':'convert','pull_cust_name':"Albertson's Safeway",'pull_loc_name':"Roanoke TX"}
,{'sales_cust_id':"Customer-5668241552703488",'sales_prod_id':"Product-5152433021911040",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Portland OR",'item_prod_name':'Mixed Mini Designer','action':'convert','pull_cust_name':"Albertson's Safeway",'pull_loc_name':"Roanoke TX"}
,{'sales_cust_id':"Customer-5689819120271360",'sales_prod_id':"Product-6692864717225984",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Salt Lake City Whse UT",'item_prod_name':'Belita Designer ','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5689819120271360",'sales_prod_id':"Product-5691814547816448",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Salt Lake City Whse UT",'item_prod_name':'Debi Lilly Duopot White Bonita ','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5689819120271360",'sales_prod_id':"Product-5167203313778688",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Salt Lake City Whse UT",'item_prod_name':'Cairo X Lunar','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5689819120271360",'sales_prod_id':"Product-6323555411165184",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Salt Lake City Whse UT",'item_prod_name':'Prague','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5689819120271360",'sales_prod_id':"Product-5160612308975616",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Salt Lake City Whse UT",'item_prod_name':'bonitaDesigner','action':'convert','pull_cust_name':"United Texas",'pull_loc_name':"Texas"}
,{'sales_cust_id':"Customer-5689819120271360",'sales_prod_id':"Product-6324773739036672",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Salt Lake City Whse UT",'item_prod_name':'Becca Gold Bead Oversize Orchid','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5689819120271360",'sales_prod_id':"Product-6291327008374784",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Salt Lake City Whse UT",'item_prod_name':'DL Oversize Orchid','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5689819120271360",'sales_prod_id':"Product-5126916570873856",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Salt Lake City Whse UT",'item_prod_name':'Athens','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5689819120271360",'sales_prod_id':"Product-6109752308269056",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Salt Lake City Whse UT",'item_prod_name':'belitaUmbra','action':'convert','pull_cust_name':"Albertson's Safeway",'pull_loc_name':"Roanoke TX"}
,{'sales_cust_id':"Customer-5689819120271360",'sales_prod_id':"Product-5665322749132800",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Salt Lake City Whse UT",'item_prod_name':'Singolo X Lace','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5689819120271360",'sales_prod_id':"Product-5666464430292992",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Salt Lake City Whse UT",'item_prod_name':'Mixed Mini Designer','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5689819120271360",'sales_prod_id':"Product-5634399089459200",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Salt Lake City Whse UT",'item_prod_name':'Mixed Mini Designer','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5689819120271360",'sales_prod_id':"Product-5688827091877888",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Salt Lake City Whse UT",'item_prod_name':'belitaFlorist','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5689819120271360",'sales_prod_id':"Product-5723698166235136",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Salt Lake City Whse UT",'item_prod_name':'Debi Lilly Belita Pedestal','action':'convert','pull_cust_name':"Albertson's Safeway",'pull_loc_name':"Roanoke TX"}
,{'sales_cust_id':"Customer-5689819120271360",'sales_prod_id':"Product-5953769044967424",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Salt Lake City Whse UT",'item_prod_name':'Mixed Mini Designer','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5689819120271360",'sales_prod_id':"Product-4593023128174592",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Salt Lake City Whse UT",'item_prod_name':'Occulus','action':'no-change','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5689819120271360",'sales_prod_id':"Product-5768782094008320",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Salt Lake City Whse UT",'item_prod_name':'Cairo X Lunar','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5689819120271360",'sales_prod_id':"Product-5152433021911040",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Salt Lake City Whse UT",'item_prod_name':'Mixed Mini Designer','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5689819120271360",'sales_prod_id':"Product-5763072618659840",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Salt Lake City Whse UT",'item_prod_name':'Mixed Mini Designer','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5689819120271360",'sales_prod_id':"Product-5753938796085248",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Salt Lake City Whse UT",'item_prod_name':'Belita X Forest','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5689819120271360",'sales_prod_id':"Product-5683708061286400",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Salt Lake City Whse UT",'item_prod_name':'Mixed Mini Designer','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5689819120271360",'sales_prod_id':"Product-5689602090205184",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Salt Lake City Whse UT",'item_prod_name':'bonitaDesigner','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5165986130952192",'sales_prod_id':"Product-5763072618659840",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Tolleson AZ",'item_prod_name':'Mixed Mini Designer','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5165986130952192",'sales_prod_id':"Product-5666464430292992",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Tolleson AZ",'item_prod_name':'Mixed Mini Designer','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5715999101812736",'sales_prod_id':"Product-5953769044967424",'item_cust_name':"Amazon",'item_loc_name':"DropShip",'item_prod_name':'Mini Succulent X Designer','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5715999101812736",'sales_prod_id':"Product-5723698166235136",'item_cust_name':"Amazon",'item_loc_name':"DropShip",'item_prod_name':'Belita GP','action':'no-change','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5715999101812736",'sales_prod_id':"Product-5749816936103936",'item_cust_name':"Amazon",'item_loc_name':"DropShip",'item_prod_name':'Bonita X GP','action':'no-change','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5715999101812736",'sales_prod_id':"Product-5689866524295168",'item_cust_name':"Amazon",'item_loc_name':"DropShip",'item_prod_name':'Bellini X Designer','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5153049148391424",'sales_prod_id':"Product-4617218155347968",'item_cust_name':"Costco",'item_loc_name':"SE",'item_prod_name':'5" Phal','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5153049148391424",'sales_prod_id':"Product-5136918324969472",'item_cust_name':"Costco",'item_loc_name':"SE",'item_prod_name':'Orchid Garden','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5153049148391424",'sales_prod_id':"Product-5134434223259648",'item_cust_name':"Costco",'item_loc_name':"SE",'item_prod_name':'Orchid Garden','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5153049148391424",'sales_prod_id':"Product-6184850348310528",'item_cust_name':"Costco",'item_loc_name':"SE",'item_prod_name':'belitaUmbra','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5761075312066560",'sales_prod_id':"Product-5953769044967424",'item_cust_name':"Crossett",'item_loc_name':"Independence KY",'item_prod_name':'Mini Succulent','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5081456606969856",'sales_prod_id':"Product-5749816936103936",'item_cust_name':"Delaware Valley",'item_loc_name':"Jessup MD",'item_prod_name':'Bonita Grow Pot','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-4935203969564672",'sales_prod_id':"Product-5723698166235136",'item_cust_name':"FTD",'item_loc_name':"FTD",'item_prod_name':'Belita GP','action':'no-change','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-4935203969564672",'sales_prod_id':"Product-5749816936103936",'item_cust_name':"FTD",'item_loc_name':"FTD",'item_prod_name':'Bonita X GP','action':'no-change','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5723562262396928",'sales_prod_id':"Product-5666464430292992",'item_cust_name':"Ahold",'item_loc_name':"Giant Carlisle",'item_prod_name':'Bellini','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5723562262396928",'sales_prod_id':"Product-5689866524295168",'item_cust_name':"Ahold",'item_loc_name':"Giant Carlisle",'item_prod_name':'Bellini','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5732108521701376",'sales_prod_id':"Product-5160612308975616",'item_cust_name':"Jewel-OSCO",'item_loc_name':"Franklin, IL",'item_prod_name':'bonitaDesigner','action':'convert','pull_cust_name':"United Texas",'pull_loc_name':"Texas"}
,{'sales_cust_id':"Customer-5732108521701376",'sales_prod_id':"Product-6692864717225984",'item_cust_name':"Jewel-OSCO",'item_loc_name':"Franklin, IL",'item_prod_name':'Belita 3" Ceramic','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5732108521701376",'sales_prod_id':"Product-6291327008374784",'item_cust_name':"Jewel-OSCO",'item_loc_name':"Franklin, IL",'item_prod_name':'Grande Designer Vase','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5732108521701376",'sales_prod_id':"Product-5753938796085248",'item_cust_name':"Jewel-OSCO",'item_loc_name':"Franklin, IL",'item_prod_name':'Belita X Forest','action':'convert','pull_cust_name':"United Texas",'pull_loc_name':"Texas"}
,{'sales_cust_id':"Customer-5732108521701376",'sales_prod_id':"Product-5746858777378816",'item_cust_name':"Jewel-OSCO",'item_loc_name':"Franklin, IL",'item_prod_name':'Mixed Mini Designer','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5732108521701376",'sales_prod_id':"Product-6109752308269056",'item_cust_name':"Jewel-OSCO",'item_loc_name':"Franklin, IL",'item_prod_name':'belitaUmbra','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5732108521701376",'sales_prod_id':"Product-5761901967441920",'item_cust_name':"Jewel-OSCO",'item_loc_name':"Franklin, IL",'item_prod_name':'Bonita Orchid Garden','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5732108521701376",'sales_prod_id':"Product-5636497101291520",'item_cust_name':"Jewel-OSCO",'item_loc_name':"Franklin, IL",'item_prod_name':'Yuma X Lunar','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5732108521701376",'sales_prod_id':"Product-6324773739036672",'item_cust_name':"Jewel-OSCO",'item_loc_name':"Franklin, IL",'item_prod_name':'Grande Designer Vase','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5732108521701376",'sales_prod_id':"Product-6207305246834688",'item_cust_name':"Jewel-OSCO",'item_loc_name':"Franklin, IL",'item_prod_name':'Yuma X Cake','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5732108521701376",'sales_prod_id':"Product-5723698166235136",'item_cust_name':"Jewel-OSCO",'item_loc_name':"Franklin, IL",'item_prod_name':'Belita GP','action':'no-change','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5732108521701376",'sales_prod_id':"Product-6192500481982464",'item_cust_name':"Jewel-OSCO",'item_loc_name':"Franklin, IL",'item_prod_name':'Paris X Lunar','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5732108521701376",'sales_prod_id':"Product-5196706811478016",'item_cust_name':"Jewel-OSCO",'item_loc_name':"Franklin, IL",'item_prod_name':'Belita X Float','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5732108521701376",'sales_prod_id':"Product-6283580900638720",'item_cust_name':"Jewel-OSCO",'item_loc_name':"Franklin, IL",'item_prod_name':'Bonita X Sorbet','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-4850674424610816",'sales_prod_id':"Product-5689866524295168",'item_cust_name':"Kroger",'item_loc_name':"Dallas Warehouse (Keller TX)",'item_prod_name':'Bellini X Designer','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-4850674424610816",'sales_prod_id':"Product-5696732151152640",'item_cust_name':"Kroger",'item_loc_name':"Dallas Warehouse (Keller TX)",'item_prod_name':'Belita X Dubai','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-4850674424610816",'sales_prod_id':"Product-5633362471419904",'item_cust_name':"Kroger",'item_loc_name':"Dallas Warehouse (Keller TX)",'item_prod_name':'Wild Orchid','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5711998679515136",'sales_prod_id':"Product-5689866524295168",'item_cust_name':"Kroger",'item_loc_name':"Dillons Produce Warehouse (Hutchinson, KS)",'item_prod_name':'Bellini X Designer','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-4878221707313152",'sales_prod_id':"Product-5749816936103936",'item_cust_name':"Kroger",'item_loc_name':"Fort Gillem Warehouse (GA)",'item_prod_name':'Bloom Haus Bonita','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-4878221707313152",'sales_prod_id':"Product-5723698166235136",'item_cust_name':"Kroger",'item_loc_name':"Fort Gillem Warehouse (GA)",'item_prod_name':'Bloom Haus Orchid Belita','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-4878221707313152",'sales_prod_id':"Product-5689866524295168",'item_cust_name':"Kroger",'item_loc_name':"Fort Gillem Warehouse (GA)",'item_prod_name':'Bellini X Designer','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-4878221707313152",'sales_prod_id':"Product-5134434223259648",'item_cust_name':"Kroger",'item_loc_name':"Fort Gillem Warehouse (GA)",'item_prod_name':'Tuscany','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-4878221707313152",'sales_prod_id':"Product-5633362471419904",'item_cust_name':"Kroger",'item_loc_name':"Fort Gillem Warehouse (GA)",'item_prod_name':'Wild Orchid','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-4878221707313152",'sales_prod_id':"Product-5696732151152640",'item_cust_name':"Kroger",'item_loc_name':"Fort Gillem Warehouse (GA)",'item_prod_name':'Belita X Dubai','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-4878221707313152",'sales_prod_id':"Product-5171667563184128",'item_cust_name':"Kroger",'item_loc_name':"Fort Gillem Warehouse (GA)",'item_prod_name':'Milan','action':'delete','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-4878221707313152",'sales_prod_id':"Product-5746858777378816",'item_cust_name':"Kroger",'item_loc_name':"Fort Gillem Warehouse (GA)",'item_prod_name':'Bellini X Designer','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-4878221707313152",'sales_prod_id':"Product-6247912816246784",'item_cust_name':"Kroger",'item_loc_name':"Fort Gillem Warehouse (GA)",'item_prod_name':'Belita Easter Garden','action':'delete','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-4878221707313152",'sales_prod_id':"Product-5668600916475904",'item_cust_name':"Kroger",'item_loc_name':"Fort Gillem Warehouse (GA)",'item_prod_name':'Mini Succulent','action':'delete','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-4855281381015552",'sales_prod_id':"Product-5633362471419904",'item_cust_name':"Kroger",'item_loc_name':"Champion Floral Warehouse (Houston, TX)",'item_prod_name':'Wild Orchid','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-4855281381015552",'sales_prod_id':"Product-5696732151152640",'item_cust_name':"Kroger",'item_loc_name':"Champion Floral Warehouse (Houston, TX)",'item_prod_name':'Belita X Dubai','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-4855281381015552",'sales_prod_id':"Product-5689866524295168",'item_cust_name':"Kroger",'item_loc_name':"Champion Floral Warehouse (Houston, TX)",'item_prod_name':'Bellini X Designer','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-4790047639339008",'sales_prod_id':"Product-5689866524295168",'item_cust_name':"Kroger",'item_loc_name':"NFC Warehouse (Ohio)",'item_prod_name':'Bellini X Designer','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5522485055324160",'sales_prod_id':"Product-4617218155347968",'item_cust_name':"Lidl",'item_loc_name':"Fredericksburg",'item_prod_name':'bonitaUmbra','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5522485055324160",'sales_prod_id':"Product-6639476394688512",'item_cust_name':"Lidl",'item_loc_name':"Fredericksburg",'item_prod_name':'bonitaDesigner','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5522485055324160",'sales_prod_id':"Product-6682585518309376",'item_cust_name':"Lidl",'item_loc_name':"Fredericksburg",'item_prod_name':'bonitaEgg','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6237236936835072",'sales_prod_id':"Product-5749816936103936",'item_cust_name':"MDI",'item_loc_name':"Hickory",'item_prod_name':'bonitaUmbra','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6237236936835072",'sales_prod_id':"Product-5762830888337408",'item_cust_name':"MDI",'item_loc_name':"Hickory",'item_prod_name':'Bonita Dubai','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6237236936835072",'sales_prod_id':"Product-5663487359451136",'item_cust_name':"MDI",'item_loc_name':"Hickory",'item_prod_name':'Bonita X Urban','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6237236936835072",'sales_prod_id':"Product-5723698166235136",'item_cust_name':"MDI",'item_loc_name':"Hickory",'item_prod_name':'Multiflora Planter','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6237236936835072",'sales_prod_id':"Product-5658565461147648",'item_cust_name':"MDI",'item_loc_name':"Hickory",'item_prod_name':'Bonita X Charcoal','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6237236936835072",'sales_prod_id':"Product-4617218155347968",'item_cust_name':"MDI",'item_loc_name':"Hickory",'item_prod_name':'bonitaUmbra','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6300086472540160",'sales_prod_id':"Product-6207305246834688",'item_cust_name':"New Seasons Markets",'item_loc_name':"CA",'item_prod_name':'Yuma X Cake','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6300086472540160",'sales_prod_id':"Product-5662227445055488",'item_cust_name':"New Seasons Markets",'item_loc_name':"CA",'item_prod_name':'Bonita X Popcorn','action':'delete','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6300086472540160",'sales_prod_id':"Product-5202627046408192",'item_cust_name':"New Seasons Markets",'item_loc_name':"CA",'item_prod_name':'Succulent X Deco','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6300086472540160",'sales_prod_id':"Product-5686185993175040",'item_cust_name':"New Seasons Markets",'item_loc_name':"CA",'item_prod_name':'Paris X Cake','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6300086472540160",'sales_prod_id':"Product-6109752308269056",'item_cust_name':"New Seasons Markets",'item_loc_name':"CA",'item_prod_name':'belitaUmbra','action':'convert','pull_cust_name':"Jewel-OSCO",'pull_loc_name':"Franklin, IL"}
,{'sales_cust_id':"Customer-6300086472540160",'sales_prod_id':"Product-5742193293656064",'item_cust_name':"New Seasons Markets",'item_loc_name':"CA",'item_prod_name':'Succulent X Deco','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5930029267550208",'sales_prod_id':"Product-5118732057706496",'item_cust_name':"Rolling Greens",'item_loc_name':"Clinton MD",'item_prod_name':'Grande GP','action':'no-change','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5930029267550208",'sales_prod_id':"Product-5749816936103936",'item_cust_name':"Rolling Greens",'item_loc_name':"Clinton MD",'item_prod_name':'Bonita Grow Pot','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5930029267550208",'sales_prod_id':"Product-5723698166235136",'item_cust_name':"Rolling Greens",'item_loc_name':"Clinton MD",'item_prod_name':'Belita Grow Pot','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5930029267550208",'sales_prod_id':"Product-5621900394889216",'item_cust_name':"Rolling Greens",'item_loc_name':"Clinton MD",'item_prod_name':'Bonita Grow Pot','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5134251410325504",'sales_prod_id':"Product-5160612308975616",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Roanoke TX",'item_prod_name':'bonitaDesigner','action':'convert','pull_cust_name':"Albertson's Safeway",'pull_loc_name':"Roanoke TX"}
,{'sales_cust_id':"Customer-5134251410325504",'sales_prod_id':"Product-5953769044967424",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Roanoke TX",'item_prod_name':' Mini Succulent Designer','action':'convert','pull_cust_name':"Kroger",'pull_loc_name':"Fort Gillem Warehouse (GA)"}
,{'sales_cust_id':"Customer-5134251410325504",'sales_prod_id':"Product-6323555411165184",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Roanoke TX",'item_prod_name':'Prague','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5134251410325504",'sales_prod_id':"Product-6109752308269056",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Roanoke TX",'item_prod_name':'belitaUmbra','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5134251410325504",'sales_prod_id':"Product-5689866524295168",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Roanoke TX",'item_prod_name':'Bellini X Deco','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5134251410325504",'sales_prod_id':"Product-5689602090205184",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Roanoke TX",'item_prod_name':'bonitaDesigner','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5134251410325504",'sales_prod_id':"Product-4617218155347968",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Roanoke TX",'item_prod_name':'bonitaUmbra','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5134251410325504",'sales_prod_id':"Product-5755287587782656",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Roanoke TX",'item_prod_name':'Belita X Stars and Stripes','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5134251410325504",'sales_prod_id':"Product-5152433021911040",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Roanoke TX",'item_prod_name':'Mixed Mini Designer','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5134251410325504",'sales_prod_id':"Product-5683708061286400",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Roanoke TX",'item_prod_name':'Mixed Mini Designer','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5134251410325504",'sales_prod_id':"Product-6198183931674624",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Roanoke TX",'item_prod_name':'Bellini X Lemon','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5134251410325504",'sales_prod_id':"Product-5196706811478016",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Roanoke TX",'item_prod_name':'Belita X Float','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5134251410325504",'sales_prod_id':"Product-5690207961612288",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Roanoke TX",'item_prod_name':'Sparta','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5134251410325504",'sales_prod_id':"Product-5663487359451136",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Roanoke TX",'item_prod_name':'DL Stone Cylinder Bonita','action':'convert','pull_cust_name':"Albertson's Safeway",'pull_loc_name':"Roanoke TX"}
,{'sales_cust_id':"Customer-5134251410325504",'sales_prod_id':"Product-6639476394688512",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Roanoke TX",'item_prod_name':'bonitaDesigner','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5134251410325504",'sales_prod_id':"Product-5635384914477056",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Roanoke TX",'item_prod_name':'Sweetheart','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5134251410325504",'sales_prod_id':"Product-5120977948114944",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Roanoke TX",'item_prod_name':'Bellini X Strawberry','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5134251410325504",'sales_prod_id':"Product-4787285241364480",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Roanoke TX",'item_prod_name':'Bellini X Pineapple','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5134251410325504",'sales_prod_id':"Product-5762830888337408",'item_cust_name':"Albertson's Safeway",'item_loc_name':"Roanoke TX",'item_prod_name':'Dubai','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5357970628018176",'sales_prod_id':"Product-6324773739036672",'item_cust_name':"Safeway",'item_loc_name':"Upper Marlboro",'item_prod_name':'Grande Designer Vase','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5357970628018176",'sales_prod_id':"Product-5691814547816448",'item_cust_name':"Safeway",'item_loc_name':"Upper Marlboro",'item_prod_name':'Sparta X Zen','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5357970628018176",'sales_prod_id':"Product-5689602090205184",'item_cust_name':"Safeway",'item_loc_name':"Upper Marlboro",'item_prod_name':'bonitaDesigner','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5357970628018176",'sales_prod_id':"Product-5690207961612288",'item_cust_name':"Safeway",'item_loc_name':"Upper Marlboro",'item_prod_name':'Sparta X Zen','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5357970628018176",'sales_prod_id':"Product-5663734483648512",'item_cust_name':"Safeway",'item_loc_name':"Upper Marlboro",'item_prod_name':'Bonita BeMine','action':'no-change','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5357970628018176",'sales_prod_id':"Product-6291327008374784",'item_cust_name':"Safeway",'item_loc_name':"Upper Marlboro",'item_prod_name':'Grande Designer Vase','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5357970628018176",'sales_prod_id':"Product-5953769044967424",'item_cust_name':"Safeway",'item_loc_name':"Upper Marlboro",'item_prod_name':'Mixed Mini Designer','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5357970628018176",'sales_prod_id':"Product-5689866524295168",'item_cust_name':"Safeway",'item_loc_name':"Upper Marlboro",'item_prod_name':'Bellini X Designer','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5357970628018176",'sales_prod_id':"Product-5152433021911040",'item_cust_name':"Safeway",'item_loc_name':"Upper Marlboro",'item_prod_name':'Anthurium X Deco','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5357970628018176",'sales_prod_id':"Product-5640029049192448",'item_cust_name':"Safeway",'item_loc_name':"Upper Marlboro",'item_prod_name':'Mixed Mini Designer','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5954224294723584",'sales_prod_id':"Product-5689866524295168",'item_cust_name':"Shaws Markets",'item_loc_name':"Methuen , MA",'item_prod_name':'Mixed Mini Designer','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5954224294723584",'sales_prod_id':"Product-6692864717225984",'item_cust_name':"Shaws Markets",'item_loc_name':"Methuen , MA",'item_prod_name':'Belita Designer ','action':'convert','pull_cust_name':"Albertson's Safeway",'pull_loc_name':"Salt Lake City Whse UT"}
,{'sales_cust_id':"Customer-5954224294723584",'sales_prod_id':"Product-6291327008374784",'item_cust_name':"Shaws Markets",'item_loc_name':"Methuen , MA",'item_prod_name':'Grande Designer Vase','action':'convert','pull_cust_name':"Albertson's Safeway",'pull_loc_name':"Roanoke TX"}
,{'sales_cust_id':"Customer-5954224294723584",'sales_prod_id':"Product-5768782094008320",'item_cust_name':"Shaws Markets",'item_loc_name':"Methuen , MA",'item_prod_name':'Cairo X Lunar','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5954224294723584",'sales_prod_id':"Product-5152433021911040",'item_cust_name':"Shaws Markets",'item_loc_name':"Methuen , MA",'item_prod_name':'Mixed Mini Designer','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5954224294723584",'sales_prod_id':"Product-5160612308975616",'item_cust_name':"Shaws Markets",'item_loc_name':"Methuen , MA",'item_prod_name':'bonitaDesigner','action':'convert','pull_cust_name':"United Texas",'pull_loc_name':"Texas"}
,{'sales_cust_id':"Customer-5954224294723584",'sales_prod_id':"Product-6109752308269056",'item_cust_name':"Shaws Markets",'item_loc_name':"Methuen , MA",'item_prod_name':'belitaUmbra','action':'convert','pull_cust_name':"Albertson's Safeway",'pull_loc_name':"Roanoke TX"}
,{'sales_cust_id':"Customer-5954224294723584",'sales_prod_id':"Product-5953769044967424",'item_cust_name':"Shaws Markets",'item_loc_name':"Methuen , MA",'item_prod_name':'Mixed Mini Designer','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5954224294723584",'sales_prod_id':"Product-5689602090205184",'item_cust_name':"Shaws Markets",'item_loc_name':"Methuen , MA",'item_prod_name':'bonitaDesigner','action':'convert','pull_cust_name':"United Texas",'pull_loc_name':"Texas"}
,{'sales_cust_id':"Customer-5954224294723584",'sales_prod_id':"Product-5167203313778688",'item_cust_name':"Shaws Markets",'item_loc_name':"Methuen , MA",'item_prod_name':'Cairo X Lunar','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5954224294723584",'sales_prod_id':"Product-6324773739036672",'item_cust_name':"Shaws Markets",'item_loc_name':"Methuen , MA",'item_prod_name':'Grande Designer Vase','action':'convert','pull_cust_name':"United Texas",'pull_loc_name':"Texas"}
,{'sales_cust_id':"Customer-5954224294723584",'sales_prod_id':"Product-5640029049192448",'item_cust_name':"Shaws Markets",'item_loc_name':"Methuen , MA",'item_prod_name':'Mixed Mini Designer','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5954224294723584",'sales_prod_id':"Product-6682585518309376",'item_cust_name':"Shaws Markets",'item_loc_name':"Methuen , MA",'item_prod_name':'bonitaEgg','action':'delete','pull_cust_name':"Lidl",'pull_loc_name':"Mebane"}
,{'sales_cust_id':"Customer-5750423122083840",'sales_prod_id':"Product-6639476394688512",'item_cust_name':"Sprouts Farmers Market",'item_loc_name':"Wilmer TX",'item_prod_name':'bonitaDesigner','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5750423122083840",'sales_prod_id':"Product-5160612308975616",'item_cust_name':"Sprouts Farmers Market",'item_loc_name':"Wilmer TX",'item_prod_name':'bonitaDesigner','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5946377657909248",'sales_prod_id':"Product-5668600916475904",'item_cust_name':"Trader Joe's",'item_loc_name':"Daytona",'item_prod_name':'Mini Succulent','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5946377657909248",'sales_prod_id':"Product-6692864717225984",'item_cust_name':"Trader Joe's",'item_loc_name':"Daytona",'item_prod_name':'belitaDesigner','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5946377657909248",'sales_prod_id':"Product-6324773739036672",'item_cust_name':"Trader Joe's",'item_loc_name':"Daytona",'item_prod_name':'Grande X Abigail','action':'no-change','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5946377657909248",'sales_prod_id':"Product-5118732057706496",'item_cust_name':"Trader Joe's",'item_loc_name':"Daytona",'item_prod_name':'Grande X Abigail','action':'no-change','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5946377657909248",'sales_prod_id':"Product-6224462798127104",'item_cust_name':"Trader Joe's",'item_loc_name':"Daytona",'item_prod_name':'Orchid Garden 22.99','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5946377657909248",'sales_prod_id':"Product-5663487359451136",'item_cust_name':"Trader Joe's",'item_loc_name':"Daytona",'item_prod_name':'bonitaDesigner','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5946377657909248",'sales_prod_id':"Product-5658565461147648",'item_cust_name':"Trader Joe's",'item_loc_name':"Daytona",'item_prod_name':'bonitaDesigner','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5946377657909248",'sales_prod_id':"Product-5639891278888960",'item_cust_name':"Trader Joe's",'item_loc_name':"Daytona",'item_prod_name':'bonitaDesigner','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5946377657909248",'sales_prod_id':"Product-5203124176289792",'item_cust_name':"Trader Joe's",'item_loc_name':"Daytona",'item_prod_name':'bonitaDesigner','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5946377657909248",'sales_prod_id':"Product-5723698166235136",'item_cust_name':"Trader Joe's",'item_loc_name':"Daytona",'item_prod_name':'belitaDesigner','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-5152433021911040",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Mini Anthurium Designer','action':'delete','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-5953769044967424",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Mini Succulent Designer','action':'delete','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-6291327008374784",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Grande Designer Vase','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-6323555411165184",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Prague','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-6692864717225984",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Belita Designer ','action':'convert','pull_cust_name':"Albertson's Safeway",'pull_loc_name':"Salt Lake City Whse UT"}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-5640029049192448",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Bromeliad','action':'delete','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-5683708061286400",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Bromeliad','action':'delete','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-5689866524295168",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Bellini X Designer','action':'delete','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-6324773739036672",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Grande Designer Vase','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-5762830888337408",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Dubai','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-5665322749132800",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Singolo X Lace','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-6109752308269056",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Belita X Umbra','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-5666464430292992",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Mixed Mini Designer','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-5160612308975616",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Bonita Debi Lily','action':'delete','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-4617218155347968",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Bonita X Umbra','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-5658565461147648",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Bonita X Charcoal','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-5661512844705792",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Bonita Orb','action':'no-change','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-5633595997683712",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Belita X Forest','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-5749816936103936",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Bonita X GP','action':'no-change','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-6207305246834688",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Yuma X Cake','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-5686185993175040",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Paris X Cake','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-5742193293656064",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Succulent X Deco','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-6283580900638720",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Bonita X Sorbet','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-4895103067881472",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Succulent X Skull','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-5755775469223936",'sales_prod_id':"Product-5704424131395584",'item_cust_name':"United Texas",'item_loc_name':"Texas",'item_prod_name':'Belita X Value','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6503738516701184",'sales_prod_id':"Product-6639476394688512",'item_cust_name':"VWI",'item_loc_name':"Mills River, NC",'item_prod_name':'bonitaDesigner','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6503738516701184",'sales_prod_id':"Product-6109752308269056",'item_cust_name':"VWI",'item_loc_name':"Mills River, NC",'item_prod_name':'belitaUmbra','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6503738516701184",'sales_prod_id':"Product-5199268369399808",'item_cust_name':"VWI",'item_loc_name':"Mills River, NC",'item_prod_name':'Singolo Designer','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6503738516701184",'sales_prod_id':"Product-5763072618659840",'item_cust_name':"VWI",'item_loc_name':"Mills River, NC",'item_prod_name':'Bromeliad X Deco','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6503738516701184",'sales_prod_id':"Product-5666464430292992",'item_cust_name':"VWI",'item_loc_name':"Mills River, NC",'item_prod_name':'Bellini X Deco','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6503738516701184",'sales_prod_id':"Product-5118732057706496",'item_cust_name':"VWI",'item_loc_name':"Mills River, NC",'item_prod_name':'Grande X Abigail','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6503738516701184",'sales_prod_id':"Product-6650065099685888",'item_cust_name':"VWI",'item_loc_name':"Mills River, NC",'item_prod_name':'Small Garden Assortment','action':'convert','pull_cust_name':"Whole Foods",'pull_loc_name':"Mid Atlantic"}
,{'sales_cust_id':"Customer-6503738516701184",'sales_prod_id':"Product-6754178059730944",'item_cust_name':"VWI",'item_loc_name':"Mills River, NC",'item_prod_name':'Small Garden Assortment','action':'convert','pull_cust_name':"Whole Foods",'pull_loc_name':"Mid Atlantic"}
,{'sales_cust_id':"Customer-6503738516701184",'sales_prod_id':"Product-5196706811478016",'item_cust_name':"VWI",'item_loc_name':"Mills River, NC",'item_prod_name':'Belita X Float','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6503738516701184",'sales_prod_id':"Product-5199880934916096",'item_cust_name':"VWI",'item_loc_name':"Mills River, NC",'item_prod_name':'Grande X Abigail','action':'convert','pull_cust_name':"Master",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6503738516701184",'sales_prod_id':"Product-6633716709326848",'item_cust_name':"VWI",'item_loc_name':"Mills River, NC",'item_prod_name':'Chinese New Years Garden','action':'delete','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6503738516701184",'sales_prod_id':"Product-5629518626684928",'item_cust_name':"VWI",'item_loc_name':"Mills River, NC",'item_prod_name':'Belita Heart','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6527042472378368",'sales_prod_id':"Product-5203124176289792",'item_cust_name':"Whole Foods",'item_loc_name':"Mid Atlantic",'item_prod_name':'bonitaTierra','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6527042472378368",'sales_prod_id':"Product-4617218155347968",'item_cust_name':"Whole Foods",'item_loc_name':"Mid Atlantic",'item_prod_name':'bonitaTierra','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6527042472378368",'sales_prod_id':"Product-5663487359451136",'item_cust_name':"Whole Foods",'item_loc_name':"Mid Atlantic",'item_prod_name':'bonitaTierra','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6527042472378368",'sales_prod_id':"Product-5953769044967424",'item_cust_name':"Whole Foods",'item_loc_name':"Mid Atlantic",'item_prod_name':'Mini Succulent','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6527042472378368",'sales_prod_id':"Product-5668600916475904",'item_cust_name':"Whole Foods",'item_loc_name':"Mid Atlantic",'item_prod_name':'Mini Succulent','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6527042472378368",'sales_prod_id':"Product-5122012909404160",'item_cust_name':"Whole Foods",'item_loc_name':"Mid Atlantic",'item_prod_name':'Large Garden Assortment','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6527042472378368",'sales_prod_id':"Product-5134434223259648",'item_cust_name':"Whole Foods",'item_loc_name':"Mid Atlantic",'item_prod_name':'Large Garden Assortment','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6527042472378368",'sales_prod_id':"Product-6650065099685888",'item_cust_name':"Whole Foods",'item_loc_name':"Mid Atlantic",'item_prod_name':'Small Garden Assortment','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6527042472378368",'sales_prod_id':"Product-5634399089459200",'item_cust_name':"Whole Foods",'item_loc_name':"Mid Atlantic",'item_prod_name':'Mini Anthurium','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6527042472378368",'sales_prod_id':"Product-5136918324969472",'item_cust_name':"Whole Foods",'item_loc_name':"Mid Atlantic",'item_prod_name':'Large Garden Assortment','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6527042472378368",'sales_prod_id':"Product-6692864717225984",'item_cust_name':"Whole Foods",'item_loc_name':"Mid Atlantic",'item_prod_name':'belitaDesigner','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-6527042472378368",'sales_prod_id':"Product-6754178059730944",'item_cust_name':"Whole Foods",'item_loc_name':"Mid Atlantic",'item_prod_name':'Small Garden Assortment','action':'convert','pull_cust_name':"",'pull_loc_name':""}
,{'sales_cust_id':"Customer-4663391872352256",'sales_prod_id':"Product-5749816936103936",'item_cust_name':"Willow Run Greenhouse",'item_loc_name':"Culpeper VA",'item_prod_name':'Bonita Grow Pot','action':'convert','pull_cust_name':"",'pull_loc_name':""}]


if __name__ == '__main__':
    '''
    You can set the datastore project by using the environment variable DS_PROJECT
    You can set the firestore project by susing the environment variable FS_PROJECT
    .. whatever you set can be overridden by command line args
    Arg 1 = DataStore Project
    Arg 2 = Firestore Project
    
    If you do neither, it will default to the folling:
    DS_PROJECT = 'item-tracking-colororchids'
    FS_PROJECT = 'backend-firestore-test'
    '''
    dsProject = os.environ.get('DS_PROJECT','sales-inv-colororchids')
    fsProject = os.environ.get('FS_PROJECT','backend-firestore-test')
    if len(sys.argv) > 1:
        dsProject = sys.argv[1]

    if len(sys.argv) > 2:
        fsProject = sys.argv[2]

    logging.info('run mapping to run...')
    msr = MapSalesReserves(compare_map,dsProject,fsProject,True)
    outJson = msr.get_conversion_data()
    for msg in msr.messages:
        logging.info(msg)

    with open(msr.filename, 'w') as fp:
         json.dump(outJson, fp)