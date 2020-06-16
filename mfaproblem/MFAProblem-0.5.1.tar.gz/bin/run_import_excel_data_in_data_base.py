#!python
# -*- coding: utf-8 -*-
"""
Integration of data from excel files into the database.

This module is dedicated to the integration of data from excel files into the database.

Data that can be transfered with this module :
    - sheets "data" and "minmax" of a regular project input file (for example bois_fr_1_1.xlsx)
    - sheets "proxis" and "data" of a proxy input file (for example bois_data.xlsx)
    - sheet "mysheet" from a file "myfile.xlsx" to a table "mytable" of the database

The module can be used with a maximum of 6 arguments :
    - The first one called "--input_file" is mandatory. It specifies the name of the input file \
        and has to be an excel file (\*.xls or \*.xlsx).
    - "--tab_data" : can be used to specify the name of the sheet containing basic data (for \
        example sheet "données FR" of exemple file tuto_fr.xlsx).
    - "--tab_minmax" : can be used to specify the name of the sheet containing min/max values.
    - "--tab_proxy" : can be used to specify the name of the sheet containing the list of the \
        proxys.
    - "--bdd_table" and "--tab_open" : can be used to fill in the database the table specified \
        by bdd_table with data found in tab_open sheet.

Specific behavior of the module :
    - Used without specifying "--tab_data" argument will lead the module to search Data sheet \
        among this list of possible names : 'data', 'données FR', 'données REG', 'data FR'. If \
        it find such a sheet it will copy its data in the "Datas" table of the database.
    - Used without "--tab_minmax" argument will lead to the same behaviour but for MinMax sheet \
        and "MinMaxs" table of the database. The list of possible sheet names will be : \
        'min_max', 'min max FR', 'min max REG'
    - Used without "--tab_proxy" argument will do the same for the table "Proxys" and sheet \
        name : 'proxis'.

Notes :
    - The module checks by itself if the input file has a correct extension (\*.xls or \*.xlsx).
    - When used with one of the 3 arguments "--tab_data", "--tab_minmax" or "--tab_proxy", the \
        module checks by itself if the specified sheet name is really a sheet of the input file.
    - By default (if the module is used without arguments about sheets names) if the input file \
        is a "proxy" file the module copy data of the sheets 'proxis' and 'data' into the tables \
        "Datas" and "Proxys" of the database. If the input file is a data model file, the module \
        will try to copy datas from sheets 'data' and 'minmax' into tables "Datas" and "MinMaxs" \
        of the database. The argument "null" can be used to neutralize one of these importations.
    - Parameters "--bdd_table" and "--tab_open" have to be used simultaneously.

Examples :
    >>> python.exe datain.py --input_file example_reg.xlsx

    Will copy values of sheets 'données REG' and 'min max REG' into tables 'Datas' and \
    'MinMaxs' of the database.

    >>> python.exe datain.py --input_file bois_data.xlsx

    Will copy values of sheets 'proxis' and 'data FR' into tables 'Proxys' and 'Datas' of \
        the database. 

    >>> python.exe datain.py --input_file bois_data.xlsx --tab_data null 

    Will copy datas from the sheet 'proxis' into the 'Proxys' table of the database and will \
        ignore datas from the sheet 'data FR'.

    >>> python.exe datain.py --input_file bois_fr_1.1.xlsx --tab_minmax null

    Will copy datas from the sheet 'données FR' into the 'Datas' table of the database and \
        will ignore datas from the sheet 'min max FR'.

    >>> python.exe datain.py --input_file somefile.xlsx --tab_data sheettdata --tab_minmax sheetmima 

    Will copy datas from sheets 'sheetdata' and 'sheetmima' into tables 'Datas' \
        and 'MinMaxs' of the database.

    >>> python.exe datain.py --input_file id_comm_aura.xlsx --bdd_table Geographics --tab_open id_comm

    Will copy values from sheet 'id_comm' of the input file 'id_comm_aura.xlsx' to fill the \
        table 'Geographics' of the database.
"""

import argparse
import sys
import os
import logging
import ast

import pandas as pd

try:
    from ..mfa_problem import io_excel
    from ..mfa_problem import io_bdd as sqdb
