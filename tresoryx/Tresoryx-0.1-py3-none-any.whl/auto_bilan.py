#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from sys import stderr
import argparse as ap
from collections import Counter
import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
#import xlsxwriter.format as xlformat
from tresoryx.communs import ChargeurDonnees

import logging
loggeur = logging.getLogger(__name__)



def print_bilan(fichier_exercice, categorisation='Classe', feuille=0, source="excel"):
    donnees = ChargeurDonnees(fichier_exercice, feuille, source)
    exercice = donnees.exercice

    print(exercice.groupby(categorisation).sum()[['Crédit', 'Débit']])
    print('-------\nTotaux:')
    print(exercice[['Crédit', 'Débit']].sum())


def auto_bilan(fichier_exercice, categorisation='Classe', feuille=0, source="excel"):
    donnees = ChargeurDonnees(fichier_exercice, feuille, source)
    exercice = donnees.exercice

    total_credit = round(exercice['Crédit'].sum(), 2)
    total_debit = round(exercice['Débit'].sum(), 2)

    colonne_categorie = exercice[categorisation]

    if isinstance(colonne_categorie.dtype, CategoricalDtype):
        if '' in colonne_categorie.cat.categories:
            colonne_categorie.cat.rename_categories({'': 'Non classé'}, inplace=True)
        else:
            colonne_categorie.cat.add_categories('Non classé', inplace=True)
    else:
        colonne_categorie.replace('', 'Non classé', inplace=True)

    loggeur.info('%d transactions avec catégorie invalide.', colonne_categorie.isna().sum())
    colonne_categorie[colonne_categorie.isna()] = 'Non classé'

    groupes = exercice.groupby(categorisation)

    excel_bilan = pd.ExcelWriter('auto_bilan-%s.xlsx' % categorisation,
                                 date_format='yyyy/mm/dd',
                                 datetime_format='yyyy/mm/dd')
    bilan = groupes.sum()[['Crédit', 'Débit']]

    # Remplace le CategoricalIndex, sinon le `append` échoue.
    bilan.index = pd.Index(bilan.index.to_list())

    bilan = bilan.append(bilan.sum().round(2).rename('Total'))
    try:
        assert np.allclose(bilan.loc['Total', ['Crédit', 'Débit']], [total_credit, total_debit])
    except AssertionError:
        print("Somme du bilan:", bilan.loc['Total'], file=stderr)
        print("Somme exercice:", total_credit, total_debit, file=stderr)
        raise

    bilan.to_excel(excel_bilan, 'Totaux')
    excel_bilan.sheets['Totaux'].set_column('A:A', 50)
    #xlformat.Format({'align': 'left'}))

    dejavu = Counter()
    for categorie, tableau in groupes:
        print(' ->', categorie)
        nom_feuille = categorie.split(' - ')[0][:27] if categorie else 'Non classé'
        if dejavu[nom_feuille.lower()]:
            nom_feuille += '.%d' % (dejavu[nom_feuille.lower()] + 1)
        dejavu[nom_feuille.lower()] += 1

        tableau.drop(columns=categorisation).to_excel(excel_bilan, nom_feuille, startrow=1)

        feuille_categorie = excel_bilan.sheets[nom_feuille]
        feuille_categorie.write(0, 0, categorie)
        feuille_categorie.set_column("B:B", 15)
        feuille_categorie.set_column("C:C", 25)
        feuille_categorie.set_column("D:D", 20)
        feuille_categorie.set_column("I:I", 20)
        feuille_categorie.set_column("J:J", 40)

    excel_bilan.close()


def main():
    logging.basicConfig()
    #logging.getLogger('tresoryx.communs').setLevel(logging.INFO)
    loggeur.setLevel(logging.INFO)

    parseur = ap.ArgumentParser(description=__doc__)
    parseur.add_argument('fichier_exercice')
    parseur.add_argument('-C', '--categorisation', default='Classe')

    auto_bilan(**vars(parseur.parse_args()))


if __name__ == '__main__':
    main()
