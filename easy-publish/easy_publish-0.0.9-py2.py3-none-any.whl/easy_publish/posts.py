import os
import time
from dataclasses import dataclass
from easy_publish import utils

__all__ = ["generate_posts"]


def generate_posts(
    directory: str,
    author=False,
    date_format="%m-%d-%y",
    date_sort="descending",
    tags_from_file=False,
    date_from_file=False,
    title_from_file=False,
    strict_mode=False,
):
    """
    Exported helper function that orchestrates and generates posts.

    The generate_posts func should be considered the 'main' function of this library. It checks inputs
    given, instantiates objects, and returns a Posts object.

    General flow of this function is as follows:
        1. Check user parameters and sets necessary flags.
        2. Generates file list.
        3. For each file given parse and create a list of parsed posts.
        4. Create and return Posts class to user.
    """
    if strict_mode:
        files = remove_non_markdown_files(files)

    files = utils.listdir_fullpath(directory)
    parsed_posts = generate_parsed_post_list(files, date_format)

    metadata_collection = MetadataCollection(parsed_posts, date_sort)
    posts_collection = PostsCollection(parsed_posts)
    posts = Posts(posts_collection.posts, metadata_collection.metadata)

    return posts


def generate_parsed_post_list(files: list, date_format: str) -> list:
    parsed_posts = []
    for file in files:
        parsed_posts.append(PostParser(file, date_format))
    return parsed_posts


class PostParser:
    """
    Parses a given file into structured data outlining a post.
    """
    # TODO
    # reading directories recursively
    # potentially hoisting them to the top level
    # not sure how to handle yet
    def __init__(self, file, date_format):
        self.file = file
        self.date_format = date_format
        self.route = self._get_route_name()
        self.parsed = self._init_parser(file)
        self.title = self.parsed["title"]
        self.date = self.parsed["date"]
        self.real_date = self.parsed["real_date"]
        self.author = self.parsed["author"]
        self.tags = self.parsed["tags"]
        self.content = self.parsed["content"]

    def __repr__(self):
        return f"PostParser('{self.route}')"

    def _get_route_name(self):
        route_with_extension = self.file.split("/")[-1]
        route = route_with_extension.split(".")[0]
        return route

    def _init_parser(self, file):
        with open(file, "r") as file:
            f = file.readlines()

        index = utils.array_splitter(f)
        metadata_list = f[0:index]
        content_list = f[index + 1 :]

        metadata = self._metadata_parser(metadata_list)
        content = self._content_parser(content_list)

        parsed = metadata
        parsed["content"] = content

        return parsed

    def _metadata_parser(self, metadata_list):
        # TODO
        metadata = {}
        for item in metadata_list:
            key, val = item.split(":")
            key = key.strip()
            val = val.strip()
            metadata[key] = val
        try:
            metadata["tags"] = self._metadata_tags_parser(metadata["tags"])
        except KeyError:
            pass
        try:
            metadata["real_date"] = self._metadata_date_parser(metadata["date"])
        except KeyError:
            pass

        return metadata

    def _metadata_tags_parser(self, tags):
        tags = tags.split(",")
        return [tag.strip() for tag in tags]

    def _metadata_date_parser(self, d):
        original_date = d
        try:
            d = time.strptime(d, self.date_format)
            return d
        except ValueError as e:
            print(f"Date error on date {original_date}. Expected date format %m-%d-%y.")
            print("Falling back to string represenation")
            return original_date

    def _content_parser(self, content_list):
        return "".join(content_list)


class Posts:
    """
    Abstraction to hoist up content for easier access.

    The Posts class exists to make access to this library smoother for the end user.
    The class has two properties: posts & metadata.
        - Posts.posts is a dictionary of posts from given list input. The Posts.posts['post'].route property
        is used as the key.
        - Posts.metadata is the list of posts with useful metadata information such as date sorting and content previews
    """

    def __init__(self, posts, metadata):
        self.posts = posts
        self.metadata = metadata


class MetadataCollection:
    def __init__(self, posts, date_sort):
        self.metadata = self._metadata_cache(posts)
        self.date_sort = date_sort
        self._sort_date()

    @staticmethod
    def _metadata_cache(posts):
        metadata = []
        for post in posts:
            metadata.append(
                Metadata(
                    post.route,
                    post.title,
                    post.date,
                    post.real_date,
                    post.author,
                    post.tags,
                )
            )

        return metadata

    def _sort_date(self):
        if self.date_sort == "descending":
            try:
                self.metadata.sort(key=lambda m: m.real_date, reverse=True)
            except TypeError:
                print("Dates failed to sort due to error in datestring.")
                pass
        elif self.date_sort == "ascending":
            try:
                self.metadata.sort(key=lambda m: m.real_date)
            except TypeError:
                print("Dates failed to sort due to error in datestring.")
                pass
        else:
            # error on strict
            print(f"Invalid date sort method: {self.date_sort}")
            pass


class PostsCollection:
    def __init__(self, posts):
        self.posts = self._posts_to_dict(posts)

    @staticmethod
    def _posts_to_dict(posts):
        dict_posts = {}
        for post in posts:
            dict_posts[post.route] = post
        return dict_posts


@dataclass
class Metadata:
    """
    Dataclass used by Posts.metadata.
    """

    route: str
    title: str
    date: str
    real_date: time.struct_time
    author: str
    tags: str
