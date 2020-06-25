#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Harmonize Data from forum MOOC discussion files."""

import logging
import argparse
from pathlib import Path

from pandas import DataFrame, Series, concat

from KolaViz.LibHD.mlkdataprep import ExpandedReplies
from KolaViz.Lib.func4unige import UnigeData2
from KolaViz.Lib.model import (
    CRSCD,
    LOGFMT,
    HARMO_FNAME_DFT,
    HARMO_ACTION_DFT,
)
from KolaViz.Lib.fnames import FName

# from typing import Literal
# ACTION_ARG = t.Literal['save', 'read']  # pour python3.8

# # Chargement des données Coursera 2017 et 2018


def main(action_=HARMO_ACTION_DFT, fname_=HARMO_FNAME_DFT, hdf=None) -> DataFrame:
    """
    Programme qui récupère les cours de Coursera 17 18 depuis les DB et renvois
    (ou sauvegarde les données wrangled. (ie. harmonisé))
    action: should be 'save' or 'read'
    fname_: should be the filename to apply the action to
       - In case of read, the fname_ is where to read
       - In case of save, the fname_ is where to save
       - build (only) load from db and return a DataFrame
    """

    fname = FName(fname_)

    if action_ == "read":

        # wrangeled text
        hdf = fname.read_as_df()
        logging.info(f"file {fname} read.")

    elif "build" in action_:

        c18 = load_from_db("c18", datadir_=fname.parent)
        c17 = load_from_db("c17", datadir_=fname.parent)
        hdf = harmonise_cours(c17, year="c17")
        hdf = harmonise_cours(c18, year="c18", res=hdf)

        if "save" in action_:

            hdf.to_pickle(fname.fn)
            logging.info(
                f"Saved the harmonized dataframe with columns {hdf.columns}\
                and {len(hdf)} rows to {fname}"
            )

    return hdf


def simpleIDs(s: Series):
    """
    Function to simplify dataframe columns with ids.
    s should be a pandas serie (implementing replace function)
    Takes a serie 's' of ID entries and return the serie where entries are replaced
    by simpleinteger ranging from 0 to len(s)
    - TODO: généraliser à des np.array
    """
    # translation dictionnary
    tdict = {u: i for i, u in enumerate(s.unique())}
    return s.replace(tdict)


# selection du cours (ou dataset)
def load_from_db(year: str, datadir_="Data/DB") -> DataFrame:
    """
    Lit les bases de données coursera des cours de 2017 et 2018.
    Renvois tous les cours d'une année donnée.
    dans un tableaux pour plusieurs cours au format c17 Coursera 2017.
    Si c17 df est renseigné y ajoute les cours de courseCodes.
    Sauvegard des résultats intermédiaires
    """
    datadir = Path(datadir_)
    resdf = None

    # construction des noms de fichiers
    _suffix = {"c17": "-forum.mydb", "c18": ".pkl"}
    fichier = {name: datadir.joinpath(f"{name}{_suffix[year]}") for name in CRSCD[year]}

    for i, (name, code) in enumerate(CRSCD[year].items()):
        # on parcours le disque à la recherches des fichiesr données
        # on les charge et stoke dans une même dataframe

        fname = FName(fichier[name])
        logging.debug(f"Chargement de {fname} ({i+1}/{len(CRSCD[year])})")

        if year == "c17":
            # ! verifier la consistence des msgid pp and pml
            tmpdf = ExpandedReplies(fn=fname.fn).df

        elif year == "c18":
            try:
                # essaye de récupérer les fichiers intermédiaires compilés
                # lors d'un précédent appel.
                tmpdf = fname.read_as_df().sort_index(axis=1)
            except FileNotFoundError:
                # on lit alors les données de tous les cours depuis la DB,
                # on les combine et on sauvgarde le fichier.
                logging.info(
                    f"Fichier {fichier[name].resolve()} n'est pas trouvé."
                    " On le reconstruit à partir des tables."
                )
                # on  reconstruit le fichier
                tmpdf = UnigeData2(code, datadir).load_df(humanize_=True).df

                # au sauvegarde pour la prochaine fois
                logging.info(
                    f"Saving {name, type(tmpdf), len(tmpdf)}  to {fname} for later"
                    " rebuild"
                )
                tmpdf.to_pickle(fname.fn)

        else:
            raise Exception(f"year {year} unknown ?")

        tmpdf.loc[:, "course"] = code

        # concatène les résultas ensemble
        resdf = tmpdf if resdf is None else concat([resdf, tmpdf], sort=False)

    return resdf


