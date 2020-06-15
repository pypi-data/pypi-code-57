# import text_speak
import os
from cardinal_numeral.tts import speak
number_dictionary = {
    1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 0: 'zero'
}
glo_part_name = {
    0: 'billion', 1: 'million', 2: 'thousand', 3: ''
}
mul10map = {
    2: 'twenty',
    3: 'thirty',
    4: 'forty',
    5: 'fifty',
    6: 'sixty',
    7: 'seventy',
    8: 'eighty',
    9: 'ninety'
}
sub20map = {
    10: 'ten',
    11: 'eleven',
    12: 'twelve',
    13: 'thirteen',
    14: 'fourteen',
    15: 'fifteen',
    16: 'sixteen',
    17: 'seventeen',
    18: 'eighteen',
    19: 'nineteen'
}



def _integer_to_english(n):
    # Convert for number from 0 - 1000 only
    if n in number_dictionary:
        return number_dictionary[n]
    hundreds, sub = divmod(n, 100)
    FinalNumber = ''
    if hundreds > 0:
        FinalNumber += number_dictionary[hundreds] + ' hundred'
    subtext = ''
    if sub > 0:
        if sub in number_dictionary:
            subtext = number_dictionary[sub]
        else:
            mul10, mul1 = divmod(sub, 10)
            if mul10 == 1:
                subtext = sub20map[sub]
            else:
                subtext = '{}-{}'.format(mul10map[mul10], number_dictionary[mul1])
            if subtext.endswith('-zero'):
                subtext = subtext[: -5]
    # Return format
    if hundreds > 0 and sub > 0:
        return FinalNumber +  ' and ' + subtext
    elif hundreds > 0 and sub == 0:
        return FinalNumber
    else :
        return subtext


def splitGroup(n):
    n = ('0'*12 + str(n))[-12:]
    listNumber = [int(n[i:i+3]) for i in range(0, 12, 3)]
    return listNumber


def integer_to_english(n, activate_tts, usingCloud = False):
    if n in number_dictionary:
        return number_dictionary[n]
    group = splitGroup(n)
    # Convert each group to numeral
    grouptext = [[_integer_to_english(g), g] for g in group]
    # Adding group unit
    groupTextWithUnit = []
    for index, _g in enumerate(grouptext):
        # if _g[1] == 0:
        #     continue
        groupTextWithUnit.append(
            [
                _g[0] + ' ' + glo_part_name[index],
                _g[1], # For tracking ( The original number )
                index # For tracking ( The group index )
            ])
    

    # Only the last group will be join by 'and', the rest is joined by ', '
    # if len(groupTextWithUnit) > 1:
    #     result = ', '.join(groupTextWithUnit[0:-1]) + ' and ' + groupTextWithUnit[-1]
    # else:
    #     result = groupTextWithUnit[0]
    # result = result.strip()

    # Filter group : Group that is 000 should not be added
    
    preAndGroup = list(filter(lambda group: group[2] != 3 and group[1] != 0, groupTextWithUnit ))
    preAndGroup = map(lambda x: x[0], preAndGroup) # Remove tracking parameter
    FinalNumber = ', '.join(preAndGroup)
    if groupTextWithUnit[3][1] > 0:
        FinalNumber += (' and ' if len(FinalNumber) else '') + groupTextWithUnit[3][0]


    if activate_tts:
        dirname, _ = os.path.split(os.path.abspath(__file__))
        address = os.path.join(dirname,'sound')
        address = os.path.abspath(address)
        # Workaround Unicode Filename Bug ??


        speak(FinalNumber, address, usingCloud= usingCloud, language='english')

    FinalNumber = FinalNumber.strip()
    return FinalNumber



if __name__ == '__main__':
    import json
    from termcolor import colored
    with open('../../../engtest.json') as f:
        testcast = json.loads(f.read())
    
    for k, v in testcast.items():
        k = int(k)
        # if k >= 1000:
        #     continue

        if v.endswith(' and'):
            v = v[:-4]
        print('testcase', k)
        kv = integer_to_english(k, False)
        if v != kv:
            print(
                colored('[ERROR]', 'red'), 
                colored(k, 'magenta'),
                '\n',
                colored(v, 'green'),
                '\n',
                colored(kv, 'yellow')
            
            )