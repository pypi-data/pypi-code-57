
import hashlib
import json

import boto3

import pandas as pd

from db import get_kxy_db_engine

if __name__ == '__main__':
	# boto3.setup_default_session(profile_name='kxy')
	# s3 = boto3.resource('s3')
	# bucket = 'api.kxysolutions.com'

	# engine = get_kxy_db_engine()
	# entropies = pd.read_sql('select * from rv_copula_entropy_all where d =2 limit 1;', engine)
	# entropies = entropies.to_dict(orient='records')

	# for e in entropies:
	# 	ordered_top_corr = e['ordered_spearman_corr_matrix']
	# 	d = e['d']
	# 	key = json.dumps(ordered_top_corr)
	# 	md5_key = hashlib.md5(str(key).encode()).hexdigest()
	# 	key = 'core/dependence/copula/maximum-entropy/entropy/all/d=%d/%s.json' % (d, md5_key)
	# 	print(ordered_top_corr, key)
	# 	# obj = s3.Object(bucket, key)
	# 	# data = {'mean_entropy': e['mean_entropy'], 'median_entropy': e['median_entropy'], \
	# 	# 	'count': e['count'], 'entropy_std_err': e['entropy_std_err'], \
	# 	# 	'ordered_spearman_corr_matrix': ordered_top_corr}
	# 	# obj.put(Body=json.dumps(data))


	# ordered_corr = {0: ['1.0', '0.100'], 1: ['0.100', '1.0']}

	# from db import get_session_factory, CopulaEntropyModel
	# session_factory = get_session_factory()
	# db_session = session_factory()
	# entropy = db_session.query(CopulaEntropyModel).filter_by(\
	# 	ordered_spearman_corr_matrix=ordered_corr).first()
	# if entropy:
	# 	print(float(entropy.median_entropy))


	from db import get_kxy_db_engine

	engine = get_kxy_db_engine()
	engine.execute('refresh materialized view rv_copula_entropy_all;')