import os
import sys
import glob

import pandas as pd

name = sys.argv[1] + ".xlsx"
writer = pd.ExcelWriter(name, engine='xlsxwriter')

user_input = input("Enter the path of directory which contains files: ")
if os.path.isdir(user_input):
    os.chdir(user_input)
else:
    print("Directory does not exists.")

csv_sheets = []
xlsx_sheets = []

def get_csv_df(files):
    for file in files:
        csv_sheets.append(str(file))
        yield pd.read_csv(file)


def get_xlsx_df(files):
    for file in files:
        xlsx_sheets.append(str(file))
        yield pd.read_excel(file)

def main():
    csv_files = glob.glob('*.csv')
    xlsx_files = glob.glob('*.xls')
    xlsx_files.extend(glob.glob('*.xlsx'))

    df_for_each_csv_file = get_csv_df(csv_files)
    df_for_each_xlsx_file = get_xlsx_df(xlsx_files)

    for idx, df in enumerate(df_for_each_csv_file):
        df.to_excel(writer, sheet_name='{0}'.format(csv_sheets[idx]))

    for idx, df in enumerate(df_for_each_xlsx_file):
        df.to_excel(writer, sheet_name='{0}'.format(xlsx_sheets[idx]))

    writer.save()
