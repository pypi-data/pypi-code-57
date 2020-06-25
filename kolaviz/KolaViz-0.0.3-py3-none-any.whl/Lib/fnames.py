# -*- coding: utf-8 -*-
"""
Utilities to read, save and make file names in my projects
"""
import os
import pickle
import json
import datetime as dt
from pathlib import Path
import logging
from typing import Union

import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix


from KolaViz.Lib.mlktypes import FNameT
from KolaViz.Lib.model import (
    COURSE_DFT,
    LANG_DFT,
    VEC_ALPHA_DFT,
    VEC_L1RATIO_DFT,
    VEC_REDUX_DFT,
    TOK_PREFIX_DFT,
)


class FName:
    def __init__(
        self,
        name_or_stem,
        ext=None,
        n_max=1000,
        fmt="%y%m%dT%H%M",
        replacespace="-",
        withtimestamp=True,
        withcount=True,
    ):
        """
        A revoir: Classe pour générer des noms de fichiers qui s'incrémentent
        automatiquement au cours d'une session et qui garde la date.
        Permet aussi de faire de petites substitutions entre le nom donné et
        celui du fichier ce qui est pratique pour nommer des fichiers
        comme le titre de ses graphiques.
        if withtimestamp is False remove timestampf from file name.
        -withcount: to add a counter at the end of the name
        - ext: avec le point
        - replace space: if not None (default '-') replace space in title
        by passed value
        """
        self.fn = Path(name_or_stem)

        # giving fname a bunch of attributes
        for att in ["parent", "name", "stem", "suffix"]:
            setattr(self, att, getattr(self.fn, att))

        if ext:
            if self.suffix and self.suffix != ext:
                logging.info(f"Overriding suffix {self.suffix} with {ext}")
            self.suffix += ext

        self.n_max = n_max  # cpt upper limit
        self.cpt = 0
        self.fmt = fmt  # format

        self.withTimestamp = withtimestamp
        self.currentStem = self.new_name_gen()
        self.currentTimedStem = None
        self.withCount = withcount

    def __repr__(self, long=False):
        keys = [
            "name",
            "fn",
            "ext",
            "n",
            "fmt",
            "currentTimedStem",
            "withTimestamp",
        ]
        D = {}
        for k in keys:
            D[k] = getattr(self, k, "Not set!")

        return f"{D}" if long else f"{self.fn}"

    def _reset(self, init=0):
        """
        reset compter to init (def. 0)
        """
        self.cpt = init

    def next(self, fullpath=False, ext=None, fmt=None):
        """
        ?ext: add extension to currentStem
        ?fmt : add a format type
        Generating a new name with a date stamp and an increment.

        """
        if ext is None:
            ext = self.suffix
        if fmt is None:
            fmt = self.fmt

        date = dt.datetime.now().strftime(fmt)
        if self.withCount:
            self.currentTimedStem = f"{next(self.currentStem)}"
        else:
            self.currentTimedStem = self.currentStem

        self.currentTimedStem += f"_{date}" if self.withTimestamp else ""
        self.currentTimedStem += f"{ext}"

        return (
            Path(self.parent, self.currentTimedStem)
            if fullpath
            else self.currentTimedStem
        )

    def new_name_gen(self):
        """
        Incrément le stem du nom pour éviter les doublons.  Si cpt == 0 ne marque rien.
        """
        while self.cpt < self.n_max:
            newName = f"{self.stem}{self.cpt}" if self.cpt else f"{self.stem}"
            yield newName
            self.cpt += 1

    def read_as_df(self):
        """
        Read the file as a dataframe independently of the suffix
        Select the correct method to read the file in fname based on extension.
        Default to csv.
        -- Returns the dataframe read
        """
        logging.debug(f"read_as_df fn={self.fn}")
        if self.suffix == ".pkl":
            df = pd.read_pickle(self.fn)
        else:
            df = pd.read_csv(self.fn)
        return df

    def to_db(self, obj):
        """
        Ecrit l'objet pandas sur le disque en essayant d'abord en pkl puis en csv.
        Essaye de résoudre le problème que souvent les objet ne sont pas picklable mais
        peut être sauvegarder en csv ou d'autre format
        """
        # pas utilisé pour l'instant faire attention à bien passer self.fn au
        # fonction de sauvegarde pandas
        try:
            self.suffix == ".pkl"
            obj.to_pickle(self.fn)
        except ValueError:
            self.suffix == ".csv"
            obj.to_csv(self.fn, index=False)

        logging.debug(f"Wrote {self.fn} to disk")
        return None


class DataJsonName(FName):
    def __init__(
        self, stem, n=100, ext=".json", fmt="%y%m%dT%H%M", replacespace="-",
    ):
        """

        Keyword Arguments:
        name_or_stem,         --
        n            -- (default 100)
        ext          -- (default ".json")
        fmt          -- (default "%y%m%dT%H%M")
        replacespace -- (default "-")

        """
        super().__init__(stem, n, ext)


