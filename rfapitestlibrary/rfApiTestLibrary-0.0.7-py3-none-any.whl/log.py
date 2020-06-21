'''
Documentation: 对日志处理的
robot framework robot.api.logger API封装。
引用包名是atApiBasicLibrary，引用本python文件，请使用Library  atApiBasicLibrary/atLogge.py.
'''
from robot.api import logger

def trace(msg, html=False):
    '''
    trace日志
   【msg】: 需要打印的消息。String类型。
   【html】: 是否打印在报告html上，boolean类型。默认是false
    '''
    logger.trace(msg, html=html)

def debug(msg, html=False):
    '''
    debug日志.
   【msg】: 需要打印的消息。String类型。
   【html】: 是否打印在报告html上，boolean类型。默认是false
    '''
    logger.debug(msg, html=html)

def info(msg,html=False, also_console=False):
    '''
    info日志.
   【msg】: 需要打印的消息。String类型。
   【html】: 是否打印在报告html上，boolean类型。默认是false
   【also_console】: 是否打印在报告console上，boolean类型。默认是false
    '''
    logger.info(msg, html=html, also_console=also_console)

def warn(msg, html=False):
    '''
    warn日志.会在console里自动打开。
   【msg】: 需要打印的消息。String类型。
   【html】: 是否打印在报告html上，boolean类型。默认是false
    '''
    logger.warn(msg, html=html)

def error(msg, html=False):
    '''
    error日志.会在console里自动打开。
   【msg】: 需要打印的消息。String类型。
   【html】: 是否打印在报告html上，boolean类型。默认是false
    '''
    logger.error(msg, html=html)
