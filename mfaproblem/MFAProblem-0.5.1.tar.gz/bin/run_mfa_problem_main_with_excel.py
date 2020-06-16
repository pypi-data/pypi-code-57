#!python
import sys
import os
import argparse
import time
import tempfile
from shutil import copyfile
from collections import OrderedDict

import pandas as pd

try:
    from ..mfa_problem import su_trace
    from ..mfa_problem import io_excel
    from ..mfa_problem import mfa_problem_main
except ImportError:
    import mfa_problem.su_trace as su_trace
    import mfa_problem.io_excel as io_excel
    import mfa_problem.mfa_problem_main as mfa_problem_main


def check_args():
    ''' This function controls parameters passed to the program
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file", type=argparse.FileType('r'), 
        help="Input excel file (.xls or .xlsx)"
    )
    parser.add_argument(
        "--output_dir", nargs='*', default="tmp", 
        help="'tmp', 'input' (same as input) or 'path'(full path)"
    )
    helpmsg = "run monte carlo simulation. Arg 1 specify number of realization. "
    helpmsg += "If arg 2 is \'False\' (default - or empty - value is True) simulations results "
    helpmsg += "are not stored in output excel file."
    parser.add_argument(
        "--uncertainty", nargs='*', 
        help=helpmsg
    )
    helpmsg = "downscaling. arg specify *.xlsx file for geographical upper level and (optional) "
    helpmsg += "the name of the geographical upper level"
    parser.add_argument(
        "--downscale", nargs='*', 
        help=helpmsg
    )
    args = parser.parse_args()
    if args.input_file is None:
        su_trace.logger.critical('Pas de fichier d\'input.\n' + parser.format_help())
        return [None, None, None, None, None]
    input_file = args.input_file
    iext = os.path.splitext(input_file.name)[1]
    if iext not in ('.xls', '.xlsx'):
        su_trace.logger.critical('Mauvaise extension pour le fichier d\'input.\n' + 
                parser.format_help())
        return [None, None, None, None, None]
    if type(args.output_dir) != list:
        args.output_dir = [args.output_dir]
    if args.output_dir[0] not in ['tmp','input','path']:
        su_trace.logger.critical("output_dir must be in ['tmp','input','path'] \n" + 
                parser.format_help())
        return [None, None, None, None, None]

    if args.uncertainty != None:
        try:
            if len(args.uncertainty) > 1:
                record_simulations = args.uncertainty[1]
                if not record_simulations in ['True', 'False', '']:
                    su_trace.logger.critical('uncertainty arg2 must be in [\'\', True, False].\n' + 
                            parser.format_help())
                    return [None, None, None, None, None]
        except Exception as expt:
            su_trace.logger.critical('uncertainty number must be an integer.\n' + 
                    parser.format_help())
            su_trace.logger.info('Exception message : ' + str(expt))
            return [None, None, None, None, None]

    if type(args.downscale) != list:
        args.downscale = [args.downscale]

    return [input_file.name, args.output_dir, args.uncertainty, args.downscale]


if __name__ == '__main__':
    t0 = time.time()
    log_file = su_trace.check_log()
    su_trace.run_log(log_file)
    # To change the logger level uncomment following line (see log_level fct for posssible values)
    # su_trace.log_level("DEBUG")

    [excel_input_file, output_dir, args_uncertainty, args_downscale] = check_args()
    upper_level_input_file = None
    upper_level_name = ''
    if args_downscale is not None:
        upper_level_input_file = args_downscale[0]
        if len(args_downscale) > 1:
            upper_level_name = args_downscale[1]
    downscale = upper_level_input_file is not None
    record_simulations = True
    uncertainty = args_uncertainty is not None
    nb_realisations = None
    if uncertainty and len(args_uncertainty) > 1:
        record_simulations = args_uncertainty[1] in ['', 'True']
    if uncertainty:
        nb_realisations = int(args_uncertainty[0])
    if excel_input_file is None:
        sys.exit()
    if output_dir[0] == 'tmp':
        output_directory = tempfile.mkdtemp()
    elif output_dir[0] == 'input':
        output_directory = os.path.dirname(excel_input_file)
    elif output_dir[0] == 'path':
        output_directory = os.path.abspath(output_dir[1])
    else:
        su_trace.logger.critical("output_dir must be in ['tmp','input','path'] \n")
        sys.exit()
    # Log infos about arguments used
    su_trace.logger.info('-- LIST OF ARGUMENTS --')
    su_trace.logger.info(f'> Input file is : {excel_input_file}')
    su_trace.logger.info(f'> Output directory : {output_directory}')
    mess = '> Downscaling : '
    if downscale:
        mess += f'file of upper geographical level is {upper_level_input_file}'
    else:
        mess += 'False'
    su_trace.logger.info(mess)
    mess = '> MonteCarlo : '
    if uncertainty:
        mess += f'number of realization is {nb_realisations}'
        if record_simulations == True:
            mess += ' and simulations data are recorded in output file.'
        else:
            mess += ' and simulations data are NOT recorded in output file.'
    else:
        mess += 'False'
    su_trace.logger.info(mess)
    t1 = time.time()
    su_trace.logger.info('-- INPUT ARGUMENTS CHECKED, TOOK ' + str(round((t1-t0),2)) + ' sec --')

    # 1. load mfa problem input from excel file
    try:
        mfa_problem_input = io_excel.load_mfa_problem_from_excel(excel_input_file)
        su_trace.logger.debug('MFA problem input loaded from excel.')
    except Exception as expt:
        su_trace.logger.critical('Loading Excel file failed.')
        su_trace.logger.info('-- MFA PROBLEM INPUT LOADED FROM EXCEL FAILED, TOOK ' + 
                str(int(time.time() - t0)) +' sec --')
        su_trace.logger.info('Exception message : ' + str(expt))
        sys.exit()
    t2 = time.time()
    su_trace.logger.info('-- MFA PROBLEM INPUT LOADED FROM EXCEL SUCCEEDED, TOOK ' + 
            str(round((t2-t1),2)) + ' / ' + str(round((t2-t0),2)) + ' sec --')

    # 2. Reconciliation
    # 2.1 load geographical upper level results 
    upper_level_solved_vector = None
    upper_level_classification = None
    upper_level_index2name = None
    input_montecarlo_results = None
    if downscale == True:
        if not os.path.isfile(upper_level_input_file):
            upper_level_input_file = os.path.join(output_directory,upper_level_input_file)
            if not os.path.isfile(upper_level_input_file):
                su_trace.logger.critical('Loading geographical upper level excel file failed.')
                su_trace.logger.info('LOADING GEOGRAPHICAL UPPER LEVEL EXCEL FILE FAILED.' + 
                        str(int(time.time()-t0)) + ' sec --')
                sys.exit()
        xls = pd.ExcelFile(upper_level_input_file)
        df_results = pd.read_excel(xls, 'Results')
        if upper_level_name != '':
            # Need to sort df_results to keep only results for the chosen upper geographical level
            mask = df_results['region'] == upper_level_name
            df_results = df_results[mask]
            # Need also to keep only corresponding sectors (between upper and sub geographical 
            # levels) keeping only agrated levels for upper geographical level
            rough_sector_list = [li[1] for li in mfa_problem_input['dim_sectors']] # list of sectors
            sector_list = list(OrderedDict.fromkeys(rough_sector_list)) # list of unique sectors names
            # Be sure to keep only consistant sectors
            mask = df_results['secteur'].isin(sector_list) 
            df_results = df_results[mask]
        upper_level_solved_vector = df_results['valeur out'].to_numpy()
        upper_level_classification = df_results['classif'].to_numpy()
        upper_level_id = df_results[['id','table','produit','secteur','origine',
                'destination']].to_numpy()
        upper_level_index2name = []
        for e in upper_level_id:
            upper_level_index2name.append({'t': e[1], 'o': e[4], 'd': e[5], 'p': e[2], 's': e[3]})
        if uncertainty:
            simulation_results = pd.read_excel(xls, 'Simulations')
            input_montecarlo_results = simulation_results.to_numpy()
        su_trace.logger.debug('Reconciled geographical upper level results loaded')

    t3 = time.time()
    su_trace.logger.info('-- RECONCILED GEOGRAPHICAL UPPER LEVEL LOADED, TOOK ' + 
            str(round((t3-t2), 2)) + ' / ' + str(round((t3-t0),2)) + ' sec --')

    # 2.2 reconciliation
    model_name = os.path.splitext(os.path.basename(excel_input_file))[0]
    mfa_problem_output = mfa_problem_main.optimisation(
        model_name,
        mfa_problem_input,
        uncertainty,nb_realisations,
        downscale,
        upper_level_index2name,upper_level_solved_vector,upper_level_classification,
        input_montecarlo_results, record_simulations=record_simulations
    )
    if mfa_problem_output == None:
        su_trace.logger.critical('Reconciliation failed.')
        su_trace.logger.info('-- RECONCILIATION FAILED, TOOK ' + 
                str(int(time.time() - t0))+ ' sec --')
        sys.exit()

    t4 = time.time()
    su_trace.logger.info('-- RECONCILIATION DONE, TOOK ' + str(round((t4-t3),2)) + ' / ' + 
            str(round((t4-t0),2)) + ' sec --')

    # 3. Writes results to excel
    try:
        root_file_name = os.path.splitext(os.path.basename(excel_input_file))[0]
        output_file_name = os.path.join(output_directory,root_file_name+'_reconciled'+'.xlsx')
        copyfile(excel_input_file, output_file_name)
        su_trace.logger.info('output file is ' + output_file_name)
        io_excel.write_mfa_problem_output_to_excel(
            output_file_name,
            mfa_problem_input,
            mfa_problem_output
        )
    except Exception as expt:
        su_trace.logger.critical('Writing results to excel file failed.')
        su_trace.logger.info('-- WRITE RESULTS TO EXCEL FAILED, TOOK ' + 
                str(int(time.time() - t0)) + ' sec --')
        su_trace.logger.info('Exception message : ' + str(expt))
        sys.exit()

    t5 = time.time()
    su_trace.logger.info('-- WRITE RESULTS TO EXCEL DONE, TOOK ' + str(round((t5-t4),2)) + 
            ' / ' + str(round((t5-t0),2)) + ' sec --')

    su_trace.logger.info('-- OVERALL RECONCILIATION PROCESS FINISHED, TOOK ' + 
            str(round(time.time()-t0,2)) + ' sec --')

