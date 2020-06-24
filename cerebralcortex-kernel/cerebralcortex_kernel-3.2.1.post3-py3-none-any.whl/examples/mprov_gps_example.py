import os
from cerebralcortex.test_suite.util.data_helper import gen_location_datastream
from cerebralcortex.algorithms.gps.clustering import cluster_gps

from pennprov.connection.mprov_connection import MProvConnection

conn = MProvConnection('ali', 'ali', host='http://localhost:8088')
conn.create_or_reset_graph()

os.environ["MPROV_USER"] = "ali"
os.environ["MPROV_PASSWORD"] = "ali"

ds_gps = gen_location_datastream(user_id="bfb2ca0c-e19c-3956-9db2-5459ccadd40c", stream_name="gps--org.md2k.phonesensor--phone")

d2=ds_gps.window(windowDuration=60)
dd=cluster_gps(d2)
dd.show()