#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Runs tokenized data in parallèle."""
import os
import warnings
import logging
import argparse
import itertools as it
from pathlib import Path
from typing import List, Union

import pandas as pd

from KolaViz.Lib.func4unige import tokenize_text
from KolaViz.Lib.model import (
    LOGFMT,
    TOK_ACTION_DFT,
    TOK_OUTDIR_DFT,
    HARMO_FNAME_DFT,
    TOK_TOKENIZERS,
    TOK_WORDENIZERS,
    TOK_NGRAMS,
)
from KolaViz.Lib.fnames import FName, as_tokenized


warnings.filterwarnings("ignore", category=UserWarning, module="bs4")


def main(
    action_: str = "readH_save_build",  # ou readT pour aller au résultat directementl
    as_thread_: bool = False,
    fname_: str = HARMO_FNAME_DFT,
    ngrams_: List[int] = TOK_NGRAMS,
    outdir_: str = TOK_OUTDIR_DFT,
    sent_tokenizers_: List[str] = TOK_TOKENIZERS,
    word_tokenizers_: List[str] = TOK_WORDENIZERS,
    hdf_=None,
):
    """
    Le but c'est d'aboutir aux données tokenizées.
    - action: on fname_ should contain one or several of:
      - 'readH' pour lire fname_ comme le fichier des données harmonisés (ie wrangled)
      - 'save': pour sauvegarder les fichiers tokenizés dans `outdir_`
         noms générés automatiquement à partir des options sent & word_tokenizers,  ngrams
      - 'build': reconstuit les tokens à partir du fichier fname_.
      - 'readT': lit le fichier déjà tokenizé dans les dossiers outdir_
    L'appelle au ngrams et tokenizer se fait en parallèles.  
      - Soit comme un thread, soit comme un process
    - ngrams: liste of ngram size to compute
    - sent_tokenizers: "punkt" and/or "mlk"
    - word_tokenizers: "punkt", "mlk", "base_punkt" or "all"
    """
    # handle parallelisation as thread or multiprocess
    if as_thread_:
        from queue import Queue
        from threading import Thread, active_count
    else:
        from multiprocessing import Queue, Process, active_children

    def nbActiveProc():
        try:
            return len(active_children())
        except Exception:
            return active_count() - 1

    # settings defaults
    fname = FName(fname_)
    outdir = fname.parent if outdir_ is None else Path(outdir_)

    # create output dir if does not exist
    if not outdir.exists():

        os.mkdir(outdir)

    hdf = hdf_
    # handle the case the function is call with hdf_
    if hdf is None and "readH" in action_:

        hdf = fname.read_as_df()
        logging.debug(f"hdf.index.names={hdf.index.names}")

        if "course" in hdf.columns and "mooc" in hdf.columns:

            ucol = [c for c in hdf.columns if "Unnamed" in c]

            assert len(ucol) == 1, f"Check columns {hdf.columns} in {fname.fn}"

            hdf = hdf.set_index(["course", "mooc", f"{ucol[0]}"]).reorder_levels(
                [f"{ucol[0]}", "course", "mooc"]
            )
            hdf.index.names = ["msgID", "course", "mooc"]

        elif len(hdf.index.names) == 3:
            # un moyen robuste de changer les noms en supposant course
            # et mooc déja renseignés
            missing_idx = idx_Lelt_not_inM(hdf.index.names, ["msgID", "course", "mooc"])[
                0
            ]
            # change the element not found above with msgID
            hdf.index.names = [
                "msgID" if i == missing_idx else e for i, e in enumerate(hdf.index.names)
            ]

            if set(hdf.index.names) != set(["msgID", "course", "mooc"]):
                logging.exception(
                    f"Il va y avoir des problèmes avec les noms de columns. Check"
                    " hdf.columns={hdf.columns}"
                    " and hdf.index.names={hdf.index.names}"
                )
                raise Exception
        logging.debug(f"After hdf.index.names={hdf.index.names}")


    # preparing variables before starting loop on multiple threads
    if word_tokenizers_ == ["all"]:
        word_tokenizers = ["mlk", "punkt", "base_punkt"]
    else:
        word_tokenizers = word_tokenizers_

    # faire une liste pour ne pas consommer l'iterator lors du premier passage
    iterator = list(it.product(ngrams_, sent_tokenizers_, word_tokenizers))

    # to use as a comunicatin channel
    Q: Queue = Queue()

    # #### parallels loops ####
    for ng, st, wt in iterator:

        tok_fname = outdir.joinpath(as_tokenized(ng, st, wt))
        args = (ng, st, wt, action_, tok_fname, hdf, Q)

        # starting as thread
        if as_thread_:
            logging.debug("Staring thread.")
            p: Union[Thread, Process] = Thread(target=prl_tokenize, args=args)

        # or processes
        else:
            p = Process(target=prl_tokenize, args=args)

        p.start()
        logging.info(
            f"{'Thread' if as_thread_ else 'Process'} {action_, tok_fname} started."
        )

    # on récupère les derniers objets dans la queue ce qui fermera les derniers process

    while nbActiveProc():  # pb parfois loop infini ??
        FD, fname = Q.get()

        if "save" in action_:
            # should be carrefull pickling images
            FD.to_pickle(fname)

            logging.info(f"Saving {fname}")
        logging.debug(f"nbActiveProc={nbActiveProc()}")

    return FD


def prl_tokenize(ng, st, wt, action, fname, hdf, comQ) -> None:
    """Dispatch jobs."""
    logging.debug(
        f">>>> go {ng, st, wt, action, fname, comQ} , "
        "len(hdf)={'none' if hdf is None else len(hdf)}"
    )
    load = tokenize(
        ngram=ng, sent_tok=st, word_tok=wt, action=action, fname=fname, hdf=hdf,
    )
    logging.debug(f">>>> got it {type(load), len(load)}, for fname '{fname}'")
    comQ.put((load, fname))

    return None


