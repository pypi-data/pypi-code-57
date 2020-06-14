from termcolor import colored
from cardinal_numeral.tts import speak
import os
# This is use for intercept the final result
class FinalResult(Exception):
    pass



NUMBER = {
    0: 'không',
    1: 'một',
    2: 'hai',
    3: 'ba',
    4: 'bốn',
    5: 'năm',
    6: 'sáu',
    7: 'bảy',
    8: 'tám',
    9: 'chín'
}

def _interger_to_text(n,region, isKhongTram = False):
    result = None
    try:
        if n in NUMBER:
            # return NUMBER[n]
            result = NUMBER[n]
            raise FinalResult
    
        ListDigits = []
        for number in str(n)[::-1]:
            ListDigits.append(int(number))
        Text = ""
        for position, number in enumerate(ListDigits):
            if n % 100 == 0:
                if position <2 :
                    continue
            
            NumberText = NUMBER[number]
            # Add Rule
            if position == 1:
                if number != 1:
                    NumberText += ' mươi' 
                else :
                    NumberText = 'mười'
            elif position == 2:
                NumberText += ' trăm'
            if 10 <= n :
                if position == 0 and number == 0:
                    NumberText = ""
                if position == 1 and number == 1 and ListDigits[0] == 0:
                    NumberText = 'mười'
                if position == 0 and number == 1 and ListDigits[1] != 1 and ListDigits[1] != 0:
                    NumberText = "mốt"
                if position == 0 and number == 5 and ListDigits[1] != 0:
                    NumberText = 'lăm'
                if position == 1:
                    if number == 0 and ListDigits[position-1] != 0:
                        NumberText = 'linh' if region == 'north' else 'lẻ'
                # Pending
                # if position == 0 and number == 4:
                #     NumberText = 'tư'
            Text = NumberText + ' ' + Text
        Text = Text.strip()
        result = Text
        raise FinalResult
    except FinalResult:
        if isKhongTram:
            if n < 10:
                result = ('không trăm linh ' if region == 'north' else 'không trăm lẻ ') + result
            if 10 < n < 100:
                result = 'không trăm ' + result
        return result

def integer_to_vietnamese(n, region= 'north',activate_tts=False, usingCloud = False):
    #input source of sounds
    
    if not isinstance(region, str):
        raise TypeError('Argument "region" is not a string')
    if not region in ['north', 'south']:
        raise ValueError('Argument "region" has not a correct value')
    if not isinstance(n, int):
        raise TypeError('Not an integer')
    elif n < 0:
        raise ValueError('Not a positive integer')
    elif n >= 10**12:
        raise OverflowError('Integer greater than 999,999,999,999')
    
    if n in NUMBER:
        return NUMBER[n]

    numberstring = ("0"* 12 + str(n))[-12:]
    
    numbersegment = [int(numberstring[i:i+3]) for i in range(0, len(numberstring), 3)]
    
    
    MAP = {
        0: 'tỷ',
        1: 'triệu',
        2: 'nghìn' if region == 'north' else 'ngàn',
        3: ''
    }
    
    FinalNumber = ""
    #get the index of the segment and the segment
    for index , segment in enumerate(numbersegment):
        isKhongTram = False
        if segment == 0:
            continue
        
        listPreviousSegment = numbersegment[0:index]
        if sum(listPreviousSegment) == 0:
            isKhongTram = False
        else :
            isKhongTram = True
        number = _interger_to_text(segment,region,  isKhongTram= isKhongTram) + ' ' + MAP[index]
        numbertext = number + ' '
        # print(isKhongTram ,colored('{} => {}'.format(segment, numbertext), 'white'))
        FinalNumber += numbertext
    FinalNumber = FinalNumber.replace('  ', ' ').strip()
    #check to speak text
    if activate_tts:
        dirname, _ = os.path.split(os.path.abspath(__file__))
        address = os.path.join(dirname,'sound', region)
        address = os.path.abspath(address)
        # Workaround Unicode Filename Bug ??


        speak(FinalNumber, address, usingCloud= usingCloud, language='vietnamese')
    return FinalNumber


# if __name__ == '__main__':
#     from termcolor import colored
#     TESTCASE = {
#         19: 'mười chín',
#         15: 'mười lăm',
#         96: 'chín mươi sáu',
#         405: 'bốn trăm linh năm',
#         1915: 'một nghìn chín trăm mười lăm',
#         5061: 'năm nghìn không trăm sáu mươi mốt',
#         1002003: 'một triệu không trăm linh hai nghìn không trăm linh ba',
#         1000000: 'một triệu',
#         1030000: 'một triệu không trăm ba mươi nghìn',
        
#         100000004: 'một trăm triệu không trăm linh bốn',
#         1002000004: 'một tỷ không trăm linh hai triệu không trăm linh bốn',
#         # 1002003004: 'một tỷ không trăm linh ba nghìn không trăm linh bốn',
#         999999999999: 'chín trăm chín mươi chín tỷ chín trăm chín mươi chín triệu chín trăm chín mươi chín nghìn chín trăm chín mươi chín',
#         100000000004 : 'một trăm tỷ không trăm linh bốn'
#     }
#     for k, v in TESTCASE.items():
#         print("=" * 45)
#         print("Test Number", k)
#         finalnumber = integer_to_vietnamese(k)
#         if finalnumber != v:
#             print(colored("Wrong [{}]: {}".format(len(finalnumber),  finalnumber), 'red'))
#             print(colored("Shoud [{}]: {}".format(len(v),v), 'magenta'))
#         else :
#             print(colored("Correct : ({}) => {}".format(k, finalnumber), 'green'))

#     import json
#     with open('../../../viettest.json') as f:
#         testcase = json.loads(f.read())
#     for k, v in testcase.items():
#         k = int(k)
        
#         region = 'north'
#         result = integer_to_vietnamese(k, region= region, activate_tts= False)
#         if region == 'south':
#             v = v.replace('nghìn', 'ngàn').replace('linh','lẻ').replace('một','mốt').replace('tư', 'bốn')
#         # Preformat

#         if v != result:
#             print(
#                 colored('[ERROR]', 'red'), 
#                 colored(k, 'magenta'),
#                 '\n',
#                 colored(v, 'green'),
#                 '\n',
#                 colored(result, 'yellow')
            
#             )
        