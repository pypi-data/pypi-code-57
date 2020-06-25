# -*- coding: utf-8 -*-
"""
Quelques outils pour le code de LSA et NMF qui cherche à guider un modèle de génération
de topiques avec les discussion (lieu) où sont publié les messages
"""

from scipy.sparse import csc_matrix, csr_matrix
from sklearn.decomposition import TruncatedSVD, NMF
import logging
import numpy as np
import pandas as pd
from typing import List

from KolaViz.Lib.fnames import read_pickle, load_model


def rowNormalizer(X_, ndigits=10):
    """
Normalize the row of X, use X.T to do if for columns. by default round to ndigitis
    """
    # keep sparse matrice. Beaucoup plus rapide

    # slicing (per row) should be faster with transpose if csc format
    X = X_.T if isinstance(X_, csc_matrix) else X_
    if isinstance(X, (csc_matrix, csr_matrix)):
        colIDs, rowIDs, data = [], [], []
        for rowID, row in enumerate(X):
            rawRow = row / row.sum()
            colIDs += list(rawRow.indices)
            rowIDs += [rowID] * len(rawRow.indices)
            data += list(rawRow.data)
        Xn = csr_matrix((data, (rowIDs, colIDs)), X.shape)
    else:
        Xn = np.empty(X.shape)
        for rowID, row in enumerate(X):
            Xn[rowID] = row / row.sum()
            print(f"i={rowID}/{X.shape[0] - 1} done.", end="\r")

    return Xn.T if isinstance(X_, csc_matrix) else Xn


def mydtypes(df: pd.DataFrame):
    """
    describe the types of the df.  this is different from df.dtypes() because
    we test object types in more detail.
    if the df.dtypes is an np.dtypes('O') we test the type of each serie elements.
    If more than one we return random elements as an illustration
    """
    baseDescription = df.dtypes
    D = {}
    for k, v in dict(baseDescription).items():
        if v == np.dtype("O"):
            val = set(df[k].apply(type).values)
            if len(val) > 1:
                D[k] = {tval: pick_rnd_type_elt(df, col=k, type_=tval) for tval in val}
            else:
                D[k] = val

        else:
            D[k] = v
    return pd.Series(D)


def pick_rnd_type_elt(df, col, type_):
    """
    returns a random element of type type from df.col
    """
    elts = [v for v in df[col] if isinstance(v, type_)]
    return np.random.choice(elts, size=1)[0]


def dtypes(s: pd.Series):
    """
describe the types of the s.
    """
    return s.dtypes


def ram_requirement(dico, num_topics=200):

    req = {
        "for U": 8 * len(dico) * num_topics * 3,
        "for V": 8 * dico.num_doc * num_topics * 3,
    }

    return [f"{k}: ~{int(v / 10e6)}MB" for k, v in req.items()]


def stringToList(chaine):
    """
    Used when loading data, from json. and liste where coerced as strings
    """
    return chaine[2:-2].split("', '") if isinstance(chaine, str) else chaine


def trim_low_freq_tokens(tokdoccount, docs, below_th=2):
    """
bth below_threshold, tokCount a dictionnary or pd.Serie
    Returns a pd Series with tokens count <= bth removed
    """
    return trim_freq_tokens_(tokdoccount, docs, cond="<", th=below_th)


def trim_high_freq_tokens(tokdoccount, docs, above_th=2):
    """
ath above_threshold, tokCount a dictionnary or pd.serie
    Returns a pd Series with token count >= ath removed
    """
    return trim_freq_tokens_(tokdoccount, docs, cond=">", th=above_th)


def trim_freq_tokens_(tokdoccount, corpus, cond="<", th=2):
    """
trim out values of the multiIndex pd.Series todoccount that satify the cond
    - tokdoccount multi-index should contain the toke and
    Returns a pd Series with token count >= ath removed
    """
    tokSCount = (
        pd.Series(tokdoccount).sort_values()
        if isinstance(tokdoccount, dict)
        else tokdoccount
    )

    # setting threshold depending on its type.
    # We consider the lengths of the whole corpus or raw_count
    th = len(corpus) * th if th < 1 and th > 0 else th
    return tokSCount[tokSCount > th] if cond == "<" else tokSCount[tokSCount < th]


