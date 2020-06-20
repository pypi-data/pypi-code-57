#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018 Guitou des Phoenix
#
# Ce fichier fait partie de Tresoryx, sous license GNU GPL.
# This file is part of Tresoryx, under GNU GPL license.


"""Script pour automatiser le remplissage du fichier `Exercice.xlsx` ou `Exercice.ods`
à partir du relevé de comptes en format .csv"""


from .communs import ChargeurDonnees

import argparse as ap
import logging


def met_a_jour_exercice(fichier_releve, fichier_exercice, feuille=0,
                    source="excel", encoding='iso8859-1', fichier_noms=None,
                    fichier_config='config.yaml'):
    """Complète l'exercice avec les nouvelles opérations présentes dans le
    relevé de compte"""
    donnees = ChargeurDonnees(fichier_exercice, feuille, source, fichier_noms)
    donnees.met_a_jour(fichier_releve, encoding, fichier_config)
    
    # Ré-écrit dans la feuille
    if source.lower() == 'excel':
        donnees.reecrit_excel()
    elif source.lower() in ('gs', 'google sheets', 'googlesheets'):
        donnees.reecrit_gsheets()
    else:
        raise ValueError("`source` doit être 'google sheets' ou 'excel'")


def main():
    # Parse les arguments de la ligne de commande.
    parseur = ap.ArgumentParser(description=__doc__)
    parseur.add_argument('releve')
    parseur.add_argument('exercice', nargs='?', default='Exercice.xlsx',
                         help='[%(default)s]')
    parseur.add_argument('config', nargs='?', default='config.yaml',
                        help='Fichier de configuration (ex: avec regles_auto)'\
                             ' au format YAML [%(default)s]')
    parseur.add_argument('-f', '--feuille', default=0,
                         help="Feuille de l'exercice à mettre à jour [%(default)s].")
    parseur.add_argument('-e', '--encoding', default='iso8859-1',
                         help='Encodage du fichier "relevé" [%(default)s].')
    parseur.add_argument('-s', '--source', default='excel',
                         choices=['excel', 'gs', 'google sheets', 'googlesheets'],
                         help="Source de l'exercice [%(default)s]")
    parseur.add_argument('-n', '--noms',
                         help='Fichier csv de conversion des noms')
    parseur.add_argument('-v', '--verbeux', action='count', default=0)

    args = parseur.parse_args()
    if args.verbeux > 1:
        logging.basicConfig(level=logging.DEBUG) #, format='%(levelname)s:%(message)s')
    elif args.verbeux > 0:
        logging.basicConfig(level=logging.INFO)

    met_a_jour_exercice(args.releve, args.exercice, args.feuille, args.source,
                        args.encoding, args.noms, args.config)


if __name__ == '__main__':
    main()
