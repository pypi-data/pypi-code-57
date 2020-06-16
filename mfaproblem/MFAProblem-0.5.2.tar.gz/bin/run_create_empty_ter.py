#!python
import sys
import os
import argparse
import time
import tempfile
from shutil import copyfile

try:
    from ..mfa_problem import su_trace
    from ..mfa_problem import io_excel
    from ..mfa_problem import mfa_problem_format_io
except ImportError:
    import mfa_problem.su_trace as su_trace
    import mfa_problem.io_excel as io_excel
    import mfa_problem.mfa_problem_format_io as mfa_problem_format_io


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
    args = parser.parse_args()
    if args.input_file == None:
        su_trace.logger.critical('Pas de fichier d\'input.\n' + parser.format_help())
        return [None,None]
    input_file = args.input_file
    iext = os.path.splitext(input_file.name)[1]
    if iext not in ('.xls', '.xlsx'):
        su_trace.logger.critical('Mauvaise extension pour le fichier d\'input.\n' + parser.format_help())
        return [None,None]
    if type(args.output_dir) != list:
        args.output_dir = [args.output_dir]
    if args.output_dir[0] not in ['tmp','input','path']:
        su_trace.logger.critical("output_dir must be in ['tmp','input','path'] \n" + parser.format_help())
        return [None,None]
    return [input_file.name,args.output_dir]

if __name__=='__main__':
    t0=time.time()
    log_file = su_trace.check_log()
    su_trace.run_log(log_file)
    # To change the logger level uncomment following line (see log_level fct for posssible values)
    # su_trace.log_level("DEBUG")

    [excel_input_file,output_dir] = check_args()
    if excel_input_file == None:
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
    t1 = time.time()
    su_trace.logger.info('-- INPUT ARGUMENTS CHECKED, TOOK ' + str(round((t1-t0),2)) + ' sec --')

    # 1. load mfa problem input from excel file
    su_trace.logger.debug(f'Input file is : {excel_input_file}')
    try:
        mfa_problem_input = io_excel.load_mfa_problem_from_excel(excel_input_file, True)
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

    # 2. Creates TER
    mfa_problem_output = {}
    ter = mfa_problem_format_io.create_empty_ter(mfa_problem_input)
    mfa_problem_output['flux pouvant exister'] = ter
    t3 = time.time()
    su_trace.logger.info('-- TER CREATED, TOOK ' + str(round((t3-t2),2)) + ' / ' + str(round((t3-t0),2)) + ' sec --')

    # 3. writes results to excel
    try:
        root_file_name = os.path.splitext(os.path.basename(excel_input_file))[0]
        output_file_name = os.path.join(output_directory,root_file_name+'_empty_ter'+'.xlsx')
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

    t4 = time.time()
    su_trace.logger.info('-- WRITE RESULTS TO EXCEL DONE, TOOK ' + str(round((t4-t3),2)) + ' / ' + str(round((t4-t0),2)) + ' sec --')

    su_trace.logger.info('-- OVERALL TER CREATION PROCESS FINISHED, TOOK ' + str(round(time.time()-t0,2)) + ' sec --')