def trim_freq_docs(tokdoccount, docs, cond="<", th=2):
    """
Returns the docs with docs no satifying the condition removed
    """
    tokSCount = (
        pd.Series(tokdoccount).sort_values()
        if isinstance(tokdoccount, dict)
        else tokdoccount
    )

    th = len(docs) * th if th < 1 and th > 0 else th
    return tokSCount[tokSCount > th] if cond == "<" else tokSCount[tokSCount < th]


def trim_freq_tokens(tokdoccount: pd.Series, docs, seuil_bas=2, seuil_haut=0.5):
    """
    Remove from the serie (or dict) tokdoccount tokens appearing in less than seuil_bas
    and more than seuil_haut documents.
    seuil_bas et seuil_haut can be int or float. if float,
    they are taken as % of documents
    - return: the trimed pd.Series
    """
    trim_bas = trim_low_freq_tokens(tokdoccount, docs, below_th=seuil_bas)
    trim_bas_haut = trim_high_freq_tokens(trim_bas, docs, above_th=seuil_haut)
    return trim_bas_haut


def vectorize(docs: pd.Series, tok2id, tokCount, mgfTok, count="tfidf"):
    """

    - tok2id a dictionary of tokens to id
    - tokCount, un dictionnaire comptabilisant le nombre de token dans le corpus
    - mgfTok, un dictionnaire comptabilisant le nombre de token dans le documents
    et les corpus (double clef)
    - docs: une liste de documents sous forme de bag of words
    - count: tfidf (default) should be 'tf' 'tfidf' or ''.
    C'est la façon de remplir la matrice
    returns: the vectorised sparse matrix of shape (nb_token, nb_documents)
    and a liste of docLenght and
    """
    # Doing the matrix count
    num_tok = len(tok2id.keys())
    num_doc = len(docs)
    shape = (num_doc, num_tok)
    lenDocs: List[int] = []  # stores the documents length
    indices_: List[int] = []  # stores the column indices or token id in each doc
    data_: List[int] = []  # stores the repetition count of token in each doc

    indptr = np.zeros((num_doc + 1,), dtype=int)  # index pointer

    logging.info(f"Vectorizing {len(docs)} docs with {num_tok} meaningfull tokens...")
    for rowID, (docID, doc) in enumerate(docs.items()):
        print(f"Vectorizing: {rowID}/{num_doc}", end="\r")

        # ! attention tokid can be 0
        dicoTok = [t for t in doc if tok2id.get(t, -1) >= 0]
        #        import ipdb; ipdb.set_trace()

        colIDs = [tok2id[token] for token in dicoTok]
        ldoc = len(colIDs)
        lenDocs += [ldoc]
        indptr[rowID + 1] = indptr[rowID] + ldoc
        indices_ += colIDs

        if count == "tfidf":
            data_ += [
                tokCount[(docID, tok)] / ldoc * np.log(num_doc / mgfTok[tok])
                for tok in dicoTok
            ]
        elif count == "tf":
            data_ += [tokCount[(docID, tok)] / ldoc for tok in dicoTok]
        else:
            data_ += [tokCount[(docID, tok)] for tok in dicoTok]

    docCountM = csr_matrix((data_, indices_, indptr), shape=shape)

    return docCountM, lenDocs


def vectorizing_docs_from_(D, count="tfidf"):
    """
    Short cut to vectorizing using the dico object
    """
    extraD = D.build_with_extra()
    kwargs = {
        "tok2id": D.build_conversion_dicos()["tok2id"],
        "tokCount": D.rawDic_,  # tok count per doc
        "mgfTok": D.mgfTok,
    }

    return vectorize(extraD["mgfDoc"], count=count, **kwargs)


