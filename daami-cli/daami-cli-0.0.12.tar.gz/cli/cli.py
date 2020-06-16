from __future__ import print_function, unicode_literals

import click
import configparser
import os
import sys
import frontmatter
import requests
from datetime import date
import pprint
from .search import Search
from cli.service.tm import Tm
from PyInquirer import prompt, print_json


def validate_rating(ctx, param, value):
    if value < 10.0 and value > 0:
        return value
    else:
        raise click.BadParameter(
            "Hold UP 0_o !!!! Your rating meter is above the roof. Roof being 10"
        )


def get_info(key):
    homde_dir = os.path.expanduser("~")
    config = configparser.ConfigParser()
    config.read(os.path.join(homde_dir, ".daamiReview"))
    try:
        return config["info"][key]
    except:
        return


def create_review(project_folder, name, template,trailer):
    review_date = date.today().strftime("%Y-%m-%d")
    template["date"] = review_date
    nl = '\n'
    if trailer:
        trailer_part = f'{{% youtube "{trailer}" %}}'
        body = f'nothing {nl}{trailer_part}'
    else:
        body = 'nothing'
    post = frontmatter.Post(body, **template)
    with open(
        os.path.join(project_folder, "_posts", review_date + "-" + name + ".md"), "w"
    ) as f:
        f.write(frontmatter.dumps(post))
    click.echo(click.style(f"The page for review {name} has been created", fg="green"))


def prompt_result(answer):
    return prompt(answer)


def get_project():
    return get_info("project")


def get_tmdb():
    return get_info("tmdb")


def get_api():
    return get_info("api")


def get_author():
    return get_info("author")


def all_files(folder_name: str):
    return [
        os.path.join(folder_name, x)
        for x in os.listdir(folder_name)
        if os.path.isfile(os.path.join(folder_name, x))
    ]


def movie_present(movie_name: str, project_path: str):
    file_list = all_files(os.path.join(project_path, "_posts"))
    for file in file_list:
        with open(file) as f:
            movie_info = frontmatter.load(f)
            if movie_info["movie_name"].lower() == movie_name.lower():
                return True
    return False


def does_contain(folder_name: str, required_folder: str):
    all_folder = [
        x
        for x in os.listdir(folder_name)
        if os.path.isdir(os.path.join(folder_name, x))
    ]
    if required_folder in all_folder:
        return True
    return False


def check_setup():
    homde_dir = os.path.expanduser("~")
    if os.path.isfile(os.path.join(homde_dir, ".daamiReview")):
        return True
    return False


def folder_Present(dir_name):
    if os.path.isdir(dir_name):
        return True
    return False


def movie_certificate(language):
    if language.lower() == "korean":
        choices = ["G-General", "PG_12-Age 12+", "PG_15-Age 15+", "R_18-Age 18+"]
    elif language.lower() == "hindi" or language.lower() == "nepali":
        choices = [
            "U-Unrestricted",
            "UA-Unrestricted with Caution",
            "A-Adults",
            "S-Restricted to special classes",
        ]
    else:
        choices = [
            "G-General Audiences",
            "PG-Parental Guidance Suggested",
            "PG_13-Parents Strongly Cautioned",
            "R-Restricted" "NC_17–Adults Only",
        ]
    movie_certi = [
        {
            "type": "list",
            "name": "mC",
            "message": "Identify the movie Certificate",
            "choices": choices,
            "filter": lambda val: val.split("-")[0].replace("_", "-"),
        }
    ]
    result = prompt(movie_certi)
    return result["mC"]

def download_image(image_url,project_folder,movie_name):
    img_data = requests.get(image_url).content
    with open(
        os.path.join(
            project_folder, "assets", "images", f"{movie_name}.jpg"
        ),
        "wb",
    ) as handler:
        handler.write(img_data)



@click.group(help="Will help to aid in creating files for daamireview")
def cli():
    pass


