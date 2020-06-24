from collections import namedtuple

TwitterContent = namedtuple("TwitterContent", ["id", "image_link", "phrase", "media_type", "tweet_url", "source"])
GetyarnContent = namedtuple("GetyarnContent", ["id", "phrase", "translation", "media_type", "source"])