except ImportError:
    import mfa_problem.io_excel as io_excel
    import mfa_problem.io_bdd as sqdb


def chk_args():
    '''Checks arguments passed to the module.

    This function checks if arguments passed to the module are consistent. If this is not the \
        case the function prints an help message and interrupts the code.
    
    Return : a list of input file, name of the data sheet, name of the min_max sheet, name of \
        the proxy sheet, name of the database table to fill, name of additionnal sheet. 
    '''

    #list of possible sheets in string format
    possible_sheet = io_excel.consistantSheetName('')
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file" , help="Input excel file (.xls or .xlsx)")
    parser.add_argument("--model_name" , help="Model name used to copy data in the database")
    parser.add_argument("--bdd_clean" , help="Cleaning strategy of the database. 0 means all \
        values are added without previous database cleaning, 1 means database is cleaned before \
        adding new values (default value), 2 means only new values are added, 3 means old values \
        are updated and new values are added.")
    parser.add_argument("--tab_list", \
        help=f'list of sheet(s) name(s) from which to import data (every element must contain \
            one of this key words {possible_sheet})')
    parser.add_argument("--bdd_table" , \
        help=f"name of the bdd's table to add data in")
    parser.add_argument("--tab_open" , \
        help=f"tabulation name containing input data to add to the bdd")
    args = parser.parse_args()
    
    # Check input file parameter
    input_fi = ''
    if args.input_file != None:
        input_fi = args.input_file
        iext = os.path.splitext(input_fi)[1]
        if iext not in ('.xls', '.xlsx'):
            logging.critical('Wrong file name extention.\n' + parser.format_help())
            sys.exit()
    else:
        logging.critical('Need a file name as argument.\n' + parser.format_help())
        sys.exit()
    
    # model_name parameter
    model_nam = args.model_name
    
    # Check bdd_clean parameter
    bdd_clea = args.bdd_clean
    if (bdd_clea != None):
        bdd_clea = ast.literal_eval(args.bdd_clean)
        test = False
        if bdd_clea in [0, 1, 2, 3]:
            test = True
        if test == False:
            mess = 'If used, value of bdd_clean argument has to be 0, 1, 2 or 3.'
            logging.critical(mess + '\n' + parser.format_help())
            sys.exit()
    else:
        bdd_clea = 1 #by default the database is cleaned

    #Check tab_list parameter
    input_xl_tablist = io_excel.xl_get_sheet_details(input_fi) #actual sheet list in input file
    tab_list = args.tab_list
    if tab_list != None:
        tab_list = ast.literal_eval(args.tab_list)
        # Check if tab_list elements are in the list of input file sheets
        error_list = []
        valid_list = []
        for msheet in tab_list:
            if not msheet in input_xl_tablist:
                error_list.append(msheet)
            else:
                valid_list.append(msheet)
        if len(error_list) != 0:
            st_list = ', '.join(error_list)
            mess = f'Sheets {st_list} are not present in the input file !'
            if len(valid_list) == 0:
                mess = 'None of the sheets in tab_list are in the input file: programm interuption.'
                logging.critical(mess + '\n' + parser.format_help())
                sys.exit()
            else:
                st_list = ', '.join(valid_list)
                mess += f'Sheets {st_list} will be processed now...'
            logging.info(mess)
        # only valid (existing) sheets names are kept for the next calculations
        input_xl_tablist = valid_list
    #check if input list of sheets are in required sheet list name
    valid_sheetlist = []
    not_valid_sheet = []
    for msheet in input_xl_tablist:
        if io_excel.consistantSheetName(msheet) != '':
            valid_sheetlist.append(msheet)
        else:
            not_valid_sheet.append(msheet)
    if len(valid_sheetlist) == 0:
        mess = 'None of the sheet name found in the input file satisfy the required name.'
        logging.critical(mess + '\n' + parser.format_help())
        sys.exit()
    else:
        if len(not_valid_sheet) != 0:
            st_list = ', '.join(error_list)
            mess = f'Some sheets names ({st_list}) are not satisfying the "naming" requirement !'
            st_list = ', '.join(valid_sheetlist)
            mess += f'\nSheets {st_list} will be processed now...'
            logging.info(mess)
    tab_list = valid_sheetlist

    #Check "Open" parameters
    bdd_tab = args.bdd_table
    tab_ope = args.tab_open
    if bdd_tab != None:
        if logging.info(sqdb.check_table_exist(bdd_tab)) == False:
            mess = 'Provided bdd_table name doesn\'t exist in the bdd.'
            logging.critical(mess + '\n' + parser.format_help())
            sys.exit()
        else:
            if tab_ope != None:
                # is input file tabulation containing required tabulation name ?
                if tab_ope not in input_xl_tablist:
                    mess = 'Wrong tabulation name for \'open\' data values.'
                    logging.critical(mess + '\n' + parser.format_help())
                    sys.exit()
            else:
                mess = 'tab_open parameter cannot be empty in this use case.'
                logging.critical(mess + '\n' + parser.format_help())
                sys.exit()

    return [input_fi, model_nam, bdd_clea, tab_list, bdd_tab, tab_ope]

