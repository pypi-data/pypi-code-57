#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle
from pathlib import Path

import requests
from PyInquirer import prompt
from uuid import getnode
from .config import AlloConfig
from .colors import BColors
from .telem import AlloTelem
from .gitutils import AlloGit


class TestingAllo:
    config_path = str(Path.home()) + "/allo-config.dict"
    api_path = "https://allo.dev.libriciel.fr/api/client"
    config: AlloConfig
    telem: AlloTelem
    git: AlloGit

    def __init__(self, env):
        self.load_config(env)
        self.telem = AlloTelem(self.config.id_client,
                               self.config.code_produit,
                               self.config.teleport_token,
                               self.config.env)
        self.git = AlloGit(self.config, self.get_valid_token())

        self.what_to_do()

    def save_config(self):
        with open(self.config_path, 'wb') as config_dictionary_file:
            pickle.dump(self.config, config_dictionary_file)

    def load_config(self, env):
        try:
            with open(self.config_path, 'rb') as config_dictionary_file:
                self.config: AlloConfig = pickle.load(config_dictionary_file)
        except FileNotFoundError:
            self.config = AlloConfig()
            self.config.env = env
            self.init_config_file()

    def init_config_file(self):
        error_config_msg = "Erreur de configuration, sortie du programme Allo"
        print(BColors.OKBLUE + "Merci de rentrer les informations suivantes afin d'initialiser Allo :")
        questions = [{'type': 'input', 'name': 'id_client', 'message': 'Identifiant unique Client'},
                     {'type': 'input', 'name': 'code_produit', 'message': 'Code Produit'}]
        cfg = prompt(questions)
        self.config.id_client = cfg['id_client']
        self.config.code_produit = cfg['code_produit']

        r = requests.get("{}/{}/versions".format(self.api_path, self.config.code_produit), headers={'channel': self.config.env})
        versions = r.json()
        if 'status' in versions :
            print(BColors.FAIL + "{} : {}".format(self.config.code_produit, versions['message']))
            print(BColors.FAIL + error_config_msg)
            exit(1)
        elif len(versions) is 0:
            print(BColors.FAIL + "{} : {}".format(self.config.code_produit, "Aucune versions disponibles"))
            print(BColors.FAIL + error_config_msg)
            exit(1)
        else:
            qversions = []
            for v in versions:
                qversions.append({"value": "0", "name": v['name']})
            questions = [{'type': 'list',
                          'name': 'version',
                          'message': 'Version du produit',
                          'choices': qversions}]
            answers = prompt(questions)
            self.config.version = versions[int(answers['version'])]

        if self.allo_activate():
            self.config.teleport_token = prompt(
                [{'type': 'input', 'name': 'teleport_token', 'message': 'Token de télémaintenance'}])['teleport_token']
            self.config.repo_path = prompt(
                [{'type': 'input', 'name': 'repo_path', 'message': 'Chemin d\'installation du logiciel'}])['repo_path']
            self.save_config()
        else:
            print(BColors.FAIL + "Erreur de configuration, sortie du programme Allo")
            exit(1)

    def allo_activate(self):
        r = requests.post("{}/{}/register".format(self.api_path, getnode()), json={
            "idClient": self.config.id_client,
            "product": self.config.code_produit,
            "version": self.config.version,
            "env": self.config.env
        })
        data = r.json()
        if 'status' in data:
            print(BColors.FAIL + "{} pour l'identifiant {} et le produit {}".format(data['message'],
                                                                                    self.config.id_client,
                                                                                    self.config.code_produit))
            return False
        if not data['active']:
            cfg = prompt([{'type': 'input', 'name': 'pin_code', 'message': 'Code PIN d\'activation Allo'}])
            r = requests.post("{}/{}/activate".format(self.api_path, getnode()), json={
                "idClient": self.config.id_client,
                "product": self.config.code_produit,
                "version": self.config.version,
                "env": self.config.env,
                'pin': cfg['pin_code']
            })
            data = r.json()
            if not data['active']:
                print(BColors.FAIL + "Mauvais code PIN")
                return False

        print(BColors.OKGREEN + "Connexion Allo OK")
        return True

    def get_valid_token(self):
        # Get deploy token
        r = requests.get(
            "{}/{}/{}/{}/token".format(self.api_path,
                                       self.config.id_client,
                                       self.config.code_produit,
                                       getnode()))
        if r.status_code is not 200:
            print(BColors.FAIL + "Impossible de récupérer le token : IP ou addresse MAC invalide")
            return False
        data = r.json()
        return data['token']

    def what_to_do(self):
        questions = [{'type': 'list', 'name': 'action', 'message': 'Que voulez-vous faire ?',
                      'choices': [
                          'Verifier la connexion',
                          'Ouvrir la télémaintenance',
                          # 'Modifier les informations de connexion',
                          'Mettre à jour',
                          'Annuler une mise à jour'
                      ]}]
        answers = prompt(questions)
        if 'action' not in answers:
            exit(0)
        if 'Verifier la connexion' in answers['action']:
            self.allo_activate()
        if 'Ouvrir la télémaintenance' in answers['action']:
            self.telem.connect()
        if 'Modifier les informations de connexion' in answers['action']:
            print("TODO")
        if 'Mettre à jour' in answers['action']:
            self.change_version(True)
        if 'Annuler une mise à jour' in answers['action']:
            self.change_version(False)
        self.what_to_do()

    def change_version(self, upgrade: bool):
        choices = self.git.get_versions_to_pass("", not upgrade)
        if len(choices) > 0:
            questions = [{'type': 'list',
                          'name': 'version',
                          'message': 'Mettre à jour vers quelle version ?' if upgrade else 'Revenir à quelle version ?',
                          'choices': choices}]
            ans = prompt(questions)
            self.git.upgrade_to(ans['version']) if upgrade else self.git.downgrade_to(ans['version'])
        else:
            print(BColors.OKBLUE +
                  ("=> Vous êtes déjà en dernière version" if upgrade else "=> Aucune version sur laquelle revenir"))


def launch():
    import sys
    env = "PROD"
    if len(sys.argv) > 1:
        env = sys.argv[1]
    TestingAllo(env)
