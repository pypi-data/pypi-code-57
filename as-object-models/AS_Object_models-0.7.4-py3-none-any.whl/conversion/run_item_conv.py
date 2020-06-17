import sys,os,logging
from google.cloud import firestore
import traceback

import argparse
import time

import google.auth.crypt
import google.auth.jwt
from google.oauth2 import service_account

import pandas as pd

import requests

from as_models.conversion import AppConfigurationConversion, DataNumbernConversion, MiscConversion, SchemaConversion, StorageBlobConversion
from as_models import DataNumberLookup


class ColorOrchids_CustTracking_Conversion(object):

    def __init__(self, datastore_project, firestore_project, steps=['all']):
        self.ds_proj = datastore_project
        self.fs_proj = firestore_project
        logging.info("data store project = "+self.ds_proj)
        logging.info("firestore project = "+self.fs_proj)
        self.db = firestore.Client(
        project=self.fs_proj, credentials=service_account_cred())
        
        self.steps = steps
        logging.info("Running conversion steps... ")

        if 'delete' in self.steps or 'all' in self.steps:
            self.__deleteFirestoreColl()   
        if 'schema' in self.steps or 'all' in self.steps:
            opFlds = self._convert_schema()
        if 'datanumber' in self.steps or 'all' in self.steps:
            self._convert_data_number()
        if 'misc' in self.steps or 'all' in self.steps:
            self._convert_misc()
        if 'storageblob' in self.steps or 'all' in self.steps:
            self._convert_storage_blob(opFlds)
        if 'spreadsheet' in self.steps or 'all' in self.steps:
            self._plt_cols = None
            self._convert_plants()

    def __deleteFirestoreColl(self):
        logging.info("deleting...")
        startCols = []
        startCols.append('application_data/Color_Orchids/Customer_Tracking')
        startCols.append('application_data/Color_Orchids/Data_API')
        startCols.append('app_configuration/Color_Orchids/Customer_Tracking')
        startCols.append('data_number_lookup/Color_Orchids/Customer_Tracking')
        startCols.append('data_number_sync/Color_Orchids/Customer_Tracking')
        startCols.append('data_schemas/Color_Orchids/Customer_Tracking')
        startCols.append('reporting_config/Color_Orchids/Customer_Tracking')
        cols = [self.db.collection(x) for x in startCols]
        #colRefs = self.db.collections()
        self.__deleteCollectin(cols)

    

    def __deleteCollectin(self, colRefs):
        for colRef in colRefs:
            logging.info("Deleteing collection:  "+colRef.id)
            docRefs = colRef.list_documents()
            for docRef in docRefs:
                self.__deleteCollectin(docRef.collections())
                docRef.delete()

    def _convert_data_number(self):
        logging.info("converting... data number")
        try:
            DataNumbernConversion(self.ds_proj, self.fs_proj)
        except Exception as e:
            logging.info("Problem trying to conver the data number... ")
            traceback.print_exc()
            raise e

    def _convert_schema(self):
        logging.info("converting schema... ")
        try:
            s = SchemaConversion(self.ds_proj, self.fs_proj)
            return s.get_op_fields()
        except Exception as e:
            logging.info("Problem trying to move over the schema definitions... ")
            traceback.print_exc()
            raise e

    def _convert_app_config(self):
        logging.info("converting app config.. ")
        try:
            AppConfigurationConversion(self.ds_proj, self.fs_proj)
        except Exception as e:
            logging.info("Problem trying to move over the app configurations... ")
            traceback.print_exc()
            raise e

    def _convert_misc(self):
        logging.info("doing misc... converting")
        try:
            MiscConversion(self.ds_proj, self.fs_proj)
        except Exception as e:
            logging.info("Problem trying to convert miscellaneous items... ")
            traceback.print_exc()
            raise e

    def _get_elements(self, _plant_entry):
        return {'name':_plant_entry.get('name'),'id':_plant_entry.id,'path':_plant_entry.reference.path}

    @property
    def plt_cols(self):
        if self._plt_cols is None:
            path = 'application_data/Color_Orchids/Customer_Tracking/StorageBlob/recipe_costing'
            colRef = self.db.collection(path)
            q = colRef.where('item_type','==','Plants')
            q = q.where('status','==','Active')
            snaps = q.stream()
            self._plt_cols = [self._get_elements(x) for x in snaps if x.get('name') != 'N/A']
        return self._plt_cols

    def _create_plt_entries(self,row):
        plt_entries = []
        for plant in self.plt_cols:
            qty = row[plant['name']]
            if qty > 0:
                plt_entries.append({'plant':plant['id']+"|"+plant['name'],'qty':qty})
        return plt_entries

    def _convert_plants(self):
        logging.info("Loading conversion info from spreadsheets")
        self._get_conv_sheets()
        logging.info("Now loading cust_plant_items with updated plants")
        for dnl in self._conv_cpi_plts.keys():
            path = DataNumberLookup._get_path_for_dnl(self.db, dnl)
            if path is not None:
                docRef = self.db.document(path)
                docRef.update(self._conv_cpi_plts[dnl])
        
        logging.info("Now loading master plant_items with updated plants")
        for dnl in self._conv_pi_plts.keys():
            path = DataNumberLookup._get_path_for_dnl(self.db, dnl)
            if path is not None:
                docRef = self.db.document(path)
                docRef.update(self._conv_pi_plts[dnl])

        logging.info("Loading the CO_Item_Num updates")
        for dnl in self._conv_cpi_item_num.keys():
            path = DataNumberLookup._get_path_for_dnl(self.db, dnl)
            if path is not None:
                docRef = self.db.document(path)
                docRef.update(self._conv_cpi_item_num[dnl])

    def _get_conv_sheets(self):
        df = pd.read_excel('as_models/scripts/item_plants_revised.xlsx',sheet_name='CustomerPlantItem')
        df['plants_new'] = df.apply(self._create_plt_entries,axis=1)
        df = df[['data_number_lookup','plants_new']]
        df.rename(columns={'plants_new':'Plants'},inplace=True)
        df = df.set_index('data_number_lookup')
        self._conv_cpi_plts = df.to_dict('index')

        dfm = pd.read_excel('as_models/scripts/item_plants_revised.xlsx',sheet_name='Master')
        dfm['plants_new'] = dfm.apply(self._create_plt_entries,axis=1)
        dfm = dfm[['data_number_lookup','plants_new','CO_Item_Num']]
        dfm.rename(columns={'plants_new':'Plants'},inplace=True)
        dfm = dfm.set_index('data_number_lookup')
        self._conv_pi_plts = dfm.to_dict('index')

        dfc = pd.read_excel('as_models/scripts/item_conv revised.xlsx',sheet_name='CustomerPlantItem')
        dfc = dfc[['data_number_lookup','CO_Item_Num']]
        dfc = dfc.set_index('data_number_lookup')
        self._conv_cpi_item_num = dfc.to_dict('index')


    def _convert_storage_blob(self,opFlds):
        logging.info("converting storage blob..")
        try:
            StorageBlobConversion(self.ds_proj, self.fs_proj,opFlds)
        except Exception as e:
            logging.info("Problem trying to convert StorageBlob items... ")
            traceback.print_exc()
            raise e


