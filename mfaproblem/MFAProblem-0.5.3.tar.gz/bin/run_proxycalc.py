#!python
import argparse
import sys
import os
import ast
import time

from shutil import copyfile

try:
    from ..mfa_problem import su_trace
    from ..mfa_problem import io_excel
    from ..mfa_problem import io_bdd as sqdb
    from ..mfa_problem import mfa_problem_format_io
except ImportError:
    import mfa_problem.su_trace as su_trace
    import mfa_problem.io_excel as io_excel
    import mfa_problem.io_bdd as sqdb
    import mfa_problem.mfa_problem_format_io as mfa_problem_format_io


def chk_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", help="Input excel or csv file (.xls, .xlsx or .csv)")
    parser.add_argument("--sheet_name", help="Name of sheet to write output results in input file")
    parser.add_argument("--model_name", help="Model name used to extract/copy data in the database")
    parser.add_argument("--proxy_geo", help="Geographic levels to use in calculations")
    parser.add_argument("--main_names", help="List of 2 elements : model name used to extract \
main geographic level data in database and name of the main upper geographic level.")
    parser.add_argument("--proxy_add", help="Additionnal optionnal information(s) about proxy(s) \
importation and/or calculation \n Should be \'BDD\' if you want to create xls proxy file from \
BDD.")
    args = parser.parse_args()
    bprint = False
    input_file = ''
    if args.input_file is not None:
        input_file = args.input_file
        iext = os.path.splitext(input_file)[1]
        if iext not in ('.xls', '.xlsx', '.csv'):
            if not bprint:
                parser.print_help()
                bprint = True
            su_trace.logger.critical('Wrong file name extention.\n' + parser.format_help())
            sys.exit()
    else:
        if args.model_name == None:
            if bprint == False:
                parser.print_help()
                bprint = True
            su_trace.logger.critical('If file argument is empty a model name argument is mandatory.\n' 
                    + parser.format_help())
            sys.exit()
    sheet_name = args.sheet_name
    model_name = args.model_name
    proxy_geo = args.proxy_geo
    if proxy_geo != None:
        proxy_geo = ast.literal_eval(args.proxy_geo)
        proxy_geo1 = proxy_geo[0]
        proxy_geo2 = proxy_geo[1]
        test1 = proxy_geo1.isdigit()
        if test1 == False:
            if not bprint:
                parser.print_help()
                bprint = True
            su_trace.logger.critical('Proxy_geo has to be a list of 1 id_int code for the main \
geographic and a sub_list of geotype code for sub-structures. \n' + parser.format_help())
            sys.exit()
        for pr_geo in proxy_geo2:
            test2 = (pr_geo.isdigit() and (len(pr_geo) == 3))
            if test2 == False:
                if not bprint:
                    parser.print_help()
                    bprint = True
                su_trace.logger.critical('Proxy_geo has to be a list of 1 id_int code for the main \
geographic and a sub_list of geotype code for sub-structures. \n' + parser.format_help())
                sys.exit()
    proxy_add = args.proxy_add
    if ((proxy_add != None) and (proxy_add != 'BDD')):
        proxy_add = ast.literal_eval(args.proxy_add)
    main_names = args.main_names
    if main_names != None:
        main_names = ast.literal_eval(args.main_names)
        if type(main_names) != list:
            main_names = [main_names]
    main_mod_name = main_names[0]
    if (proxy_add == 'BDD'):
        if main_mod_name == None:
            su_trace.logger.critical('main_mod_name (first argument of --main_names) is ' +
                    'mandatory when BDD argument is used. \n' + parser.format_help())
            sys.exit()
    if not os.path.isfile(input_file):
        if proxy_add != 'BDD':
            su_trace.logger.critical('proxy_add is madatory when trying to work from BDD. \n' + \
parser.format_help())
            sys.exit()    
        
    return [input_file, sheet_name, model_name, proxy_geo, main_names, proxy_add]