def harmonise_cours(rawdf, year, res=None):
    """
    Extrait de rawdf, les valeurs du dictionnaire d'harmonisation pour year
    et renvois une DataFrame au format unifiée.  La concatène à res si fournie
    Renvois une Dataframe harmonisée: avec un multi-index year, cours.

    C'est  ici que l'on choisi le colonnes (les donées) à garder.
    Il s'agit normalement de données partagé par les différentes plateformes

    """
    if year == "c17":

        def harmoDico(df):
            return {
                "threadID": df.tid,
                "tTitle": df.p_title,
                "msgID": simpleIDs(df.p_id),
                "authorID": simpleIDs(df.author_id),
                "author": df.full_names,
                "msgContent": df.p_text,
                "msgMREd": df.p_newts.apply(lambda d: d.timestamp()),
                "autRole": df.roles,
            }

    elif year == "c18":

        def harmoDico(df):
            return {
                "threadID": simpleIDs(df.dscQid),
                "tTitle": df.dscQtitle,
                "msgID": simpleIDs(df.dscAid),
                "authorID": simpleIDs(df.Udscs_uid_DA),
                "author": df.Udscs_uid_DA,
                "msgContent": df.dscAcontent,
                "msgMREd": df.dscA_uts,
                "autRole": df.crs_mbs_role,
            }

    courses = list()
    for code, df in rawdf.groupby("course"):
        print(f"Harmonisation de {code}...")
        courses.append(code)

        tmpdf = DataFrame(harmoDico(df))
        # creating a multi index for later ease of access
        tmpdf.loc[:, "mooc"] = year
        tmpdf.loc[:, "course"] = code
        tmpdf = tmpdf.set_index([df.index, "mooc", "course"])

        res = tmpdf if res is None else concat([res, tmpdf])

    res = (
        res.reset_index()
        .drop("level_0", axis=1)
        .set_index(["mooc", "course"], append=True)
    )

    return res


def format_msgID(id):
    """
    format the id number to make it more readable
    """
    asChar = str(int(id))

    return f"{asChar[:-6]}-{asChar[-6:-3]}-{asChar[-3:]}"


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Fonction qui lit les données depuis la base de donnée\
        et qui les regroupe dans un fichier unique avec des colonnes harmonisées."
    )

    logLevel_dft = "INFO"
    logLevel_hlp = f"Log level (def. {logLevel_dft})"
    parser.add_argument(
        "-L", "--logLevel", default=logLevel_dft, help=logLevel_hlp,
    )

    action_dft = HARMO_ACTION_DFT
    action_hlp = f"Action to carry out with fname (buil, save or read) (def. {action_dft})."
    parser.add_argument("-A", "--Action", default=action_dft, help=action_hlp)

    wfname_dft = HARMO_FNAME_DFT
    wfname_hlp = f"pickle file name to apply the action to. (def. {wfname_dft})."
    parser.add_argument("-f", "--fname", default=wfname_dft, help=wfname_hlp)

    return parser.parse_args()


def main_prg():
    """Parse arguments and run main function."""
    args = parse_arguments()

    logging.basicConfig(level=args.logLevel, format=LOGFMT)
    logging.debug(f"{__name__} Charged")

    kwargs = {"action_": args.Action, "fname_": args.fname}
    main(**kwargs)


if __name__ == "__main__":
    main_prg()
