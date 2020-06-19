from googleapiclient.discovery import build
from PyInquirer import prompt
import re
import os
import requests
import click
from imdb import IMDb
from bs4 import BeautifulSoup


class Search:
    """Extending the search functionality for movie info"""

    def __init__(self, api_key, review_template):
        self.review_template = review_template
        self.search_service = build("customsearch", "v1", developerKey=api_key)
        self.cx = "008985690000369000569:gswsgp4ncli"

    def _imdb_search(self, movie_name, movie_language):
        """search the custom search engine with imdb"""
        return (
            self.search_service.cse()
            .list(q=f"{movie_name} {movie_language}", cx=self.cx,)
            .execute()
        )

    def _check_name_correction(self, data, name):
        if "spelling" in data:
            corrected_query = data["spelling"]["correctedQuery"].replace(
                self.review_template["language"], ""
            )
            correct_name = [
                {
                    "type": "confirm",
                    "name": "changeMovieName",
                    "message": f"Instead of {name} are you looking for {corrected_query}",
                    "default": False,
                }
            ]
            answers = prompt(correct_name)
            if answers:
                self.review_template["movie_name"] = corrected_query.strip()

    def _filter_result(self, data):
        movie_result = [
            {
                "type": "list",
                "name": "movie_name",
                "message": "Identify the name from the IMDb list",
                "choices": [],
            }
        ]
        info = {}
        for item in data["items"]:
            if re.match(r".*\s*\([0-9]{4}\)\s*\-\s*IMDb", item["title"]):
                movie_result[0]["choices"].append(item["title"])
                info[item["title"]] = item
        # add an option for if things don't match
        movie_result[0]["choices"].append("other")
        result = prompt(movie_result)
        if result["movie_name"] == "other":
            click.echo(click.style("Nothing from IMDb to use", fg="green"))
            return False
        else:
            name = re.sub(r"\s*\([0-9]{4}\)\s*\-\s*IMDb", "", result["movie_name"])
            if name.lower() != self.review_template["movie_name"].lower():
                self.review_template["movie_name"] = name
            return info[result["movie_name"]]

    def _image_useable(self, image_url):
        if "imdb_fb_logo" in image_url:
            return False
        return True

    def _crawl_imdb_info(self, movie_id):
        movie_number = movie_id[2:]
        imdb_instance = IMDb()
        movie = imdb_instance.get_movie(movie_number)
        movie_info = {}
        if "certificates" in movie:
            american_certificate = [
                x
                for x in movie["certificates"]
                if "United States" in x and "TV" not in x
            ]
            if american_certificate:
                movie_info["rating"] = american_certificate[0].replace("United States:", "")
        cast_crew = {}
        cast_crew["starring"] = [x["name"] for x in movie["cast"][:5]]
        cast_crew["director"] = [x["name"] for x in movie["directors"][:11]]
        cast_crew["producer"] = [x["name"] for x in movie["producers"][:11]]
        movie_info["genre"] = [x for x in movie["genres"]]
        if 'runtimes' in movie:
            length = movie["runtimes"][0]
            movie_info["length"] = f"{length} mins"
        self.review_template["movie"] = movie_info
        self.review_template["cast-crew"] = cast_crew

    def data(self):
        data = self._imdb_search(
            self.review_template["movie_name"], self.review_template["language"]
        )
        self._check_name_correction(data, self.review_template["movie_name"])
        movie_data = self._filter_result(data)
        if movie_data:
            image_url = movie_data["pagemap"]["metatags"][0]["og:image"]
            self._crawl_imdb_info(movie_data["pagemap"]["metatags"][0]["pageid"])
            if "og:image" in movie_data["pagemap"]["metatags"][
                0
            ] and self._image_useable(image_url):
                self.review_template["image"] = image_url
        return self.review_template, movie_data["pagemap"]["metatags"][0]["pageid"]
