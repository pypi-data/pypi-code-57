import os
import click
import cli.info as info
import difflib
import frontmatter
from PyInquirer import prompt, print_json


def validate_rating(ctx, param, value) -> str:
    if value < 10.0 and value > 0:
        return value
    raise click.BadParameter(
        "Hold UP 0_o !!!! Your rating meter is above the roof. Roof being 10"
    )


def movie_present(movie_name: str, project_path: str) -> bool:
    file_list = info.all_files(os.path.join(project_path, "_posts"))
    movie_name_list = []
    for file in file_list:
        with open(file, encoding="cp850") as f:
            movie_info = frontmatter.load(f)
            movie_name_list.append(movie_info["movie_name"].lower())
    ## closest match check
    matches = difflib.get_close_matches(movie_name.lower(), movie_name_list)
    if movie_name.lower() in movie_name_list:
        return True
    elif matches:
        choices = matches
        choices.append("Not Above")
        movie_match = [
            {
                "type": "list",
                "name": "match",
                "message": "Found some similar movie that are already reviewed. Are you sure it's not same as",
                "choices": choices,
            }
        ]
        result = prompt(movie_match)
        if result["match"] != "Not Above":
            return True
    return False


def is_folder(folder_name: str) -> bool:
    if os.path.isdir(folder_name):
        return True
    return False


def is_file(file_name: str) -> bool:
    if os.path.isfile(file_name):
        return True
    return False


def is_jekyll_site(folder: str) -> bool:
    """
    Check if it is a jekyll site
    For it to be a jekyll site for our project
    we need to have _posts,assets
    """
    # check if it is a folder
    if is_folder(folder):
        list_folders = [
            x for x in os.listdir(folder) if is_folder(os.path.join(folder, x))
        ]
        if "_posts" in list_folders and "assets" in list_folders:
            return True
        return False
    return False


def is_setup_complete() -> bool:
    homde_dir = os.path.expanduser("~")
    needed_key = ["project", "api", "author", "tmdb"]
    if os.path.isfile(os.path.join(homde_dir, ".daamiReview")):
        for key in needed_key:
            if not info.get_info(key):
                return False
        return True
    return False
