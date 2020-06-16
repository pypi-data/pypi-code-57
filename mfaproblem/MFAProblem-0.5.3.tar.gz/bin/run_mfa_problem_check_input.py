#!python
import sys
import os
import argparse
import tempfile
import time
from shutil import copyfile
import copy
from collections import OrderedDict

try:
    from ..mfa_problem import su_trace
    from ..mfa_problem import io_excel
    from ..mfa_problem import mfa_problem_check_io
except ImportError:
    import mfa_problem.su_trace as su_trace
    import mfa_problem.io_excel as io_excel
    import mfa_problem.mfa_problem_check_io as mfa_problem_check_io


def check_args():
    ''' This function controls parameters passed to the program
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file" , type=argparse.FileType('r'), 
        help="Input excel file (.xls or .xlsx)"
    )
    parser.add_argument(
        "--output_dir" , nargs='*', default="tmp", 
        help="'tmp', 'input' (same as input) or 'path'(full path)"
    )
    parser.add_argument(
        "--merge_with" , 
        help="second excel input file, the two ter1 will be merged into a new one. It is assumed that tab names are the same as the first file."
    )
    args = parser.parse_args()
    if args.input_file == None:
        su_trace.logger.critical('Pas de fichier d\'input.\n' + parser.format_help())
        return [None,None]
    input_file = args.input_file
    if args.merge_with != None:
        merge_with = args.merge_with
    else:
        merge_with=None
    iext = os.path.splitext(input_file.name)[1]
    if iext not in ('.xls', '.xlsx'):
        su_trace.logger.critical('Mauvaise extension pour le fichier d\'input.\n' + parser.format_help())
        return [None,None]
    if type(args.output_dir) != list:
        args.output_dir = [args.output_dir]
    if args.output_dir[0] not in ['tmp','input','path']:
        su_trace.logger.critical("output_dir must be in ['tmp','input','path'] \n" + parser.format_help())
        return [None,None]
    return [input_file.name,args.output_dir,merge_with]

if __name__=='__main__':
    t0=time.time()
    log_file = su_trace.check_log()
    su_trace.run_log(log_file)
    # To change the logger level uncomment following line (see log_level fct for posssible values)
    # su_trace.log_level("DEBUG")

    [excel_input_file,output_dir,merge_with] = check_args()
    if excel_input_file == None:
        sys.exit()
    if output_dir[0] == 'tmp':
        output_directory = tempfile.mkdtemp()
    elif output_dir[0] == 'input':
        output_directory = os.path.dirname(excel_input_file)
    elif output_dir[0] == 'path':
        output_directory = os.path.dirname(output_dir[1])
    else:
        su_trace.logger.critical("output_dir must be in ['tmp','input','path'] \n")
        sys.exit()
    t1 = time.time()
    su_trace.logger.info('-- INPUT ARGUMENTS CHECKED, TOOK ' + str(round((t1-t0),2)) + ' sec --')

    # 1. load mfa problem input from excel file
    su_trace.logger.debug(f'Input file is : {excel_input_file}')
    try:
        mfa_problem_input = io_excel.load_mfa_problem_from_excel(excel_input_file)
        su_trace.logger.debug('MFA problem input loaded from excel.')
    except:
        su_trace.logger.critical('Loading Excel file failed.')
        su_trace.logger.info('-- MFA PROBLEM INPUT LOADED FROM EXCEL FAILED, TOOK ' + str(int(time.time() - t0)) +' sec --')
        sys.exit()
    t2 = time.time()
    su_trace.logger.info('-- MFA PROBLEM INPUT LOADED FROM EXCEL SUCCEEDED, TOOK ' + str(round((t2-t1),2)) + ' / ' + str(round((t2-t0),2)) + ' sec --')

    # 2. Check mfa problem input
    # 2.1
    try:
        [input_ter,ter1_dict, js1_di] = mfa_problem_check_io.check_input_file(
            mfa_problem_input
        )
    except:
        su_trace.logger.info('exception caught')
    # 2.2
    if merge_with != None:
        [input_ter2,ter2_dict, js2_di] = mfa_problem_check_io.check_input_file(
            merge_with
        )
        names1_p = ter1_dict['s'].keys()
        nb1_p = len(names1_p) # number of products (rows) in ter1 of file 1
        for p in names1_p:
            names1_s = ter1_dict['s'][p].keys()
            nb1_s = len(names1_s) # number of sectors (columns) in ter1 of file 1
            break
        ter3_dict = copy.deepcopy(ter1_dict)
        names3_p = list(names1_p)
        names3_s = list(names1_s)
        output_ter3 = {}
        for t in ter2_dict.keys():
            output_ter3[t] = {}
            for i,p in enumerate(ter2_dict[t]):
                if p not in names1_p:
                    ter3_dict[t][p] = OrderedDict()
                    names3_p.append(p)
                if i not in output_ter3[t].keys():
                    output_ter3[t][i] = {}
                for j,s in enumerate(ter2_dict[t][p]):
                    try: # product and sector exist in file 1
                        if ter3_dict[t][p][s] == 0 and ter2_dict[t][p][s] == 1: # else do nothing
                            su_trace.logger.info('tab. {}, prod. {}, sect. {}, from 0 (file 1) to 1 (file 2)'.format(t,p,s))
                    except:
                        ter3_dict[t][p][s] = ter2_dict[t][p][s]
                    if s not in names3_s:
                        names3_s.append(s)
                    output_ter3[t][i][j] = ter3_dict[t][p][s]
        su_trace.logger.info('Merged TER successfully written to Excel sheet.')

    # 3.  Writes results to excel
    try:
        root_file_name = os.path.splitext(os.path.basename(excel_input_file))[0]
        output_file_name = os.path.join(output_directory,root_file_name+'_reconciled'+'.xlsx')
        copyfile(excel_input_file, output_file_name)
        su_trace.logger.info('output file is ' + output_file_name)
        io_excel.write_mfa_problem_output_to_excel(
            output_file_name,
            mfa_problem_input,
            mfa_problem_input
        )
    except:
        su_trace.logger.critical('Writing results to excel file failed.')
        su_trace.logger.info('-- WRITE RESULTS TO EXCEL FAILED, TOOK ' + str(int(time.time() - t0)) + ' sec --')
        sys.exit()

    t5 = time.time()
    su_trace.logger.info('-- WRITE RESULTS TO EXCEL DONE, TOOK ' + str(round((t5-t4),2)) + ' / ' + str(round((t5-t0),2)) + ' sec --')

    su_trace.logger.info('-- OVERALL RECONCILIATION PROCESS FINISHED, TOOK ' + str(round(time.time()-t0,2)) + ' sec --')