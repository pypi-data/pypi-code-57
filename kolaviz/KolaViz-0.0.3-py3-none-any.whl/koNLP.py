#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Main File with NLP outils for kolaViz project # ## Computing topics."""
from pathlib import Path
import argparse
import logging
import os

from typing import Tuple, Sequence, Optional, Dict, Any, Union
from pandas import (
    DataFrame,
    IndexSlice,
    read_pickle,
    read_csv,
    Series,
    concat,
)
import pickle
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import TruncatedSVD

from KolaViz.Lib.model import TOK_INFLUENCIAL_NUM
from KolaViz.Lib.nlpDico import Dico
from KolaViz.Lib.outilsKoNLP import (
    stringToList,
    vectorizing_docs_from_,
    get_reduced_M,
)

xs = IndexSlice


def main():
    """
    Process arguments and call main methodes to load data from DB, harmonize it,
    tokenize it, vectorize it and clusterize it
    """
    args = parse_arguments()

    # data loader
    docs = loading_harmonized_data(
        args.fname, args.lang, course_=args.course.split("_")
    ).apply(stringToList)

    # building full Dico
    D = Dico(docs)

    # il manque la dico D
    _ = D.build_with_extra()

    # vectorizing
    M, docLens = vectorizing_docs_from_(D, count="tfidf")

    # dim reduction
    logging.info("Truncating")
    Mred, svd = truncate(M, main_dico=D, n_components=args.nreduce)
    save(model=svd, tof=args.svdfo)

    logging.info("Clustering")
    km = clustering(Mred, n_clusters=args.ncluster)
    save(model=km, tof=args.kmfo)

    logging.info("**** KoNLP Finished ****")


def read_with_extension(fname):
    """
    Select the correct method to read the file in fname based on extension.
    Default to csv.
    -- Returns the dataframe read
    """
    fname = Path(fname)
    ext = fname.suffix

    if ext == ".pkl":
        df = read_pickle(fname)
    else:
        # pourquoi Unnamed: 2 ?? trop d'appriori sur la structure du fichiers csv
        df = (
            read_csv(fname)
            .set_index(["course", "mooc", "Unnamed: 2"])
            .reorder_levels(["Unnamed: 2", "course", "mooc"])
        )
    df.index.names = ["msgID", "course", "mooc"]
    return df


def loading_harmonized_data(
    fname_, lang_: str = "en", course_="ufm_c18", data_: Optional[DataFrame] = None,
) -> DataFrame:
    """
    Charge le fichier de données TOKENIZÉ dans une dataframe et n'en garde que les
    message appartenant à lang et course
    """

    course = course_.split("_") if isinstance(course_, str) else course_

    if data_ is None:
        logging.debug(f"Reading data from {fname_}")
        df = read_with_extension(fname_)
    else:
        logging.info(
            f"Copying data from {type(data_), data_.shape}"
            f" instead of loading the file={fname_}"
        )
        df = data_

    # import ipdb; ipdb.set_trace()

    # une slice qui dépend de course
    slc = xs[:, :, :] if course == "all" else xs[:, course]

    df = df.loc[slc, :].reset_index(level=[1, 2], drop=False)

    res = df if lang_ == "all" else df.loc[df.lang == lang_]

    logging.info(
        f"Keep {res.shape} {lang_} from {df.shape} {course} rows"
        f" of data with dims {data_.shape if data_ is not None else 'aucune'}"
    )
    logging.debug(f"Keeping columns {res.columns}")

    return res


def simple_dico_loading(docs_: Sequence, verbose_: bool = False) -> Tuple[Dico, Series]:
    """
    Charge simplement un dictionnaire en initialisant au minimun.
    - docs_:  une liste de documents

    Return: un tuple
    D (Dico object) et dico (raw_dico)
    """

    D = Dico(docs_, verbose=verbose_)

    # appel pour etre construit simplement
    raw_dico = D.build_raw_dico(rType_="pd.Series")

    return D, raw_dico


def loading_dicos(docs):
    "charge les différents dico en mémoire"
    D, raw_dico = simple_dico_loading(docs)
    _ = D.build_with_extra()
    return D, D.id2tok, D.tok2id


def truncate(M, main_dico, n_components=100):
    """
    Reduce the matrix M selon une SVD truncated
    """
    svd = TruncatedSVD(n_components=n_components, n_iter=7)
    svd.fit(M)
    logging.info(
        f"Total var explained with {n_components}: {sum(svd.explained_variance_ratio_)}"
    )
    reduced = get_reduced_M(svd, M, docindex=main_dico.docs.index)

    return reduced.values, svd


def clustering(rM, n_clusters=5):
    km = MiniBatchKMeans(
        n_clusters=n_clusters,
        init="k-means++",
        n_init=1,
        init_size=2000,
        batch_size=2000,
        verbose=False,
    )
    logging.info(f"Clustering sparse data with {km}")
    _ = km.fit(rM)
    return km


def load(model, fromf):
    """
    write a pickled version fo model to file byte stream

    """
    # koNLP.py:172: error: Argument 1 to "load" has incompatible type "bytes"; expected "IO[bytes]"
    # koNLP.py:172: error: Argument 1 to "read" of "IO" has incompatible type "BinaryIO"; expected "int"
    with open(fromf, "rb") as f:
        model = pickle.load(f.read(f))

    return model


