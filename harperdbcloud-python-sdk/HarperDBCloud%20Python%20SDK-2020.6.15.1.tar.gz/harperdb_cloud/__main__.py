#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Xonshiz
Github: https://github.com/Xonshiz/HarperDBCloud-Python
"""

import sys

import harperdb_cloud

if __name__ == "__main__":
    harperdb_cloud.HarperDbCloud(sys.argv[1:], instance_url="https://sdktest-xonshiz.harperdbcloud.com/", username="test_user", password="GuessMe24!")

