import configparser
import click
import os
import sys


def get_project():
    return get_info("project")


def get_tmdb():
    return get_info("tmdb")


def get_api():
    return get_info("api")


def get_author():
    return get_info("author")


def get_info(key):
    homde_dir = os.path.expanduser("~")
    config = configparser.ConfigParser()
    config.read(os.path.join(homde_dir, ".daamiReview"))
    try:
        return config["info"][key]
    except:
        return None


def all_files(folder_name: str):
    return [
        os.path.join(folder_name, x)
        for x in os.listdir(folder_name)
        if os.path.isfile(os.path.join(folder_name, x))
    ]
