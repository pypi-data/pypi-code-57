from easy_publish import utils
import os
from dataclasses import dataclass

__all__ = ["generate_posts"]

def generate_posts(directory: str, strict_mode=False):
    """
    Exported helper function that orchestrates and generates posts.

    The generate_posts func should be considered the main function of this library. It checks inputs
    given, generates objects, and returns a collection of posts in the form of the class PostCollection.
    General flow of this function is as follows:
        1. Checks user parameters and sets necessary flags.
        2. Generates file list.
        3. For each file creates a list of Post class.
        4. Creates and returns a PostCollection class from posts list.
    """
    if strict_mode:
        files = remove_non_markdown_files(files)

    files = utils.listdir_fullpath(os.path.expanduser(directory))

    parsed_posts = []
    for file in files:
        parsed_posts.append(PostParser(file))

    post_collection = PostCollection(parsed_posts)
    return post_collection

class PostCollection():
    """
    Abstraction to hoist up content for easier access.

    The PostCollection class exists to make access to this library smoother for the end user.
    The class has two properties: posts & metadata.
        - Posts is a dictionary of posts from given list input. The Post.route property
        is used as the key.
        - Metadata is a list of the posts class with content removed.
    """
    # TODO
    # duplicate title handling
    def __init__(self, posts):
        self.posts = self._posts_to_dict(posts)
        self.metadata = self._metadata_cache(posts)

    @staticmethod
    def _posts_to_dict(posts):
        dict_posts = {}
        for post in posts:
            dict_posts[post.route] = post
        return dict_posts

    @staticmethod
    def _metadata_cache(posts):
        metadata = []
        for post in posts:
            metadata.append(Metadata(post.route, post.title, post.date, post.author, post.tags))

        return metadata

@dataclass
class Metadata():
    """
    Dataclass used by PostCollection.metadata.
    """
    route: str
    title: str
    date: str
    author: str
    tags: str


class PostParser():
    """
    Parses a given file into structured data outlining a post.
    """
    # TODO
    # reading directories recursively
    # potentially hoisting them to the top level
    # not sure how to handle yet
    def __init__(self, file):
        self.file = file
        self.route= self._get_route_name()
        self.parsed = self._init_parser(file)
        self.title = self.parsed['title']
        self.date = self.parsed['date']
        self.author = self.parsed['author']
        self.tags = self.parsed['tags']
        self.content = self.parsed['content']

    def __repr__(self):
        return f"PostParser('{self.route}')"

    def _get_route_name(self):
        route_with_extension = self.file.split("/")[-1]
        route = route_with_extension.split(".")[0]
        return route

    def _init_parser(self, file):
        with open(file, 'r') as file:
            f = file.readlines()

        index = utils.array_splitter(f)
        metadata_list = f[0:index]
        content_list = f[index+1:]

        metadata = self._metadata_parser(metadata_list)
        content = self._content_parser(content_list)

        parsed = metadata
        parsed['content'] = content

        return parsed

    @staticmethod
    def _metadata_parser(metadata_list):
        # TODO 
        # add list parser for tags (split on comma and create list)
        # currently just a string
        metadata = {}
        for item in metadata_list:
            key, val = item.split(":")
            key = key.strip()
            val = val.strip()
            metadata[key] = val
        return metadata

    @staticmethod
    def _content_parser(content_list):
        return ''.join(content_list)


if __name__ == "__main__":
    # small testing func
    # will be removed once tests are integrated
    p = generate_posts("~/fakenotes")
    print(p)