class DataPickleName(FName):
    def __init__(
        self,
        stem,
        n=100,
        ext=".pkl",
        fmt="%y%m%dT%H%M",
        replacespace="-",
        withtimestamp=False,
        withcount=True,
    ):
        """

        Keyword Arguments:
        name         --
        n            -- (default 100)
        ext          -- (default ".pkl")
        fmt          -- (default "%y%m%dT%H%M")
        replacespace -- (default "-")

        """
        super().__init__(
            stem, ext, n, fmt, replacespace, withtimestamp=withtimestamp,
        )


class ChartName(FName):
    def __init__(
        self,
        stem,
        n=100,
        ext=".pdf",
        fmt="%y%m%dT%H%M",
        replacespace="-",
        withtimestamp=True,
    ):
        """

        Keyword Arguments:
        name         --
        n            -- (default 100)
        ext          -- (default ".pdf")
        fmt          -- (default "%y%m%dT%H%M")
        replacespace -- (default "-")

        """
        super().__init__(
            stem, ext, n, fmt, replacespace, withtimestamp=withtimestamp,
        )


def get_course_name_from_model_filestem(fstem: str):
    """
    returns what should be the course part of a nmf_file
    """
    parts = fstem.split("ng")
    course, mooc, lang = parts[0].split("_")[-4:-1]
    return course, mooc, lang


def build_tokenized_filestem(fstem: str, suffix: str = "tokenized"):
    """
    Build the tokenize stem from the nmf stem (model dico and nmf).
    eg: from 'nmf_5n_0a_1l_ufm_c18_en_2ng_mlkst_mlkwt_XWHD0' to
    'tokenized_2_mlkst_mlkwt_XWHD0'
    """
    parts = fstem.split("ng")
    ngram = parts[0].split("_")[-1] + "ng"
    course, mooc, lang = get_course_name_from_model_filestem(fstem)
    stem = ngram + "_".join(parts[-1].split("_")[:-1])
    return f"{suffix}_{stem}", f"{course}_{mooc}", lang


def build_model_filestem(
    redux_: int,
    alpha_: float,
    l1ratio_: float,
    course_: str,
    lang_: str,
    fstem_: Union[FNameT, FName] = ".",
    prefix_: str = "nmf",
) -> str:
    """
    Build the model fstem from the tokenized fstem and arguments:
nerd, alpha and l1ratio.
    eg: from 'tokenized_2_mlkst_mlkwt_XWHD0' to '
    nmf_5n_1a_1l_ufm_c18_en_2ng_mlkst_mlkwt_XWHD'
    """
    stem = Path(fstem_).stem.strip("_")

    redux = int(redux_)
    alpha = float(alpha_)
    l1ratio = float(l1ratio_)
    courseName = f"{course_}_{lang_}"
    return f"{prefix_}_{redux}n_{alpha}a_{l1ratio}l_{courseName}_{stem}"


def as_tokenized(
    ngram_: int,
    sentTok_: str,
    wordTok_: str,
    outdir_: Union[FNameT, FName] = "",
    prefix_: str = "tokenized",
) -> Path:
    """
    standardize the naome of tokenized files
    """
    fname = FName(f"{prefix_}_{ngram_}ng_{sentTok_}st_{wordTok_}wt.pkl")

    return Path(outdir_).joinpath(fname.fn)


def saving_NMF_data(load_, outdir_, ofname1_, ofname2_) -> None:
    """
    juste saving nmf data in two separate file on with the dictionnary the other
    with reduced matrices
    """
    name1 = DataPickleName(f"{ofname1_.name}", withcount=False).next()
    name2 = DataPickleName(f"{ofname2_.name}", withcount=False).next()

    save_pickle(load_.pop("D").__dict__, name2, outdir_)
    save_pickle(load_, name1, outdir_)
    return None


def create_output_fnames(
    outdir_: Union[FNameT, FName] = ".",
    fstem_: Union[FNameT, FName] = ".",
    redux_: int = VEC_REDUX_DFT,
    alpha_: float = VEC_ALPHA_DFT,
    l1ratio_: float = VEC_L1RATIO_DFT,
    course_: str = COURSE_DFT,
    lang_: str = LANG_DFT,
    prefix_: str = "",
) -> Path:
    """
    create two filenames, one for dictionnary one for vectorized data
    """
    outdir_ = Path(outdir_)
    outStem = build_model_filestem(
        redux_=redux_,
        alpha_=alpha_,
        l1ratio_=l1ratio_,
        course_=course_,
        lang_=lang_,
        fstem_=fstem_,
        prefix_=prefix_,
    )
    ofname1 = outdir_.joinpath(f"{outStem}_modelXWH")

    # saving dico separately because I can't pickle it directly
    ofname2 = outdir_.joinpath(f"{outStem}_D")

    return ofname1, ofname2


