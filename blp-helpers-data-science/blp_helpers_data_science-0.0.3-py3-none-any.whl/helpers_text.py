import nltk
import re
import string
import codecs
from collections import Counter


def worthaeufigkeiten_berechnen(text):
    # text = String
    # haeufigkeiten berechnen
    haeufigkeiten_dict = dict(Counter(text.split()))

    # dict sortieren
    haeufigkeiten_list_sorted = sorted(haeufigkeiten_dict.items(), key=lambda kv: kv[1], reverse=True)

    return haeufigkeiten_dict, haeufigkeiten_list_sorted


def remove_stopwords(text, custom_stopwords_file='industry_classifier_custom_stopword_list'
                     , default_stopwords_language='german'):
    """

    :param text:
    :param custom_stopwords_file: string, optional
        Voller Pfad zu einer benutzerdefinierten Datei mit Stoppwörtern.
        Dateiformat muss .csv sein.
        Inhalt der .csv-Datei: jede Zeile ist eine Stoppwort.

        Beispiel für Inhalt einer .csv-Datei:

        070316umschlagfu
        100prozentzielwert
        12f
        132r1


    :return:
    """
    default_stopwords = set(nltk.corpus.stopwords.words(default_stopwords_language))
    all_stopwords = default_stopwords

    if custom_stopwords_file:
        custom_stopwords = set(codecs.open(custom_stopwords_file, 'r', 'utf-8').read().splitlines())
        all_stopwords = default_stopwords | custom_stopwords
    else:
        pass
    tokens = tokenize_text(text)
    filtered_tokens = [token for token in tokens if token not in all_stopwords]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text


def tokenize_text(text):
    """
    Returns text tokenized as words
    :param str text: Text to be tokenized
    :return: Words
    :rtype: String


    Examples
    --------
    text = ' drehmomentwandlervorrichtung, insbesondere für einen antriebsstrang eines kraftfahrzeugs  '

    print(tokenize_text(titel[0]))
    ['drehmomentwandlervorrichtung',
    ',',
    'insbesondere',
    'für',
    'einen',
    'antriebsstrang',
    'eines',
    'kraftfahrzeugs']

    """
    tokens = nltk.word_tokenize(text)
    tokens = [token.strip() for token in tokens]
    return tokens


def replace_special_characters(text, substitutionsstring=' '):
    """Entfernt special_characters gänzlich.

    special_characters = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' - siehe <pattern>
    Beispiele:
    Vorher: http //www.linkedin.com/company/daimler/
    Nachher: wwwlinkedincomcompanydaimler
    """
    tokens = tokenize_text(text)
    pattern = re.compile('[{}]'.format(re.escape(string.punctuation)))
    filtered_tokens = filter(None, [pattern.sub(substitutionsstring, token) for token in tokens])
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text
