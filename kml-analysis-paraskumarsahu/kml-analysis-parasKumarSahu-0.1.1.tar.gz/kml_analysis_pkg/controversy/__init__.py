import xml.etree.ElementTree as ET
import xml.dom.minidom
import re
import difflib
import collections
import sys

wiki_link_dict = collections.defaultdict(lambda: 0)

def analyze(s, s2, num):
	print("Checking Revisison", num, "...")

	d = difflib.Differ()
	result = list(d.compare(s, s2))

	i = 0
	while(True):
		if i == len(result):
			break;
		if result[i][0] == '?':
			del result[i]
		else:	
			i += 1	

	#print(result)
	boolPos = False
	boolNeg = False
	start = 0
	end = 0
	delimiters = ['.', '?', '!']
	sentenceDict = {}
	line_no = 1

	for x in result:
		if x[0] == '+':
			boolPos = True
		if x[0] == '-':
			boolNeg = True
		if x[-1] in delimiters or x == result[-1]:
			if boolNeg:
				sentance = ""
				for i in range(start, end):
					sentance += result[i]+" "
				if x != result[-1]:
					sentance += result[end]+" "
				sentenceDict[line_no] = sentance 
			line_no += 1
			start = end+1
			boolPos = boolNeg = False
		#print(end, boolPos, boolNeg)
		end += 1

	for x in sentenceDict:
		elements = sentenceDict[x]
		#print("No:", x, "Line:", re.findall(r'\*?\[\[[^\]]*\]\]', elements))
		elements = re.findall(r'\*?\[\[[^\]]*\]\]', elements)
		for y in elements:
			wiki_link_dict[y] += 1/(len(elements))


def run(file_name):
	tree = ET.parse(file_name)
	root = tree.getroot()
	last_rev = ""
	count = 0
	length = len(root[0].findall('Instance'))

	revisionsList = []

	for each in root.iter('Instance'):
		instanceId = int(each.attrib['Id'])
		for child in each:
			if 'Body' in child.tag:
				revision = child[0].text
				revision = re.sub(r'\*?\{\{[^\}]*\}\}', "", revision)
				#[[]] can is a wikilink
				#revision = re.sub(r'\*?\[\[[^\]]*\]\]', "", revision)
				revision = ' '.join(revision.split())
				#print(revision)
				#print()
				revisionsList.append(revision)

	#List of all revisions			
	#print(revisionsList)

	#Sentence Number, modified sentence
	for i in range(1, len(revisionsList)):
		analyze(revisionsList[i-1].split(), revisionsList[i].split(), i+1)

	print("\n\n======Ranking based on controversy==========\n\n")

	for x in sorted(wiki_link_dict.items() ,  key=lambda x: x[1]):
		print(x[0], "\n--->", x[1])
		