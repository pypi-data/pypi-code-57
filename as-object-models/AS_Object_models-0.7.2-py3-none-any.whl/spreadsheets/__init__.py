import pandas as pd
import logging,os,json
from datetime import datetime
import jmespath
from xlsxwriter.utility import xl_col_to_name
from .. client_utils import FirestoreClient
from .. utils import Email
from .. pub_sub import publish_message
from .. import DataNumberLookup, StorageBlob, DataStorageType, InventoryActiveItems

class DownloadItemData(object):

    output_fields = ['id','customer_name','location_name','customer_id','location_id',
    'Cust_Item_Num','Item_Num','Product_Name','CO_Item_Num','customer_item_number',
    'Pack_Size','Tray','Double_Spike_Percent',
    'customer_item_description','customer_case_number',
    'Ti','Hi','Case_Width','Cases_Per_Pallet',
    'Case_UPC','Case_Weight_lbs','Case_Height','Ethyl_Block','Box',
    'CO_Case_Num', 'Special_Instructions_Recipe','Date_Code','Pot_Size_ML',
    'Branches', 'POP','Pick','UPC_Location','Vase_Style',
    'Sleeve','Top_Dressing','Heat_Pack',
    'Date_Code_Type','Grade','Assortment','Tag_Type','Staging','Case_Length',
    'Insert','List_Price_FOB_CO','List_Price',
    'Commission_Pricing','profit_margin','retail_price','recipe_cost',
    'retail_on_upc','Consumer_UPC']

    TMP_FOLDER = "/tmp/"
    CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
    def __init__(self, spreadSheetName, customer_id=None, 
               location_id=None, 
               emailAddress="system@analyticssupply.com",
               bucket_name=None,
               use_tmp=True):
        
        self.email = emailAddress
        self._client = FirestoreClient.getInstance()
        self.use_tmp_folder = use_tmp
        self.file_name = self.create_file_name(spreadSheetName)
        if bucket_name is None:
            bucket_name = os.environ.get("DATA_DOWNLOAD_BUCKET","prod_analytics_supply_download_data")
            if bucket_name.find("download") < 0:
               raise Exception("Invalid bucket name being used") 
        
        self.bucket_name = bucket_name
        self.custId = customer_id
        self.locId = location_id
        self.init_items = None
        self.items = []
        self.custPlantItem = None
        self.fields = None
        self.dropdowns = None
        self.plants = None
        self.df = None
        self.file_url = None

    def create_file_name(self, file_suffix):
        prefix = str(datetime.now()).replace("-","").replace(":","").replace(" ","").replace(".","")+"_"
        if not file_suffix.endswith(".xlsx"):
            parts = file_suffix.split(".")
            file_suffix = parts[0] + ".xlsx"
        
        tmp_file = prefix+"_"+file_suffix
        if self.use_tmp_folder:
            tmp_file = DownloadItemData.TMP_FOLDER+tmp_file
        return tmp_file

    def upload_to_storage(self):
        logging.info("Beggining load to storage")
        sClient = self._client.storeClient
        bucket = sClient.bucket(self.bucket_name)
        email_folder = self.email.replace("@","__at__").replace(".","__dot__")
        storageFile = self.file_name.replace(DownloadItemData.TMP_FOLDER,"")
        blob = bucket.blob(email_folder+"/"+storageFile)
        with open(self.file_name, "rb") as my_file:
            blob.upload_from_file(my_file,DownloadItemData.CONTENT_TYPE)
        blob.make_public()
        logging.info("Load complete, url created")
        self.file_url = blob.public_url

    def email_file(self, file_url=None):
        '''

        '''
        logging.info("Setting up to send email")
        e = Email()
        e.sender = "system@analyticssupply.com"
        e.subject = "Your file download"
        e.receivers.append(self.email)
        e.receivers.append('system@analyticssupply.com')
        storageFile = self.file_name.replace(DownloadItemData.TMP_FOLDER,"")
        url = self.file_url
        if file_url is not None:
            url = file_url
        
        if url is None:
            raise Exception("The file hasn't been uploaded yet... do that first")

        e.html = '<p>Click the link to download the items you selected.</p><span><a href="'+url+'">'+storageFile+'</a></span>'
        e.html = e.html + "<p> Thank you, <br> System Administrator (system@analyticssupply.com)"
        resp = e.send()
        logging.info(resp)
        logging.info("Email sent... Done.")
        return resp

    def set_df(self,inDf):
        self.df = inDf

    def _run_load(self):
        logging.info("Beginning item load")
        self.init_items = self.load_items()
        logging.info("Load complete... now filtering")
        self._filter_items()
        self.custPlantItem = DataStorageType.get_dataStorageType('cust_plant_item')
        self.fields = self.custPlantItem.get_storage_fields()
        self.dropdowns = self.get_dropdowns()
        self.plants = self.get_plants()
        logging.info("Loaded all system info..  complete")
        logging.info("loading up the pandas dataframe")
        self.df = self.load_df()
        logging.info("Dataframe Loaded... now ready to create file")


    def write_spreadsheet(self,fileName=None):
        if fileName is None:
            fileName=self.file_name
        
        logging.info("Writing output to file: "+fileName)
        writer = pd.ExcelWriter(fileName, engine='xlsxwriter')
        logging.info("Writing pandas output to excel")
        self.df.to_excel(writer, sheet_name='Customer_Items',index=False)
        workbook  = writer.book
        worksheet = writer.sheets['Customer_Items']
        lookup = workbook.add_worksheet('lookup')

        dCol = 0
        refDict = {}
        logging.info("Setting up dropdowns")
        for key in self.dropdowns.keys():
            dropdown = self.dropdowns[key]
            aCol = xl_col_to_name(dCol)
            vals = [x['name'] for x in dropdown]
            ref = '=lookup!$'+aCol+'$2:$'+aCol+'$'+str(len(vals)+1)
            dRow = 1
            lookup.write(0,dCol,key)
            for val in vals:
                lookup.write(dRow,dCol,val)
                dRow += 1
            dCol += 1
            refDict[key] = ref

        for fldName in self.dropdowns.keys():
            if fldName in list(self.df.columns):
                self._add_validation(worksheet,fldName,refDict)
        
        length_list = [len(x) for x in self.df.columns]
        for i, width in enumerate(length_list):
            worksheet.set_column(i, i, width+5)
        
        logging.info("Writing finished spreadsheet")
        writer.save()
    
    def _add_validation(self, wrkSht, fldName, refDict):
        col = self.df.columns.get_loc(fldName)
        validate = {'validate':'list','source':refDict[fldName]}
        wrkSht.data_validation(0, col, 1048575, col,validate)

    
    def load_df(self):
        df = pd.DataFrame(self.items)
        for plt in self.plants:
            df[plt] = df.Plants.apply(lambda x: self._load_plants(plt,x))
        
        cols = self.output_fields + self.plants
        df = df[cols]
        for fld in cols:
            df[fld] = df[fld].apply(self._clean_up_fields)
        return df

    def _clean_up_fields(self,fldVal):
        if isinstance(fldVal, str) and fldVal is not None:
            if len(fldVal.split("|")) == 1:
                return fldVal
            else:
                return fldVal.split("|")[1]
        return fldVal

    def _load_plants(self, plant_name, plant_arr):
        qty = 0
        if plant_arr is not None:
            if isinstance(plant_arr,list): 
                for plt_ent in plant_arr:
                    if isinstance(plt_ent,dict):
                        name = plt_ent.get('plant','--none--')
                        if len(name.split("|"))>1:
                            name = name.split("|")[1]
                        tempQty = plt_ent.get('qty',0)
                    else:
                        name = plt_ent if len(plt_ent.split("|")) == 1 else plt_ent.split("|")[1]
                        tempQty = 1
                    
                    if name == plant_name:
                        qty = tempQty
        return qty

    def load_items(self):
        logging.info("Grabbing all items")
        items = StorageBlob.getSB_of_Type('items')
        logging.info("Now getting customer and location info")
        return [self.get_item_information(x) for x in items]

    def get_item_information(self, inItem):
        loc = StorageBlob.getInstanceByPath(inItem.reference.parent.parent.path)
        cust = StorageBlob.getInstanceByPath(loc.reference.parent.parent.path)
        item = inItem.get_dict()
        item['customer_name'] = cust.customer_name
        item['customer_id'] = cust.id
        item['location_name'] = loc.location_name
        item['location_id'] = loc.id
        return item

    def _filter_items(self):
        if self.custId is not None:
            if self.locId is not None:
                self.items = [x for x in self.init_items if x['location_id'] == self.locId]
            else:
                self.items = [x for x in self.init_items if x['customer_id'] == self.custId]
        else:
            self.items = self.init_items

    def get_plants(self):
        plts = InventoryActiveItems.get_all_dict('Plants')
        plts = [plts[x]['name'] for x in plts.keys()]
        return plts

    def get_dropdowns(self):
        return DownloadItemData.GetDropdowns(self.fields)
    
    @classmethod
    def GetDropdowns(cls,inFields):
        dropdowns = {}
        optEntries = StorageBlob.getSB_of_Type('options')
        options = {'options':[x.get_dict() for x in optEntries]}

        for key in inFields.keys():
            field = inFields[key]
            if field.is_option_filled and field.field_name != 'Plants':
                if field.option_container.startswith("options"):
                    parts = field.option_container.split(".")
                    vals = jmespath.search(parts[0]+".{id: id, name: option_value}",options)
                    vals = [{'name': x['name'],'id':x['id']} for x in vals]
                else:
                    opts = StorageBlob.retrieve_option_data(field.field_name,field.option_container)
                    vals = [{'name':x['label'],'id':x['option_id']} for x in opts]
                dropdowns[key] = vals
        return dropdowns