if __name__=='__main__':

    t0=time.time()
    log_file = su_trace.check_log()
    su_trace.run_log(log_file)
    # To change the logger level uncomment following line (see log_level fct for posssible values)
    # su_trace.log_level("DEBUG") 
    
    [excel_input_file, sheet_name, model_name, proxy_geo, main_names, proxy_add] = chk_args()
    main_mod_name = ''
    upper_level_name = ''
    if main_names != None:
        main_mod_name = main_names[0]
        if len(main_names) > 1:
            upper_level_name = main_names[1]
    # Log infos about arguments used
    su_trace.logger.info('-- LIST OF ARGUMENTS --')
    su_trace.logger.info(f'> Input file is: {excel_input_file}')
    su_trace.logger.info(f'> Sheet name to write results in: {sheet_name}')
    su_trace.logger.info(f'> Model name: {model_name}')
    mess = '> Geographic codes: '
    if proxy_geo != None:
        mess += f'upper geographical level is {proxy_geo[0]} and sub level is {proxy_geo[1]}'
    else:
        mess += 'Not used'
    su_trace.logger.info(mess)
    mess = '> Main model names:'
    if main_names != None:
        if main_mod_name != '':
            mess += f' main model name is \'{main_mod_name}\''
        if upper_level_name != '':
            mess += f' upper geographical level name is \'{upper_level_name}\''
    else:
        mess += 'Not used'
    su_trace.logger.info(mess)
    su_trace.logger.info(f'> Additional arguments: {proxy_add}')
    t1 = time.time()
    su_trace.logger.info('-- INPUT ARGUMENTS CHECKED, TOOK ' + str(round((t1-t0),2)) + ' sec --')

    #Results are wrotten on input file backup copy
    if proxy_add != 'BDD' or sheet_name != None:
        root_file_name, iext = os.path.splitext(os.path.basename(excel_input_file))
        output_file_name = os.path.join(os.path.dirname(excel_input_file), 
                root_file_name + '_subterri' + iext)
        copyfile(excel_input_file, output_file_name)
        su_trace.logger.info('output file is ' + output_file_name)
        

    # CONNECTION TO THE DATABASE
    sess = sqdb.connect_aff(0)

    if model_name == None:
        model_name = os.path.splitext(os.path.basename(excel_input_file))[0]
        # Usual general importation (from data base) case handled from here
        gr_name = model_name.split('_')
        model_name = '_'.join(gr_name[:3]) #Keep only group of string before the 3rd '_' char
    t2 = time.time()
    su_trace.logger.info('-- INITIALISATION DONE, TOOK ' + 
            str(round((t2-t1),2)) + ' / ' + str(round((t2-t0),2)) + ' sec --')

    # Data importation
    if proxy_add != 'BDD':
        # importation from excel file
        try:
            proxy_input = io_excel.excel_proxy_to_json(output_file_name, upper_level_name)
        except Exception as expt:
            t3 = time.time()
            su_trace.logger.info('Import from excel file FAILLED, TOOK ' + 
                    str(round((t3-t2),2)) + ' / ' + str(round((t3-t0),2)) + ' sec --')
            su_trace.logger.info('Exception message : ' + str(expt))
            sys.exit()
    else:
        # Extraction from database
        try:
            proxy_input = sqdb.database_proxy_to_json(sess, model_name, main_mod_name, proxy_geo)
        except Exception as expt:
            t3 = time.time()
            su_trace.logger.info('Import from database FAILLED, TOOK ' + 
                    str(round((t3-t2),2)) + ' / ' + str(round((t3-t0),2)) + ' sec --')
            su_trace.logger.info('Exception message : ' + str(expt))
            sys.exit()
    t3 = time.time()
    su_trace.logger.info('-- DATA IMPORTATION DONE, TOOK ' + 
            str(round((t3-t2),2)) + ' / ' + str(round((t3-t0),2)) + ' sec --')

    #_____COMPUTE PROXI DATA_____
    try:
        proxy_output = mfa_problem_format_io.computes_data_from_proxy(proxy_input)
    except Exception as expt:
        t4=time.time()
        su_trace.logger.info('Proxy calculation FAILLED, TOOK ' + 
                str(round((t4-t3),2)) + ' / ' + str(round((t4-t0),2)) + ' sec --')
        su_trace.logger.info('Exception message : ' + str(expt))
        sys.exit()   
    t4=time.time()
    su_trace.logger.info('-- PROXY CALCULATION DONE, TOOK ' + 
            str(round((t4-t3),2)) + ' / ' + str(round((t4-t0),2)) + ' sec --')

    #_____WRITE DATA REG_____ (By default results are saved in the data_base)
    try:
        sqdb.write_proxy_output_in_db(sess, model_name, proxy_output)
        mess = '-- PROXY WRITTEN IN DATABASE, TOOK '
    except Exception as expt:
        su_trace.logger.info('Exception message : ' + str(expt))
        mess = 'Write proxy results in database FAILLED, TOOK '
    t5=time.time()
    su_trace.logger.info(mess + str(round((t5-t4),2)) + ' / ' + str(round((t5-t0),2)) + ' sec --')

    # If required write results in a dedicated sheet of the excel file
    if sheet_name != None:
        try:
            io_excel.write_proxy_output_in_excel(output_file_name, 
                    proxy_input['headers'], sheet_name, proxy_output)
            mess = '-- PROXY WRITTEN IN EXCEL FILE, TOOK '
        except Exception as expt:
            su_trace.logger.info('Exception message : ' + str(expt))
            mess = 'Write proxy results in excel file FAILLED, TOOK '
        t6=time.time()
        su_trace.logger.info(mess + str(round((t6-t5),2)) + ' / ' + str(round((t6-t0),2)) + ' sec --')

    su_trace.logger.info('PROXY CALCULATION DONE IN ' + str(round(time.time() - t0,2)) + ' sec')
