#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from itertools import zip_longest
import argparse as ap
import pandas as pd
import logging


def fusionne_dettes(fichiers_dettes):

    fichiers_dettes, categories_dette = zip_longest(*(f.split(',')
                                                    for f in fichiers_dettes))
    print(fichiers_dettes, categories_dette)
    chaque_dette = [pd.read_excel(f, header=0, index_col=0)
                    for f in fichiers_dettes]
    toutes_dettes = chaque_dette[0]
    for i, autre_dette in enumerate(chaque_dette[1:], start=1):
        toutes_dettes = pd.merge(toutes_dettes, autre_dette,
                                 how='outer',
                                 left_index=True,
                                 right_index=True,
                                 validate='one_to_one',
                                 suffixes=('_%s' % categories_dette[i-1],
                                           '_%s' % categories_dette[i]))
                        #.fillna(0)
    toutes_dettes['Reste à rembourser'] = toutes_dettes[
                        [col for col in toutes_dettes.columns
                         if col.startswith('Reste à rembourser_')]].sum(axis=1)
    toutes_dettes.to_excel('toutes_dettes.xlsx')


if __name__ == '__main__':
    parser = ap.ArgumentParser(description=__doc__)
    parser.add_argument('fichier_dette', nargs='+')
    
    args = parser.parse_args()
    fusionne_dettes(args.fichier_dette)
