import os
import time
import logging, logging.handlers
import tempfile
import psutil

import pandas as pd

logger = logging.getLogger()

def logger_init(logname,mode):
    global logger
    logger = logging.getLogger("sumoptimisation")  #root logger
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)
    hdlr = logging.FileHandler(logname, mode)
    fmt = logging.Formatter("%(levelname)-5s %(message)s", "%x %X")
    hdlr.setFormatter(fmt)
    logger.addHandler(hdlr)

def base_filename():
    return logging.getLogger("sumoptimisation").handlers[0].baseFilename

def run_log(myfile):
    IsNew = not os.path.isfile(myfile) 
    logging.basicConfig(filename=myfile, format='%(asctime)s,%(msecs)03d - %(levelname)-8s - \
%(funcName)-20s (%(lineno)04d): %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    #console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    co_formatter = logging.Formatter('%(funcName)-20s (%(lineno)04d): %(message)s')
    # tell the handler to use this format
    console.setFormatter(co_formatter)
    # add the handler to the root logger
    logging.getLogger().addHandler(console)
    if IsNew:
        strnow = time.strftime('%Y-%m-%d')
        logging.info(f'Log file just created. Date of creation : {strnow}')
    else:
        logging.info('*****************************')
        logging.info('********** New run **********')
        logging.info('*****************************')

def log_level(StrLevel="INFO"):
    '''
    Change the level information of the current logger
    Possible values are (All calls with a higher value than the selected one are logged)
    "NOTSET"(value 0), "DEBUG"(value 10), "INFO"(20), "WARNING"(30), "ERROR"(40), "CRITICAL"(50)
    '''
    switcher = {"NOTSET": 0, "DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "CRITICAL": 50}
    NewLevel = 20
    if StrLevel in switcher:
        NewLevel = switcher[StrLevel]
    logging.getLogger().setLevel(NewLevel)

def check_log(nbmax=20):
    log_def = 'log_' + time.strftime('%Y%m%d') + '.log'
    dir_fi = 'logs' + os.path.sep
    if not os.path.isdir('logs'):
        os.makedirs('logs')
    else:
        li_file = os.listdir('logs')
        df_file = pd.DataFrame(li_file, columns=['files'])
        df_file['date'] = [os.path.getctime(dir_fi + fi) for fi in li_file]
        df_sort = df_file.sort_values(by=['date'], ascending=False)
        if len(df_sort['date'] > nbmax):
            df_del = df_sort['files'][nbmax:]
            for fi in df_del:
                os.remove(dir_fi + fi)
    log_def = dir_fi + log_def
    return log_def

def timems(
    t_input : float,
    f_out = '',
    b_full = False,
):
    if b_full:
        st0 = time.localtime(t_input)
        comp = 0
        if f_out == 'milli':
            comp = int(round((t_input-int(t_input))*1000))
        elif f_out == 'micro':
            comp = int(round((t_input-int(t_input))*1000000))
        return time.strftime(f'%Y-%m-%d %H:%M:%S,{comp}', st0) #return a string
    else:
        if f_out == 'milli':
            comp = int(round(t_input*1000))
        elif f_out == 'micro':
            comp = int(round(t_input*1000000))
        else:
            comp = int(round(t_input)) #time in sec
        return comp #return an integer

def perf_process(procname='python'):
    first_pid_found = False
    procname = procname.lower()
    for proc in psutil.process_iter():
        pname = proc.name().lower()
        if procname in pname :
            if not first_pid_found:
                first_pid_found = True
                pyid = proc.pid
                stproc_id = f'process id is : {pyid}'
            else :
                stproc_id += f', id_add: {proc.pid}'
    #PROCESS INFOS
    ppy = psutil.Process(pyid)
    stproc_inf = f'PROCESS - cpu_percent: {ppy.cpu_percent()}, '
    mem_val = str(round(ppy.memory_percent(),2))
    stproc_inf += f'mem_percent: {mem_val}, '
    ppym = ppy.memory_full_info()
    mem_val = str(round(ppym.uss/1024/1024))
    stproc_inf += f'mem_dedic_PID: {mem_val} Mo, '   
    ppym = psutil.Process().memory_full_info()
    mem_val = str(round(ppym.uss/1024/1024))
    stproc_inf += f'mem_dedic: {mem_val} Mo'   
    sysm = psutil.virtual_memory()
    #SYSTEM INFOS
    stsys_inf = f'SYSTEM - cpu_percent: {psutil.cpu_percent()}, '
    mem_val = str(round(sysm.percent,2))
    stsys_inf += f'mem_percent: {mem_val}, '
    mem_val = str(round(sysm.used/1024/1024))
    stsys_inf += f'mem_used: {mem_val} Mo, '
    mem_val = str(round(sysm.available/1024/1024))
    stsys_inf += f'mem_avail: {mem_val} Mo'
    return [stproc_id, stproc_inf, stsys_inf]