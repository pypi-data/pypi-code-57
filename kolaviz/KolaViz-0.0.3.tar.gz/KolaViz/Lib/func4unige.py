# -*-coding:utf-8-*-
import csv
import logging
import os
from operator import itemgetter
from pathlib import Path
import re
from typing import Set, Any, Union, Optional, Dict, List

import pandas as pd
from pandas import DataFrame

import langdetect as lgd
import nltk
from bs4 import BeautifulSoup as BS
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import (
    PunktSentenceTokenizer,
    wordpunct_tokenize,
    word_tokenize,
)

from KolaViz.Lib.tbutils import uid_humanize_dico
from KolaViz.Lib.model import STOPWLIST, COLT, STOPWORD_DIR

# #Rangement des fonctions à faire
path = os.path.abspath("./")
BSTOPWDIR = Path(STOPWORD_DIR)


def tokenize_text(
    df_: DataFrame,
    ngramR: int = 1,
    stopW=None,
    # basedir=STOPWORD_DIR,
    textCol=None,
    inplace: bool = True,
    lang_detect: Optional[Union[str, int]] = True,
    strong_lem=True,
    sent_tokenizer: str = "mlk",
    word_tokenizer: str = "mlk",
):
    """
    A REVOIR: entrée: un dataframe avec au moins une colonne contenant des textes
    à tokenizer.
    Sortie: un dataframe avec les colonnes suivantes ajoutée et renseignée
    en fonction du texte d'entrée :
    'lang_detect': if int detect language with int trys, if str, set lang
    to lang_detect else lang will be None.
    'msgContent': text avec balise xml, html ou non,
    'link': liens qui apparaisse dans le texte,
    'img',: liens vers des images (contenu de img)
    'code': contenu des balise code,
    'contact': nom et références contenant @
    'wtext': le texte débarassé des balises
    'sentTok': les tokens de la phrase (avec leur casse),
    'lang': langue probable du text,
    'tokens': le tokens après avoir enlevé les stopwods.  utilisé poru faire le ngrames,
    'bow', les tokens de la phrase en lowercase. voir cas des tokens exclus mais
    dans ngrams
    'lenT': longueur des tokens (sans les ngrams)
    'lenTng': longueur des tokens (avec les ngrams)
    'bigTok', plus grand token (sans les ngrams)
    'lenBigT, longueur du plus long token (sans les ngrams)


    Option: la taille des ngramR, la langue de la stopW, le basedir
    où se trouve les stopW, le nom de la colonne qui contient le texte. Utilisé
    si il y a plus d'une colonne en entrée.
    """
    df = (
        df_
        if inplace
        else pd.DataFrame(data=df_.values, columns=df_.columns, index=df_.index)
    )

    if len(df_.columns) == 1:
        textCol = df_.columns[0]
    elif textCol is None:
        textCol = fcol("discussion_answer_content")  # the previous default

    # wrangle text
    # commonTags = {'em', 'a', 'u', 'strong', 'li', 'list', 'code', 'sup',
    # 'text', 'img', 'co-content'}
    # text en dernier car on supprime aussi à ce moment là.
    for cmd in [
        "link",
        # "img",
        # "code",
        "contact",
        "text",
    ]:
        print("\n")
        new_cpt = compteur(titre=f"Wrangle '{cmd}' in text: ", end=len(df))

        df.loc[:, cmd] = df.loc[:, textCol].apply(
            lambda d: wrangle_text(
                d, cmd=cmd, cpt=new_cpt, sent_tokenizer=sent_tokenizer,
            )
        )

    # texte withtout xml tags
    df.loc[:, "wtext"] = df.text.apply(lambda d: d[0])

    # texte coupé en phrase
    df.loc[:, "sentTok"] = df.text.apply(lambda d: d[1])
    df = df.drop("text", axis=1)

    # Estimation de la langue
    if isinstance(lang_detect, str):
        df.loc[:, "lang"] = lang_detect
    elif isinstance(lang_detect, int):
        print("\n")
        new_cpt = compteur(titre="Detecte language: ", end=len(df))
        # à faire sur les tokens ou les sentences?
        df.loc[:, "lang"] = df.wtext.apply(
            lambda d: detect_language(d, cpt=new_cpt, nb_estime=lang_detect)
        )
    else:
        df.loc[:, "lang"] = None

    # découpage des phrases en ngrams
    new_cpt = compteur(titre="Tokenize: ", end=len(df))
    df.loc[:, "tokens"] = df.loc[:, ["sentTok", "lang"]].apply(  # f pour frame
        lambda f: UNIGEtokenize(
            sents_list=f.sentTok,
            ngramR=ngramR,
            stopWlist=stopW,
            # basedir=basedir,
            lang=f.lang,
            cpt=new_cpt,
            strong_lem=strong_lem,
            word_tokenizer=word_tokenizer,
        ),
        axis=1,
    )
    df.loc[:, "bow"] = df.tokens.apply(lambda d: d[1])
    df.loc[:, "tokens"] = df.tokens.apply(lambda d: d[0])

    #    df.loc[:, 'lenTng'] = df.tokens.apply(len)
    df.loc[:, "lenT"] = df.bow.apply(len)
    df = df.loc[df.lenT != 0, :]  # phrase sans token

    def big_token(tokens):
        return sorted([(t, len(t)) for t in tokens], key=lambda x: x[1])[-1]

    # big tokens
    df.loc[:, "bigTok"] = df.bow.apply(lambda toks: big_token(toks)[0])
    df.loc[:, "lenBigT"] = df.bow.apply(lambda toks: big_token(toks)[1])

    # on filtre
    # les messages dont le token est plus grand que Honorificabilitudinitatibus
    # (shakespear) les messages avec au moins un token  # à voir
    mask = (df.lenBigT < 27) & (df.lenT > 0)  # tobig words and empty sentences
    df = df.loc[mask]

    return df


