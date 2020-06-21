from antiplagiat import Antiplagiat
from antiplagiat.helpers import domain_rule, url_rule

import json
import os
import pytest
import time


TOKEN = os.getenv('ADVEGO_TOKEN')


with open('func_tests/text.txt', 'r') as fp:
	text = fp.read()

# @pytest.mark.skip(reason="no way of currently testing this")
# def test_unique_text_add():
# 	response = api.unique_text_add(text)
# 	print(response)


# def test_unique_check():
# 	key = '13029708'
# 	result = api.unique_check(key)
# 	with open('report.json', 'w') as fp:
# 		json.dump(result, fp, ensure_ascii=False, indent=4)


def test_checking_text():
	"""
	Тест на успешную проверку.
	"""
	api = Antiplagiat(TOKEN)
	res = api.unique_text_add(text)
	key = res['key']
	while True:
		time.sleep(200)
		result = api.unique_check(key)
		if result['status'] == 'done':
			print('Done!')
			with open('report.json', 'w') as fp:
				json.dump(result, fp, ensure_ascii=False, indent=4)
			break
		elif result['status'] == 'error':
			print(f'Error: {result}')
			return
		elif result['status'] == 'not found':
			print('Not found!')
			return
		else:
			print('In progress...')
			print(result)

	import pdb; pdb.set_trace()