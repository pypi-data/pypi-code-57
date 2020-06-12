import argparse
import os
import pathlib
import datetime
from string import Template

import sys

APP_DEC = """                                                                           
YYYYYYY       YYYYYYY          QQQQQQQQQ           NNNNNNNN        NNNNNNNN
Y:::::Y       Y:::::Y        QQ:::::::::QQ         N:::::::N       N::::::N
Y:::::Y       Y:::::Y      QQ:::::::::::::QQ       N::::::::N      N::::::N
Y::::::Y     Y::::::Y     Q:::::::QQQ:::::::Q      N:::::::::N     N::::::N
YYY:::::Y   Y:::::YYY     Q::::::O   Q::::::Q      N::::::::::N    N::::::N
   Y:::::Y Y:::::Y        Q:::::O     Q:::::Q      N:::::::::::N   N::::::N
    Y:::::Y:::::Y         Q:::::O     Q:::::Q      N:::::::N::::N  N::::::N
     Y:::::::::Y          Q:::::O     Q:::::Q      N::::::N N::::N N::::::N
      Y:::::::Y           Q:::::O     Q:::::Q      N::::::N  N::::N:::::::N
       Y:::::Y            Q:::::O     Q:::::Q      N::::::N   N:::::::::::N
       Y:::::Y            Q:::::O  QQQQ:::::Q      N::::::N    N::::::::::N
       Y:::::Y            Q::::::O Q::::::::Q      N::::::N     N:::::::::N
       Y:::::Y            Q:::::::QQ::::::::Q      N::::::N      N::::::::N
    YYYY:::::YYYY          QQ::::::::::::::Q       N::::::N       N:::::::N
    Y:::::::::::Y            QQ:::::::::::Q        N::::::N        N::::::N
    YYYYYYYYYYYYY              QQQQQQQQ::::QQ      NNNNNNNN         NNNNNNN
                                       Q:::::Q                             
                                        QQQQQQ                             
                                                                           
"""

templates = {
    'config': [
        'template_config$cfg',
        'template_config$py',
    ],
    'infer': [
        'template_infer$py',
    ],
    'model': [
        'template_model$py',
    ],
    'train': [
        'template_acc$py',
        'template_dataset$py',
        'template_engine$py',
        'template_loss$py',
        'template_train$py',
    ],
}


def capitalize(name):
    return name.capitalize()


def get_args_parser():
    from yqn_cli import __version__
    parser = argparse.ArgumentParser(description='create module base on yqn pytorch framework')
    parser.add_argument('-version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-name', type=str, default='*', help='module name exp: "key_attention"')
    parser.add_argument('-out', type=str, default='./', help='file output path')
    parser.add_argument('-author', type=str, default='yqn', help='author')
    return parser


def get_name_for_class(module_name):
    return ''.join(list(map(capitalize, module_name.split('_'))))


def create_dirs(module_name, output_dir):
    pathlib.Path(os.path.join(output_dir,
                              module_name,
                              "config")).mkdir(parents=True, exist_ok=True)
    pathlib.Path(os.path.join(output_dir,
                              module_name,
                              "train")).mkdir(parents=True, exist_ok=True)
    pathlib.Path(os.path.join(output_dir,
                              module_name,
                              "model")).mkdir(parents=True, exist_ok=True)
    pathlib.Path(os.path.join(output_dir,
                              module_name,
                              "infer")).mkdir(parents=True, exist_ok=True)


def output_gen_files(args, class_name, template_dir):
    module_name, output_dir, author = args.name, args.out, args.author
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for sub_dir in templates:
        files = templates[sub_dir]
        for file in files:
            lines = []
            template_file_path = os.path.join(template_dir,
                                              sub_dir,
                                              file)
            if sub_dir == 'config':
                out_name = file.replace("template_", module_name + "_").replace("$", ".")
            else:
                out_name = file.replace("template_",
                                        "pytorch_" + module_name + "_").replace("$", ".")
            gen_file_path = os.path.join(output_dir,
                                         module_name,
                                         sub_dir,
                                         out_name)
            template_file = open(template_file_path)
            gen_file = open(gen_file_path, "w")
            tmp = Template(template_file.read())
            lines.append(tmp.safe_substitute(class_name=class_name, module_name=module_name))
            gen_file.writelines(lines)
            template_file.close()
            gen_file.close()


def parse_command(parser_fn=get_args_parser, printed=True):
    root_project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 项目次目录
    module_dir = os.path.join(root_project_dir, "yqn_cli")
    print(module_dir)
    template_dir = os.path.join(module_dir, 'template')
    args = parser_fn().parse_args()
    if printed:
        param_str = '\n'.join(['%20s = %s' % (k, v) for k, v in sorted(vars(args).items())])
        print('usage: %s\n%20s   %s\n%s\n%s\n' % (' '.join(sys.argv), 'ARG', 'VALUE', '_' * 50, param_str))
    create_dirs(args.name, args.out)
    class_name = get_name_for_class(args.name)
    output_gen_files(args, class_name, template_dir)


def main():
    print(APP_DEC)
    parse_command()


if __name__ == "__main__":
    main()
