import wikipedia
from bs4 import BeautifulSoup
from PyInquirer import prompt


class WikiSearch:
    def __init__(self, template):
        self.template = template

    def _wiki_result(self, result):
        result.append("None")
        wiki_result = [
            {
                "type": "list",
                "name": "wiki",
                "message": "Does the wiki search result match any movie you picked",
                "choices": result,
            }
        ]
        result = prompt(wiki_result)
        if result["wiki"] == "None":
            return
        try:
            wiki_page = wikipedia.page(result["wiki"], auto_suggest=False)
        except:
            return None
        summary = wiki_page.summary
        correct_result = [
            {
                "type": "confirm",
                "name": "confirm_wiki",
                "message": f"Is this summary for the same movie {summary}",
                "default": False,
            }
        ]
        answers = prompt(correct_result)
        if answers["confirm_wiki"]:
            return wiki_page
        return None

    def _start_scrapping(self, html):
        parsed_html = BeautifulSoup(html, "html.parser")
        info_table = parsed_html.find("table", class_="infobox vevent")
        # find all the inside data
        lists = info_table.find_all("tr")
        info_list = {}
        for item in lists:
            item_name_elm = item.find("th")
            item_info_elm = item.find("td")
            if item_name_elm and item_info_elm:
                info_list[
                    item_name_elm.get_text().strip()
                ] = item_info_elm.get_text().strip()
        return info_list

    def wiki_search(self):
        movie_name = self.template["movie_name"]
        movie_lan = self.template["language"]
        result = wikipedia.search(f"{movie_name} {movie_lan} movie")
        page = self._wiki_result(result)
        if page:
            info = self._start_scrapping(page.html())
            if "length" not in self.template["movie"] and "Running time" in info:
                self.template["movie"]["length"] = info["Running time"].replace(
                    "minutes", "mins"
                )
            if "producer" not in self.template["movie"] and "Produced by" in info:
                self.template["cast-crew"]["producer"] = info["Produced by"]
        return self.template