def getNthElt(datum, n):
    return itemgetter(n)


def getFirstElt(datum):
    return getNthElt(datum, 0)


def getSecondElt(datum):
    return getNthElt(datum, 1)


def wrangle_text(message, cmd="text", sent_tokenizer="mlk", cpt=None):
    """
    Enlève les tags, en récupère quelques uns
    récupère des bouts importants du text
    """
    if cpt:
        print(f"{next(cpt)}", end="\r")

    if pd.isna(message):
        return None

    # try to get urls ands emails
    speA = "[]!*'();:&=+$,/?#[A-Za-z0-9_.~%-]"
    speR = "[A-Za-z0-9-]"
    urlpat = f"(?:https?|file)://(?:{speA}|@)+"
    domext = "(?:" + "|".join(["com", "org", "edu", "fr"]) + "\W)"
    dompat = f"(?:(?:{speR}+\.)?{speR}+)?(?:\.{domext})"
    mailpat = f"(?:(?:{speR}+{speA}*|\s)@{speA}*{speR}+)"

    if cmd == "text":
        # on supprime les liens et référence à quelqu'uns des messages
        message, n = re.subn(urlpat, "", message)
        message, n = re.subn(mailpat, "", message)
        message, n = re.subn(dompat, " _domain_ ", message)

        message = message.replace("><", "> <")
        # pour eviter que les mots se collent (pas de point ou \n car span)
        text = BS(message, features="xml").get_text()
        # faudrait vérifier à nouveau avec du text de l'unige
        if not len(text):
            # In case BS parsing removed all text, goes to default which usualy is lxml
            text = BS(message, features="lxml").get_text()

        # smileys
        text, n = re.subn(":\)|:o\)|:-\)|;-\)|;o\)|;\)", " _smiley_ ", text)
        # the dots
        # Ajoute au réponses d'un mot qui est une quantité les mots "My answer is"
        # afin d'avoir une phrase.
        qtypat = "((?:\d|<)(?:\d|\s|-|=|%|/|<)*)"
        if re.fullmatch(qtypat, text):
            text = re.sub(qtypat, lambda m: f"My answer is {m.group(1)}.", text,)

        # Pourrait, devrait faire plus de wrangling ici ?

        return get_sentences(text, sent_tokenizer=sent_tokenizer)

    elif cmd == "link":
        return re.findall(f"{urlpat}|{dompat}", message)
    elif cmd == "img":
        return BS(message, features="xml").find_all("img")
    elif cmd == "code":
        return BS(message, features="xml").find_all("code")
    elif cmd == "contact":
        return re.findall(mailpat, message)
    else:
        raise (Exception("command not known"))


