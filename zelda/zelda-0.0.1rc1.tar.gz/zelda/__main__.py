# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: kebo0912@outlook.com
@version: 1.0

@file: __main__.py 
@time: 2020/6/13 下午3:28

这一行开始写关于本文件的说明与解释

"""
import logging
import os
import sys

LEVEL = logging.DEBUG

sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", level=LEVEL)

from zelda.commands import main  # noqa


def run():
    main(program="zelda")


if __name__ == "__main__":
    run()
