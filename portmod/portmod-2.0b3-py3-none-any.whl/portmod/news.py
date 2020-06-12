# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Critical News module

See https://www.gentoo.org/glep/glep-0042.html for details

We use yaml instead of txt for ease of parsing, while having almost the same structure
Note that a Body field is used for the article body.
"""

import os
from fnmatch import fnmatch
from typing import Callable, Mapping

from .colour import blue, bright, green, yellow
from .config import get_config
from .globals import env
from .repo.list import read_list
from .repo.loader import load_installed_mod
from .repo.profiles import get_profile_path, profile_exists
from .repo import Atom
from .repos import Repo
from .yaml import yaml_load


def get_article_path(repo: Repo, article: str) -> str:
    return os.path.join(
        repo.location, "metadata", "news", article, article + ".en.yaml"
    )


def get_news_content(path: str) -> Mapping:
    with open(path, "r") as file:
        article = yaml_load(file)
    return article


def is_news_visible(repo: Repo, article: str) -> bool:
    """
    Returns true if the given news article is visible to the user.
    """
    article = get_news_content(get_article_path(repo, article))

    def get_list(ob, key):
        if isinstance(ob, list):
            li = ob
        elif isinstance(ob, str):
            li = ob.split()
        else:
            raise TypeError(
                f"{key} should contain a string or a list, " f"but contained {ob}"
            )
        return li

    installed_conditions = get_list(
        article.get("Display-If-Installed", ""), "Display-If-Installed"
    )
    keyword_conditions = get_list(
        article.get("Display-If-Keyword", ""), "Display-If-Keyword"
    )
    profile_conditions = get_list(
        article.get("Display-If-Profile", ""), "Display-If-Profile"
    )

    profile_name = os.path.relpath(
        get_profile_path(), os.path.join(repo.location, "profiles")
    )
    if profile_conditions and not any(
        fnmatch(profile_name, profile_condition)
        for profile_condition in profile_conditions
    ):
        return False

    if installed_conditions and not any(
        load_installed_mod(Atom(atom)) for atom in installed_conditions
    ):
        return False

    ACCEPT_KEYWORDS = set(get_config()["ACCEPT_KEYWORDS"])
    if keyword_conditions and not any(
        keyword in ACCEPT_KEYWORDS or keyword.lstrip("~") in ACCEPT_KEYWORDS
        for keyword in keyword_conditions
    ):
        return False

    return True


def is_news_unread(repo: Repo, article: str) -> bool:
    """
    Returns true if the given news article needs to be read.
    """
    news_dir = os.path.join(env.PORTMOD_LOCAL_DIR, "news")
    unread_file = os.path.join(news_dir, "news-" + repo.name + ".unread")
    if not os.path.exists(unread_file) or article in read_list(unread_file):
        return True

    return False


def mark(repo: Repo, article: str, read=True):
    """Marks the given news article as read"""
    news_dir = os.path.join(env.PORTMOD_LOCAL_DIR, "news")
    os.makedirs(news_dir, exist_ok=True)
    if read:
        remove_file = os.path.join(news_dir, "news-" + repo.name + ".unread")
        add_file = os.path.join(news_dir, "news-" + repo.name + ".read")
    else:
        add_file = os.path.join(news_dir, "news-" + repo.name + ".unread")
        remove_file = os.path.join(news_dir, "news-" + repo.name + ".read")

    if os.path.exists(remove_file):
        contents = read_list(remove_file)

        if article in contents:
            del contents[contents.index(article)]
            with open(remove_file, "w") as file:
                for line in contents:
                    print(line + "\n", file=file)
        else:
            return

    with open(add_file, "a") as file:
        print(article, file=file)


def iterate_news(repo: Repo, unread_only=False):
    news_dir = os.path.join(repo.location, "metadata", "news")
    unread_file = os.path.join(
        os.path.join(env.PORTMOD_LOCAL_DIR, "news"), "news-" + repo.name + ".unread"
    )
    if os.path.exists(unread_file):
        unread = set(read_list(unread_file))
    else:
        unread = set()

    if os.path.exists(news_dir):
        for news_item in sorted(os.listdir(news_dir)):
            if (not unread_only or news_item in unread) and (
                not profile_exists() or is_news_visible(repo, news_item)
            ):
                yield os.path.join(news_dir, news_item)


def display_unread_message():
    news_dir = os.path.join(env.PORTMOD_LOCAL_DIR, "news")
    total_unread = 0
    for repo in env.REPOS:
        unread_file = os.path.join(news_dir, "news-" + repo.name + ".unread")
        if os.path.exists(unread_file):
            unread = len(read_list(unread_file))
            if unread:
                if not total_unread:
                    print()
                print(
                    bright(yellow(" * IMPORTANT:"))
                    + f" {unread} news items need reading for repository '{repo.name}'"
                )
            total_unread += unread

    if total_unread:
        print(
            bright(yellow(" * "))
            + "Use "
            + bright(green("omwselect news read"))
            + " to view new items."
        )
        print()


def update_news():
    news_dir = os.path.join(env.PORTMOD_LOCAL_DIR, "news")
    os.makedirs(news_dir, exist_ok=True)
    for repo in env.REPOS:
        unread_file = os.path.join(news_dir, "news-" + repo.name + ".unread")
        skip_file = os.path.join(news_dir, "news-" + repo.name + ".skip")
        if os.path.exists(skip_file):
            skip = set(read_list(skip_file))
        else:
            skip = set()

        for news_dir in iterate_news(repo):
            news_item = os.path.basename(news_dir)
            if news_item in skip:
                continue

            if profile_exists():
                # If user has no profile, then they must be installing for the
                # first time. All news is thus old news
                with open(unread_file, "a+") as file:
                    print(news_item, file=file)

            with open(skip_file, "a+") as file:
                print(news_item, file=file)

    return True


def read_news(index=None, unread_only=False):
    i = 0
    for repo in env.REPOS:
        for news_dir in iterate_news(repo, unread_only=unread_only):
            if index is not None and i < index:
                i += 1
                continue
            elif index is not None and i > index:
                break

            news_item = os.path.basename(news_dir)
            article = get_news_content(os.path.join(news_dir, news_item + ".en.yaml"))
            print(bright(green((news_item))))
            print(f'  Title: \t\t{article["Title"]}')
            print(f'  Author: \t\t{article["Author"]}')
            print(f'  Posted: \t\t{article["Posted"]}')
            print(f'  Revision: \t\t{article["Revision"]}')
            print()
            print(article["Body"])
            print()

            mark(repo, news_item)
            i += 1


def add_news_parsers(subparsers):
    news = subparsers.add_parser("news", help="manage news")
    news_subparsers = news.add_subparsers()
    news_list = news_subparsers.add_parser("list", help="List all news articles")
    news_read = news_subparsers.add_parser(
        "read", help="Displays news article and marks as read"
    )
    news_read.add_argument(
        "target",
        help="new (default) all or item",
        default="new",
        metavar="<item>",
        nargs="?",
    )
    news_unread = news_subparsers.add_parser(
        "unread", help="Marks news article as unread"
    )
    news_unread.add_argument(
        "target", help="all or item number", metavar="<item>",
    )

    def read_func(args):
        if args.target == "new":
            read_news(unread_only=True)
        elif args.target == "all":
            read_news()
        else:
            read_news(int(args.target))

    def list_func(args):
        i = 0
        print(bright(green("News items:")))
        for repo in env.REPOS:
            for path in iterate_news(repo):
                article_name = os.path.basename(path)
                article = get_news_content(
                    os.path.join(path, article_name + ".en.yaml")
                )
                if is_news_unread(repo, article_name):
                    print(
                        f'  {bright("[" + str(i) + "]")}  {blue("N")}  '
                        f'{article["Posted"]}  {blue(article["Title"])}'
                    )
                else:
                    print(
                        f'  {bright("[" + str(i) + "]")}     '
                        f'{article["Posted"]}  {article["Title"]}'
                    )
                i += 1

    def news_help(args):
        news.print_help()

    def unread_func(args):
        i = 0
        for repo in env.REPOS:
            for path in iterate_news(repo):
                if args.target == "all" or i == int(args.target):
                    article_name = os.path.basename(path)
                    mark(repo, article_name, read=False)
                i += 1

    news.set_defaults(func=news_help)
    news_read.set_defaults(func=read_func)
    news_list.set_defaults(func=list_func)
    news_unread.set_defaults(func=unread_func)


def validate_news(repo_root: str, err: Callable[[str], None]):
    path = os.path.join(repo_root, "metadata", "news")
    if os.path.exists(path):
        for directory in os.listdir(path):
            news_file = os.path.join(path, directory, directory + ".en.yaml")
            if os.path.exists(news_file):
                article = get_news_content(news_file)
                required_keys = [
                    "Title",
                    "Author",
                    "Posted",
                    "Revision",
                    "News-Item-Format",
                    "Body",
                ]
                for key in required_keys:
                    if key not in article:
                        err(
                            f"News article {directory} doesn't contain required key {key}"
                        )

                if "Display-If-Installed" in article:
                    string = article["Display-If-Installed"]
                    for atom in string.split():
                        Atom(atom)
            else:
                err(
                    f"News directory {path}/{directory} doesn't contain {directory}.en.yaml"
                )
