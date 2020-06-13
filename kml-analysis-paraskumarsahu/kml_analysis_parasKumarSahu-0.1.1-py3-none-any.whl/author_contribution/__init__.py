import xml.etree.ElementTree as ET
import xml.dom.minidom
import re
import difflib
import collections
from datetime import datetime
import sys

author_contribution = collections.defaultdict(lambda: [])


def run(file_name, date1, date2, measure):
	d1 = datetime.strptime(date1, '%Y-%m-%d')
	d2 = datetime.strptime(date2, '%Y-%m-%d')

	tree = ET.parse(file_name)
	root = tree.getroot()
	last_rev = ""
	count = 0
	length = len(root[0].findall('Instance'))

	revisionsList = []

	last_contribution = 0

	for each in root.iter('Instance'):
		instanceId = int(each.attrib['Id'])
		dict_key = 0
		dict_val = 0
		for child in each:
			if 'TimeStamp' in child.tag:
				contr_date = datetime.strptime(child[0].text.split("T")[0], '%Y-%m-%d')
				if d1 > contr_date or d2 < contr_date:
					break 
			if 'Contributors' in child.tag:
				dict_key = revision = child[0].text
			if 'Body' in child.tag:
				dict_val = 0
				if measure == "sentences":
					dict_val = len(re.split('\!|\?|\.', child[0].text))
				elif measure == "wikilinks":
					dict_val = len(re.findall(r'\*?\[\[[^\]]*\]\]', child[0].text))
				elif measure == "bytes":
					dict_val = len(child[0].text.encode('utf-16-le'))
				elif measure == "words":
					dict_val = len(child[0].text.split())
				else:
					dict_val = len(child[0].text.split())
				#print(dict_key)
				#print(dict_val)	
				author_contribution[dict_key].append(dict_val-last_contribution)
				last_contribution = dict_val


	print("\n\n======Authors' Contribution==========\n\n")
	'''
	for x in sorted(author_contribution.items() ,  key=lambda x: x[1]):
		print(x[0], "\n--->", x[1])
	'''
	for x in author_contribution.items():
		print(x[0], "\n--->", x[1])