def get_sentences(text, sent_tokenizer="mlk"):
    """
    capitalize sentence using my own sent tokenizer or that of nltk
    use 'mlk (malik koné)' or punkt (nltk) sent tokenizer
    """
    text = text.strip()
    if sent_tokenizer == "mlk":
        # ~90 µs mais ne gère pas peut-être pas bien les abréviations eg Mlle."
        # debsent = r'(?:(?<!\b\w)([.?!]|\A)+)'  # exclus les phrase d'une lettre
        # startpat = debsent + r'\s*(?<=\b)(\w)'
        # wtext = re.subn(startpat, lambda m: m.group(1) + '\n' +
        # m.group(2).upper(), text)[0].
        # ! doit être testé rigoureusement !
        endsent1 = r"(?:[.?!]?\Z)"  # ponctu à la toute fin du text text
        # ponctu suivie de deux lettres
        endsent2 = r"(?:[.?!]+(?=[a-zA-Z][a-zA-Z]))"
        cexp = "(?:\d|\w.|com)"
        # point non suivi d'un chifre ou d'une lettre ou de com et pas précédé
        # non plus d'une lettre
        endsent3 = f"(?:(?<!.\w)[.?!]+(?!{cexp}))"
        # point suivis d'espace et précédé de 3 chars ou plus
        endsent4 = f"(?:(?<!\W\w\w\w)[.?!]+\s+)"
        end = "(?:" + "|".join([endsent1, endsent2, endsent3, endsent4]) + ")"

        # une phrase est n'importe quelle caractères suivie d'une fin 'end' ou
        # d'un retour à la ligne
        sentpat = f"(.*?)(?:{end}|\n)"
        sents = [s for s in re.findall(sentpat, text) if len(s)]
        # je recompose le texte en allant à la ligne.
        wtext = " \n ".join([s[0].upper() + s[1:] for s in sents])

    elif sent_tokenizer == "punkt":
        # ~310 µs
        sent_tokenizer = PunktSentenceTokenizer(text)
        sents = [x.capitalize() for x in sent_tokenizer.tokenize(text) if len(text)]
        wtext = " \n ".join(sents)

    return wtext, sents


