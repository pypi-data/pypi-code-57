# Read Excel documents like Matlab

#wb = 'file.xlsx' # workbook
#ws = 'sheet1' # Pick worksheet from workbook
#cell_tl = 'a20' # Cell - top left
#cell_br = 'c30' # Cell - bottom right

# Ryan Gosselin

import numpy as np
import openpyxl

def xlsread(wb, ws, cell_tl, cell_br):

    wb = openpyxl.load_workbook(wb)
    ws = wb[ws] # Pick worksheet from workbook
    ws = ws[cell_tl:cell_br] 
    
    X = []
    for row in ws:
        for obj in row:
            #print(obj.coordinate, obj.value)
            X.append((obj.value))
    col_count = len(row)
    row_count = len(ws)
    X = np.reshape(X,(row_count,col_count))

    return X