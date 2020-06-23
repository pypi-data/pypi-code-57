import argparse
from typing import List


class Arg:
    """
    参数
    """
    def __init__(self, name, flags, help, default=None, required=False):
        self.name = name
        self.flags = flags
        self.help = help
        self.default = default
        self.required = required


class Args:
    """
    参数集
    """
    def __init__(self, args: List[Arg], name, desc=''):
        self.args = args
        self.name = name
        self.desc = desc

    def parse(self):
        """
        解析控制台输入的参数
        :return:
        """
        parser = argparse.ArgumentParser(prog=self.name, description=self.desc)

        for arg in self.args:
            parser.add_argument(arg.name, arg.flags, help=arg.help, default=arg.default, required=arg.required)

        return parser.parse_args()


if __name__ == '__main__':
    args = Args(
        name='args-demo',
        args=[
            Arg('-c', '--config', '配置文件路径', 'config.yaml'),
            Arg('-f', '--file', 'csv文件路径', required=True),
        ],
        desc='Args Demo desc'
    )

    args.parse()
