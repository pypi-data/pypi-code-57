import configparser
import click
import os
import sys
import frontmatter
from PyInquirer import prompt, print_json


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


def all_folders(folder_name: str):
    return [
        os.path.join(folder_name, x)
        for x in os.listdir(folder_name)
        if os.path.isdir(os.path.join(folder_name, x))
    ]


def all_images_posts(project_path: str) -> (dict, list):
    post_list = all_files(os.path.join(project_path, "_posts"))
    image_list = all_files(os.path.join(project_path, "assets/images/"))
    movie_lists = []
    movie_data = {}
    for file in post_list:
        with open(file, encoding="cp850") as f:
            movie_info = frontmatter.load(f)
            movie_date = movie_info["date"]
            movie_data["name"] = movie_info["movie_name"]
            movie_data["file"] = file
            movie_data["image"] = movie_info["image"]
            movie_data["date"] = movie_info["date"]
        movie_lists.append(movie_data)
        movie_data = {}
    return movie_lists

def _delete_check(filename:str) ->None:
    correct_name = [
                {
                    "type": "confirm",
                    "name": "canDelete",
                    "message": f"Do you want to delete {filename}",
                    "default": False,
                }
            ]
    result = prompt(correct_name)
    if result['canDelete']:
        os.remove(filename)
        return
    return 

def delete_file(file_list:list) ->None:
    for f in file_list:
        _delete_check(f)

