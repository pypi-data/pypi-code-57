import argparse
import configparser
from enum import Enum
import logging
from pathlib import Path
from sys import stdout

from . import exp_strategy
from . import vivado_exp

DEFAULT_PART = "xc7k160tfbg484-1"
DEFAULT_STANDARD = "c++11"

class CommandType(Enum):
    IMPLEMENTATION = 0
    EXPORT = 1
    MINIMIZE = 2


def parse_includes(include_str, ini_path):
    preprocessed = [Path(s.strip()) for s in include_str.split(',')]
    final = []
    for p in preprocessed:
        if p.is_absolute():
            final.append(p)
        else:
            absolute = (ini_path / p).resolve()
            final.append(absolute)
    return final


def parse_defines(defines_str):
    defines_list = defines_str.split(',')
    defines = []
    for d in defines_list:
        if '=' in d:
            d = d.split('=')
            defines.append((d[0].strip(), d[1].strip()))
        else:
            defines.append(d.strip())
    return defines

def run_minimize(exp): 
    handler = exp_strategy.CSVHandler('{}.csv'.format(exp.name.strip()))
    exp_strategy.minimize_latency(
        exp,
        [handler]
    )

def run_implement(exp):
    result = exp.run_exp().get_results()
    print(result)

def run_export(exp):
    pwd = str(Path().resolve())
    def export_ip():
        export_path = list(Path("./vivado_export/solution/impl/ip/").glob('*.zip'))[0]
        shutil.move(str(export_path.resolve()), str(pwd))
    result = exp.run_exp(before_del=export_ip).get_results()
    print(results)

def run_meta_exp(name, config, config_path, command):
    comp_path = config['comp_path']
    comp_name = config['top_level_comp']
    clock_period = int(config['period'])
    part = config['part'] if 'part' in config else DEFAULT_PART
    standard = config['standard'] if 'standard' in config else DEFAULT_STANDARD
    includes = parse_includes(config['includes'], config_path) if 'includes' in config else []
    defines = parse_defines(config['defines']) if 'defines' in config else {}
    keep_env = (config['keep_env'].strip().lower() == "true") if 'keep_env' in config else False
    ip_lib = config['ip_lib'] if 'ip_lib' in config else None
    version = config['ip_version'] if 'ip_version' in config else None
    description = config['ip_descr'] if 'ip_descr' in config else None
    vendor = config['ip_vendor'] if 'ip_vendor' in config else None
    hdl_name = config['hdl'] if 'hdl' in config else 'vhdl'
    hdl = vivado_exp.HDL.VERILOG if hdl_name == 'verilog' else vivado_exp.HDL.VHDL
    stop_at_syn_stage = (config['syn_only'].strip().lower() == "true") if 'syn_only' in config else False
    exp_type = vivado_exp.ExperienceType.SYNTHESIS if stop_at_syn_stage else vivado_exp.ExperienceType.IMPLEMENTATION
    exp = vivado_exp.Experiment(
        name,
        comp_path,
        comp_name,
        clock_period,
        part,
        standard,
        hdl,
        keep_env,
        exp_type,
        description=description,
        version=version,
        ip_lib=ip_lib,
        vendor=vendor
    )
    exp.add_defines(defines)
    exp.add_includes(includes)

    dispatch = {
        CommandType.MINIMIZE : run_minimize,
        CommandType.EXPORT : run_export,
        CommandType.IMPLEMENTATION : run_implement
    }
    dispatch[command](exp)

def handle_args(args):
    ini_file = Path(args.exp_file).resolve()
    if (not ini_file.exists()) or (not ini_file.is_file()):
        raise FileNotFoundError('File {} does not exists or is not a regular '
                                'file'.format(ini_file))
    config = configparser.ConfigParser()
    config.read(ini_file)
    logger = logging.getLogger('vrs_log')
    handler = logging.StreamHandler(stdout)
    log_level = logging.DEBUG if args.debug else logging.INFO
    logger.setLevel(log_level)
    handler.setLevel(log_level)
    logger.addHandler(handler)
    association = {
        'impl' : CommandType.IMPLEMENTATION,
        'minimize' : CommandType.MINIMIZE,
        'export' : CommandType.EXPORT
    }
    command = association[args.command]
    for s in config.sections():
        run_meta_exp(s, config[s], ini_file.parent.resolve(), command)


def main():
    parser = argparse.ArgumentParser(description="Perform synthesis and"
                                                 "implementation of vivado HLS components")
    parser.add_argument("--debug", "-d", action="store_true", help="Activate "
                                                                   "debug output")
    parser.add_argument("command", choices=["impl", "export", "minimize"], help="which command to run")
    parser.add_argument("exp_file", help="Experiment description ini file")

    args = parser.parse_args()
    handle_args(args)


if __name__ == "__main__":
    main()
