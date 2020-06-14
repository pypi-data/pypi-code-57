from Indexer import Indexer

p1 = Indexer('Cat')
p1.read_csv_file('titanic_train.csv', 1)

p1.nRecords
p1.nAttributes
p1.data.columns
p1.outcomeMetric
p1.outcome 
p1.calculateWOE(10) 