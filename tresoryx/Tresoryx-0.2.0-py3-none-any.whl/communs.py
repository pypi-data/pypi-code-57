# -*- coding: utf-8 -*-

# Copyright 2018 Guitou des Phoenix
#
# Ce fichier fait partie de Tresoryx, sous license GNU GPL.
# This file is part of Tresoryx, under GNU GPL license.



import os.path as op
from io import StringIO
import re
import codecs
import datetime as dt
import csv
import yaml
import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype

from collections import namedtuple

import logging
loggeur = logging.getLogger(__name__)

import locale
from locale import delocalize, atof  # Non utilisés actuellement
try:
    locale.setlocale(locale.LC_NUMERIC, "fr_FR.UTF-8")  # Pour convertir les nombres en format français
except locale.Error as err:
    loggeur.warning(str(err) + ' fr_FR.UTF-8')


cree_regles_auto = namedtuple('Regex_classes', ['charges', 'produits'])

# ~~> config
format_date = '%d/%m/%Y'

exemple_encoding = 'iso8859-1'
exemple_fichier_noms = "noms.csv"


def nombre_europeen_vers_us(numberstr):
    return numberstr.replace('\u202f', '').replace(' ', '').replace(',', '.')

def parse_date(datestr):
    """Convertit un texte de date en objet 'datetime'."""
    return dt.datetime.strptime(datestr, format_date)


def fusionne_infosupp(ligne_infosupp):
    """Réecrit la `Series` en une seule cellule."""
    ligne = ligne_infosupp.dropna()
    nom_info = ligne.index.to_series()
    padding = nom_info.str.len().max()

    return '\n'.join(nom_info.str.pad(padding, 'right') + ': ' + ligne.apply(str))


def obtient_premiere_ligne(group):
    # Il ne doit pas y avoir de NaN, sauf dans Débit OU (exclusif) Crédit
    # Remarque: Le libellé interbancaire peut être NaN apparemment.
    try:
        NaN_ok = group.notnull().sum(axis=0).sum() == group.shape[1] - 1
        if not NaN_ok:
            loggeur.warning("Inattendu: tous NaNs (%d) dans une colonne:\n%s",
                           group.shape[1]-1, group)
    #TODO: NaN in Libellé Interbancaire (voir 2019/03/10)
    except IndexError as e:
        e.args += (group,)
        raise
    return group.iloc[0]


def parse_config(lecteur_config):
    config = yaml.safe_load(lecteur_config)
    regles_auto = cree_regles_auto(
                charges=[(re.compile(pattern, re.I), resultats)
                         for pattern,resultats in config['regles_auto']['charges'].items()],
                produits=[(re.compile(pattern, re.I), resultats)
                          for pattern,resultats in config['regles_auto']['produits'].items()]
                )
    return config, regles_auto


def charge_config(fichier_config='config.yaml'):
    try:
        with open(fichier_config) as lecteur_config:
            return parse_config(lecteur_config)

    except FileNotFoundError as err:
        # On se trouve peut-être dans Google Colab. Essayons via le Drive.
        try:
            from google.colab import auth
            from pydrive.auth import GoogleAuth
            from pydrive.drive import GoogleDrive
        except ImportError:
            # Rien n'a été trouvé
            loggeur.warning('Aucune expression régulière configurée pour détecter '
                    'automatiquement la classe (fichier %r) : %s', (fichier_config, err))
                    #'automatiquement la classe (fichier `regex_classes.py`) : %s', err)
            config = {}
            regles_auto = cree_regles_auto([], [])

        gauth = GoogleAuth()
        # Uses GoogleCredentials provided by google.colab.
        gauth.credentials = GoogleCredentials.get_application_default()
        drive = GoogleDrive(gauth)
        # fichier_config doit alors être un "id" (la dernière partie de l'URL de partage du fichier.)
        config_drive_import = drive.CreateFile({'id': fichier_config})
        lecteur_config = StringIO(config_drive_import.GetContentString())
        config_drive_import.clear()
        return parse_config(lecteur_config)

    return config, regles_auto



def devine_classe(operation, regles_auto, champ='Classe'):
    """`operation` est une ligne du tableau `operations`"""

    motif = operation['MOTIF']
    
    if np.isnan(operation['Crédit']):
        # C'est une charge
        
        if pd.notnull(motif):
            for regex, resultats in regles_auto.charges:
                if regex.search(motif):
                    try:
                        return resultats[champ]
                    except KeyError:
                        pass
    
        return '6'

    elif np.isnan(operation['Débit']):
        assert not np.isnan(operation['Crédit'])
        # C'est un produit
        
        if pd.notnull(motif):
            for regex, resultats in regles_auto.produits:
                if regex.search(motif):
                    try:
                        return resultats[champ]
                    except KeyError:
                        pass
        
        return '7'


