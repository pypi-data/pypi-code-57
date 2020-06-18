from pypinyin import pinyin, Style, load_phrases_dict
import os

def _pinyinformat(txt):
	'''format pinyin to mtts's format'''
	pinyin_list = pinyin(txt, style=Style.TONE3)
	res = []
	for i in pinyin_list:
		syllable = i[0]
		if not syllable[-1].isdigit():
			syllable = syllable + '0'  # Dacidian format
		assert syllable[-1].isdigit()
		res.append(syllable)
	RES = []
	for i in res:
		RES.append(i[:-1].upper()+'_' + i[-1])
	return RES

def syl2ph_dict():
	syllable_to_phones={}
	filename = os.path.join(os.path.dirname(__file__), 'pinyin_to_phone.txt')
	with open(filename,'r', encoding='utf-8') as fi:
		for l in fi.readlines():  # "ZHENG	zh eng"
			cols = l.strip().split('\t')
			assert(len(cols) == 2)
			syllable = cols[0]
			phones = cols[1].split()
			syllable_to_phones[syllable] = phones
	return syllable_to_phones

def py2ph(txt):
	symbol_list = ['sil','<space>','<unk>']
	phone_seq = []
	syllable_to_phones = syl2ph_dict()
	for syllable in _pinyinformat(txt):
		base, tone = syllable.split('_')
		phones = [phn for phn in syllable_to_phones[base]]

		if phones[-1] in symbol_list:
			pass
		else:
			phones[-1] = phones[-1] + '_' + tone
		phone_seq.extend(phones)
	return phone_seq

if __name__ =="__main__":
    txt = "我是光啊"
    print(py2ph(txt))

