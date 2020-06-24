#!/usr/bin/env python3
# coding: utf-8

'''
DBLIB for Bairong Data Tech.
easy run ~

'''
__version__ = "1.0.3"
__date__ = "20200624"
__welcome__ = '''
  .--,       .--,
 ( (  \.---./  ) )
  '.__/o   o\__.'
     {=  ^  =}
      >  -  <
     /       \
    //       \\
   //|   .   |\\
   "'\       /'"_.-~^`'-.
      \  _  /--'         `
    ___)( )(___
   (((__) (__)))   不积小流，无以成江海!
'''


from b_i.utils.hive_handle import hiveClient
from b_i.utils.mysql_handle import mysqlClient

from b_i.config.setting import MYSQL_URI, HIVE_URI

hive_client = hiveClient()
mysql_client = mysqlClient()



if __name__ == "__main__":
    pass