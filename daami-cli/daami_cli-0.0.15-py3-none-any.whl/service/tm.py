import tmdbsimple as tmdb
import configparser
import requests
import ast
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
    def __init__(self, template, imdb_id):
        self.tmdb = tmdb
        self.tmdb.API_KEY = get_tmdb()
        self.template = template
        self.imdb_id = imdb_id

    def _search(self):
        search_string = self.tmdb.Search()
        movie_search = search_string.movie(query=self.template["movie_name"])
        return search_string

    def _get_trailer(self, id):
        url = (
            f"http://api.themoviedb.org/3/movie/{id}/videos?api_key={self.tmdb.API_KEY}"
        )
        result = requests.get(url).content
        dict_result = result.decode("UTF-8")
        info = ast.literal_eval(dict_result)
        for video_list in info["results"]:
            if video_list:
                if "Trailer" in video_list["name"] or 'Promo' in video_list['name']:
                    video_id = video_list["key"]
                    return f"https://www.youtube.com/watch?v={video_id}"
        return None

    def get_info(self):
        search_string = self._search()
        movie_id = []
        movie_info = {}
        trailer = ""
        image_url = None
        for r in search_string.results:
            data = self._movie_info(r["id"])
            if data["imdb_id"] == self.imdb_id:
                if self._get_trailer(r["id"]):
                    trailer = self._get_trailer(r["id"])
                poster = data["poster_path"]
                if poster:
                    image_url = f"https://image.tmdb.org/t/p/original{poster}"
                for k in self.template["movie"]:
                    if "rating" in k:
                        movie_info["rating"] = k["rating"]
                movie_info["genre"] = [x["name"] for x in data["genres"]]
                run = data["runtime"]
                movie_info["length"] = f"{run} mins"
                if movie_info:
                    self.template["movie"] = movie_info
                if image_url:
                    self.template["image"] = image_url
        return self.template, trailer

    def _movie_info(self, id):
        movie = self.tmdb.Movies(id)
        response = movie.info()
        return response
