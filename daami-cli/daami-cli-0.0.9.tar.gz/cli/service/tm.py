import tmdbsimple as tmdb
import configparser
import os
import sys
import click


def get_info(key):
    homde_dir = os.path.expanduser("~")
    config = configparser.ConfigParser()
    config.read(os.path.join(homde_dir, ".daamiReview"))
    try:
        return config["info"][key]
    except:
        click.echo(
            click.style(
                "The TMDB api key hasn't been setup contact the slack for the key",
                fg="red",
            )
        )
        sys.exit(1)


def get_tmdb():
    return get_info("tmdb")


class Tm:
    def __init__(self, movie,imdb_id):
        self.tmdb = tmdb
        self.tmdb.API_KEY = get_tmdb()
        self.movie = movie
        self.imdb_id = imdb_id


    def _search(self):
        search_string = self.tmdb.Search()
        movie_search = search_string.movie(query=self.movie)
        return search_string, movie_search

    def get_info(self):
        search_string, response = self._search()
        movie_id = []
        movie_info = {}
        for r in search_string.results:
            data = self._movie_info(r["id"])
            if data["imdb_id"] == self.imdb_id:
                poster = data['poster_path']
                image_url = f'https://image.tmdb.org/t/p/original{poster}'
                movie_info["genres"] = [x["name"] for x in data["genres"]]
                movie_info["runtime"] = data["runtime"]
                movie_info["imdb_id"] = data["imdb_id"]
                return image_url,movie_info
        return False,{}

    def _movie_info(self, id):
        movie = self.tmdb.Movies(id)
        response = movie.info()
        return response
