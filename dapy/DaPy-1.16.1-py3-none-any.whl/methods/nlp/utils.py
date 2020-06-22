from itertools import chain, repeat
from re import compile as re_compile
from string import punctuation

from .constant import END, HEAD, OOV, WEB, NUMBER


def count_iter(iterable):
    '''function as "len()" but it supports iterable objects'''
    count = 0.0
    while True:
        try:
            next(iterable)
            count += 1.0
        except StopIteration:
            return count

def get_left_padding(input, nmax):
    return tuple(chain(repeat(HEAD, nmax + 1), input))

def get_right_padding(input, nmax):
    return tuple(chain(input, repeat(END, nmax)))

def get_ngram(input, nmin=1, nmax=1):
    padding = tuple(chain(repeat(HEAD, nmax + 1), input, repeat(END, nmax)))
    length = len(padding) - nmax
    for sublen in range(nmin - 1, nmax):
        for index in range(sublen, length):
            yield padding[index : index + 1 + sublen]

en_transfer_table = [
    ("it's", 'it is'), ("i'm", 'i am'), ("he's", 'he is'), ("she's", 'she is'),
    ("we're", 'we are'), ("they're", "they are"), ("you're", 'you are'), ("that's", 'that is'),
    ("this's", 'this is'), ("can't", 'can not'), ("don't", 'do not'), ("doesn't", 'does not'),
    ("we've", 'we have'), ("i've", 'i have'), ("isn't", 'is not'), ("won't", 'will not'),
    ("didn't", 'did not'), ("hadn't", 'had not'), ("what's", 'what is'), ("couldn't", 'clould not'),
    ("you'll", 'you will'), ("you've", 'you have')
]

BLANK = re_compile(u'[ |\\n]{2,}')
WEB_PATTERN = re_compile('(ht|f)tp(s?)\:\/\/[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:(0-9)*)*(\/?)([a-zA-Z0-9\-\.\?\,\'\/\\\+&amp;%\$#_]*)?')
PUNCTUATION = str.maketrans('', '', punctuation)
NUM_PATTERN = re_compile('[-]{0,1}([1-9]{0,1}[0-9]{0,}[.]{0,1}[0-9]+?|[0-9]{0,3}[,][0-9]{0,3}[,][0-9]{0,3})$')
def clean_text(input):
    input = BLANK.sub(' ', input).strip()
    for abbr, sep in en_transfer_table:
        input = input.replace(abbr, sep)
    input = WEB_PATTERN.sub(WEB, input)
    input = NUM_PATTERN.sub(NUMBER, input)
    return input.translate(PUNCTUATION)