def reading_vectorized_data(fname):
    """
    Charge une matrix vectorisée depuis arg.fname
    """
    # Vérifier que c'est bien une matrice à charger.  Si dict renvoyer le dict
    logging.info(f"Reading Vectorized data from {fname}")
    load = read_pickle(Path(fname))

    if not isinstance(load, dict):
        X = load
        assert isinstance(X, (np.ndarray, csr_matrix)), (
            f"Le Type des données chargées n'est pas bon type(X)={type(X)}. "
            "Vérifier le fichier des données véctorisée chargé '{fname}'"
        )

        if X.min() < 0:
            logging.info(f"Negative values in X, shifting it positively.")
            X = X.toarray() - X.min() if isinstance(X, csr_matrix) else X - X.min()
        return csr_matrix(X)
    return load


def read_pickle(fname, dirname="./"):
    """
    Load a pickled object from file
    """
    ffname = Path(dirname).joinpath(fname)

    if ffname.suffix != ".pkl":
        ffname = f"{ffname}.pkl"

    logging.info(f"Reading {ffname} from disk")
    with open(f"{ffname}", mode="br") as f:
        res = pickle.load(f)

        return res


def load_model(fname, dirname=""):
    """
    Short hand to load models from the data dir.
    detects if it is a pickle format (pkl, pkd)
    and return the loaded models
    """
    return read_pickle(fname, dirname=dirname)


def save_model(obj, fname, dirname=""):
    """
    Short hand to save models from the data dir.
    detects if is a pickle format (pkl, pkd) and return the loaded models
    """
    return save_pickle(obj, fname, dirname=dirname)


def save_type(obj, fname, dirname=""):
    "save an obj to pickle or json format depending on extention"
    fname = Path(dirname).joinpath(fname)

    if "pkl" in fname.suffix:
        mode = "bw"
    elif "json" in fname.suffix:
        mode = "w"
    else:
        raise Exception(
            f"format for '{fname}' not yet supported. Try adding an extension"
        )

    with open(fname, mode) as f:
        if "b" in mode:
            pickle.dump(obj, f)
        else:
            json.dump(obj, f)

    if isinstance(obj, dict) and len(obj) < 10:
        logging.info(f"Wrote a {type(obj)} with keys={obj.keys()} to {fname}")
    else:
        logging.info(f"Wrote a {type(obj)} to {fname}")

    return None


def save_pickle(obj, fname, dirname=""):
    """
kSave pickled version of object in fname of dirname
    """
    fname = Path(fname)
    if not fname.suffix.endswith("pkl"):
        fname = fname.parent.joinpath(f"{fname.name}.pkl")

    return save_type(obj, fname, dirname=dirname)


def save_json(obj, fname, dirname=""):
    """
    Save pickled version of object in fname of dirname
    """
    # can be factored with decorator
    fname = Path(fname)
    if not fname.suffix.endswith("json"):
        fname = fname.parent.joinpath(f"{fname.name}.json")

    return save_type(obj, fname, dirname=dirname)


def create_dir(dirname_, createdir_=True):
    """
    returns a directory (Path) and create it if necessary
    """
    dirname = Path(".") if dirname_ is None else Path(dirname_)
    # create output dir if does not exist
    if createdir_ and not dirname.exists():
        os.mkdir(dirname)

    return dirname


def prepare_vec_dft_names(
    alpha_=VEC_ALPHA_DFT,
    course_=COURSE_DFT,
    fname_=".",
    l1ratio_=VEC_L1RATIO_DFT,
    lang_=LANG_DFT,
    outdir_=".",
    prefix_=TOK_PREFIX_DFT,
    redux_=VEC_REDUX_DFT,
):
    """
    Génère un ensemble de noms de fichiers pour une standardisation des noms
    Return:
    - ofname1, ofname2 nom des fichiers sorties pour 1 les données vectorisées, 2 le dico
    - outdir : dossier où sont stocker les fichiers ci-dessus
    - courseName c'est juste la concaténation de course et lang
    - fname c'est juste fname dans Path
    -
    """
    course = "_".join(course_) if isinstance(course_, list) else course_
    courseName = f"{course}_{lang_}"
    fname = Path(fname_)
    bstem = fname.stem.split(prefix_)[1] if prefix_ in fname.as_posix() else fname.stem

    # on construit le nom du fichier à lire ou sauvegarder à partir des arguments
    outdir = create_dir(outdir_)
    ofname1, ofname2 = create_output_fnames(
        outdir_=outdir,
        fstem_=bstem,
        redux_=redux_,
        alpha_=alpha_,
        l1ratio_=l1ratio_,
        course_=course_,
        lang_=lang_,
        prefix_="nmf",
    )
    return courseName, fname, outdir, ofname1, ofname2


def prepare_cir_dft_name(
    alpha_=VEC_ALPHA_DFT,
    course_=COURSE_DFT,
    fname_=".",
    l1ratio_=VEC_L1RATIO_DFT,
    lang_=LANG_DFT,
    outdir_=".",
    prefix_=TOK_PREFIX_DFT,
    redux_=VEC_REDUX_DFT,
):
    outStem = build_model_filestem(
        alpha_=alpha_,
        course_=course_,
        fstem_=fname_,
        l1ratio_=l1ratio_,
        lang_=lang_,
        prefix_=prefix_,
        redux_=redux_,
    )
    outdir = create_dir(outdir_, True)
    fname = outdir.joinpath(f"{outStem}_GC")
    return outdir, fname
