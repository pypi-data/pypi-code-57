
spelling_corrections = {
    'anglular': 'angular',
    'contraint': 'constraint',
    'derivates': 'derives',
    'exisiting': 'existing',
    'fisrt': 'first',
    'identifie': 'identify',
    'litteral': 'literal',
    'Literaql': 'Literal',
    'obect': 'object',
    'porduct': 'product',
    'poistion': 'position',
    'refrence': 'reference',
    'retrived': 'retrieved',
    'Retuns': 'Returns',
    'settting': 'setting',
    'seted': 'set',
    'surgace': 'surface',
    'tensuion': 'tension',
    'tranformation': 'transformation',
    'thirs': 'third',
}


def correct_spelling(text):

    words = text.split(" ")
    new_words = []

    for word in words:

        if word in spelling_corrections:
            word = spelling_corrections[word]

        new_words.append(word)

    return ' '.join(new_words)