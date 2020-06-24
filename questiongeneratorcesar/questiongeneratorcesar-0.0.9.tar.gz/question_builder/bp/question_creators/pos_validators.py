VERB = "VERB"
AUX = "AUX"
NOUN = "NOUN"
PRON = "PRON"
PROPN = "PROPN"
ADJ = "ADJ"
ADV = "ADV"


def is_verb(pos):
    return pos == VERB

def is_auxiliar(pos):
    return pos == AUX 

def is_noun(pos):
    return pos == NOUN or pos == PROPN or pos == PRON

def is_adjective(pos):
    return pos == ADJ

def is_adverb(pos):
    return pos == ADV