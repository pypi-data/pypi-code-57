# -*- coding: utf-8 -*-
"""
 Object Dictionnaire
"""
import logging
import functools
from collections import OrderedDict as odict
from typing import Union, Any, Dict, Tuple
import pandas as pd

from KolaViz.Lib.outilsKoNLP import trim_freq_tokens
from KolaViz.Lib.model import STOPWORD_DIR


def check_for_rebuild(objk=None):
    """
    Check if the class attribute getattr(class, objk) is None and rebuild it if
    rebuild==True else returns cached object.
    """

    def wrapper_of(F):
        @functools.wraps(F)
        def wrapped_F(self, *args, **kwargs):
            nonlocal objk
            # how do I get the instance Class of Method F (self) ??
            obj = getattr(self, objk, None)
            # TODO            print(f"{args}, {kwargs}, {self}, {obj}")
            # régler le pb de non passage des args
            rebuild = kwargs.get("rebuild")

            if not rebuild and obj is not None:
                logging.info(f"Rebuild={rebuild}.  Using the cached 'self.{objk}'.")
                return obj

            res = F(self, *args, **kwargs)
            return res

        return wrapped_F

    return wrapper_of


class Dico:
    # mgf stand for mgf
    def __init__(self, docs: pd.Series, rType="pd.Series", verbose=None):
        """
        Initialise un dictionnaire avec une series de docs dont l'index est docID et
        la valeurs les tokens du docs.
        L'objet Dico contient les documents (.docs), les tokens, le count des tokens
        par documents et en général dans le corpus.
        - .mgfTok contient les tokens qui par défaut ne sont pas dans plus de 50% des
        documents et au moins dans deux.
        - .id2tok et .tok2id sont des dictionnaires pour passer des id de token au
        token eux même.
        - .repiDico !! A recoder !! ...garde en mémoire les répétitions de mots

        **Les extras**:
            - allTokens": self.allTokens,
            - "tokCorpCount": self.tokCorpCount,
            - "mgfTok": self.mgfTok,
            - "allTokens": self.allTokens: non filtered tokens
            - "rareCorpTok": self.tokCorpCount[self.tokCorpCount < 2],
            - "rareDocTok": self.mgfTok[self.mgfTok < 2],
            - "notRareCorpTok
            - "mgfDico":  c'est le dico des token, tokenid, tokendoc count fait
        uniquement avec les token mgf
            - "mgfDoc":  c'est les docs avec des tokesn mgf
            - "boid_corpus": bag of id corpus

        Keyword Arguments:
        docs -- une liste de documents d'où extraire un dictionnaire de tokens
        """
        self.docs = docs
        self.mgfDoc = None

        self.rawDic_ = None
        self.mgfDico = None

        self.rawTok_ = None
        self.mgfTok = None
        self.mgfCorpTok = None

        self.extra_ = None
        self.docCountTok = None
        self.bow_corpus = None
        self.boid_corpus = None
        self.num_rdocs = len(docs)
        self.num_mdocs = None  # documents with at least one meaning full tokens
        self.num_rtoks = None  # raw toks
        self.num_mtoks = None  # meaning_full toks

        self.id2tok = None
        self.tok2id = None
        self.repiDico = None
        # to log additionnal info while building the dictionnaries
        self.verbose = False if verbose is None else verbose

    def __repr__(self):
        EMPTY = "Not initialisé."

        def get_sa(funkey, opt=EMPTY):
            """
            get self attribute
            """
            return getattr(self, funkey, opt)

        extra_ = get_sa("extra_", False)
        id2tok = get_sa("id2tok", False)
        tok2id = get_sa("tok2id", False)

        toDisplay = {
            "# documents avec du sens": get_sa("num_mdocs"),
            "# documents brutes": get_sa("num_rdocs"),
            "# tokens brutes": get_sa("num_rtoks"),
            "# tokens avec du sens": get_sa("num_mtoks"),
            "L'initialisation de id2tok": "Initialisé" if id2tok else EMPTY,
            "L'initialisation de tok2id": "Initialisé" if tok2id else EMPTY,
            "Les extras": extra_.keys() if extra_ else EMPTY,
            "# raw tokens par doc pour tous raw docs...\n": get_sa("rawDic_"),
        }

        Keys = [
            "# documents brutes",
            "# documents avec du sens",
            "# tokens brutes",
            "# tokens avec du sens",
            "L'initialisation de id2tok",
            "L'initialisation de tok2id",
            "Les extras",
            "# raw tokens par doc pour tous raw docs...\n",
        ]
        rep = "Object: >>>> Dico <<<<\n"

        for k in Keys:
            rep += f"{k}: {toDisplay[k]}\n"

        return rep

    def get_num_rdocs(self):
        """
        Returns the number of documents in the corpus
        """
        return len(self.docs)

    def get_num_mdocs(self):
        """
        Returns the number of documents in the corpus containing some meaning
        full tokens
        """
        if self.mgfDoc is None:
            self.build_mgf_docs()
        return len(self.mgfDoc)

    def get_num_mtoks(self):
        """
        Returns the number of meaning full tokens in the corpus
        """
        if self.mgfTok is None:
            self.build_mgf_tokens()

        return len(self.mgfTok)

    def get_num_rtoks(self):
        """
        Returns the full number full tokens in the corpus, meaning_full or not
        """
        if self.rawTok_ is None:
            self.build_raw_tokens()

        return len(self.rawTok_)

    def get_mgf_tokens_in_corpus(self):

        if self.mgfDico is None:
            self.build_mgf_dico()

        self.mgfCorpTok = (
            self.mgfDico.groupby("mgfTok").rawTokCount.agg(sum).sort_values()
        )

        return self.mgfCorpTok

    def build_raw_tokens(self):
        """
        Returns alls the corpus tokens
        """
        if self.rawDic_ is None:
            self.rawDic_ = self.build_raw_dico()

        raw_tokens = self.rawDic_.index.get_level_values("tokens").unique()
        self.num_rtoks = len(raw_tokens)
        logging.info(f"{self.num_rtoks} tokens extracted from raw documents")
        return raw_tokens

    def build_bag_of_word_corpus(self):
        """
        Transforme le corpus des docs mgf en liste de liste de tuple (tokID,
        docTokCount).
        Un document est une liste de (word, docTokCount)
        """
        G = self.mgfDico.groupby(["docID", "mgfTok"]).agg(sum)
        self.bow_corpus = [
            list(zip(G.loc[i].index, G.loc[i].values.T[0])) for i in G.index.levels[0]
        ]
        return self.bow_corpus

    def build_bag_of_tokID_corpus(self):
        """
        Transforme le corpus des docs mgf en liste de liste de tuple (tokID,
        docTokCount).
        Un document est une lite de (tokID, docTokCount)
        """
        if self.bow_corpus is None:
            self.build_bag_of_word_corpus()
        if self.tok2id is None:
            self.build_conversion_dicos()

        self.boid_corpus = []
        for doc in self.bow_corpus:
            self.boid_corpus.append(
                [(self.tok2id[tok], int(count)) for tok, count in doc]
            )

        return self.boid_corpus

    def build_mgf_docs(self, mgfTok=None):
        """
        returns the docs from which unmgf tokens are exfiltered.
        """
        # filter out docs without any mgf tokens
        if self.mgfTok is None:
            self.build_mgf_tokens()

        # filter out tokens from docs
        self.mgfDoc = self.docs.apply(
            lambda doc: [t for t in doc if t in self.mgfTok.index]
        )

        # removing empty docs
        self.mgfDoc = self.mgfDoc[self.mgfDoc.apply(len) > 0]

        self.num_mdocs = len(self.mgfDoc)

        return self.mgfDoc

    def build_mgf_dico(self, mgfTok=None):
        """
        Build dico of meaning full tokens
        """
        if mgfTok is None:
            mgfTok = self.mgfTok.reset_index()
            mgfTok.index.name = "tokID"

        if self.rawDic_ is None:
            self.build_raw_dico()

        rawDico = self.rawDic_.reset_index()
        rawDico.index.name = "rawDico"

        self.mgfDico = (
            rawDico.merge(mgfTok, how="left", left_on="tokens", right_on="mgfTok",)
            .dropna()
            .drop("tokens", axis=1)
        )

        self.mgfDico.index.name = "mgfDico"

        return self.mgfDico

    @check_for_rebuild(objk="rawDic_")
    def build_raw_dico(
        self, rType_: str = "pd.Series", rebuild: bool = False
    ) -> Union[Dict[Tuple[Any, Any], int], pd.Series]:
        """
        Count the occurences of tokens in each document.
        - to get the tokens occurences in the whole corpus, one can groupby and sum on
        the index
        - to get the number of documents containing a token, one ca do the same too.
        check other extra dicos too
        - Returns a serie (or dict) with a pd.multi Index
        """

        rawTokCount = dict()

        for docID, docTok in self.docs.items():
            if self.verbose:
                # could use a test on logging.level instead of present
                print(
                    f"Processing docID {docID}/{self.docs.index.max()}(max)", end="\r",
                )
            for tok in docTok:
                rawTokCount[(docID, tok)] = rawTokCount.get((docID, tok), 0) + 1

        # a Serie with a mutli index, docID, tok and the number of count of token in
        # that document

        if rType_ == "pd.Series":

            self.rawDic_ = pd.Series(rawTokCount).sort_values()
            self.rawDic_.index.set_names(["docID", "tokens"], inplace=True)
            self.rawDic_.name = "rawTokCount"

        else:

            self.rawDic_ = rawTokCount

        # tokenizing in some ways
        self.build_raw_tokens()

        logging.info(f"{self.num_rdocs} docs used to build a raw_dico.")

        return self.rawDic_

    @check_for_rebuild(objk="extra_")
    def build_with_extra(self, rebuild=False):
        """
        Return:
        - the uniq tokens, les tokens. PAS forcement ceux qui apparaissent une fois
        - the token Corpus Count, le nombre de fois que le token apparait dans le corpus
        - the token Document Count, le nombre de documents qui contienent un token donné
        """

        if self.rawDic_ is None:
            self.build_raw_dico()

        tokCountG = self.rawDic_.groupby(level=1)  # groupy by token

        # count # tokens occurence in corpus
        self.tokCorpCount = tokCountG.agg(sum).sort_values()
        self.tokCorpCount.name = "tokCorpCount"

        # count # documents containing the each tokens
        self.docCountTok = tokCountG.count().sort_values()
        self.docCountTok.name = "docCountTok"

        # building construct more mgf
        seuil_bas = 2
        seuil_haut = 0.5

        self.mgfTok = self.build_mgf_tokens(
            self.docCountTok, seuil_bas=seuil_bas, seuil_haut=seuil_haut,
        )
        self.mgfCorpTok = self.get_mgf_tokens_in_corpus()
        self.mgfDico = self.build_mgf_dico()
        self.mgfDoc = self.build_mgf_docs()

        self.bow_corpus = self.build_bag_of_word_corpus()
        self.boid_corpus = self.build_bag_of_tokID_corpus()

        self.extra_ = {
            "tokCorpCount": self.tokCorpCount,
            "docCountTok": self.docCountTok,
            "mgfTok": self.mgfTok,
            "mgfCorpTok": self.mgfCorpTok,
            "mgfDico": self.mgfDico,
            "mgfDoc": self.mgfDoc,
            "bow_corpus": self.bow_corpus,
            "boid_corpus": self.boid_corpus,
            "rareCorpTok": self.tokCorpCount[self.tokCorpCount < seuil_bas],
            "rareDocTok": self.docCountTok[self.docCountTok < seuil_bas],
            "notRareCorpTok": self.tokCorpCount[self.tokCorpCount >= seuil_bas],
        }

        self.log_extra_info()

        return self.extra_

    def log_extra_info(self):
        logging.info("Extras of dictionnary built!")
        if not self.verbose:
            return None
        rareCorpTok = self.extra_["rareCorpTok"]
        rareDocTok = self.extra_["rareDocTok"]
        notRareCorpTok = self.extra_["notRareCorpTok"]
        _ = self.extra_["docCountTok"]

        if (
            len(rareCorpTok.index) == len(rareDocTok.index)
            and (rareCorpTok.index == rareDocTok.index).all()
        ):
            logging.info(
                f"{len(rareDocTok)} des {len(notRareCorpTok)}"
                "({len(notRareCorpTok)/len(docCountTok)*100:.0f}%) tokens apparaissant "
                "2 fois ou plus dans le corpus, apparaissent uniquement dans "
                "un même document.   Et ne servent donc (quantitativement) à rien pour "
                "discriminer les documents entre eux.  Il y a de plus {len(rareCorpTok)} "
                "({len(rareCorpTok)/len(docCountTok)*100:.0f}%) tokens uniques dans le corpus"
            )
        else:
            logging.info(
                f"Aucun des {len(notRareCorpTok)} "
                "({len(notRareCorpTok)/len(docCountTok)*100:.0f}%) tokens apparaissant "
                "2 fois ou plus apparaissent uniquement dans un même document.  Il y a "
                "par contre {len(rareCorpTok)} "
                "({len(rareCorpTok)/len(docCountTok)*100:.0f}%) tokens uniques dans le corpus"
            )

    def build_mgf_tokens(
        self,
        docCountTok,
        seuil_bas=2,
        seuil_haut=0.5,
        stopwordfile="normalUnige.txt",
        datadir=STOPWORD_DIR,
        rebuild=False,
    ):
        """
        Remove rare words based on seuil_bas and seuil_haut and the stopwordfile.
        Will look for the stopword file in the ./Data/Stopwords dir (default)
        Returns a dataframe of meaning full tokens order by doc count
        """
        # en cas d'absence du fichier le recherche dans les dossiers en dessous

        if not rebuild and self.mgfTok is not None:
            logging.info(f"Using cached mgfTokens")
            return self.mgfTok

        # Enlever les mots qui apparaissent dans moins de seuil_bas document et plus
        # de seuil_haut documents
        mgfTok = trim_freq_tokens(docCountTok, self.docs, seuil_bas, seuil_haut)

        # filtering stop words
        with open(f"{datadir}/{stopwordfile}") as f:
            stopWords = f.readlines()

        stopWords = [w.rstrip("\n") for w in stopWords]

        new_index = pd.Index(set(mgfTok.index) - set(stopWords))
        mgfTok = mgfTok.reindex(new_index).sort_values(ascending=False)
        mgfTok.index.name = "mgfTok"
        mgfTok.name = "docCount"

        self.mgfTok = mgfTok
        self.num_mtoks = len(mgfTok)

        return mgfTok

    def build_conversion_dicos(self):
        """
        Returns a dictionnary with converters between tokens and id in bag of word
        represenations, using only meangfull tokens
        """
        if self.mgfTok is None:
            logging.warning(
                f"Running build_mgf_tokens with default to populate the meaning full "
                "dictionnary"
            )
            self.build_mgf_tokens()

        # assert self.menaingFullTok is not None, f" You should explicitly run
        # get mgf_tokens first."

        id2tok = odict(self.mgfTok.reset_index()["mgfTok"])
        self.id2tok = id2tok
        self.tok2id = odict(zip(id2tok.values(), id2tok.keys()))
        return {"id2tok": self.id2tok, "tok2id": self.tok2id}

    def repetitions(self, rebuild=False):
        """
        build a df with general statistics on the corpus.  Especially word repetitions
        """
        if self.repiDico is not None and not rebuild:
            return self.repiDico

        df = pd.concat(
            [self.mgfTok, self.extra_["tokCorpCount"]], axis=1, sort=True, join="inner",
        )

        # tokens qui se répètent dans certains documents
        mask = df.apply(lambda c: c.docCount != c.tokCorpCount, axis=1)

        # taux de répétition à l'intérieur des documents.  Ce sont donc
        # les répétitions qui sont le plus caractéristiques des certains documents
        # où elles se répètent
        repetitions = (
            df[mask]
            .apply(lambda c: (c.tokCorpCount - c.docCount) / c.tokCorpCount, axis=1,)
            .apply(lambda x: round(x * 100, 2))
            .sort_values()
        )
        repetitions.name = "docRepetitions"

        repiDico = (
            df.merge(repetitions, how="outer", left_index=True, right_index=True,)
            .fillna(0)
            .reset_index()
        )
        repiDico.columns = ["token" if c == "index" else c for c in repiDico.columns]

        self.repiDico = repiDico
        return repiDico