def save(model, tof=""):
    """
    write a pickled version fo model to file byte stream
    """
    if tof:
        logging.info(f"Saving a model to {tof}")
        with open(tof, "wb") as f:
            pickle.dump(model, f)


ids = IndexSlice

# influencial_tokens_ids(H, nTokens_=10).loc[ids[:, 'tokID'], :]


def influencial_tokens(
    dico_: Dico,
    topMatrix_: np.array,
    topNum_: Optional[int] = None,
    nTokens_: int = TOK_INFLUENCIAL_NUM,
    ascending_=False,
    show_weights_=False,
) -> Union[Series, DataFrame]:
    """
    Renvois les tokens influents dans la topMatrix_
    """
    influencialTok = influencial_tokens_ids(
        topMatrix_, topNum_=topNum_, nTokens_=nTokens_, ascending_=ascending_,
    )
    influencialTokIDs = influencialTok.loc[ids[:, "tokID"]]

    def get_toks_from_ids(aList_: list):
        return [dico_.id2tok[i] for i in aList_]

    res = DataFrame(influencialTokIDs.apply(get_toks_from_ids))
    res.columns = ["iTokens"]

    if show_weights_:
        influencialTokStg = influencialTok.loc[ids[:, "tokStg"]]
        res = concat([res, influencialTokStg], axis=1)
        res.columns = ["iTokens", "strength"]
        res.index.name = "topic#"

    return res


def influencial_tokens_ids_(
    topVector_: np.array, nTokens_: Optional[int] = None, ascending_=False,
) -> Dict[Any, Any]:
    """
    Return the nTokensid_ most influencial (id where topVector[id] is the greatest)
    """
    orientation = 1 if ascending_ else -1
    sort = np.argsort(topVector_)[::orientation]

    influencialTokenIDs = sort[:nTokens_] if nTokens_ else sort

    tokTopicStrength = np.round(topVector_ / topVector_.sum() * 100, 1)

    influencialStrength = tokTopicStrength[influencialTokenIDs]

    return {
        "tokID": influencialTokenIDs,
        "tokStg": influencialStrength,
    }


def influencial_tokens_ids(
    topMatrix_: np.array,
    topNum_: Optional[int] = None,
    nTokens_: int = TOK_INFLUENCIAL_NUM,
    ascending_=False,
) -> DataFrame:
    """
    Return a topic most influencial words
    """

    if isinstance(topNum_, int):

        assert topNum_ < topMatrix_.shape[0], (
            f"Il n'y a pas de topique avec ce numéro {topNum_}, nb max thèmes"
            f"{topMatrix_.shape[0]}"
        )

        return DataFrame(
            {
                topNum_: influencial_tokens_ids_(
                    topMatrix_[topNum_], nTokens_, ascending_
                )
            }
        ).unstack()

    elif topNum_ is None or isinstance(topNum_, list):

        idx = range(topMatrix_.shape[0]) if topNum_ is None else topNum_
        res = {}

        for i, topVec in enumerate(topMatrix_[idx]):
            res[i] = influencial_tokens_ids_(topMatrix_[i], nTokens_, ascending_)

        return DataFrame(res).unstack()

    else:
        raise Exception(f"Check topNum_={topNum_}")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Programme pour faire un LSA sur les données de l'UNIGE"
    )

    nDimReduce_dft = 500
    nDimReduce_hlp = (
        f"The number of dimension for the truncation of SVD should be "
        "less than token count (or num_features). "
        "Default = {nDimReduce_dft}"
    )

    nCluster_dft = 1000
    nCluster_hlp = (
        f"The number of groups of documents to find.  Can be like the"
        "number of thread or a lot less. Default ({nCluster_dft})"
    )

    svdfo_dft = "./Data/svd.pkd"
    svdfo_hlp = (
        f"The file path to save the svd model.  Default ({svdfo_dft})"
        "Set to the empty string to not save"
    )

    kmfo_dft = "./Data/km_cluster.pkd"
    kmfo_hlp = f"The file path to save the km model.  Default ({kmfo_dft})"

    parser.add_argument(
        "-r", "--nreduce", type=int, default=nDimReduce_dft, help=nDimReduce_hlp,
    )
    parser.add_argument(
        "-c", "--ncluster", type=int, default=nCluster_dft, help=nCluster_hlp,
    )
    parser.add_argument(
        "-s", "--svdfo", type=str, default=svdfo_dft, help=svdfo_hlp,
    )

    parser.add_argument("-k", "--kmfo", type=str, default=kmfo_dft, help=kmfo_hlp)

    logLevel_dft = "INFO"
    logLevel_hlp = f"Log level (def. {logLevel_dft})"
    parser.add_argument(
        "-L", "--logLevel", default=logLevel_dft, help=logLevel_hlp,
    )

    return parser.parse_args()


def main_prg():
    """Parse arguments and run the main function."""
    args = parse_arguments()

    LOGFMT = "/%(filename)s@%(lineno)s@%(funcName)s/ %(message)s"
    logging.basicConfig(level=args.logLevel, format=LOGFMT)
    logging.info(f"Running with: {os.sys.version}")

    main()


if __name__ == "__main__":
    main_prg()
