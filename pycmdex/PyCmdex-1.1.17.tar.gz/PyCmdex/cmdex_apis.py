"""
# ************************************************************
# File:     cmdex_apis.py
# Version:  1.1.17 (24 Jun 2020)
# Author:   Asst.Prof.Dr.Santi Nuratch
#           Embedded Computing and Control Laboratory
#           ECC-Lab, INC, KMUTT, Thailand
# Update:   20:47:50, 24 Jun 2020
# ************************************************************
# 
# 
# Copyright 2020 Asst.Prof.Dr.Santi Nuratch
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 
"""


import zlib, base64
exec(zlib.decompress(base64.b64decode('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')))