def normalise_nom(nom_du_releve, tableau_noms, de='Relevé', vers='Complet'):
    """Renvoie nom uniquement identifiable à partir de celui du relevé"""
    # Normaliser les espaces multiples en un seul espace.
    regex_espaces = re.compile(r'\s+')
    # Supprime les Monsieur/Madame...
    regex_titre = re.compile(r'\b(M[r.]? (?:[Oo]u|[Ee]t) (?:Mme|Mll?e)|Mr?|Mll?e|Mme)\b\.? ')
    nom = nom_du_releve.str.title()\
             .str.replace(regex_espaces, ' ')\
             .str.replace(regex_titre, '')\
             .str.strip()
    #TODO: vérifier existence dans fichier inscription (par ex. pour inverser
    # nom et prénom)
    
    # Convertit noms du relevé en noms du remboursements
    trouve_noms = pd.Series(tableau_noms[vers])
    trouve_noms.index = tableau_noms[de]
    noms_double = trouve_noms.index.duplicated()
    lignes_noms_double = np.where(noms_double)
    assert not noms_double.any(), \
        "Nom dupliqué dans la colonne %r du fichier de conversion, "\
        "corrigez svp: l.%s: %s" %\
        (de, lignes_noms_double,
         trouve_noms.index.to_series().iloc[lignes_noms_double])

    loggeur.debug("Taille de la colonne `Noms` : %s\n"
                 "    Valeurs invalides: %s\n"
                 "    Taille de la série de conversion des noms: %s",
                 nom.shape,
                 nom.hasnans,
                 trouve_noms.shape)
    nouveaux_noms = trouve_noms[nom.fillna('')]
    nouveaux_noms.index = nom.index
    noms_inconnus = nouveaux_noms.isna().values
    if noms_inconnus.any():
        loggeur.warning('Attention, ces noms ne sont pas reconnus. Inchangés.'
                       '\n%s', pd.concat((nom[noms_inconnus].drop_duplicates(),
                                          nom_du_releve),
                                         axis=1, join='inner'))
                       #'\n'.join('%r' % n for n in nom[noms_inconnus].unique()))
    nouveaux_noms[noms_inconnus] = nom[noms_inconnus]
    return nouveaux_noms


def charge_classes(fichier_exercice, feuille='Classes'):
    ### TODO: changer 'Feuil1' en 'classes'/'catégories'
    raise NotImplementedError


# ~~> parseur_SoG
def parse_nature(operation_group):
    """Transforme un groupe de lignes décrivant la nature d'une opération en 
    dataframe.

    Exemple:
    24/09/2018            000001 VIR EUROPEEN…
                          POUR: ASSOC Zzyzx
                          REF: 9856257828664
                          REMISE: Repas champ…
                          MOTIF: Repas champi…
    """
    # crée la colonne 0 pour les identifiants ('POUR', 'REF', etc), 
    # la colonne 1 pour les valeurs (y compris quand il n'y a pas d'identifiant)
    operation = operation_group.str.extract(r'^(?:([A-Z]+)\s*:\s*)?(.*)$', expand=True)
    
    operation[0].iloc[0] = 'Info'
    operation[0].fillna('Commentaire', inplace=True)  # .fillna("ffill")
    
    # Fusionne identifiants dupliqués
    operation = operation.groupby(0)[1].agg(lambda values: '\n'.join(str(v) for v in values))

    # Ajoute les colonnes obligatoire de l'exercice
    operation = operation.reindex(index=operation.index.union(
                        ('Info', 'DE', 'POUR', 'MOTIF', 'REF', 'REMISE',
                         'Commentaire')))
    return operation.to_frame()


# ~~> parseur_SoG
def charge_releve_SoG(fichier_releve, encoding='iso8859-1'):
    """Lis le fichier de relevé en .csv au format Société Générale."""
    #TODO: si dans le drive, utiliser pydrive.
    with codecs.open(fichier_releve, 'r', encoding=encoding) as fr:

        # Lis le solde du relevé de compte (5 premières lignes)
        infos = []
        relevereader = csv.reader(fr, delimiter=';')
        for i, row in enumerate(relevereader):
            infos.append(row)
            if i == 4:
                break

        releve_info = {'agence'   : infos[0][0].rstrip(),
                       'compte'   : infos[1],
                       'CAV ADMI' : infos[2],  # Aucune idée de ce que c'est.
                       infos[3][0]: parse_date(infos[3][1]),
                       infos[4][0]: float(nombre_europeen_vers_us(infos[4][1])),
                       'Devise': infos[4][2]}

        # Lis le reste du fichier: le relevé de comptes en csv.

        releve = pd.read_csv(fr, sep=';', #skiprows=5,
                             decimal=',',
                             thousands=' ',
                             parse_dates=[0], #, 5],
                             dayfirst=True,
                             dtype={'Débit': str,
                                    'Crédit': float})

    # Bug de Pandas : n'arrive pas à lire nombre à virgules négatifs...
    releve['Débit'] = releve['Débit'].astype(str)\
                        .apply(nombre_europeen_vers_us).astype(float)

    return releve_info, releve