def get_reduced_M(svd, M, docindex, colbasename="d"):
    """
Returns the topics (ie the dot product of doc and eigvectors) for each document in M
    from M of shape (n,p) we get N of shape (n, svd.n_components)
    """
    topicData = np.zeros((len(docindex), svd.n_components))

    for i, idx in enumerate(docindex):
        #        print(f"{i / len(docindex) * 100:.0f}% doc done.", end="\r")
        # par defaut are dtype('float64')
        topicData[i] = np.dot(M[i].todense(), svd.components_.T)

    cols = [f"{colbasename}{i}" for i in range(svd.n_components)]

    return pd.DataFrame(data=topicData, index=docindex, columns=cols)


# -*- coding: utf-8 -*-


def get_model(model, dirname="./Data", reduxdims=2, **kwargs):
    """
    load an model ("svd" or "nmf") from modelref (a filename or a préprocessed model)
    if present.  or reinit it with dimension of reductiong given by reduxdims
    """
    assert (
        model is not None
    ), f"You should pass a model either as modelinstance, filename or modelclasse name"

    # first as modelclass name
    if model == "TruncatedSVD":
        modelEng = TruncatedSVD
    elif model == "NMF":
        modelEng = NMF
    elif isinstance(model, (NMF, TruncatedSVD)):
        # here we don't do much, just return the model
        return model
    else:
        # loading from a file
        logging.info(f"Loading {model} from {dirname}")
        return load_model(model, dirname)

    logging.info(f"Initialisation of a {model} with n_components={reduxdims}.")
    return modelEng(n_components=reduxdims, **kwargs)


def get_svd(ref=None, dirname="./Data", n_components=2, **kwargs):
    """
shorthand for get_model if NMF requested
    """
    return get_model(ref, dirname, reduxdims=n_components, **kwargs)


def get_svdXfit(
    xfitref=None,
    dirname="./Data",
    D=None,
    count="tfidf",
    svdref=None,
    n_components=2,
    **kwargs,
):
    """
short hand if SVD in wanted see get_modelXfit
    """
    return get_modelXfit(
        model=svdref,
        xfitref=xfitref,
        dirname=dirname,
        D=D,
        count=count,
        reduxdims=n_components,
        **kwargs,
    )


def get_modelXfit(
    model=None, xfitref=None, dirname="./Data", D=None, count="tfidf", reduxdims=2,
):
    """
tries to load data from disk but if not present recomputes it.
    - xfitref (def. None): if given, should the file name of svd model saved
    on the disk.  If not present will recompute the SVD.
    - dirname (def. './Data')
    - D (def. None): a Dico object
    - count (def. 'tfidf'): how to compute vectorized matrix entries
    - svdref (def. None): ...
    - reduxdims (def. 2):  # target dimension for the reduced Matrice

    Given a M (n,p) and reduxdims (r) returns, A (n, r) B (r, p)
    and the model choosen in model
    if loading from file not fully implemented

    """

    if xfitref is None:
        logging.info(f"Rebuilding X_fit for {model} in {reduxdims} reduced dims.")
        assert (
            D is not None and model is not None
        ), f"Since xfitref is None need to pass a Dico object as D to vectorize\
        the corpus and a model but {{k: k is None for k in ['model', 'D']}}"

        X, docLens = vectorizing_docs_from_(D, count=count)
        model = get_model(model, dirname=dirname, reduxdims=reduxdims)

        return model.fit_transform(X), model.components_, model
    else:
        logging.warning(f"Ignoring {model} and loading a saved X_fit from {xfitref}")
        X_fit = read_pickle(xfitref, dirname)
        return X_fit, None, None


def get_nmfXfit(
    xfitref=None,
    dirname="./Data",
    D=None,
    count="tfidf",
    nmfref=None,
    n_components=2,
    **kwargs,
):
    """
short hand to fit using nmf
    """
    return get_modelXfit(
        model=nmfref,
        dirname=dirname,
        D=D,
        count=count,
        reduxdims=n_components,
        **kwargs,
    )


def coerce_string2number(chaine):
    """
    Essaye de transformer une chaine en nombre.
    Renvois le nombre si succès, Sinon renvois la chaine
    """
    return pd.to_numeric(chaine, errors="ignore", downcast="integer")


def is_numeric(arg):
    """
tests is nombre is numeric
    """
    try:
        # handle 0
        return pd.to_numeric(arg, errors="raise") == arg
    except Exception:
        return False
