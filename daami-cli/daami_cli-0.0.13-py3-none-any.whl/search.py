from googleapiclient.discovery import build
from PyInquirer import prompt, print_json
import re
import os
import requests
import click
from imdb import IMDb
from bs4 import BeautifulSoup


class Search:
    """Extending the search functionality for movie info"""

    def __init__(
        self, movie_name, api_key, movie_language, review_template, project_folder
    ):
        self.movie_name = movie_name
        self.movie_language = movie_language
        self.review_template = review_template
        self.search_service = build("customsearch", "v1", developerKey=api_key)
        self.cx = "008985690000369000569:gswsgp4ncli"
        self.project_folder = project_folder

    def _imdb_search(self):
        """search the custom search engine with imdb"""
        return (
            self.search_service.cse()
            .list(q=f"{self.movie_name} {self.movie_language}", cx=self.cx,)
            .execute()
        )

    def _check_name_correction(self, data):
        if "spelling" in data:
            corrected_query = data["spelling"]["correctedQuery"].replace(language, "")
        correct_name = [
            {
                "type": "confirm",
                "name": "changeMovieName",
                "message": f"Instead of {self.movie_name} are you looking for {corrected_query}",
                "default": False,
            }
        ]
        answers = prompt(correct_name)
        if answers:
            return corrected_query.strip()
        return self.movie_name

    def _filter_result(self, data):
        movie_result = [
            {
                "type": "list",
                "name": "movie_name",
                "message": "Identify the name from the IMDb list",
                "choices": [],
                # 'filter': lambda val: val.lower()
            }
        ]
        info = {}
        for item in data["items"]:
            movie_result[0]["choices"].append(item["title"])
            info[item["title"]] = item
        # add an option for if things don't match
        movie_result[0]["choices"].append("other")
        result = prompt(movie_result)
        if result["movie_name"] == "other":
            click.echo(click.style("Nothing from IMDb to use", fg="green"))
            return None
        else:
            return info[result["movie_name"]]
            # template['movie_name'] = re.sub(r'\([0-9]{4}\)\s*\-\s*imdb','',result['movie_name']).title()

    def _image_download(self, image_url):
        if "imdb_fb_logo" in image_url:
            return False
        return True

    def _crawl_imdb_info(self, movie_id):
        movie_number = movie_id[2:]
        imdb_instance = IMDb()
        movie = imdb_instance.get_movie(movie_number)
        cast_crew = {}
        cast_crew["starring"] = [x["name"] for x in movie["cast"][:11]]
        cast_crew["director"] = [x["name"] for x in movie["directors"][:11]]
        cast_crew["producer"] = [x["name"] for x in movie["producers"][:11]]
        movie_info = {}
        movie_info["genre"] = [x for x in movie["genres"]]
        length = movie["runtimes"][0]
        movie_info["length"] = f"{length} mins"
        return movie_info, cast_crew

    def data(self):
        data = self._imdb_search()
        movie_data = self._filter_result(data)
        if movie_data:
            image_url = movie_data["pagemap"]["metatags"][0]["og:image"]
            movie_info, cast_info = self._crawl_imdb_info(
                movie_data["pagemap"]["metatags"][0]["pageid"]
            )
            if "og:image" in movie_data["pagemap"]["metatags"][0]:
                return self._image_download(image_url), movie_info, cast_info,movie_data["pagemap"]["metatags"][0]["pageid"]
            return False, movie_info, cast_info,movie_data["pagemap"]["metatags"][0]["pageid"]
        return False,None,None,None
