# # Cardinal Number
# import cardinal_numerals_eng
# import cardinal_numerals_vie

from .language.vietnamese import integer_to_vietnamese
from .language.english import integer_to_english

def integer_to_vietnamese_numeral(n, region='north', activate_tts=False, usingCloud = False):
    if region is None:
        region = 'north'
    elif not isinstance(region, str):
        raise TypeError('Argument "region" is not a string')
    if activate_tts is None:
        activate_tts = False
    elif not isinstance(activate_tts, bool):
        raise TypeError('Argument "activate_tts" is not a boolean')
    if not isinstance(n, int):
        raise TypeError('Not an integer')
    if region != 'north' and region != 'south':
        raise ValueError('Argument "region" has not a correct value')
    if n < 0:
        raise ValueError('Not a positive integer')
    if n > 999999999999:
        raise OverflowError('Integer greater than 999,999,999,999')
    
    numbertext = integer_to_vietnamese(n, region, activate_tts, usingCloud)
    return numbertext


def integer_to_english_numeral(n, activate_tts=False, usingCloud = False):
    if activate_tts is None:
        activate_tts = False
    elif not isinstance(activate_tts, bool):
        raise TypeError('Argument "activate_tts" is not a boolean')
    if not isinstance(n, int):
        raise TypeError('Not an integer')
    if n < 0:
        raise ValueError('Not a positive integer')
    if n > 999999999999:
        raise OverflowError('Integer greater than 999,999,999,999')
    return integer_to_english(n, activate_tts,usingCloud)