def tokenize(
    ngram=1, sent_tok="mlk", word_tok="mlk", action="load", fname="", hdf=None,
):
    """
    Charge en mémoire les données tokenizées.

    Returns a dataframe de message tokenizés et filtré tel queles messages aient au moins
    un token après que les stop word ait été enlevés.
    Attention ! il y aura un autre filtre lorsque les documents seront pris
    dans leur ensemble et que l'on gardera que les tokens en fonction de leur fréquence
    """
    build_only = ("build" in action) and ("readT" not in action)
    readT_only = ("build" not in action) and ("readT" in action)
    assert (
        build_only or readT_only
    ), f"Should be build or readT only, but {build_only, readT_only} and action={action}."

    if "build" in action:

        logging.info(f"action is {action}.  Building")

        assert hdf is not None, "Add 'readH' to action or pass a harmonized hdf."

        Tf = tokenize_text(
            df_=pd.DataFrame(hdf.msgContent),
            ngramR=ngram,
            stopW=None,
            # default nltk stopWord ou "normalUnige for mlk"
            # basedir=STOPWORD_DIR,
            textCol=None,
            inplace=False,
            lang_detect=10,
            strong_lem=True,
            sent_tokenizer=sent_tok,
            word_tokenizer=word_tok,
        )

        assert Tf is not None
        # concatenation of tokens with original dataframe
        FD = (
            hdf.drop("msgContent", axis=1)
            .join(Tf, how="right")
            .reorder_levels([0, 2, 1])
        )

        # supprime les lignes sans tokens
        # y a un truc avec les phrase du type "You're method is very good
        # here is how d it..."  id (6303, pp c17)  CHECK !change regex to catche
        # first sent word add \n in sentpat
        mask = FD.tokens.apply(len) == 0
        FD = FD.where(~mask).dropna()
        logging.debug(f"len(FD)={len(FD)}")
        return FD

    elif "readT" in action:
        logging.debug(f"action={action} reading {fname}")
        return pd.read_pickle(fname)
    else:
        raise Exception(f"****Check action={action}****")


def idx_Lelt_not_inM(L, M):
    """Return the index of the elements of L, not in M."""
    return [i for i, e in enumerate(L) if e not in M]


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Charge les textes pré-traité ou harmonisé et les tokenize"
        " pour sauvegarder ensuite un fichiers aves les données pré-traitées"
        " adjointes des données tokenizées"
    )
    logLevel_dft = "INFO"
    logLevel_hlp = f"Set le log Level (def. {logLevel_dft})."
    parser.add_argument(
        "-L", "--logLevel", default=logLevel_dft, help=logLevel_hlp,
    )

    ngrams_dft = [1]
    ngrams_hlp = f"Une liste de # pour les ngrams (def. {ngrams_dft})."
    parser.add_argument(
        "-g", "--grams", nargs="*", type=int, default=ngrams_dft, help=ngrams_hlp,
    )

    sentTok_dft = ["mlk"]
    sentTok_hlp = (
        f"Choose the tokenizer type.  Can be mlk or punkt (def. {sentTok_dft})."
    )
    parser.add_argument(
        "-s", "--sentTok", nargs="*", default=sentTok_dft, help=sentTok_hlp,
    )

    wordTok_dft = ["mlk"]
    wordTok_hlp = (
        "Choose the word tokenizer.  Can be 'mlk', 'punkt' ou"
        f" 'base_punk' (def. {wordTok_dft}). use all for all"
    )
    parser.add_argument(
        "-w", "--wordTok", nargs="*", default=wordTok_dft, help=wordTok_hlp,
    )

    action_dft = TOK_ACTION_DFT
    action_hlp = (
        "kewords separated by '_' for actions. can be:\n"
        "- readH, to read the Harmonized text file\n"
        "- build, to rebuild the tokenized files\n"
        "- readT, to a previously tokenized file\n"
        "- save, to savel the tokenized to disk"
        " contains read, trys to read the file"
        f" {TOK_OUTDIR_DFT}/tokenized_xng_yst_zwt.pkl. Si contains save"
        f" will also write the file (def. {action_dft})."
    )
    parser.add_argument("-A", "--Action", default=action_dft, help=action_hlp)

    hdfFname_dft = HARMO_FNAME_DFT
    hdfFname_hlp = (
        "Chemin vers le fichiers à charger pour reconstruire les"
        " tokens. C'est le fichiers de textes unifié (harmonisé)"
        f" (def. {hdfFname_dft})."
    )
    parser.add_argument(
        "-f", "--hdfFname", default=hdfFname_dft, help=hdfFname_hlp,
    )

    outDir_dft = TOK_OUTDIR_DFT
    outDir_hlp = (
        "The directory to save the tokenized file too. "
        f"If does not exist will create it (def. {outDir_dft})."
    )
    parser.add_argument("-O", "--OutDir", default=outDir_dft, help=outDir_hlp)

    return parser.parse_args()


def main_prg():
    """Parse arguments and run the main function."""
    args = parse_arguments()

    logging.basicConfig(level=args.logLevel, format=LOGFMT)
    logging.info(f"Running with: {os.sys.version}")
    kwargs = {
        "ngrams_": args.grams,
        "sent_tokenizers_": args.sentTok,
        "word_tokenizers_": args.wordTok,
        "action_": args.Action,
        "fname_": args.hdfFname,
        "outdir_": args.OutDir,
    }
    main(**kwargs)


if __name__ == "__main__":
    main_prg()