def operations_vers_exercice(operations, regles_auto, precedent_solde=np.NaN,
                             fichier_noms=None):

    loggeur.info('Traite %d operations, %d colonnes', *operations.shape)

    #colonnes_exercice = ['Intitulé', 'Nom', 'Date', 'Crédit', 'Débit', 'Solde',
    #                     'Mode', 'Classe', 'Commentaire', 'Info_supp']
    colonnes_diagnostique = ['Date', 'POUR', 'DE', 'Débit', 'Crédit', 'MOTIF']  # ~~> config
    # Combine bénéficiaire ou source
    crediteur = operations.DE.notnull()
    debiteur = operations.POUR.notnull()
    credite = operations['Crédit'].notnull()
    debite  = operations['Débit'].notnull()

    #pd.set_option('display.width', 180)
    #pd.set_option('display.max_columns', None)
    #loggeur.debug('Crédite:\n%s', pd.concat((credite, operations[colonnes_diagnostique]), axis=1))
    #print(crediteur.shape, debiteur.shape, credite.shape, debite.shape)
    #print(type(operations['Crédit']), operations['Crédit'].shape)
    #print(type(operations['Débit']), operations['Débit'].shape)

    assert (credite ^ debite).all(), \
            "`Crédit` et `Débit` devraient être mutuellement exclusifs.\n" + \
            str(operations[~(credite ^ debite)][colonnes_diagnostique])
    if (crediteur & debiteur).any():
        loggeur.warning("`DE` et `POUR` devraient être mutuellement exclusifs:"
                       "\n%s\nCorrige en fonction du débit/crédit.",
                   str(operations[crediteur & debiteur][colonnes_diagnostique]))

    # Ou utiliser .fillna()
    nom = operations.POUR.astype(str)
    nom[credite] = operations.DE[credite].astype(str)  # Ou .combine()

    sans_nom = (nom == str(np.NaN))
    if sans_nom.any():
        loggeur.warning('Débits sans destinataire reconnu-e (POUR):\n' + \
                       str(operations[sans_nom][colonnes_diagnostique]))
        nom[sans_nom & debite] = operations.DE[sans_nom & debite].astype(str)

    sans_nom = (nom == str(np.NaN))
    if sans_nom.any():
        loggeur.warning('Mouvements sans destinataire ou source reconnu-e :\n' + \
                       str(operations[sans_nom][colonnes_diagnostique]))
        nom[sans_nom] = ''
        # Ça peut être les remises de chèques, mais pas seulement.
        # Ça peut aussi être les échecs de virements.
    
    ### TODO: convertir les noms avec le nom usuel chez les Phoenix, pas en majuscule.
    if fichier_noms is not None:
        try:
            nom = normalise_nom(nom, pd.read_csv(fichier_noms))
        except FileNotFoundError as err0:
            # On se trouve peut-être dans Google Colab. Essayons via le Drive.
            try:
                from google.colab import auth
                from pydrive.auth import GoogleAuth
                from pydrive.drive import GoogleDrive
            except ImportError:
                raise err0
            gauth = GoogleAuth()
            # Uses GoogleCredentials provided by google.colab.
            gauth.credentials = GoogleCredentials.get_application_default()
            drive = GoogleDrive(gauth)
            # fichier_noms doit alors être un "id" (la dernière partie de l'URL de partage du fichier.)
            noms_drive_import = drive.CreateFile({'id': fichier_noms})
            lignes_noms = noms_drive_import.GetContentString().split('\n')
            noms_drive_import.clear()
            csv_noms = csv.reader(lignes_noms)
            titres_noms = next(csv_noms)
            nom = normalise_nom(nom,
                                pd.DataFrame.from_records(csv_noms,
                                                          columns=titres_noms))
    else:
        loggeur.warning("Les noms seront écrits tels qu'ils apparaissent dans le relevé.\n"\
                       "Il serait préférable de les normaliser")

    mvt = operations['Crédit'].copy()
    mvt[debite] = operations['Débit'][debite]
    assert not mvt.isna().sum(), 'Mouvements sans montant détecté:\n' + str(operations[mvt.isna()])
    # ~~> config
    mode = operations['Libellé interbancaire'].replace({
                                                'AUTRES VIREMENTS RECUS': 'VR',
                                                'AUTRES VIREMENTS EMIS': 'VR',
                                                'REMISES DE CHEQUES': 'CH'})
    classe = operations.apply(devine_classe, args=(regles_auto,),
                              axis=1, result_type='reduce')
    
    # ~~> config
    info_supp = operations[operations.columns.difference(('MOTIF', 'DE', 'POUR',
        'Date', 'Crédit', 'Débit', 'Libellé interbancaire'))]\
        .apply(fusionne_infosupp, axis=1, result_type='reduce')

    assert operations.MOTIF.index is operations.index
    assert (operations.index == nom.index).all(), "%s VS %s" % (operations.MOTIF.index, nom.index)
    assert (operations.index == operations.Date.dt.floor('d').index).all()
    assert (operations.index == operations['Crédit'].index).all()
    assert (operations.index == (-operations['Débit']).index).all()
    assert (operations.index == mvt.cumsum().index).all() #TODO: formule
    assert (operations.index == mode.index).all()
    assert (operations.index == classe.index).all()
    #assert (operations.index == pd.Series().index).all() #operations['Commentaire']
    assert (operations.index == info_supp.index).all()
    
    nlign = operations.MOTIF.shape[0]

    assert nom.shape == (nlign,),    (type(nom), nom.shape)
    assert (mvt.cumsum() + precedent_solde).shape == (nlign,), (type(mvt), mvt.shape)
    assert mode.shape == (nlign,),   (type(mode), mode.shape)
    assert classe.shape == (nlign,), (type(classe), classe.shape)
    assert info_supp.shape == (nlign,), (type(info_supp), info_supp.shape, str(info_supp))

    ajouts_exercice = pd.concat((operations.Date.dt.floor('d'),
                                 pd.Series(dtype=str),
                                 nom,
                                 operations['Crédit'],
                                 -operations['Débit'],
                                 mvt.cumsum() + precedent_solde, #TODO: formule
                                 mode,
                                 classe,
                                 operations.MOTIF,
                                 info_supp
                                 ),
                                 axis=1,
                                 keys=['Date',
                                       'Catégorie',
                                       'Nom',
                                       'Crédit',
                                       'Débit',
                                       'Solde',
                                       'Mode',
                                       'Classe',
                                       'Intitulé',
                                       'Info_supp'],
                                 sort=False)

    return ajouts_exercice


