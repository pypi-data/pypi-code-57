"""
# ************************************************************
# File:     cmdex_mcu.py
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