from google.cloud import storage

class ProcessItemUpload(object):

    def __init__(self, blob_uri, email, filename):
        self.blob_uri = blob_uri
        self.email = email
        self.client = FirestoreClient.getInstance()
        self.upload_file = DownloadItemData.TMP_FOLDER+filename
        self.blob = self._load_blob()
        self.df = None
        self.dropdowns = None
        self.fields = None
        self.plant_lookup = None

    def process_blob(self):
        self._pre_process()
        self._load_blob()
        self._process_updates()

    def _load_blob(self):
        return storage.Blob.from_string(self.blob_uri,self.client.storeClient)

    def _process_updates(self):
        self.df = pd.read_excel(self.upload_file,'Customer_Items')
        plts = InventoryActiveItems.get_all_dict('Plants')
        self.plant_lookup = {plts[x]['name']:plts[x] for x in plts.keys()}
        self.df['Plants'] = self.df.apply(self._create_plants, axis=1)
        for fieldName in self.dropdowns.keys():
            if fieldName in list(self.df.columns):
                self.df[fieldName] = self.df[fieldName].apply(lambda x: self._update_recipes(x,fieldName))
        self.df['id'] = self.df.Cust_Item_Num
        update_fields = [x for x in list(self.fields.keys()) if x not in ['plant_image','Recipe','recipe_cost','profit_margin','Simplewick']]
        update_fields.append('id')
        self.df = self.df[update_fields]
        for fld in update_fields:
            self.df[fld] = self.df[fld].apply(self._clear_nans)
        updateDict = self.df.to_dict('records')
        for ent in updateDict:
            self._publish_updates(ent)
    
    def _publish_updates(self,entry):
        publish_message('updateItem', json.dumps(entry), {'id':entry.get('id','0'),'email':self.email})   

    def _clear_nans(self,value):
        if isinstance(value, list):
            return value
        if pd.isna(value) or pd.isnull(value):
            return ''
        return value
    
    def _create_plants(self,row):
        pltArray = []
        for plant in self.plant_lookup.keys():
            entry = self.plant_lookup[plant]
            qty = row[plant]
            if qty is not None and qty > 0:
                pltArray.append({'plant':entry['id']+"|"+plant,'qty':qty})
        
        return pltArray

    def _update_recipes(self, value,colName):
        dropdown = self.dropdowns.get(colName,None)
        if dropdown is None:
            return value
            
        if len(dropdown) == 0 or dropdown[0]['id'].startswith('options'):
            return value
        newval = value
        for entry in dropdown:
            if entry['name'] == value:
                return entry['id']+"|"+entry['name']
        return newval

    def _pre_process(self):
        with open(self.upload_file,"wb") as file_obj:
            self.blob.download_to_file(file_obj)

        custPlantItem = DataStorageType.get_dataStorageType('cust_plant_item')
        self.fields = custPlantItem.get_storage_fields()
        self.dropdowns = DownloadItemData.GetDropdowns(self.fields)

class ProcessItemUpdate(object):

    def __init__(self, updated_dict, item_id,email):
        self.updated_entry = updated_dict
        self.item_id = item_id
        self.email = email

    def update_sb(self):
        updatePath = DataNumberLookup.get_path_for_dnl(self.item_id)
        logging.info("Updating... "+updatePath)
        StorageBlob.update_blob_parent_fromPath(self.updated_entry,updatePath)