def trouve_debut_operations(exercice, operations):
    """Renvoie uniquement les lignes d'opération non présentes dans exercice."""

    if exercice.Date.iloc[-1] >= operations.Date.iloc[-1]:
        loggeur.info("Pas de nouvelles opérations à ajouter.")
        return
    
    # Ne pas matcher sur 'Intitulé' et 'Nom', car elles ont pu être manuellement modifiées.
    matching_cols = ['Date', 'Crédit', 'Débit']
    fin_exercice = exercice.iloc[-1][matching_cols].fillna(0)
    fin_exercice['Débit'] = -fin_exercice['Débit']
    
    n_operations = operations.shape[0]
    debut_ajouts = operations.Date.searchsorted(fin_exercice.Date,
                                                side='right')
    try:
        # Older pandas version always returns an array
        debut_ajouts = debut_ajouts[0] - 1
    except IndexError:
        # Pandas update that now returns scalar on scalar input.
        debut_ajouts = debut_ajouts - 1
    loggeur.debug("Trouve debut_ajouts: %d", debut_ajouts)
    #if debut_ajouts == n_operations:
    if debut_ajouts == -1:
        loggeur.warning("Toutes les opérations sont *strictement* plus récentes que l'exercice.")

    loggeur.debug("fin_exercice[matching_cols]:\n%s", fin_exercice[matching_cols])
    #while debut_ajouts < n_operations and \
    #        (fin_exercice != operations[matching_cols].iloc[debut_ajouts].fillna(0)).any():
    #    debut_ajouts += 1
    if debut_ajouts != -1 and \
            (fin_exercice != operations[matching_cols].iloc[debut_ajouts].fillna(0)).all():

        # Cas particulier: quand c'est la 1e ligne: ni débit, ni crédit.
        if exercice.shape[0]==1 and fin_exercice['Débit']==0 \
                and fin_exercice['Crédit']==0:
            loggeur.info('Exercice est vide. Remplis les 1e opérations à partir du %s', operations.Date[debug_ajouts+1])
        else:
            raise ValueError("Les opérations antérieures à la dernière date de "
                "l'exercice ne correspondent pas (montants) à la fin de l'exercice:\n" +
            str(operations[matching_cols].iloc[debut_ajouts].fillna(0)))

    #if debut_ajouts == n_operations and operations.Date.iloc[-1] > fin_exercice.Date:
    #    loggeur.warning(
    #            "La dernière ligne d'exercice n'a pas pu être trouvée dans le relevé d'opérations:\n" \
    #            + exercice.iloc[-1][['Date', 'Intitulé', 'Nom', 'Débit', 'Crédit', 'Solde']]\
    #                .to_frame().to_string() \
    #            + "\nUtilise la date comme seule info de départ.")
    #    debut_ajouts = operations.Date.searchsorted(fin_exercice.Date, "right")[0] - 1
    #assert exercice.iloc[-1].Solde == solde_debut, "Le solde trouvé dans opérations ne correspond pas."

    loggeur.debug("%d opérations, début des ajouts: %d", n_operations, debut_ajouts+1)
    
    return operations.iloc[(debut_ajouts+1):]


