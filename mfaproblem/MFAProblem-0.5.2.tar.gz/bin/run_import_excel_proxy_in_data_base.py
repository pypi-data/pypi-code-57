#!python
import argparse
import sys
import os
import logging
import ast

import numpy as np
import pandas as pd
from shutil import copyfile

try:
    from ..mfa_problem import io_bdd as sqdb
except ImportError:
    import mfa_problem.io_bdd as sqdb


def chk_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file" , help="Input excel or csv file (.xls, .xlsx or .csv)")
    parser.add_argument("--model_name" , help="Model name used to copy data in the database")
    parser.add_argument("--proxy_name" , help="Name(s) of the proxy(s) to calculate")
    parser.add_argument("--proxy_sheet" , help="Name of the sheet to use in input excel file")
    parser.add_argument("--proxy_geo" , help="Geographic levels to use in calculations")
    parser.add_argument("--proxy_add" , help="Additionnal optionnal information(s) about proxy(s) \
importation and/or calculation \n Should be \'BDD\' if you want to create xls proxy file from BDD.")
    args = parser.parse_args()
    bprint = False
    input_file = ''
    if args.input_file != None:
        input_file = args.input_file
        iext = os.path.splitext(input_file)[1]
        if iext not in ('.xls', '.xlsx', '.csv'):
            if not bprint:
                parser.print_help()
                bprint = True
            logging.critical('Wrong file name extention.\n' + parser.format_help())
            sys.exit()
    else:
        if not bprint:
            parser.print_help()
            bprint = True
        logging.critical('Need a file name as argument.\n' + parser.format_help())
        sys.exit()
    model_name = args.model_name
    proxy_name = args.proxy_name
    if proxy_name != None:
        proxy_name = ast.literal_eval(args.proxy_name)
    proxy_sheet = args.proxy_sheet
    proxy_geo = args.proxy_geo
    if proxy_geo != None:
        proxy_geo = ast.literal_eval(args.proxy_geo)
    proxy_add = args.proxy_add
    if (proxy_add != None):
        proxy_add = ast.literal_eval(args.proxy_add)
    if proxy_name != None:
        if ((proxy_sheet == None) and (iext in ('.xls', '.xlsx'))):
            if not bprint:
                parser.print_help()
                bprint = True
            logging.critical('proxy_sheet is madatory when proxy_name is used. \n' + \
parser.format_help())
            sys.exit()
        else:
            if proxy_geo != None:
                proxy_geo1 = proxy_geo[0]
                proxy_geo2 = proxy_geo[1]
                test1 = proxy_geo1.isdigit()
                test2 = (proxy_geo2.isdigit() and (len(proxy_geo2) == 3))
                if ((test1 == False) or (test2 == False)):
                    if not bprint:
                        parser.print_help()
                        bprint = True
                    logging.critical('When proxi_name is not null, proxy_geo has to \
be a string with the id_int code for the main geographic and geotype code for sub-structures. \n'\
 + parser.format_help())
                    sys.exit()
            if 'proxi_population' in proxy_name:
                proxy_add = ''
            berr = False
            bprox = False
            if 'proxi_papiers' in proxy_name:
                bprox = True
                idx = proxy_name.index('proxi_papiers')
                if '1712Z' in proxy_add:
                    berr = proxy_add.index('1712Z') == idx
            if 'proxi_emballages' in proxy_name:
                bprox = True
                idx = proxy_name.index('proxi_emballages')
                if '1724Z' in proxy_add:
                    berr = proxy_add.index('1724Z') == idx
            if 'proxi_parquets' in proxy_name:
                bprox = True
                idx = proxy_name.index('proxi_parquets')
                if '1622Z' in proxy_add:
                    berr = proxy_add.index('1622Z') == idx
            if ((berr == False) and (bprox == True)):
                logging.critical('NAF rev2 code and proxy name have to be at the same \
place in their respective lenght.')
                sys.exit()
        
    return [input_file, model_name, proxy_name, proxy_sheet, proxy_geo, proxy_add]
    
