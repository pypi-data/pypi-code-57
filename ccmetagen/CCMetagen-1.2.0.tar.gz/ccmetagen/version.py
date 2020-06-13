"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

major = 1
minor = 2
micro = 0
revision = None

def get_version():
  if revision:
    return "{}.{}.{}+{}".format(major, minor, micro, revision)
  return "{}.{}.{}".format(major, minor, micro)
