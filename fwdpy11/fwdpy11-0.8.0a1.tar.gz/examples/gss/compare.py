import sqlite3

import pandas as pd

with sqlite3.connect("stats.sqlite3") as conn:
    df = pd.read_sql("select * from data", conn)
with sqlite3.connect("master/stats.sqlite3") as conn:
    df2 = pd.read_sql("select * from data", conn)

print(df.equals(df2))