class ChargeurDonnees(object):
    """Classe stockant les différents tableurs et éxécutant la mise à jour de l'exercice."""

    # ~~> config
    feuille_validation = 'Classes'
    exercice_colonne_debut = 1
    exercice_colonne_fin = 11  # exclue  #TODO: optionnelle: drop les colonnes au nom vide.
    exercice_ligne_debut = 4  # Entrée et sortie
    classes_ligne_debut = 2
    classes_colonne = 1
    modes_ligne_debut = 2
    modes_colonne = 0
    modes_nlignes = 3

    def _charge_exercice_excel(soi):  # dtypes_attendus
        # Lis la feuille courante du fichier exercice
        exercice_workbook = pd.ExcelFile(soi.fichier_exercice)
        
        if isinstance(soi.feuille, int):
            soi.feuille = exercice_workbook.sheet_names[soi.feuille]
            loggeur.info("Lis la feuille %r", soi.feuille)

        soi.exercice = pd.read_excel(exercice_workbook, sheet_name=soi.feuille,
                                 skiprows=soi.exercice_ligne_debut,
                                 usecols=list(range(soi.exercice_colonne_debut,
                                                    soi.exercice_colonne_fin)))

        soi.precedents_soldes = exercice_workbook.parse(soi.feuille,
                                        skiprows=(soi.exercice_ligne_debut-2),
                                        header=None,
                                        usecols=(soi.exercice_colonne_debut+7,
                                                 soi.exercice_colonne_debut+8),
                                        nrows=2, dtype={1: float},
                                        names=['date', 'montant'])

        if soi.feuille_validation in exercice_workbook.sheet_names:
            soi.modes = pd.read_excel(exercice_workbook,
                                      sheet_name=soi.feuille_validation,
                                      skiprows=soi.modes_ligne_debut,
                                      usecols=(soi.modes_colonne,),
                                      nrows=soi.modes_nlignes,
                                      squeeze=True)
            soi.classes = pd.read_excel(exercice_workbook,
                                        sheet_name=soi.feuille_validation,
                                        skiprows=soi.classes_ligne_debut,
                                        usecols=(soi.classes_colonne,),
                                        squeeze=True).dropna()
        else:
            loggeur.warning("La feuille de validation %r est absente du "
                           "fichier !\nLes valeurs de validation de 'modes' "
                           "et 'classes' ne seront pas chargées.",
                           soi.feuille_validation)

        exercice_workbook.close()


    def _charge_exercice_gsheets(soi):
        """Télécharge localement un tableur Google Sheets et lis les données.
        Fonctionne aussi depuis un notebook colab (en ligne dans le drive).
        """
        exercice_workbook = soi.gc.open(soi.fichier_exercice)
        # Ça pourrait être mieux d'utiliser gc.open_by_key()  # En cas de synonymes.
        # Cf. gc.list_spreadsheet_files

        try:
            worksheet = exercice_workbook.get_worksheet(soi.feuille)
        except TypeError:
             worksheet = exercice_workbook.worksheet(soi.feuille)

        # get_all_values gives a list of rows.
        lignes = worksheet.get_all_values()
        
        # Convert to a DataFrame and render.
        soi.exercice = pd.DataFrame.from_records(
                [l[soi.exercice_colonne_debut:soi.exercice_colonne_fin] for l in lignes[soi.exercice_ligne_debut+1:]],
                columns=lignes[soi.exercice_ligne_debut][soi.exercice_colonne_debut:soi.exercice_colonne_fin])

        soi.precedents_soldes = pd.DataFrame.from_records(
            [l[soi.exercice_colonne_debut+7:soi.exercice_colonne_debut+9:]
                for l in lignes[soi.exercice_ligne_debut-2:soi.exercice_ligne_debut]],
            columns=['date', 'montant'])
        
        try:
            lignes_val = exercice_workbook.worksheet(soi.feuille_validation).get_all_values()
            titre_modes = lignes_val[soi.modes_ligne_debut][soi.modes_colonne]
            titre_classes = lignes_val[soi.classes_ligne_debut][soi.classes_colonne]
            if not re.match(r'modes?$', titre_modes, re.I) or not re.match(r'classes?$', titre_classes, re.I):
                loggeur.warning('Noms des plages de validations inattendus: %r, %r (vérifier les index de début)',
                                titre_modes, titre_classes)
            soi.modes = pd.Series([l[soi.modes_colonne] for l in
                            lignes_val[soi.modes_ligne_debut+1:soi.modes_ligne_debut+1+soi.modes_nlignes]],
                            name=titre_modes)
            soi.classes = pd.Series([l[soi.classes_colonne] for l in
                                     lignes_val[soi.classes_ligne_debut+1:]
                                     if l[soi.classes_colonne]],
                                    name=titre_classes)
            #TODO: vérifications: assert soi.modes.iloc[0,0] == 'mode' and soi.classes.iloc[0,0] == 'classe'
        except gspread.exceptions.WorksheetNotFound:
            loggeur.warning("La feuille de validation %r est absente du "
                           "fichier !\nLes valeurs de validation de 'modes' "
                           "et 'classes' ne seront pas chargées.",
                           soi.feuille_validation)


    def charge_operations(soi, fichier_releve, encoding='iso8859-1'):
        """Charge le relevé et le convertit en 'opérations' (tableau avec
        une opération par ligne).
        Stocke : 
            - releve_info
            - releve
            - operations.
        """
        soi.releve_info, soi.releve = charge_releve_SoG(fichier_releve, encoding)
        
        # Chaque opération est codée sur plusieurs lignes. Crée un identifiant pour
        # chaque opération.
        valid_date = soi.releve.Date.notnull()
        operation_id = valid_date.astype(int)
        operation_id[valid_date] = np.arange(0, valid_date.sum(), dtype=int)
        operation_id[~valid_date] = np.NaN
        operation_id = operation_id.fillna(method='ffill').astype(int)
        
        releve_g = soi.releve.groupby(operation_id)
        
        nature = releve_g["Nature de l'opération"].agg(parse_nature)  # ~~> config
        releve_nature = pd.concat(nature.values, axis=1, ignore_index=True,
                                  sort=False).T

        ope_colonnes = ["Date", "Débit", "Crédit", "Devise", "Date de valeur",
                        "Libellé interbancaire"]  # ~~> config
        releve_compact = releve_g[ope_colonnes].apply(obtient_premiere_ligne)
        soi.operations = pd.concat((releve_compact, releve_nature), axis=1)

        # Complète les motifs manquants par le champ "REF".  ~~> config
        sans_motif = soi.operations.MOTIF.isna()
        soi.operations.loc[sans_motif, 'MOTIF'] = soi.operations.loc[sans_motif, 'REF']

    def __init__(soi, fichier_exercice, feuille=0, source="excel",
                 fichier_noms=None, brut=False):
        """Charge l'exercice et effectue des vérifications"""
        soi.fichier_exercice = fichier_exercice
        soi.feuille = feuille
        soi.fichier_noms = fichier_noms
        soi.dans_google_colab = False

        if source.lower() == "excel":
            soi._charge_exercice_excel()
        elif source.lower() in ("google sheets", "gs", "googlesheets"):
            try:
                from google.colab import auth
                auth.authenticate_user()
                soi.dans_google_colab = True
                # Remarque: il faut alors téléverser les fichiers nécessaires sur le colab:
                # fichier_noms (si pas dans le drive)
                # relevé (si pas dans le drive)
            except ImportError:
                loggeur.info('Importe les Google Sheets localement.')

            import gspread
            from oauth2client.client import GoogleCredentials
            global gspread  # Ré-utilisé dans _charge_exercice_gsheets.
            global GoogleCredentials

            # Or:
            # Read <https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html>

            #from oauth2client.service_account import ServiceAccountCredentials

            ## use creds to create a client to interact with the Google Drive API
            #scope = ['https://spreadsheets.google.com/feeds']
            #creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
            #gc = gspread.authorize(creds)
            soi.gc = gspread.authorize(GoogleCredentials.get_application_default())
            soi._charge_exercice_gsheets()
        else:
            raise ValueError("`source` doit être 'google sheets' ou 'excel'")

        loggeur.debug('Raw reading of exercice: shape %s\ndtypes: %s\nHead:\n%s.',
                     soi.exercice.shape, soi.exercice.dtypes, soi.exercice.head())
        if not brut:  # Active "brut" pour débugger.
            soi._prepare()


    def _prepare(soi):
        """Sanity check de l'exercice après chargement et transformations de colonnes."""
        ### TODO: (no unnamed colonnes, valid data types)
        soi.exercice.columns = soi.exercice.columns.str.capitalize()
        #colonnes_attendues = np.array(['Date', 'Intitulé', 'Nom', 'Crédit', 'Débit', 'Solde', 'Mode', 'Classe'])
        colonnes_attendues = np.array(['Date', 'Catégorie', 'Nom', 'Crédit', 'Débit', 'Solde', 'Mode', 'Classe', 'Intitulé'])  # ~~> config
        if set(soi.exercice.columns[:len(colonnes_attendues)]) != set(colonnes_attendues):
            loggeur.warning('Les colonnes trouvées ne correspondent pas:\n%s\n' % soi.exercice.head().to_string())
            loggeur.debug('Indexation à partir de 0:\n'
                         'Colonne de début: %2d\n'
                         'Colonne de fin:   %2d\n'
                         'Ligne de début:   %2d',
                         soi.exercice_colonne_debut,
                         soi.exercice_colonne_fin,
                         soi.exercice_ligne_debut)

        soi.exercice['Nom'] = soi.exercice.Nom.fillna('').str.rstrip()
        soi.exercice['Date'] = pd.to_datetime(soi.exercice.Date, errors='coerce',
                                           dayfirst=True)\
                                        .dt.floor('d')\
                                        .replace('', np.NaN)\
                                        .fillna(method='ffill')
        loggeur.debug('Classes chargées:\n%s', soi.classes.head())
        soi.exercice['Classe'] = soi.exercice.Classe\
                                .astype(CategoricalDtype(
                                            [''] + soi.classes.tolist()))  # voir le range 'classe'
        soi.exercice['Catégorie'] = soi.exercice['Catégorie'].astype(CategoricalDtype())
        soi.precedents_soldes.index = ['réel', 'théorique']
        if soi.precedents_soldes['montant'].dtype != float:
            soi.precedents_soldes['montant'] = soi.precedents_soldes['montant'].map(nombre_europeen_vers_us).replace('', np.NaN).astype(float)


        # Vérifie les types de valeurs (nombres voulus dans 'Crédit', 'Débit', 'Solde').
        for colonne in ('Crédit', 'Débit', 'Solde'):
            if soi.exercice[colonne].dtype != float:
                # Si chargé depuis gspread, les nombres sont des strings...
                soi.exercice[colonne] = soi.exercice[colonne].map(nombre_europeen_vers_us).replace('', np.NaN).astype(float)
                # Identifie les valeurs problématiques grâce au message d'erreur de Pandas
        #assert soi.precedents_soldes.montant.dtype == float  #déjà vérifié

        if soi.precedents_soldes['montant'].isna().any():
            loggeur.warning("Attention, tous les précédents soldes ne sont pas renseignés.")
        else:
            assert soi.precedents_soldes['montant']['réel'] == soi.precedents_soldes['montant']['théorique'], "Précédent solde réel != théorique"
        precedent_solde_reel = soi.precedents_soldes['montant']['réel']
        dernier_solde = soi.exercice.Solde.iloc[-1]
        assert precedent_solde_reel == dernier_solde, \
            "%s %r != dernier solde de l'exercice %r" % \
                (soi.precedents_soldes.date['réel'], precedent_solde_reel,
                 dernier_solde)


    def met_a_jour(soi, fichier_releve, encoding, fichier_config='config.yaml'):
        """Fusionne les nouvelles opérations dans exercice."""
        soi.charge_operations(fichier_releve, encoding)
        soi.mtn = dt.datetime.now().strftime('%y%m%d-%H%M%S')
        soi.ajd = dt.datetime.now().strftime('%y-%m-%d')
        soi.feuille_sortie = soi.feuille if isinstance(soi.feuille, str) else soi.ajd
        soi.fichier_config = fichier_config
        soi.config, soi.regles_auto = charge_config(fichier_config)

        nouvelles_operations = trouve_debut_operations(soi.exercice,
                                                       soi.operations)
        if nouvelles_operations is None or nouvelles_operations.shape[0]==0:
            soi.nouvel_exercice = None
            return

        ajouts_exercice = operations_vers_exercice(nouvelles_operations,
                                                   soi.regles_auto,
                                                   soi.exercice.iloc[-1].Solde,
                                                   soi.fichier_noms)
                                                   #soi.precedents_soldes['montant']['théorique'])
        loggeur.debug("type(ajouts_exercice): %s, "
                     "taille: %s, colonnes: %s",
                     type(ajouts_exercice),
                     getattr(ajouts_exercice, 'shape', None),
                     ajouts_exercice.columns)
        loggeur.debug("taille exercice: %s", soi.exercice.shape)

        soi.nouvel_exercice = pd.concat((soi.exercice, ajouts_exercice), sort=False)
        nouvelle_date = soi.nouvel_exercice.Date.iloc[-1].strftime(format_date)

        # Calcule et vérifie le nouveau solde
        solde_reel = soi.releve_info['Solde']
        solde_theo = soi.nouvel_exercice.Solde.iloc[-1]
        if round(solde_reel, 4) != round(solde_theo, 4):
            loggeur.warning('Solde réel %f != Solde théorique %f',
                           solde_reel, solde_theo)

        soi.nouveaux_soldes = pd.DataFrame([['solde réel au ' + nouvelle_date,
                                             solde_reel],
                                            ['solde théorique au ' + nouvelle_date,
                                             solde_theo]])

    def reecrit_excel(soi, nouveau_suffixe='-maj', suffixe_date=False, entier=False):
        if soi.nouvel_exercice is None: #or soi.nouvel_exercice.shape[0]==soi.exercice.shape[0]:
            loggeur.warning("Rien à écrire.")
            return

        fichier_sortie = soi.fichier_exercice.replace('.xls',
                                 (nouveau_suffixe +
                                  (soi.mtn if suffixe_date else '') +
                                  '.xls'))
        if op.exists(fichier_sortie):
            loggeur.warning("Fichier %r existe. Remplacé." % fichier_sortie)

        excelwriter = pd.ExcelWriter(fichier_sortie,
                                     date_format='yyyy/mm/dd',
                                     datetime_format='yyyy/mm/dd')

        final = (soi.nouvel_exercice if entier else soi.nouvel_exercice.iloc[soi.exercice.shape[0]+1:])
        final.to_excel(excelwriter, soi.feuille_sortie,
                       index=False, startrow=soi.exercice_ligne_debut,
                       startcol=soi.exercice_colonne_debut)

        worksheet = excelwriter.sheets[soi.feuille_sortie]
        try:
            # ~~> config
            #TODO: Obtenir ces largeurs depuis le fichier original.
            worksheet.set_column("B:B", 15)
            worksheet.set_column("C:C", 25)
            worksheet.set_column("D:D", 20)
            worksheet.set_column("J:J", 20)
            worksheet.set_column("K:K", 40)
        except AttributeError:
            # Module xlwt
            try:
                worksheet.col(soi.exercice_colonne_debut).set_width(15)
                worksheet.col(soi.exercice_colonne_debut+1).set_width(25)
                worksheet.col(soi.exercice_colonne_debut+2).set_width(20)
                worksheet.col(soi.exercice_colonne_debut+8).set_width(20)
                worksheet.col(soi.exercice_colonne_debut+9).set_width(40)
            except AttributeError:
                # Module openpyxl
                # use `openpyxl.utils.get_column_letter`
                worksheet.column_dimensions["B"].width = 15
                worksheet.column_dimensions["C"].width = 25
                worksheet.column_dimensions["D"].width = 20
                worksheet.column_dimensions["J"].width = 20
                worksheet.column_dimensions["K"].width = 40

        ## Exemple de code pour ajouter des menus déroulants ("data validation")
        #worksheet.data_validation('B15', {'validate': 'list',
        #                                  'source': '=$E$4:$G$4'})
        # In `openpyxl`: worksheet.add_data_validation

        # Réécrit le nouveau solde
        soi.nouveaux_soldes.to_excel(excelwriter, soi.feuille_sortie, index=False,
                                     header=False,
                                     startrow=(soi.exercice_ligne_debut - 2),
                                     startcol=(soi.exercice_colonne_debut + 7))

        excelwriter.save()

    def reecrit_gsheets(soi, nouveau_suffixe='-maj', suffixe_date=True, entier=False):
        """Attention, ici la date est ajoutée au nom de fichier par défaut."""
        if soi.nouvel_exercice is None:
            loggeur.warning("Rien à écrire.")
            return

        fichier_sortie = soi.fichier_exercice + nouveau_suffixe
        if suffixe_date:
            fichier_sortie += soi.mtn
        
        if any(sh['name'] == fichier_sortie for sh in soi.gc.list_spreadsheet_files()):
            loggeur.warning('Une googlesheets à ce nom existe déjà (%s), un doublon est créé.',
                            fichier_sortie)
        gsheet = soi.gc.create(fichier_sortie)
        #try: ... except BaseException: delete gsheet; raise
        
        feuille_sortie = soi.gc.open(fichier_sortie).sheet1
        final = (soi.nouvel_exercice if entier else soi.nouvel_exercice.iloc[soi.exercice.shape[0]+1:])

        lettres = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        # C.f. gpread.utils.rowcol_to_a1
        # Template pour écrire :
        # 'B5:K5'
        adresse_ligne = (lettres[soi.exercice_colonne_debut] + '{0:d}:' +
                         lettres[soi.exercice_colonne_fin-1] + '{0:d}')
        adresse = adresse_ligne[:-5] + '{1:d}'
        plage_solde = (lettres[soi.exercice_colonne_debut + 7]
                        + str(soi.exercice_ligne_debut - 1)
                        + ':'
                        + lettres[soi.exercice_colonne_debut + 7 + 1]
                        + str(soi.exercice_ligne_debut))

        final = final.assign(Date=final.Date.map(lambda t: t.strftime(format_date))).fillna('')
        #feuille_sortie.spreadsheet.fetch_sheet_metadata['properties']['locale'] = 'fr_FR'
        # Nécessite pydrive pour changer les Metadata, ou:
        #feuille_sortie._properties[]
        try:
            # .update() et .format() sont nouveaux dans la version 3.3.
            feuille_sortie.format(adresse_ligne.format(soi.exercice_ligne_debut+1),
                         {'textFormat': {'bold': True}})
            # Écrit les noms de colonnes d'abord:
            feuille_sortie.batch_update([{
                'range': adresse_ligne.format(soi.exercice_ligne_debut+1),
                'values': [final.columns.tolist()]},
                {
                'range': adresse.format(soi.exercice_ligne_debut+2,
                                        soi.exercice_ligne_debut+1+final.shape[0]),
                'values': final.values.tolist()},
                {
                'range': plage_solde,
                'values': soi.nouveaux_soldes.values.tolist()}])
        except AttributeError:
            loggeur.warning('Mettez à jour gspread pour des updates de googlesheets plus efficaces.')

            # Écrit les noms de colonnes d'abord:
            cell_colonnes = feuille_sortie.range(adresse_ligne.format(soi.exercice_ligne_debut+1))
            for cell, contenu in zip(cell_colonnes, final.columns):
                cell.value = contenu
            feuille_sortie.update_cells(cell_colonnes)
            # L'ordre d'update à l'air d'être important. Mieux vaux update par morceaux.

            loggeur.debug('Titres de colonnes en %s (%d cellules)',
                          adresse_ligne.format(soi.exercice_ligne_debut+1),
                          len(cell_colonnes))
            toutes_cellules = []
            for i, (_, ligne) in enumerate(final.iterrows(), start=soi.exercice_ligne_debut+1):
                cell_ligne = feuille_sortie.range(adresse_ligne.format(i+1))
                for j, contenu in enumerate(ligne): #, start=soi.exercice_colonne_debut):
                    cell_ligne[j].value = contenu
                toutes_cellules += cell_ligne
            loggeur.debug('Valeurs en %s -> %s (%d cellules)',
                          adresse_ligne.format(soi.exercice_ligne_debut+2),
                          adresse_ligne.format(i+1),
                          len(toutes_cellules))
            feuille_sortie.update_cells(toutes_cellules)

            cell_solde = feuille_sortie.range(plage_solde)
            loggeur.debug('Solde en %s (%d cellules)', plage_solde, len(cell_solde))
            for cell, contenu in zip(cell_solde, soi.nouveaux_soldes.values.flat):
                cell.value = contenu

            feuille_sortie.update_cells(cell_solde)
            

