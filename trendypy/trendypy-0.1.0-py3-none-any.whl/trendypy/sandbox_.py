'''

find trendypy -name Icon? -delete

'''
import sys
sys.path.append('../')
import matplotlib.pyplot as plt
import pandas as pd
from trendy import Trendy
import algos
import utils
import time
import pickle


import json
import pymysql
path = '../../stock_prediction_v2'
sys.path.append(path)
from StockDB import StockDB
env = json.loads(open(path+'/env.json', 'r').read())
conn = pymysql.connect(
	host=env['host'], database=env['db'], 
	user=env['user'], password=env['pw'])
db = StockDB(conn, env['api_key'])

out = pd.DataFrame()
ticks = ['AAPL', 'FB', 'GOOGL', 'AMZN']
ticks += ['BAC', 'WFC', 'c']
X = []
for t in ticks:
	df = db.select_table(t, start='2018-01-01', end=None)
	tmp = df[['open']]
	tmp.columns = [t]
	out = pd.concat([out, tmp], axis=1)
	x = df.open.tolist()
	x = utils.scale_01(x)
	X.append(x)

out = out[:-1]
out.to_csv('stock_data.csv', index=False)

to_fit = X#[3:]
to_test = [to_fit.pop(0), to_fit.pop(-1)]

# 
t = Trendy(n_clusters=2)
start = time.time()
t.fit(to_fit)
# pkl_file = open('asd.pkl', 'rb')
# t = pickle.load(pkl_file)
# pkl_file.close()
# t.to_pickle('asd.pkl')
print('fit in '+str(time.time()-start))
print(t.labels_)

start = time.time()
print(t.predict(to_test))
print('predict in '+str(time.time()-start))

for i, x in enumerate(to_fit):
	plt.plot(range(len(x)), x, label=i+1)
plt.legend(loc="upper left")
plt.show()

conn.close()