import re
import logging
from xkcdpass import xkcd_password as xp  # seul 'real' module du pakage
import os
import numpy.random as rnd
import argparse

# générateur de password

fname = os.path.expanduser("~/Prog/nltk_data/corpora/words/wl_french3")

WORDFILE = xp.locate_wordfile(fname)
WORDS = xp.generate_wordlist(wordfile=WORDFILE, min_length=1, max_length=5)
LOWERWORDS = [
    re.subn(r"[`'.,-^]", "", word)[0] for word in WORDS
]  # removing les points

CAPITALIZEWORDS = xp.first_upper_case(LOWERWORDS)
ACCENTS = set("àâäéèêëïîöôüûÀÂÄÉÈÊËÏÎÖÔÜÛ")

# xp.generate_xkcdpassword(CAPITALIZEWORDS, acrostic="SNCF", case="lower", delimiter=':')


def get_words(case="phrase", minlen=1, maxlen=4):
    LOWERWORDS = xp.generate_wordlist(
        wordfile=WORDFILE, min_length=minlen, max_length=maxlen
    )
    CAPITALIZEWORDS = xp.first_upper_case(LOWERWORDS)
    if case == "lower":
        return LOWERWORDS
    elif case == "upper":
        return [w.upper() for w in LOWERWORDS]
    elif case == "camel":
        return CAPITALIZEWORDS
    elif case == "phrase":
        return CAPITALIZEWORDS + LOWERWORDS
    elif case == "all":
        return CAPITALIZEWORDS + LOWERWORDS + [w.upper() for w in LOWERWORDS]


def test_word_case(mot):
    """Test la casse d'un mot et renvois lower, upper ou camel"""
    if mot.lower() == mot:
        return "lower"
    elif mot.upper() == mot:
        return "upper"
    else:
        return "phrase"


def mtp_generator(
    acrosticOrNbWords=None,
    delimIntra=None,
    delimExtra=None,
    case=None,
    avecAccents=False,
    minlen=None,
    maxlen=None,
):
    if acrosticOrNbWords is None:
        acrosticOrNbWords = 3
        if case is None:
            case = "phrase"
    elif case is None:
        case = test_word_case(acrosticOrNbWords)

    minlen = 1 if minlen is None else minlen
    maxlen = 4 if maxlen is None else maxlen
    delimIntra = "/" if delimIntra is None else delimIntra
    delimExtra = "" if delimExtra is None else delimExtra
    case = "phrase" if case is None else case

    if avecAccents:
        MOTS = [word for word in get_words(case, minlen, maxlen)]
    else:
        MOTS = [
            word
            for word in get_words(case, minlen, maxlen)
            if not any(set(word) & ACCENTS)
        ]

    mtp = delimExtra

    if isinstance(acrosticOrNbWords, str):
        for initial in list(acrosticOrNbWords):
            mots = [word for word in MOTS if word.startswith(initial)]
            mtp += rnd.choice(mots)
            mtp += delimIntra
    else:
        n = int(acrosticOrNbWords)
        for i in range(n):
            mtp += rnd.choice(MOTS)
            mtp += delimIntra

    mtp = mtp[:-1]
    mtp += delimExtra
    return mtp


def mtp_with_size_contrainte(maxMTPlen=None, **args):
    maxMTPlen = 99 if maxMTPlen is None else maxMTPlen
    mtp = None
    i = 0
    while not mtp and i < 999:
        mtp = mtp_generator(**args)
        print(len(mtp), end="\r")
        if len(mtp) > maxMTPlen:
            mtp = None

    if i == 999:
        logging.warning(
            "La contraite sur la taille du mtp était trop forte.  Aucun mtp satisfaisants trouvés en 999 essais."
        )
    else:
        return mtp


def parse_arguments():
    # mettre à jour la doc
    description = """Un générateur de mot de passe."""
    acrosticOrNbWords_help = "Trouver des mots dont les initials forme l'acrostic. respect la case. ou passe le nombre de mots à utiliser pour le mtp  (défaut: 3 mots) "
    delimIntra_help = "Délimiteur entre les mots. Défault: '/'"
    delimExtra_help = "Délimiteur à l'éxtrémité des mots. Défault: '' (empty string)"
    minlen_help = "longueur minimal des mots dans le mtp"
    maxlen_help = "longueur maximal des mots dans le mtp"
    case_help = "Casse des mots a utiliser.  peut être, lower, upper, camel, phrase (lower+camel) ou all (lower, camel, upper). Défault: phrase.  Le type d'acrostic determinera le type de case si celle fournie ne permet pas de la générée."
    avecAccents_help = "Si présent ajoute les mots qui ont des accents"
    maxMTPlen_help = "taille maximale du mot de passe, par défault 99"

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--acrosticOrNbWords", "-a", help=acrosticOrNbWords_help)
    parser.add_argument("--delimIntra", "-i", help=delimIntra_help)
    parser.add_argument("--delimExtra", "-e", help=delimExtra_help)
    parser.add_argument("--minlen", "-n", type=int, help=minlen_help)
    parser.add_argument("--maxlen", "-x", type=int, help=maxlen_help)
    parser.add_argument("--case", "-c", help=case_help)
    parser.add_argument(
        "--avecAccents", "-é", action="store_true", help=avecAccents_help
    )
    parser.add_argument("--maxMTPlen", "-m", type=int, help=maxMTPlen_help)

    logLevel_dft = "INFO"
    logLevel_hlp = f"Log level (def. {logLevel_dft})"
    parser.add_argument("-L", "--logLevel", default=logLevel_dft, help=logLevel_hlp)

    return parser.parse_args()


def run(args):
    if args.acrosticOrNbWords:
        for acc in ACCENTS:
            if acc in args.acrosticOrNbWords:
                args.avecAccents = True
                break

    print(mtp_with_size_contrainte(**vars(args)))


if __name__ == "__main__":
    args = parse_arguments()

    LOGFMT = " %(asctime)s %(levelname)s-%(name)s %(funcName)s@%(filename)s-%(lineno)d :%(message)s"
    logging.basicConfig(level=args.logLevel, format=LOGFMT)

    run(args)