def xl_import_geo_aura(xl_fi, stab, def_val, js_tab, js_di):
    """Import informations from workbook tab called id_comm if it exists
    - xl_fi : workbook file name
    - stab : name of the workbook sheet to work on
    - def_val : dictionnary of default values (default columns values of excel sheet)
    - js_tab : name of the main JSon dictionnary key for this entry
    - js_di : dictionnary with informations to convert in JSon format
    """
    my_json = []
    try:
        df_prod = pd.read_excel(xl_fi, sheet_name=stab, skiprows=0) #saut des 2 1eres lignes
        #Keeping only non descriptive lines (ones for those 'Type_Territoire' has a non null value)
        df_prod = df_prod.loc[~df_prod['Type_Territoire'].isnull()]
        df_prod = df_prod.replace('69D', '69')
        df_prod = df_prod[[':parent',':child','Code_Insee','Nom_Territoire',\
                                  'Type_Territoire']]
        df_prod = df_prod.reset_index(drop=True)
        # Creation of newchild column with complete INSEE code if available or :child otherwise
        df_prod['newchild'] = df_prod['Code_Insee'].where(~df_prod['Code_Insee'].isnull(), \
df_prod[':child'])
        # Creation of newpar column with newchild values instead of :child ones
        df_wrk = df_prod.copy()
        for i in range(len(df_wrk.index)):
            my_self = df_wrk.iloc[[i]][':parent'].values
            strself = my_self[0]
            maval = df_prod[(df_prod[':child'] == strself)]
            if len(maval) > 0:
                maval = maval['newchild'].values[0]
            else:
                maval = strself
            df_wrk.at[i, 'newpar'] = maval
        df_prod = df_wrk.copy() #New dataframe with correct values
        # Add a line for France entry
        codeFR = 250 #INSEE code for France 
        LibFR = 'France'
        strchi = ', '.join(['01','02','03','04','06','11','24','27',\
'28','32','44','52','53','75','76','84','93','94'])
        my_li = [codeFR, 100, codeFR, LibFR, '', strchi]
        my_json.append(my_li)
        #Corresponding table : Type_Territoire (AURA file) <=> geotype (db)
        geotab = {'0': 100, '1': 405, '2': 400, '5': 401, '6': 407, '7': 200, '8': 300, \
'9': 500, '50': 402, '101': 407, '151': 407, '152': 407, '154': 403, '155': 404, \
'156': 201, '157': 406, '158': 407}
        #Driving dataframe
        df_drv = df_prod.copy()
        df_drv = df_drv.drop_duplicates(['newchild'])
        df_drv = df_drv.reset_index(drop=True)
        df_wrk = df_prod.copy()
        df_wrk = df_wrk.replace(np.nan, '', regex=True)
        for i in range(len(df_drv.index)):
            df_row = df_drv.iloc[[i]][[':parent',':child','Code_Insee','Nom_Territoire',\
                                'Type_Territoire', 'newchild', 'newpar']]
            strchild = df_row['newchild'].values[0]
            #strpar = df_row['newpar'].values[0]
            strgeo = str(int(df_row['Type_Territoire'].values[0]))
            strname = df_row['Nom_Territoire'].values[0]
            strinsee = df_row['Code_Insee'].values[0]
            df_par = df_wrk.loc[df_wrk['newpar'] == strchild]
            li_child = ''
            if len(df_par) != 0:
                li_child = ', '.join(df_par['newchild'].tolist())
            #df_chi = df_wrk[(df_wrk['newchild'] == strchild) & (df_wrk['newpar'] != strpar)]
            df_chi = df_wrk[df_wrk['newchild'] == strchild]
            li_par = ''
            if len(df_chi) != 0:
                li_par = ', '.join(df_chi['newpar'].tolist())
            my_li = [strchild,geotab[strgeo],strinsee,strname,li_par,li_child]
            my_json.append(my_li)
    except:
        logging.error(f'Exception in xl_import_geo_aura for {js_tab} entry')
    js_di[js_tab] = my_json

