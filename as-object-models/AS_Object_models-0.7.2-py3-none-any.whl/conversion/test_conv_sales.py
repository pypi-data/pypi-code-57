import os
import sys
import json

import pandas as pd

plt_cols = ['Poinsettia'
,'Bonita'
,'Singolo'
,'Mini Bromeliad'
,'3" Pothos'
,'3" ZZ'
,'2.5" Kalanchoe'
,'4" Frosty Fern'
,'4" Mini Rose'
,'3" Neantha Bella Palm'
,'2.5" Haworthia'
,'Grande'
,'Succulent'
,'ZZ'
,'Bromeliad'
,'4" Frosty Fern'
,'2.5" Frosty Fern'
,'Bellini'
,'Mini Succulent'
,'Ivy'
,'Anthurium'
,'4" Spathiphyllum'
,'Belita']

def create_plt_entries(row):
  plt_entries = []
  for plant in plt_cols:
    qty = row[plant]
    if qty > 0:
      plt_entries.append({'plant':plant,'qty':qty})
  return plt_entries

with open("../../myfile.txt","w") as file1:
    L = ["This is Delhi \n","This is Paris \n","This is London \n"]
    file1.writelines(L)

df = pd.read_excel('../../item_plants_revised.xlsx',sheet_name='CustomerPlantItem')
df.head()