def filter(data, dict_of_filters, headers=None):
    if headers is None:
        headers = ['period', 'region', 'table', 'origin', 'destination', 'value',
           'uncert', 'constraint', 'quantity', 'unit', 'factor', 'source']
    d = np.array(data)
    for k, v in dict_of_filters.items():
        if type(v) != list:
            d = d[d[:,headers.index(k)] == v]
        else:
            enum_distinct=[]
            for vi in v:
                if vi not in enum_distinct:
                    enum_distinct.append(vi)
                    if len(enum_distinct)==1:
                        d_tmp = np.array(d)
                        d = d[d[:, headers.index(k)] == vi]
                    else:
                        d = np.append(d, d_tmp[d_tmp[:, headers.index(k)] == vi], axis=0)
    return d

def select_distinct(data, cols, headers=None):
    if headers is None:
        headers = ['period', 'region', 'table', 'origin', 'destination', 'value',
           'uncert', 'constraint', 'quantity', 'unit', 'factor', 'source']
    df = pd.DataFrame(data=data, columns=headers)
    df = df.drop_duplicates(subset=cols)
    return df[cols].values

if __name__=='__main__':
    [input_file, model_name, proxy_name, proxy_sheet, proxy_geo, proxy_add] = chk_args()

    #Working on input file backup copy
    iname, iext = os.path.splitext(input_file)
    root_file_name, iext = os.path.splitext(os.path.basename(input_file))
    xl_wrk = os.path.join(root_file_name + '_wkr' + iext)
    copyfile(input_file,xl_wrk)

    # CONNECTION TO THE DATABASE
    sess = sqdb.connect_aff(0)

    extract_from_input = False
    if model_name == None:
        extract_from_input = True
        model_name = os.path.splitext(os.path.basename(input_file))[0]

    if proxy_name != None:
        bcalcok = False
        if extract_from_input == True:
            gr_name = model_name.split('_')
            model_name = '_'.join(gr_name[:3]) #Keep only group of string before the 3rd '_' char
            #model_name = model_name[:12]
        # Extraction of geographic list from geotable
        geo_max = proxy_geo[0]
        geo_min = proxy_geo[1]
        data_geo = np.array(sqdb.read_inputs(sqdb.Geographic, sess, model_name, geo_max, geo_min))
        #The first line is the main parent line : need to be removed
        data_geo = np.delete(data_geo, (0), axis=0)
        df_geo = pd.DataFrame(data=data_geo, columns=['id_int', 'Nom', 'Code_Parents'])
        df_geo = df_geo.reset_index(drop=True)
        # Handling individual proxy cases in this section
        if 'proxi_population' in proxy_name:
            bcalcok = True
            # Get population values from input file
            if iext == '.csv':
                df_pop = pd.read_csv(xl_wrk, skiprows=7, dtype=str)
            else:
                df_pop = pd.read_excel(xl_wrk, sheet_name=proxy_sheet, skiprows=7, dtype=str)
            df_pop = df_pop[['Code région', 'Code département', 'Code commune', \
                'Population totale']]
            df_pop = df_pop[df_pop['Code région'] == '84']
            df_pop['id_int'] = df_pop['Code département'].astype(str) + \
                df_pop['Code commune'].astype(str)
            df_pop = df_pop[['id_int', 'Population totale']]
            df_pop['Population totale'] = df_pop['Population totale'].astype(int)
            df_pop = df_pop.reset_index(drop=True)
            # List of communes in one dataframe and not in the other
            li_geo = df_geo['id_int'].values.tolist()
            li_pop = df_pop['id_int'].values.tolist()
            li_dif = list(set(li_geo) - set(li_pop))
            logging.info('List of geographic ID difference between db and INSEE file :\n' + \
str(li_dif))
            #df_geo = df_geo[~df_geo['id_int'].isin(li_dif)]
            #df_pop = df_pop[~df_pop['id_int'].isin(li_dif)]
            # Merge dataframes
            #df_join = pd.merge(df_geo, df_pop, how='inner', on=['id_int'])
            df_join = pd.merge(df_geo, df_pop, how='left', on=['id_int'])
            df_join.fillna(0, inplace=True)
            poptot = df_join['Population totale'].sum()
            #df_join['Pop %'] = (100 * df_join['Population totale']) / poptot
            df_join['Pop %'] = df_join['Population totale'] / poptot
            mess = 'Total population before merging : ' + str(df_pop['Population totale'].sum())
            mess = mess + '\nTotal population after merging : ' + str(poptot)
            logging.info(mess) 
            df_join['proxy_name'] = proxy_name[0]
            df_join['Source'] = 'population communale insee 2019'
            df_rec = df_join[['proxy_name', 'id_int', 'Nom', 'Pop %', 'Population totale', 
                    'Source']]
            # Saving data in db
            js_di = {}
            js_di['proxy'] = df_rec.values.tolist()
        if (('proxi_papiers' in proxy_name) or ('proxi_emballages' in proxy_name) or \
('proxi_parquets' in proxy_name)):
            bcalcok = True
            js_di = {}
            # Get clap values from excel file
            if iext == '.csv':
                #df_clap = pd.read_csv(xl_wrk, skiprows=0, dtype=str)
                df_clap = pd.read_csv(xl_wrk, skiprows=0)
            else:
                df_clap = pd.read_excel(xl_wrk, sheet_name=proxy_sheet, skiprows=0)
            df_clap['id_int'] = df_clap['id_comm'].astype(str).str.zfill(5)
            df_clap['Quantity'] = df_clap['nbetab'] + df_clap['effectif']
            df_clap['Quantity'] = df_clap['Quantity']
            df_clap = df_clap[['codenaf', 'id_int', 'Quantity']]
            proxy_coup = list(zip(proxy_name, proxy_add))
            li_prox = []
            for proxy, naf_co in proxy_coup:
                #print(naf_co)
                df_wrk = df_clap[df_clap['codenaf'] == naf_co]
                df_wrk = pd.merge(df_geo, df_wrk, how='left', on=['id_int'])
                df_wrk.fillna(0, inplace=True)
                #print(df_wrk.info())
                #print(df_wrk.head(5))
                valtot = df_wrk['Quantity'].sum()
                print(f'{naf_co} --> {valtot}')
                df_wrk['perct'] = df_wrk['Quantity'] / valtot
                df_wrk['proxy_name'] = proxy
                df_wrk['Source'] = 'emplois (INSEE clap ' + naf_co + ')'
                df_rec = df_wrk[['proxy_name', 'id_int', 'Nom', 'perct', 'Quantity', 'Source']]
                # Saving data in db
                li_prox.extend(df_rec.values.tolist())
            js_di['proxy'] = li_prox
        if (('proxi_prod_granulés' in proxy_name) or ('proxi_panneaux' in proxy_name) or \
('proxi_contreplaqués' in proxy_name) or ('proxi_pap_mécanique' in proxy_name) or \
('proxi_pap_chimique' in proxy_name)):
            bcalcok = True
            js_di = {}
            if iext == '.csv':
                df_prox = pd.read_csv(xl_wrk, skiprows=0)
            else:
                df_prox = pd.read_excel(xl_wrk, sheet_name=proxy_sheet, skiprows=0, dtype=object)
            li_prox = []
            for proxi in proxy_name:
                df_wrk = df_prox[df_prox['Nom proxi'] == proxi]
                df_wrk = pd.merge(df_geo, df_wrk, how='left', on=['id_int'])
                df_wrk.fillna(0, inplace=True)
                df_wrk['Nom proxi'] = proxi
                df_wrk['Source'] = df_wrk['source'].astype(str) + ' ' + \
                                df_wrk['Info complémentaire'].astype(str)
                df_rec = df_wrk[['Nom proxi', 'id_int', 'Nom', 'Pourcentage', 'Quantity', 'Source']]
                li_prox.extend(df_rec.values.tolist())
            js_di['proxy'] = li_prox     
        # Saving data in db
        if len(js_di) > 0:
            sqdb.save_inputs(js_di, sess, 1, model_name, proxy_name)
        # Delete working file
        os.remove(xl_wrk)  

        #Put this in a separate function
        '''#_____WRITE DATA REG_____
        js_di = {}
        js_di['data'] = data_reg
        model_name = model_name + '_REG'
        if len(js_di) > 0:
            sqdb.save_inputs(js_di, sess, 1, model_name)'''