@cli.command()
@click.option("--project", "-p", prompt=True, default=get_project(), type=click.Path())
@click.option(
    "--api_key",
    "-p",
    prompt=True,
    default=get_api(),
    help="Api key to do google search check the channel to get one",
)
@click.option(
    "--tmdb_key", "-p", prompt=True, default=get_tmdb(), help="Api key to do tmdb"
)
@click.option("--author", "-a", default=get_author(), prompt=True, help="The writter")
def setup(project, api_key, author, tmdb_key):
    """Setup daami-cli to point to the given project"""
    homde_dir = os.path.expanduser("~")
    config = configparser.ConfigParser()
    config["info"] = {
        "project": project,
        "api": api_key,
        "author": author,
        "tmdb": tmdb_key,
    }
    with open(os.path.join(homde_dir, ".daamiReview"), "w") as configfile:
        config.write(configfile)


@cli.command()
@click.option("--project", "-p", help="The location of the project")
@click.option("--title", "-T", prompt=True, help="title of the article")
@click.option("--movie", "-m", prompt=True, help="Name of the movie being reviewed")
@click.option("--language", "-l", prompt=True, help="The language the movie is in")
@click.option(
    "--rating",
    "-r",
    prompt=True,
    default=0,
    help="Your rating",
    type=float,
    callback=validate_rating,
)


def review(title, movie, project, language, rating):
    """ Generates the review file in the _post folder of the project"""
    # check if setup file is there or not before proceeding
    if not check_setup():
        click.echo(
            click.style("Cannot find config file do run daami-cli setup", fg="red")
        )
        sys.exit(1)
    # get the project folder
    project_folder = get_project()
    api_key = get_api()
    author = get_author()
    if not project_folder or not api_key or not author:
        click.echo(
            click.style(
                "The setup for the project is not complete rerun daami-cli setup",
                fg="red",
            )
        )
        sys.exit(1)
    # checks to make sure the project folder is present
    if not folder_Present(project_folder):
        click.echo(
            click.style(
                "The project folder specified in setup is not present", fg="red"
            )
        )
        sys.exit(1)
    # checks to make sure the project folder has _posts
    if not does_contain(project_folder, "_posts"):
        click.echo(
            click.style(
                "The project folder doesn't look like a jekyll project", fg="red"
            )
        )
        sys.exit(1)

    # read all other posts to check if that movie is present or not
    if movie_present(movie, project_folder):
        click.echo(
            click.style(f"The movie {movie} has already been reviewed", fg="red")
        )
        sys.exit(1)

    # create a movie review post
    template = {
        "layout": "post",
        "rating": "change",
        "title": title.title(),
        "language": language.capitalize(),
        "movie_name": movie.capitalize(),
        "movie": ["change"],
        "cast-crew": {"change": "change"},
        "date": "change",
        "image": "change",
        "author": author.title(),
        "tags": [language.title()],
    }
    movie_info = {}
    trailer = None
    # collecting other data for info
    # searching imdb with google
    click.echo(click.style(f"Looking through imdb for movie {movie}", fg="green"))
    a = Search(movie, api_key, language, template, project_folder)
    image_im, movie_info_im, cast_info,imdb_id = a.data()
    ## looking through tmdb
    click.echo(click.style(f"Looking through tmdb for movie {movie}", fg="green"))
    a = Tm(movie,imdb_id)
    image_tm,movie_info_tm = a.get_info()
    if movie_info_tm:
        if movie_info_tm['trailer']:
            trailer = movie_info_tm['trailer']
        movie_info["genre"] = movie_info_tm["genres"]
        length = movie_info_tm["runtime"]
        movie_info["length"] = f"{length} mins"
    else:
        movie_info = movie_info_im
    template["cast-crew"] = cast_info
    movie_info["rating"] = movie_certificate(language)
    if movie_info:
        template["movie"] = movie_info
        template["tags"].extend(movie_info["genre"])
    template["rating"] = rating
    if image_tm:
        download_image(image_tm,project_folder,movie)
    elif image_im:
        download_image(image_im,project_folder,movie)
    template["image"] = f"/assets/images/{movie}.jpg"
    # create a review file
    create_review(project_folder, title, template,trailer)
