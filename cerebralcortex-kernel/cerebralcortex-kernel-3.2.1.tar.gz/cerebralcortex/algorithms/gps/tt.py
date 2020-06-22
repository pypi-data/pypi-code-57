from cerebralcortex.kernel import Kernel
from pyspark.sql import functions as F
from cerebralcortex.algorithms.gps.clustering import cluster_gps, stay_time_graph_in_gps_cluster, impute_gps_data

CC = Kernel("/home/jupyter/cc3_conf/", study_name='rice')

data = CC.get_stream('location--org.md2k.phonesensor--phone')
data_with_day = data.withColumn('day',F.date_format('localtime',"YYYYMMdd"))

# impute GPS data
grouped_data = data_with_day.window(groupByColumnName=['user','version','day'])
imputed_data = impute_gps_data(grouped_data)

# cluster GPS data
grouped_data2 = imputed_data.window(groupByColumnName=['version','day'])
gps_clusters = cluster_gps(grouped_data2)

# extract timebased clusters
grouped_data3 = gps_clusters.window(groupByColumnName=['user','version','day'])
timebased_gps_clusters = stay_time_graph_in_gps_cluster(grouped_data3)
timebased_gps_clusters.show()