from antiplagiat.helpers import AdvanceReport

import json


with open('tests/data/sample_text.txt', 'r') as fp:
	text = fp.read()

with open('tests/data/sample_report.json', 'r') as fp:
	data = json.load(fp)
	report_data = data.get('report')



adv_report = AdvanceReport(report_data, text)


print(f'уникальность текста {adv_report.uniqueness}/{adv_report.originality}')

print('Найденные источники:')
for domain in adv_report.layers_by_domain:
    for layer in domain.layers:
        print(layer.uri)
