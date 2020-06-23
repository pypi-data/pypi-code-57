import sqlite3

import pandas as pd

with sqlite3.connect("stats.sqlite3") as conn:
    df = pd.read_sql("select * from data", conn)

with sqlite3.connect("temp/stats.sqlite3") as conn:
    df2 = pd.read_sql("select * from data", conn)

print(df.head())
print(df2.head())
print(df.tail())
print(df2.tail())
print(df.equals(df2))
