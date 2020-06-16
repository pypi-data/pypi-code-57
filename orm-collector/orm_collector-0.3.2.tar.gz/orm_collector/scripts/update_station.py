from collector.orm.manager import SessionCollector
from pathlib import Path
import csv

pwd = str(Path(__file__).resolve().parent)

file_station=pwd+'/fixtures/updpos.csv'
s=SessionCollector()
this_protocol=dict()

with open(file_station, 'r') as rfile:
    reader = csv.DictReader(rfile, delimiter=';', quoting=csv.QUOTE_NONE)
    for row in reader:
        ids=None
        station=None
        print(row)
        code=row['code']
        ids=s.get_station_id(code)
        station=s.get_station_by_id(ids)
        print("IDS %s STATION: %s" % (ids,station))
        if ids and station:
            print("Nueva actualizacion station")
            print(station)
            print(row)
            s.update_station(station,row)
