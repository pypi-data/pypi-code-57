VERB_PAST_TENSE = "VBD"
VERB_PAST_PARTICIPLE = "VBN"


def verb_is_past(tag):
    return tag == VERB_PAST_TENSE or tag == VERB_PAST_PARTICIPLE