def langexception(f):
    """Wrapper pour la langue detect."""

    def f_with_exception(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except LangDetectException as lde:
            # gestion des messages avec pas assez de mots pour détecter la langue
            if "No features in text" in lde.__repr__():
                return None
            else:
                raise (lde)
            pass
        pass

    return f_with_exception


@langexception
def detect_language(msg, cpt=None, nb_estime=10):
    """Détecter la langue."""
    if cpt:
        print(f"{next(cpt)}", end="\r")

    # à paralléliser ?
    langue = detect(msg)
    if langue != "en":
        langue = filtre_lang(msg, nb_estime, seuil=0.95)

    return langue


def filtre_lang(
    msg,
    nb_estim=10,
    seuil=0.60,
    deflang=["en", "af"],
    possible_langs=["pt", "es", "fr", "ca", "zh-cn", "de"],
):
    """
    Effectuer plusieurs estimation de language pour un message. La langue par
    défaut sera deflang[0].  Avec un mechanisme pour choisir la langue en cas de doute
    """
    altl: Dict[str, Any] = {}
    estims = []
    # l'idée c'est de voir la moyenne sur un nombre k d'estimation.  Si > seuil
    # alors lang sinon, doute. en ?
    # si au cours des estimation il y a l'anglais alors on le prend
    for i in range(nb_estim):
        estim = lgd.detect_langs(msg)[0]
        estims.append(estim)
        #        langs.append(estim)
        # fait un dict avec le max pour chaque langue trouvé
        # langs = {l.lang: max(langs.get(l, 0), l.prob) for l in estim}
        if set(deflang) & set(estim.lang):
            return deflang[0]

    # on fait un dict avec les langues trouvées et leur proba cumulées
    for i, estim in enumerate(estims):
        altl[estim.lang] = (
            altl.get(estim.lang, (0, 0))[0] + estim.prob,
            altl.get(estim.lang, (0, 0))[1] + 1,
        )

    # si la proba de max_lang est forte et que ce n'est pas une langue autorisée
    # renvois deflang
    alLg = sorted(list(altl.items()), key=lambda x: x[1])[::-1]
    # on parcours les alternatives dans l'ordre décroissant de proba cumulé et vérifie
    # que la proba moyenne est supérieure au seuil fixé sinon renvois la langue
    # par défaut
    for max_lang, (max_prob, max_it) in alLg:
        if max_lang not in possible_langs:
            pass
        elif max_prob / max_it < seuil:
            return deflang[0]
        else:
            return max_lang
    else:
        return deflang[0]


def UNIGEtokenize(
    sents_list,
    ngramR=1,
    stopWlist=None,
    # basedir=None,
    lang="en",
    cpt=None,
    strong_lem=True,
    word_tokenizer="mlk",
):
    """
    tokenizer pour le corpus d'UNIGE.  Les tokenizer publiques sont souvent pleins
    d'assomptions qu'il faut maîtriser  voir # see

    http://aclweb.org/anthology/W18-2502
    pour avoir de bon résultats avec la veditisation (leming) qui suit logiquement
    - msg : est une liste de phrases de charactère représentant un message dans un
    forum du MOOC
    stopWlist string.  remove stop words of lang stopWlist si présent (par def oui), before
    doing ngrams and saving tokens

    """
    if cpt:
        print(f"{next(cpt)}", end="\r")

    if stopWlist is None:
        # gestion multi-lingue. Doit être définie comme un string maintenant
        stopWlist = STOPWLIST.get(lang, "english")

    # identifier les caractères de séparation
    sents = list()
    spechar = '[]["();:-?!|~{}]'

    # catching formulas (roughly)  'grammaire pour formule math?'
    nb = "(?:-?\d*(?:\.)?\d+(?:\s?%)?)"
    mathops1 = "[+/*-=^]"
    mathops2 = "[][(){}/*+-^]"
    lt = "[a-zA-Z]"
    # variable d'une lettre (un caractère) dans des opérations mathématiques
    cr = f"(?:\b{lt}(?={mathops2})?|(?<={mathops2})\s*{lt}\b)"
    nbs = f"(?:{cr}+|{nb})"  # nombre symbolique
    mathC = f"(?:{nbs}(?:\s*{mathops1}\s*{nbs})*)"
    mathC2 = f"(?:{mathops2}*{mathC}{mathops2}*)"
    mathC3 = f"(?:{mathC2}(?:\s*{mathops1}\s*{mathC2})*)"
    segal = f"(?:{lt}+\s*=\s*(?:{mathC3}|{lt}+))"  # string egal
    mathexp = f"(?:{mathC3}|{segal})"

    for sent in sents_list:
        sent, _ = re.subn(
            r"\bP/Es?\b", "_P_E_", sent
        )  # domain expressions pour cours umf
        sent, _ = re.subn(r"\bvs\b", "_vs_", sent)  # domain expressions

        sent, _ = re.subn(mathexp, " _mathexp_ ", sent)
        sent, _ = re.subn("(_mathexp_\s*)+", " _mathexp_ ", sent)
        sent, _ = re.subn("\.\.+", " _suspension_ ", sent)
        sent, _ = re.subn("\!+", " _exclamation_ ", sent)
        sent, _ = re.subn("\?+", " _interogation_ ", sent)

        if lang == "en":
            #  the idea here is not to remove too much word but lematize them
            # have and be may not be usefull in ngrams
            sent, _ = re.subn(r"n't\b", " not", sent)  # not
            sent, _ = re.subn(r"'ll\b", " will", sent)  # not
            sent, _ = re.subn(r"'d\b", " would", sent)  # not
            sent, _ = re.subn(r"'re\b", " are", sent)  # not
            sent, _ = re.subn(r"'ve", " have", sent)  # 've -> have
            # remove 's of that's or bob's car (can say if is or possesive)
            sent, _ = re.subn(r"'s\b", "", sent)
        # on enlève les caractères de spérations
        sent, _ = re.subn(f"{spechar}" + "|'", " ", sent)
        sents.append(sent)

    bow: List[str] = list()
    ngrams: List[str] = list()

    for sent in sents:

        if word_tokenizer == "mlk":
            veds = mlk_tokenizer(sent, strong_lem, stopWlist)

        elif "punkt" in word_tokenizer:
            language = STOPWLIST.get(lang, "english")

            if "base" in word_tokenizer:  # base_punkt
                toks = wordpunct_tokenize(sent)
            else:
                toks = word_tokenize(sent, language=language, preserve_line=True)

            veds = remove_stop_words(toks, stopWlist=language)

        bow += veds
        # pour le 1gram
        if (isinstance(stopWlist, str) and "minimal" in stopWlist.lower()) or (
            isinstance(stopWlist, Path) and "minimal" in stopWlist.as_posix().lower()
        ):
            stopWlist = Path(stopWlist).parent.joinpath("normalUnige")

        ngrams += mlk_ngrammer(veds, ngramR, stopWlist)

    # renvois les ngrams et le bag of words propre de la sents_list
    return ngrams, bow


def mlk_tokenizer(sent, lang, strong_lem, stopWlist="normalUnige"):
    """
    tokenize et vedetise sent selon lang
    """
    cdmot = "(?:_|\w)"  # char de mot
    mot = r"(?:\b%s{2,}\b)" % cdmot

    sent_tokens = re.findall(mot, sent.lower())
    # lemmatize selon la langue
    if lang == "en":
        # vedetisation faible ex. is ne devient pas be
        # ! pos_tag tient compte du contexte pour déterminer les tag.
        if strong_lem:
            # on réduit le context pour avoir une lemmatisation plus forte
            veds = vedettes(
                nltk.tag.pos_tag(remove_stop_words(sent_tokens, stopWlist=stopWlist))
            )
        else:
            veds = vedettes(nltk.tag.pos_tag(sent_tokens))
    else:
        veds = sent_tokens

    return veds


def mlk_ngrammer(veds, ngramR, stopWlist):
    """Renvois ngrams pour veds."""
    ngrams = remove_stop_words(veds, stopWlist=get_stop_words(stopWlist))
    # pour les 2gram et plus
    # on construit les ngrams après avoir enlevé un minimum de stopwords
    veds = remove_stop_words(
        veds, stopWlist=get_stop_words(BSTOPWDIR.joinpath("minimalUnige")),
    )
    for ng in range(2, ngramR + 1):
        ngrams += get_ngrams(veds, ng)

    return ngrams


def get_ngrams(tokens, ng=2):
    """Renvois juste les n grams fait avec les tokens."""
    N = len(tokens)

    return ["_".join(tokens[i : i + ng]) for i in range(N - ng + 1)]


def vedettes(tagposl):
    """
    recoit une tag pos list, renvois une liste avec les vedettes si trouvé sinon entrée,
    doit implémenter les autres langes.. fr
    """
    # check nltk.help.upenn_tagset('RB')
    resultats = list()
    for tag, pos in tagposl:
        # treebankpos : tree bank part of speech list
        # wordent part of speech.  Ex. boss ou has
        if (len(tag) > 1 and tag[-2:] == "ss") or (tag[-1:] == "s" and len(tag) <= 3):
            # on n'enlève pas de s au mot se finissant par double ss
            # n'y aux mots de 3 lettres ou moins qui finissent par s
            ved = tag
        else:
            ved = get_ved(tag, pos)

        resultats.append(ved)

    return resultats


def get_ved(tag, pos):
    """Returns the vedette of tag associated with pos."""
    converter = {
        wn.NOUN: ["NN", "NNS", "NNP", "NNPS"],
        wn.VERB: ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"],
        wn.ADV: ["RB", "RBR", "RBS"],
        wn.ADJ: ["JJ", "JJR", "JJS"],
    }

    # !  la lemitasation des mot se finissant en s est souvent probélamtique. le s
    # est éludé même dans boss ou BS or vs

    # see nltk.help.upenn_tagset('RB')
    # ne retour la vedette que si le POS est dans les values de converter
    # les valeurs sont les POS renvoyé par nltk.tag.pos_tag
    # les clefs sont ce qui est nécessaire à lemmatize (wordnet)
    for wdpos, treebankpos in converter.items():
        if pos in treebankpos:
            return WordNetLemmatizer().lemmatize(tag, wdpos)
    return tag


def remove_stop_words(tokList, stopWlist="english"):
    """
    renvois une liste de token d'où sont exfiltré les stop words de langue lang.
    if stopWL (liste de stop words) est none
    prend la liste par de nltk pour lang.
    peut passer une liste
    """

    # reçois un string ou une list
    if stopWlist is None or isinstance(stopWlist, (str, Path)):
        stopWlist = get_stop_words(stopWlist=stopWlist)
    elif isinstance(stopWlist, list):
        stopWlist = stopWlist

    return [t for t in tokList if t not in stopWlist]


def get_stop_words(stopWlist, basedir=BSTOPWDIR):
    """
    Charge une list de stop word qui se trouve dans basedir.  Si stopWlist ne contient
    pas unige, se rabat sur les stopword par défaut ('english', 'french' ect..)
    get the stop word list for unige( normalUnige by default) in the folder ./StopWord.
    l'autre posssibilité est normalUnige (voir folder).  Doti.
    Si stopWlist ne contient pas la chaine unige, charge les stop words list
    de nltk par exemple 'english
    """
    if isinstance(stopWlist, Path) and "unige" in stopWlist.stem.lower():
        suffix = stopWlist.suffix if stopWlist.suffix else "txt"
        fname = Path(f"{stopWlist.parent}").joinpath(f"{stopWlist.stem}.{suffix}")
        stopWords: Set[str] = set()

        if os.path.exists(fname):
            with open(fname, "r") as f:
                stopWords |= set(f.readlines())

            return {sw.split("\n")[0] for sw in stopWords}

        else:
            logging.exception(
                f"{fname} n'existe pas.  Impossible de charger"
                "la stopword list. Actuellement dans {os.getcwd()}"
            )
            raise Exception

    elif stopWlist in STOPWLIST.values():

        try:
            return set(nltk.corpus.stopwords.words(stopWlist))
        except AttributeError as e:
            logging.error(
                f"nltk n'a probablement pas trouvé de stopword list {stopWlist}."
                " Vérifier les chemins"
            )
            raise (e)
    else:
        raise Exception(f"Need to check stopWlist={stopWlist}")


def compteur(titre="cpt", start=0, end=100):
    """Un compteur pour suivre les appels dans les applys."""
    i = start
    while True:
        i += 1

        yield f"{titre} {i} / {end}"


def fcol(x, colT=COLT):
    """Get the translated name from the columns name. Does a translation for one name."""

    return translate([x], colT)[0]


def translate(liste, dicoT):
    """
    replace all occurence of dicoT key found in each list element by dicoT value.
    Usefull for translation of long pd columns names
    """
    ncols = []
    for c in liste:
        for key, val in dicoT.items():
            c = c.replace(key, val)
        ncols.append(c)

    return ncols


class UnigeData2:
    def __init__(self, course, rdir):
        """
        Contient les infos de la base de données d'un cours de façon
        relativement organisé.
        - rdir est le dossier parent au dossier des cours contenant les course en sql ou csv
        - course, c'est le nom du dossier mais aussi le nom de code du cours
        une fois charger essayer obj.df pour afficher les données

        """
        # used to simplify reduce name attributes
        self.Names = {
            "DQ": "discussion_questions",
            "DA": "discussion_answers",
        }
        self.others = {
            "CM": "course_memberships",
            "ID": "unige_course_user_ids",
            "U": "users",
        }
        # columns not used
        self.notUsedColNames = [
            "gender",
            "profile_lang",
            "browser_lang",
            "ctr_cd",
            "crt_id",
            "gp_id",
            "crs_id",
            "crs_module_id",
            "crs_item_id",
            "nancols",
            "dscAparent_dscAid",
            "user_join_ts",
            "region_cd",
            "employment_status",
            "educational_attainment",
            "student_status",
        ]

        self.AllNames = self.Names
        self.AllNames.update(self.others)
        self.course = course
        self.rdir = rdir
        self.df = pd.DataFrame()

        self.dialect = "coursera-postgres-format"
        csv.register_dialect(
            self.dialect,
            delimiter=",",
            doublequote=False,
            escapechar="\\",
            lineterminator="\n",
            quotechar='"',
        )

        # dictionnaire de traduction
        self.colT = {
            "_question_": "Q",
            "_questions": "Q",
            "_answer_": "A",
            "_answers": "A",
            "course": "crs",
            "membership": "mbs",
            "user_id": "uid",
            "discussion": "dsc",
            "answers_": "aw",
            "created_ts": "_cts",
            "updated_ts": "_uts",
            "group": "gp",
            "country": "ctr",
            "context": "ctx",
            "unige_": "U",
            "reported_or_inferred_": "",
            "language_cd": "lang",
            "droits_de_lhomme": "ddl",
            "understanding_financial_markets": "ufm",
        }
        self.rdir = Path(rdir)

    def humanizing_ids(self, table):
        """Humanizing ID and anonymisation."""
        logging.info(f"humanizing ID columns.")

        # humanize ID columns
        IDS = table["ID"].unstack().reset_index(drop=True)
        uidDicoT = uid_humanize_dico(IDS, maxlen=12, idtype="uid")

        disDicoT = uid_humanize_dico(
            pd.concat([table["DA"].dscQid, table["DQ"].dscQid]), maxlen=7, idtype="D",
        )

        for k in list(set(table.keys()) - {"ID"}):
            for c in table[k]:
                # pour chaque colonnes des tables k (toutes sauf ID)
                # on remplace les contenus par des contenus aléatoire si
                # la colonne est l'une des trois suivante, sauf si uidonly
                if "uid" in c:
                    logging.debug(f"Changing {k, c}")
                    table[k][c] = table[k][c].apply(lambda x: uidDicoT[x])

                elif "dscQid" in c:
                    logging.debug(f"Changing {k, c}")
                    table[k][c] = table[k][c].apply(lambda x: disDicoT[x])

                elif "id" in c:
                    # en général le id vient à la fin
                    suffix = re.sub(r"_?id", "", c).split("_")[-1]
                    dico = uid_humanize_dico(
                        table[k][c], maxlen=6, idtype="_" + suffix.upper(),
                    )
                    logging.debug(f"Changing {k, c}")
                    table[k][c] = table[k][c].apply(lambda x: dico[x])

        # On sauvegarde la traduction dans ID (que 2 colonnes)
        assert (
            "ID" in self.others
        ), f"La suite du traitement repose sur la présence de la table ID"

        bk_cols = table["ID"].columns
        table["ID"].columns = [f"{c}_raw" for c in bk_cols]
        for c in bk_cols:
            table["ID"][c] = table["ID"][f"{c}_raw"].apply(lambda x: uidDicoT[x])
        logging.debug(f'table["ID"].columns={table["ID"].columns}')

        return table

    def parsing_date(self, table, astimestamp=True):
        """Given a dictionnary of table, parse their time columns"""
        for tbid in table:
            for col in table[tbid].columns:
                match = re.compile(".*(_|u|c)ts").search(col)
                if match is not None:

                    logging.info(f"Parsing date {col} of table {tbid}")

                    # str -> pd.Timestamp
                    table[tbid].loc[:, col] = pd.to_datetime(table[tbid].loc[:, col])

                    # pd.Timestamp rounded to seconds
                    table[tbid].loc[:, col] = (
                        table[tbid].loc[:, col].apply(lambda d: d.round("s"))
                    )

                    if astimestamp:
                        # pd.Timestamp -> float
                        table[tbid].loc[:, col] = (
                            table[tbid].loc[:, col].apply(pd.Timestamp.timestamp)
                        )

        return table

    def load_df(self, humanize_: bool = False):
        """
        Charge les données d'un cours depuis plusieurs fichiers contenus dans AllNames
        et le stocke dans une table

        """
        table = {}

        for (code, tbname) in self.AllNames.items():

            fname = self.rdir.joinpath(self.course).joinpath(f"{tbname}.csv")
            logging.info(f"Reading {fname}")

            table[code] = pd.read_csv(filepath_or_buffer=fname, dialect=self.dialect)
            table[code].columns = translate(table[code], self.colT)
            table[code].index.name = translate([tbname], self.colT)[0]

            # drop columns we wont use
            notUsedColNames = set(self.notUsedColNames) & set(table[code].columns)
            table[code] = table[code].drop(columns=notUsedColNames)

        # maintenant que tout est dans la table on format les diff. types

        if humanize_:
            table = self.humanizing_ids(table)

        # parsing time from str to ts
        table = self.parsing_date(table, astimestamp=True)

        # on regroupe toutes les tables dans une dataFrame
        df = self.merge_tables(table)

        # Le champs réponses des questions qui n'ont par défaut rien dedans
        # sont remplis avec le titre de la question
        df = self.copier_lesQ_dans_lesA(df)

        # on peut avoir plusieurs fois le même utilisateurs avec différent rôle
        # LEARNER, TUTEUR, ect.. On ne garde que son dernier role
        try:
            df = df.loc[df.groupby("dscAid").crs_mbs_ts.idxmax()]
        except ValueError as ex:
            # import ipdb;  ipdb.set_trace()
            raise (ex)

        df.index = pd.Index(range(len(df)))

        self.df = df

        return self

    def merge_tables(self, table):
        """Rassemble en un block les tables qui sont dans table."""
        logging.info(f"Merging tables {table.keys()}")
        DQ, CM, U, DA, ID = (
            table["DQ"],
            table["CM"],
            table["U"],
            table["DA"],
            table["ID"],
        )
        try:
            df = (
                ID.merge(U, left_on="Uuid", right_on="Uuid", suffixes=("", "_U_drop"),)
                .merge(
                    DQ, left_on="Uuid", right_on="Udscs_uid", suffixes=("", "_DQ_drop"),
                )
                .merge(
                    DA,
                    how="outer",
                    left_on="dscQid",
                    right_on="dscQid",
                    suffixes=("", "_DA"),
                )
                .merge(CM, left_on="Uuid", right_on="Uuid", suffixes=("", "_CM_drop"),)
            )
        except KeyError as ke:
            D = {c: table[c].columns for c in ["ID", "U", "DQ", "DA"]}
            logging.warning(f"columns = {D} ")
            raise (ke)

        df = df.drop(
            columns=[c for c in df if c.endswith("_drop")]
            + ["Uuid", f"{self.course}_uid", f"{self.course}_uid"]
        )
        return df

    def copier_lesQ_dans_lesA(self, df):
        """Remplit le champs de données des Réponses des questions en général vide."""
        logging.info(f"filling holes in the answer table")
        T = ("dscAcontent", "dscQdetails")
        mask = df[T[0]].isna()
        df.loc[mask, T[0]] = df.loc[mask].loc[:, T[1]]

        #
        T = ("Udscs_uid_DA", "Udscs_uid")
        mask = df[T[0]].isna()
        df.loc[mask, T[0]] = df.loc[mask].loc[:, T[1]]

        # pour les question sans titre (exceptionnel)
        # en mettre un par défaut
        T = ("dscQtitle", "dscQtitle")
        mask = df[T[0]].isna()
        df.loc[mask, T[0]] = df.loc[mask].loc[:, T[1]].apply(lambda x: "Sans titre")

        cols = ["id", "_cts", "_uts"]
        for c in cols:
            mask = df.loc[:, f"dscA{c}"].isna()
            df.loc[mask, f"dscA{c}"] = df.loc[mask].loc[:, f"dscQ{c}"]
        return df

    def prepare_text(self, ngramR=1, stopWlist="english", basedir=None):
        """
        Attention change la df, créer plusieurs colones avec des (features du text)
        'lang, tokens, nb token long bigest token, bigest token text, img, code,
        contact, links\n
        tokenize = n for ngrams, 0 will not tokenize\n
        stopWlist détermine si on excluse les stop words de langue
        stopWlist (default english)
        """

        # func to translate original columns names
        # on complète le tableau
        msgCol = fcol("discussion_answer_content")

        mask = self.df[msgCol].isna()
        for col in [
            fcol("discussion_answer_parent_discussion_answer_id"),
            fcol("discussion_answer_id"),
        ]:
            self.df.loc[mask, col] = self.df.loc[mask, fcol("discussion_question_id")]

        self.df.loc[mask, msgCol] = self.df.loc[
            mask, fcol("discussion_question_details")
        ]
        # self.df.index = pd.Index(range(len(self.df)))

        if basedir is None:
            basedir = self.rdir
        # Tokenize text
        if ngramR:
            self.df = tokenize_text(self.df, ngramR, stopWlist, textCol=msgCol,)

        return self.df
