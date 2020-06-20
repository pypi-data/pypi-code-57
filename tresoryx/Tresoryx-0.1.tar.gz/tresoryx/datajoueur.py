#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from sys import stderr
import re
import argparse as ap
import numpy as np
import pandas as pd


def charge_inscription(fichier_inscription):
    return pd.read_excel(fichier_inscription)


def infojoueurs(joueurs, data, info='Adresse mail'):
    assert info in data.columns

    infos = []
    trouves = []
    for joueur in joueurs:
        prenom, nom = joueur.split()
        loc = data.NOM.str.match(r'\b' + re.escape(nom) + r'\b', case=False)
        if loc.any():
            if loc.sum() != 1:
                loc &= data['Prénom'].str.match(r'\b' + re.escape(prenom) + r'\b', case=False)
                if not loc.sum().any():
                    print('WARNING: joueur non trouvé: %r' % joueur, file=stderr)
                    continue
                if loc.sum() > 1:
                    print('WARNING: plusieurs correspondances pour %r:\n%s' % (joueur,
                          data.loc[loc, ['NOM', 'Prénom']]), file=stderr)
                    continue
            infos.append(data[info][loc].values[0])
            trouves.append(joueur)
        else:
            print('WARNING: joueur non trouvé: %r' % joueur, file=stderr)
            #infos.append(None)

    return pd.Series(infos, index=trouves)


def main():
    parseur = ap.ArgumentParser(description=__doc__)
    parseur.add_argument('fichier_inscription')
    parseur.add_argument('info', help='exemple: "Adresse mail"')
    parseur.add_argument('joueurs', nargs='+')
    args = parseur.parse_args()
    data = charge_inscription(args.fichier_inscription)
    print(infojoueurs(args.joueurs, data, args.info))


if __name__=='__main__':
    main()