if __name__=='__main__':

    [input_file, model_name, bdd_clean, tab_list, bdd_table, tab_open] = chk_args()

    # CONNECTION TO THE DATABASE
    sess = sqdb.connect_aff(0)

    if model_name == None: # The name of input file is used as model_name by default
        model_name = os.path.splitext(os.path.basename(input_file))[0]

    df_input = pd.read_excel(input_file, None) #import all sheets in one dict of dataframes

    prox_dir = input_file.split('/')
    fromprox = False
    if prox_dir[0] == 'proxys':
        fromprox = True

    js_di = {}
    for mtab in tab_list:
        import_tab = True
        allowed_tab = io_excel.consistantSheetName(mtab)        
        if allowed_tab == 'param':
            jstab = 'param'
            import_tab = False
            io_excel.xl_import_param(df_input, mtab, js_di)
        elif allowed_tab == 'prod':
            jstab = 'dim_products'
            valdef = [1, '', False, False, None, None, False, '']
        elif allowed_tab == 'sect':
            jstab = 'dim_sectors'
            valdef = [1, '', False, False, None, None, False, '']
        elif allowed_tab == 'flux':
            jstab = 'ter_base'
            import_tab = False
            io_excel.xl_import_terbase(df_input, mtab, js_di) 
        elif allowed_tab == 'data':
            jstab = 'data'
            valdef = ['', '', '', '', '', None, None, None, '', '', '', '']
            #valdef = ['', '', '', '', '', None, None, '', None, '', None, '']
        elif allowed_tab == 'minmax':
            jstab = 'min_max'
            valdef = ['', '', '', '', '', None, None, '', '', '', '', '']
            #valdef = ['', '', '', '', '', None, None, '', '', '', None, '']
        elif allowed_tab == 'constr':
            jstab = 'constraints'
            valdef = [None, '', '', '', '', '', None, None, None, None, None]
        elif allowed_tab == 'proxy':
            jstab = 'proxy'
            valdef = ['', '', None, None, '']
            # Add a virtual geographic code
            js_geo = js_di['proxy']
            for mli in js_geo:
                mli.insert(1, '0')
            js_di['proxy'] = js_geo
        elif allowed_tab == 'pflow':
            jstab = 'proxytypeflow'
            valdef = ['', '', '', '']
        elif allowed_tab == 'psect':
            jstab = 'proxytypesect'
            valdef = ['', '', '', '']
        else:
            import_tab = False
        if import_tab == True:
            io_excel.xl_import_tab(df_input, mtab, valdef, jstab, js_di)
    js_tmp = [] 
    if len(js_di['proxytypeflow']) != 0:
        for mli in js_di['proxytypeflow']:
            mli.append('flow')
            js_tmp.append(mli)
        del js_di['proxytypeflow']
    if len(js_di['proxytypesect']) != 0:
        for mli in js_di['proxytypesect']:
            mli.append('sector')
            js_tmp.append(mli)
        del js_di['proxytypesect']
    if len(js_tmp) != 0:
        js_di['proxytype'] = js_tmp
    
    if tab_open != None:
        jstab = 'geographic'
        valdef = [None,0,None,'',None,'',None,'',None,'',None,'']
        xl_import_geo_aura(input_file,tab_open,valdef,jstab,js_di)

    if len(js_di) > 0:
        sqdb.save_inputs(js_di, sess, bdd_clean, model_name, '')
