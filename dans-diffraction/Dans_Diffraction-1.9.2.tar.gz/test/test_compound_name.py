"""
Test regex methods for compounds
"""

import re

ELEMENT_LIST = [
    'Zr', 'Mo', 'Es', 'Eu', 'Fe', 'Fl', 'Fm', 'Fr', 'Ga', 'Gd', 'Ge',
    'He', 'Hf', 'Hg', 'Ho', 'Hs', 'In', 'Ir', 'Kr', 'La', 'Li', 'Lr',
    'Lu', 'Lv', 'Mc', 'Zn', 'Mg', 'Er', 'Dy', 'Ds', 'Bk', 'Ag', 'Al',
    'Am', 'Ar', 'As', 'At', 'Au', 'Ba', 'Be', 'Bh', 'Bi', 'Br', 'Db',
    'Ca', 'Cd', 'Ce', 'Cf', 'Cl', 'Cm', 'Cn', 'Co', 'Cr', 'Cs', 'Cu',
    'Mn', 'Md', 'Mt', 'Rb', 'Rf', 'Rh', 'Rn', 'Ru', 'Sb', 'Sc', 'Se',
    'Sg', 'Si', 'Sm', 'Sn', 'Sr', 'Ta', 'Tb', 'Tc', 'Te', 'Th', 'Ti',
    'Tl', 'Tm', 'Ts', 'Xe', 'Yb', 'Re', 'Rg', 'Ac', 'Pb', 'Nh', 'Ni',
    'No', 'Np', 'Nd', 'Ra', 'Og', 'Os', 'Pa', 'Pd', 'Nb', 'Pm', 'Po',
    'Pr', 'Pt', 'Na', 'Pu', 'Ne', 'B', 'W', 'V', 'Y', 'U', 'F', 'K',
    'C', 'I', 'P', 'H', 'S', 'N', 'O',
    'D',  # add Deuterium
]

ELEMENT_LIST_CASE = [
    'Zr', 'Mo', 'Es', 'Eu', 'Fe', 'Fl', 'Fm', 'Fr', 'Ga', 'Gd', 'Ge',
    'He', 'Hf', 'Hg', 'Ho', 'Hs', 'In', 'Ir', 'Kr', 'La', 'Li', 'Lr',
    'Lu', 'Lv', 'Mc', 'Zn', 'Mg', 'Er', 'Dy', 'Ds', 'Bk', 'Ag', 'Al',
    'Am', 'Ar', 'As', 'At', 'Au', 'Ba', 'Be', 'Bh', 'Bi', 'Br', 'Db',
    'Ca', 'Cd', 'Ce', 'Cf', 'Cl', 'Cm', 'Cn', 'Co', 'Cr', 'Cs', 'Cu',
    'Mn', 'Md', 'Mt', 'Rb', 'Rf', 'Rh', 'Rn', 'Ru', 'Sb', 'Sc', 'Se',
    'Sg', 'Si', 'Sm', 'Sn', 'Sr', 'Ta', 'Tb', 'Tc', 'Te', 'Th', 'Ti',
    'Tl', 'Tm', 'Ts', 'Xe', 'Yb', 'Re', 'Rg', 'Ac', 'Pb', 'Nh', 'Ni',
    'No', 'Np', 'Nd', 'Ra', 'Og', 'Os', 'Pa', 'Pd', 'Nb', 'Pm', 'Po',
    'Pr', 'Pt', 'Na', 'Pu', 'Ne', 'B', 'W', 'V', 'Y', 'U', 'F', 'K',
    'C', 'I', 'P', 'H', 'S', 'N', 'O',
    'zr', 'mo', 'es', 'eu', 'fe', 'fl', 'fm', 'fr', 'ga', 'gd', 'ge',
    'he', 'hf', 'hg', 'ho', 'hs', 'in', 'ir', 'kr', 'la', 'li', 'lr',
    'lu', 'lv', 'mc', 'zn', 'mg', 'er', 'dy', 'ds', 'bk', 'ag', 'al',
    'am', 'ar', 'as', 'at', 'au', 'ba', 'be', 'bh', 'bi', 'br', 'db',
    'ca', 'cd', 'ce', 'cf', 'cl', 'cm', 'cn', 'co', 'cr', 'cs', 'cu',
    'mn', 'md', 'mt', 'rb', 'rf', 'rh', 'rn', 'ru', 'sb', 'sc', 'se',
    'sg', 'si', 'sm', 'sn', 'sr', 'ta', 'tb', 'tc', 'te', 'th', 'ti',
    'tl', 'tm', 'ts', 'xe', 'yb', 're', 'rg', 'ac', 'pb', 'nh', 'ni',
    'no', 'np', 'nd', 'ra', 'og', 'os', 'pa', 'pd', 'nb', 'pm', 'po',
    'pr', 'pt', 'na', 'pu', 'ne', 'b', 'w', 'v', 'y', 'u', 'f', 'k',
    'c', 'i', 'p', 'h', 's', 'n', 'o',
    'D', 'd', # add Deuterium
]

# Tests
st=[]
st+=['Sr4Ru2.6Mn0.4O10']
st+=['Li0.8CoO2']
st+=['Li3V2(PO4)3']
st+=['(Na0.9Ca0.1)1.6Co2O4']
st+=['Mn0.3(Fe3.6(Co1.2)2)4(Mo0.7Pr44)3']


def test(regex):
    print('New test')
    for s in st:
        print('%s: %s' % (s, regex.findall(s)))


regex_brackets = re.compile('\(.+\)[\d\.]+')
regex_bracket_n = re.compile('\)[\d\.]+')
element_or = '|'.join(ELEMENT_LIST)
regex_elements = re.compile('|'.join(ELEMENT_LIST_CASE))
regex_element_num = re.compile('|'.join(['%s[\d\.]*' % el for el in ELEMENT_LIST_CASE]))
regex_ele_or_num = re.compile(element_or + '|[\d\.]+')
regex_num = re.compile('[\d\.]+')

test(regex_elements)
test(regex_brackets)
test(regex_ele_or_num)

def element_num(str):
    return regex_ele_or_num.findall(str)


def replace_bracket(name):
    bracket = []
    start_idx = []
    level=0
    for n, s in enumerate(name):
        if s in ['(', '[', '{']:
            start_idx += [n]
            level += 1
        elif s in [')', ']', '}']:
            level -= 1
            if level == 0:
                num = regex_bracket_n.findall(name[n:])
                if len(num) > 0:
                    bracket_end = n + len(num[0])
                    num = float(num[0][1:])
                else:
                    bracket_end = n+1
                    num = 1.0
                bracket += [(
                    name[start_idx[0]+1:n],  # insde brackets
                    name[start_idx[0]:bracket_end],  # str to replace
                    num
                )]
                start_idx = []

    for oldstr, repstr, num in bracket:
        oldstr = replace_bracket(oldstr)
        for oldnum in regex_num.findall(oldstr):
            oldstr = oldstr.replace(oldnum, '%0.3g'%(float(oldnum)*num))
        name = name.replace(repstr, oldstr)
    return name

print('\n\n')
print(st[-1])
print(replace_bracket(st[-1]))


# Put it together
def compound_name(name):
    name = replace_bracket(name)
    return regex_element_num.findall(name)

print('\n\nMain Test:')
for s in st:
    print('%20s:  %s' % (s, compound_name(s)))