def service_account_cred(sa_keyfile='/home/analyticssupply/tmp/auth.json'):
    return service_account.Credentials.from_service_account_file(sa_keyfile)


def generate_jwt(sa_keyfile='/home/analyticssupply/tmp/auth.json',
                 sa_email='local-testing@backend-firestore-test.iam.gserviceaccount.com',
                 audience='local-testing',
                 expiry_length=3600):
    """Generates a signed JSON Web Token using a Google API Service Account."""

    now = int(time.time())

    # build payload
    payload = {
        'iat': now,
        # expires after 'expiry_length' seconds.
        "exp": now + expiry_length,
        # iss must match 'issuer' in the security configuration in your
        # swagger spec (e.g. service account email). It can be any string.
        'iss': sa_email,
        # aud must be either your Endpoints service name, or match the value
        # specified as the 'x-google-audience' in the OpenAPI document.
        'aud':  audience,
        # sub and email should match the service account's email address
        'sub': sa_email,
        'email': sa_email
    }

    # sign with keyfile
    signer = google.auth.crypt.RSASigner.from_service_account_file(sa_keyfile)
    jwt = google.auth.jwt.encode(signer, payload)

    return jwt

def parse_arg(args, arg_num):
    if len(args) > arg_num:
        arg = args[arg_num]
        if arg.startswith("-"):
            arg_dash = arg[1:]
            if arg_dash.lower() == 's' or arg_dash.lower() == 'step':
                return args[arg_num+1],arg_num+2,'step'
            elif arg_dash.lower() == 'ds':
                return args[arg_num+1],arg_num+2,'ds_project'
            elif arg_dash.lower() == 'fs':
                return args[arg_num+1],arg_num+2,'fs_project'
            else:
                logging.info('unknown flag: '+arg)
                return None, arg_num+1,'unknown'
        else:
            return arg,arg_num+1,'project'
    else:
        return None, 0,None

if __name__ == '__main__':
    '''
    You can set the datastore project by using the environment variable DS_PROJECT
    You can set the firestore project by susing the environment variable FS_PROJECT
    .. whatever you set can be overridden by command line args
    -ds <project_name> = DataStore Project
    -fs <project_name> = Firestore Project
    -s <step_name> = Step to Run  (run all by default)
    
    If you do neither, it will default to the folling:
    DS_PROJECT = 'item-tracking-colororchids'
    FS_PROJECT = 'backend-firestore-test'
    '''
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.INFO)
    dsProject = os.environ.get('DS_PROJECT','item-tracking-colororchids')
    fsProject = os.environ.get('FS_PROJECT','backend-firestore-test')
    steps = []
    
    arg,num,arg_type = parse_arg(sys.argv,1)
    while arg is not None:
        logging.info("Arg passed: {}, next number: {}, argument type: {}".format(arg,num,arg_type))
        if arg_type == 'fs_project':
            fsProject = arg
        if arg_type == 'ds_project':
            dsProject = arg
        if arg_type == 'step':
            parse_steps = arg.split(",")
            for stp in parse_steps:
                steps.append(stp)
        arg, num,arg_type = parse_arg(sys.argv,num)

    process_steps = steps if len(steps) > 0 else ['all']
    #process_steps = ['spreadsheet']
    os.environ['GOOGLE_CLOUD_PROJECT'] = fsProject
    os.environ['APP_FIRESTORE_COMPANY'] = 'Color_Orchids'
    os.environ['APP_FIRESTORE_NAME'] = 'Customer_Tracking'
    ColorOrchids_CustTracking_Conversion(dsProject, fsProject,process_steps)
