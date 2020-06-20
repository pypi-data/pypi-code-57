from __future__ import print_function, unicode_literals

import sys
import os
import configparser
import click
import cli.validator as validator
import cli.info as info
from datetime import datetime, date
from cli.service.search import Search
from cli.review.main import Review
from cli.service.tm import Tm


@click.group(help="Will help to aid in creating files for daamireview")
def cli():
    pass


@cli.command()
@click.option(
    "--project", "-p", prompt=True, default=info.get_project(), type=click.Path()
)
@click.option(
    "--api_key",
    "-p",
    prompt=True,
    default=info.get_api(),
    help="Api key to do google search check the channel to get one",
)
@click.option(
    "--tmdb_key", "-p", prompt=True, default=info.get_tmdb(), help="Api key to do tmdb"
)
@click.option(
    "--author", "-a", default=info.get_author(), prompt=True, help="The writter"
)
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
@click.option("--title", "-T", prompt=True, help="title of the article", type=str)
@click.option(
    "--movie", "-m", prompt=True, help="Name of the movie being reviewed", type=str
)
@click.option(
    "--language", "-l", prompt=True, help="The language the movie is in", type=str
)
@click.option(
    "--rating",
    "-r",
    prompt=True,
    default=0,
    help="Your rating",
    type=float,
    callback=validator.validate_rating,
)
def review(title, movie, language, rating):
    """ Generates the review file in the _post folder of the project"""
    # check if setup file is there or not before proceeding
    if not validator.is_setup_complete():
        click.echo(click.style("Rerun the daami-cli setup to setup the tool", fg="red"))
        sys.exit(1)

    # get the key from config file

    project_folder = info.get_project()
    api_key = info.get_api()
    author = info.get_author()
    tmdb = info.get_tmdb()

    ## check if the project folder is a jekyll folder
    if not validator.is_jekyll_site(project_folder):
        click.echo(click.style("The project folder is not a jekyll folder", fg="red",))
        sys.exit(1)

    # read all other posts to check if that movie is present or not
    if validator.movie_present(movie, project_folder):
        click.echo(
            click.style(f"The movie {movie} has already been reviewed", fg="red")
        )
        sys.exit(1)

    # # create a movie review post
    template = {
        "layout": "post",
        "spoiler": "False",
        "rating": rating,
        "title": title.title(),
        "language": language.capitalize(),
        "movie_name": movie.capitalize(),
        "movie": {"change": "change"},
        "cast-crew": {"change": "change"},
        "date": "change",
        "image": "change",
        "author": author.title(),
        "tags": [language.title()],
    }
    review = Review(tmdb, api_key, template, project_folder)
    review.create()


@cli.command()
@click.option("--movie", "-m", help="Name of the movie to be deleted", type=str)
@click.option(
    "--day",
    "-d",
    help="delete all reviews from this date format mm/dd/yy also takes today,yesterday",
    type=str,
    callback=validator.validate_date,
)
@click.option(
    "--since",
    "-s",
    help="delete all reviews since this date format mm/dd/yy also takes today,yesterday",
    type=str,
    callback=validator.validate_date,
)
def delete(movie, day, since):
    """Remove the review posts"""
    ## get a list of all files in _posts
    ## check if the project folder is a jekyll folder
    project_folder = info.get_project()
    if not validator.is_jekyll_site(project_folder):
        click.echo(click.style("The project folder is not a jekyll folder", fg="red",))
        sys.exit(1)

    to_delete = []
    all_movie = info.all_images_posts(project_folder)
    if day:
        day_obj = datetime.strptime(day, "%m/%d/%y").date()
        for movie_s in all_movie:
            if movie_s["date"] == day_obj:
                to_delete.append(movie_s["file"])
                to_delete.append(os.path.join(project_folder, movie_s["image"][1:]))

    elif since:
        since_obj = datetime.strptime(since, "%m/%d/%y").date()
        for movie_s in all_movie:
            if movie_s["date"] >= since_obj:
                to_delete.append(movie_s["file"])
                to_delete.append(os.path.join(project_folder, movie_s["image"][1:]))

    # check movie is present
    elif movie:
        if validator.movie_present(movie, project_folder):
            for movie_s in all_movie:
                if movie_s["name"].lower() == movie.lower():
                    to_delete.append(movie_s["file"])
                    to_delete.append(os.path.join(project_folder, movie_s["image"][1:]))

    if to_delete:
        info.delete_file(to_delete)
