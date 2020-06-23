"""Miscellaneous tools"""
import platform
from plumbum import local

def run_script(vivado_script):
    exec_name = "vivado_hls.exe" if platform.system() == 'Windows' else "vivado_hls" 
    vivado_hls = local[exec_name]
    vivado_hls(str(vivado_script))
