#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Script vectorise in parallele a corpus and run an NMF on it.

Point de départ vectorized data (or toknenized, or even harmonized) data
Save vectorised results on disk
"""

import argparse
import os
import logging
from pathlib import Path
from multiprocessing import Process, Queue, active_children
from typing import Optional
from pandas import DataFrame

from sklearn.decomposition import NMF
from sklearn.cluster import KMeans

from KolaViz.harmonisation_data import simpleIDs
from KolaViz.Lib.mlktypes import FNameT
from KolaViz.Lib.nlpDico import Dico
from KolaViz.Lib.fnames import (
    saving_NMF_data,
    read_pickle,
    prepare_vec_dft_names,
    as_tokenized,
)

from KolaViz.Lib.outilsKoNLP import (
    vectorizing_docs_from_,
    coerce_string2number,
    is_numeric,
    stringToList,
)
from KolaViz.koNLP import (
    loading_harmonized_data,
    simple_dico_loading,
    influencial_tokens,
)

from KolaViz.Lib.model import (
    COURSE_DFT,
    LOGLEVEL_DFT,
    VEC_ACTION_DFT,
    VEC_ALPHA_DFT,
    VEC_COUNT_DFT,
    VEC_FNAME_DFT,
    VEC_INDIR_DFT,
    VEC_L1RATIO_DFT,
    LANG_DFT,
    VEC_MAXITER_DFT,
    VEC_OUTDIR_DFT,
    TOK_PREFIX_DFT,
    VEC_REDUX_DFT,
    VEC_TOL_DFT,
    VEC_VERBOSE_DFT,
    ESSENTIALCOLS,
    TOK_OUTDIR_DFT,
)


def main_parallel(
    indir_: str = TOK_OUTDIR_DFT,
    outdir_: str = VEC_OUTDIR_DFT,
    prefix_: str = TOK_PREFIX_DFT,
    **kwargs_,
):
    """
    Run the main programme in parallelle for several files at onces
    - look at file in 'indir_' with 'prefix_'
    - save the result in 'outdir_'  ! DOES NOT WORK for now
    - Return: nothing but write on disk
    """

    # setting default

    indir = Path(indir_)
    outdir = Path(outdir_)

    # Creating output dir if does not exist

    if not outdir.exists():
        os.mkdir(outdir)

    # Getting names of files to process

    prefix = prefix_
    fnames = [indir.joinpath(f) for f in os.listdir(indir) if f.startswith(prefix)]

    fname = kwargs_.pop("fname_", "all")
    if fname != "all" and not is_numeric(fname):
        fnames = [Path(fname)]

    elif is_numeric(fname) and fname < len(fnames):
        fnames = fnames[:fname]

    elif fname != "all":
        _msg = f"Check fname={fname, type(fname)} while len(fnames)={len(fnames)}."
        raise Exception(_msg)

    # lancement du batch

    Q: Queue = Queue()

    kwargs_.update(
        {"comQ_": Q, "prefix_": f"{prefix}", "indir_": indir, "outdir_": outdir,}
    )

    for fname in fnames:
        kwargs_["fname_"] = fname
        p = Process(target=main_prl, kwargs=kwargs_)
        p.name = fname.stem  # en vu d'un log bien formaté
        p.start()

    for fname in fnames:
        load = Q.get()
        logging.info(
            f"Got load for '{load[1]}'. {len(active_children())} active children left."
        )

    return load


def main_prl(comQ_: Queue, fname_=None, **kwargs_):
    """
    Lancer en parallèle la fonction de vectorisation
    """
    logging.info(f"Process for {fname_} starting with {kwargs_}...")
    load = main(fname_=fname_, **kwargs_)
    comQ_.put(load)

    return None


def main(
    action_: str = VEC_ACTION_DFT,
    alpha_: Optional[float] = VEC_ALPHA_DFT,
    count_: Optional[str] = VEC_COUNT_DFT,
    course_: Optional[str] = COURSE_DFT,
    fname_: Optional[FNameT] = VEC_FNAME_DFT,
    indir_: Optional[FNameT] = VEC_INDIR_DFT,
    l1ratio_: Optional[float] = VEC_L1RATIO_DFT,
    lang_: Optional[str] = LANG_DFT,
    maxiter_: Optional[int] = VEC_MAXITER_DFT,
    outdir_: Optional[FNameT] = VEC_OUTDIR_DFT,
    prefix_: Optional[str] = TOK_PREFIX_DFT,
    redux_: Optional[int] = VEC_REDUX_DFT,
    tol_: Optional[float] = VEC_TOL_DFT,
    verbose_: Optional[bool] = VEC_VERBOSE_DFT,
    data_: Optional[DataFrame] = None,
    ngram_: Optional[int] = None,
    sentTok_: Optional[str] = None,
    wordTok_: Optional[str] = None,
):
    """
    LE but c'est d'avoir les textes vectorisé et catégorisés à l'aide d'une NMF.

    Les textes déjà tokenizé sont dans fname_.
    Le nom du fichier avec les données vectorisée est standardisé automatiquement
    à partir des arguments...
    - action, qui peut être:
      - build: récupère le fichier fname et build the vectors
      - read: lit les fichiers vectorisés qui sont déjà sur le disque dans outdir en
    utilisant les autres parametres
    pour construire le noms standardisé du fichier
      - save: sauvegarde les fichier vectorisé sur le disque dans outdir
    redux_: Int = The number of dimension de la troncation Default = 10
    verbose_: Bool = def. False,
    count_ = Façon de constuire la matrice de données lorsqu'il faut revectoriser.
    Les alternatives au défaut (def. 'tfidf')
    sont 'tf' ou 'count'
    tol_: The number below which the error has to go to stop the iterations.
    def. 1e-4
    maxiter_: The maximun number of iterations to reach convergence.  def. 300
    logLevel_ = Log level (def. 'INFO')
    fname_ = Nom du fichier de la matrice vectorisée à charger OU à sauvegarder
    si recomputing (def. None)
    ex ./Data-circuits/tokenized_{ng}ng_{st}st_{wt}wt.pkl
    ou nmf_{redux}n_{alpha}a_{l1ratio}l_{courseName}_....pkl
    alpha_ = Importance du terme de régulation (def. 0)
    l1ratio_ = Ratio de régularisation l1 (1) vs l2 (0), (def. 1)
    lang_ = à garder si on extrait les données à nouveau du doc (def. 'en').
    'all' pour tout garder
    course_ = Course à garder si on extrait à nouveau les données de la doc
    (def. 'ufm_c18'). 'all' pour tout garder
    (pas implémenté)

    """
    # build some defaults file names

    if fname_ is None:
        tokArgs = (ngram_, sentTok_, wordTok_, indir_, prefix_)

        assert all([x is not None for x in tokArgs]), (
            f"Si fname_ `{fname_}` n'est pas renseigné il faut"
            f" renseigné tous les {tokArgs}"
        )

        # on reconstruit fname à partir d'autre variables
        fname_ = as_tokenized(*tokArgs)

    kwargs = {
        "alpha_": alpha_,
        "course_": course_,
        "fname_": fname_,
        "l1ratio_": l1ratio_,
        "lang_": lang_,
        "outdir_": outdir_,
        "prefix_": prefix_,
        "redux_": redux_,
    }
    (courseName, fname, outdir, ofname1, ofname2,) = prepare_vec_dft_names(**kwargs)

    assert "build" in action_ or "read" in action_

    if "build" in action_:

        args = (
            redux_,
            tol_,
            maxiter_,
            verbose_,
            alpha_,
            l1ratio_,
        )
        kwargs = {
            "fname_": fname,
            "lang_": lang_,
            "course_": course_,
            "count_": count_,
        }
        logging.info(f"Vectorize with {kwargs} and args={args}")

        # does this change my data_?
        model, X, W, H, courseData, D = computing_vectorized_data(
            *args, data_=data_, **kwargs
        )

        # adding categories of clusters
        courseData.loc[:, "nmf_ctg"] = W.argmax(axis=1)
        courseData.loc[:, "nmf_km_ctg"] = get_kmean_category(W, redux_, verbose=False)

        # On récupères les 10 tokens associés aux thèmes (les plus influants)
        # pour tous les catégories
        iTokens = influencial_tokens(D, H, show_weights_=True)

        # et on les associe au data renvoyé
        courseData = courseData.merge(iTokens, left_on="nmf_ctg", right_index=True)

        # réduit les colonnes au colonnes essentielles
        # import ipdb; ipdb.set_trace()
        courseData = courseData.loc[:, ESSENTIALCOLS]

        # on coerce les id columns to int
        courseData = simplify_idColumns(courseData)

    elif "read" in action_:

        load = read_pickle(ofname1)
        # penser à récupérer les liste à partir des string
        # df = read_pickle(
        #     "/Clustered_files/nmf_5n_0.0a_1.0l_ddl_c18_fr_1ng_mlkst_punktwt_modelXWH.pkl"
        # )

        model, X, W, H, courseData = (
            load.pop("model"),
            load.pop("X"),
            load.pop("W"),
            load.pop("H"),
            load.pop(courseName),
        )
        old_D = read_pickle(ofname2)
        D = Dico(old_D["docs"])
        D.__dict__.update(old_D)

        # on coerce les id columns to int
        courseData = simplify_idColumns(courseData)

    newload = {"model": model, "X": X, "W": W, "H": H, "D": D}

    load = newload.copy()

    load[f"{courseName}"] = courseData

    if "save" in action_:

        saving_NMF_data(load, outdir, ofname1, ofname2)

    logging.info(f"**** koNMF and clustering results Done ****")

    return newload, fname, courseData


def simplify_idColumns(df_: DataFrame) -> DataFrame:
    """
    Coerce the columns ending with ID to int
    """
    idColumns = [col for col in df_.columns if col.endswith("ID")]

    # traduire les threadIDs to consecutive numbers
    for col in idColumns:
        df_.loc[:, col] = simpleIDs(df_[col])
        df_.loc[:, col] = df_.loc[:, col].apply(int)

    return df_


def get_kmean_category(X, redux, verbose=False):
    """
    run a basic kmean algorithm and return predicted values for the rows of X
    """
    kwargs = {
        "n_clusters": redux,
        "init": "k-means++",
        "n_init": 10,  # number of runs
        "verbose": verbose,
        "precompute_distances": "auto",
        "n_jobs": -1,
    }
    return KMeans(**kwargs).fit_predict(X)


def computing_vectorized_data(
    redux_,
    tol_,
    maxiter_,
    verbose_,
    alpha_,
    l1ratio_,
    fname_="",
    lang_="en",
    course_="ufm_c18",
    count_=None,
    data_=None,
):
    """
    loading data from fname and keeping only course ("ufm", "c18") and lang=en" messages
    Returns a dictionnary with
    - modle
    - X la matrice des documents vectorisés
    - W, H les matrices réduites
    - les données harmonizé lues sur le disque pour le cours course_
    - D le dictionnaire
    - data, should be a a file name or a pd.DataFarme object in the latter
    the data is not loaded from the filenmae
    """

    kwargs = {
        "fname_": fname_,
        "lang_": lang_,
        "course_": course_,
        "data_": data_,
    }

    # getting the data
    data = loading_harmonized_data(**kwargs)
    _ = kwargs.pop("data_")

    logging.info(
        f"Building the dictionnary with {kwargs}, data={type(data), data.shape}"
    )

    # On construit les docs à partir des tokens qui ont déjà été traité.
    # Peu de filtrage sera fait dans le Dico
    docs = data.tokens.apply(stringToList)
    D, raw_dico = simple_dico_loading(docs)

    # Vectorizing the documents
    X, _ = vectorizing_docs_from_(D, count=count_)

    # on reindex data avec les Documents qui ont des tokens meaning full
    # en gros on supprimes les messages pour lequel il y avait de tokens pas
    # meaningfull (unique peut être? ou trop fréquent)
    # le mgfDoc a été caclulé dans vectorizing_docs_from_
    data = data.reindex(D.mgfDoc.index)

    model, W, H = reducing(
        X,
        n_components=redux_,
        init=None,
        random_state=None,
        tol=tol_,
        max_iter=maxiter_,
        verbose=verbose_,
        alpha=alpha_,  # use regularisation
        l1_ratio=l1ratio_,  # element wise penality
    )

    return model, X, W, H, data, D


def reducing(X, **kwargs):

    model = NMF(**kwargs)

    W = model.fit_transform(X)
    H = model.components_
    logging.info(f"X {X.shape} ≈ W {W.shape} H {H.shape}, computed with {kwargs}")

    return model, W, H


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Script qui lance une NMF sur des données.  "
        "Sauvegarde le modèle et les résultats sur le disque."
    )
    verbose_hlp = (
        "Verbose Bolean, True if present.  show ||X - WH||_F."
        f"Default = {VEC_VERBOSE_DFT}"
    )
    redux_hlp = f"The number of dimension de la troncation Default = {VEC_REDUX_DFT}"
    tol_hlp = (
        "The number below which the error has to go to stop the iterations. "
        f"Default = {VEC_TOL_DFT}"
    )
    maxIter_hlp = (
        "The maximun number of iterations to reach convergence. "
        f"Default = {VEC_MAXITER_DFT}"
    )
    alpha_hlp = f"Importance du terme de régulation (def. {VEC_ALPHA_DFT})"
    l1Ratio_hlp = f"Ratio de régularisation l1 (1) vs l2 (0), (def. {VEC_L1RATIO_DFT})"
    action_hlp = (
        "'build' 'save', 'read' or a combination. "
        "Action to carry out. read pre-vectorized file and recompute "
        "NMF + clustering, or vectorize, data, revectorise and recompute "
        f"NMF + clustering (def. {VEC_ACTION_DFT}). If save is not in the action"
        " then nothing is written on the disk"
    )
    count_hlp = (
        "Façon de constuire la matrice de données lorsqu'il faut revectoriser. "
        f"Les alternatives au défaut (def. {VEC_COUNT_DFT}) sont 'tf' ou 'count'"
    )
    fname_hlp = (
        "Nom du fichier des données tokenizés à charger pour executer ACTION"
        f" (def. {VEC_FNAME_DFT}).  Peut aussi être un int 'x' pour ne prendre que"
        f" les 'x' premier fichier dans {VEC_INDIR_DFT}. Si 'all' alors traite tous "
        "les fichiers."
    )
    lang_hlp = f"Langue (def. {LANG_DFT}). 'all' pour tout garder"
    course_hlp = f"Cours (def. {COURSE_DFT}). 'all' pour tout garder"
    inDir_hlp = (
        "Parallèle option, Directory to seach for the input file"
        f" (the tokenized files) (def. {VEC_INDIR_DFT})."
    )
    outDir_hlp = (
        "Parallèle option, Directory to save the reduces matrices"
        f" (def. {VEC_OUTDIR_DFT})."
    )
    prefix_hlp = (
        "Parallèle option, The prefixe of the files to process in {VEC_INDIR_DFT}"
        f" (def. {TOK_PREFIX_DFT})."
    )
    logLevel_hlp = f"Log level (def. {LOGLEVEL_DFT})"

    parser.add_argument("-V", "--verbose", action="store_true", help=verbose_hlp)
    parser.add_argument(
        "-x", "--redux", type=int, default=VEC_REDUX_DFT, help=redux_hlp,
    )
    parser.add_argument(
        "-t", "--tol", type=float, default=VEC_TOL_DFT, help=tol_hlp,
    )
    parser.add_argument(
        "-m", "--maxIter", type=int, default=VEC_MAXITER_DFT, help=maxIter_hlp,
    )
    parser.add_argument(
        "-a", "--alpha", type=float, default=VEC_ALPHA_DFT, help=alpha_hlp,
    )
    parser.add_argument(
        "-r", "--l1Ratio", type=float, default=VEC_L1RATIO_DFT, help=l1Ratio_hlp,
    )
    parser.add_argument("-A", "--Action", default=VEC_ACTION_DFT, help=action_hlp)
    parser.add_argument("-c", "--count", default=VEC_COUNT_DFT, help=count_hlp)
    parser.add_argument("-f", "--fname", default=VEC_FNAME_DFT, help=fname_hlp)
    parser.add_argument("-l", "--lang", default=LANG_DFT, help=lang_hlp)
    parser.add_argument("-C", "--course", default=COURSE_DFT, help=course_hlp)
    parser.add_argument("-I", "--InDir", default=VEC_INDIR_DFT, help=inDir_hlp)
    parser.add_argument("-O", "--OutDir", default=VEC_OUTDIR_DFT, help=outDir_hlp)
    parser.add_argument("-P", "--Prefix", default=TOK_PREFIX_DFT, help=prefix_hlp)
    parser.add_argument(
        "-L", "--logLevel", default=LOGLEVEL_DFT, help=logLevel_hlp,
    )

    return parser.parse_args()


def main_prg():
    """Parse arguments and run the main function."""
    args = parse_arguments()

    LOGFMT = "/%(filename)s@%(lineno)s@%(funcName)s/ %(message)s"
    logging.basicConfig(level=args.logLevel, format=LOGFMT)
    logging.info(f"Running with: {os.sys.version}")

    kwargs = {
        "action_": args.Action,
        "alpha_": args.alpha,
        "count_": args.count,
        "course_": args.course,
        "fname_": coerce_string2number(args.fname),
        "l1ratio_": args.l1Ratio,
        "lang_": args.lang,
        "maxiter_": args.maxIter,
        "redux_": args.redux,
        "tol_": args.tol,
        "verbose_": args.verbose,
    }

    main_parallel(
        indir_=args.InDir, outdir_=args.OutDir, prefix_=args.Prefix, **kwargs,
    )


if __name__ == "__main__":
    main_prg()
