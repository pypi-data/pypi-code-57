# -*- coding: utf-8 -*-

# Copyright 2016-2020 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://twitter.com/"""

from .common import Extractor, Message
from .. import text, exception
from ..cache import cache
import hashlib
import time


class TwitterExtractor(Extractor):
    """Base class for twitter extractors"""
    category = "twitter"
    directory_fmt = ("{category}", "{user[name]}")
    filename_fmt = "{tweet_id}_{num}.{extension}"
    archive_fmt = "{tweet_id}_{retweet_id}_{num}"
    cookiedomain = ".twitter.com"
    root = "https://twitter.com"
    sizes = (":orig", ":large", ":medium", ":small")

    def __init__(self, match):
        Extractor.__init__(self, match)
        self.user = match.group(1)
        self.retweets = self.config("retweets", True)
        self.replies = self.config("replies", True)
        self.twitpic = self.config("twitpic", False)
        self.videos = self.config("videos", True)
        self._user_cache = {}

    def items(self):
        self.login()
        metadata = self.metadata()
        yield Message.Version, 1

        for tweet in self.tweets():

            if not self.retweets and "retweeted_status_id_str" in tweet or \
                    not self.replies and "in_reply_to_user_id_str" in tweet:
                continue

            if self.twitpic:
                self._extract_twitpic(tweet)
            if "extended_entities" not in tweet:
                continue

            tdata = self._transform_tweet(tweet)
            tdata.update(metadata)

            yield Message.Directory, tdata
            for tdata["num"], media in enumerate(
                    tweet["extended_entities"]["media"], 1):

                tdata["width"] = media["original_info"].get("width", 0)
                tdata["height"] = media["original_info"].get("height", 0)

                if "video_info" in media and self.videos:

                    if self.videos == "ytdl":
                        url = "ytdl:{}/i/web/status/{}".format(
                            self.root, tweet["id_str"])
                        tdata["extension"] = None
                        yield Message.Url, url, tdata

                    else:
                        video_info = media["video_info"]
                        variant = max(
                            video_info["variants"],
                            key=lambda v: v.get("bitrate", 0),
                        )
                        tdata["duration"] = video_info.get(
                            "duration_millis", 0) / 1000
                        tdata["bitrate"] = variant.get("bitrate", 0)

                        url = variant["url"]
                        text.nameext_from_url(url, tdata)
                        yield Message.Url, url, tdata

                elif "media_url_https" in media:
                    url = media["media_url_https"]
                    urls = [url + size for size in self.sizes]
                    text.nameext_from_url(url, tdata)
                    yield Message.Urllist, urls, tdata

                else:
                    url = media["media_url"]
                    text.nameext_from_url(url, tdata)
                    yield Message.Url, url, tdata

    def _extract_twitpic(self, tweet):
        twitpics = []
        for url in tweet["entities"].get("urls", ()):
            url = url["expanded_url"]
            if "//twitpic.com/" in url:
                response = self.request(url, fatal=False)
                if response.status_code >= 400:
                    continue
                url = text.extract(
                    response.text, 'name="twitter:image" value="', '"')[0]
                twitpics.append({
                    "original_info": {},
                    "media_url"    : url,
                })
        if twitpics:
            if "extended_entities" in tweet:
                tweet["extended_entities"]["media"].extend(twitpics)
            else:
                tweet["extended_entities"] = {"media": twitpics}

    def _transform_tweet(self, tweet):
        entities = tweet["entities"]
        tdata = {
            "tweet_id"      : text.parse_int(tweet["id_str"]),
            "retweet_id"    : text.parse_int(
                tweet.get("retweeted_status_id_str")),
            "quote_id"      : text.parse_int(
                tweet.get("quoted_status_id_str")),
            "reply_id"      : text.parse_int(
                tweet.get("in_reply_to_status_id_str")),
            "date"          : text.parse_datetime(
                tweet["created_at"], "%a %b %d %H:%M:%S %z %Y"),
            "user"          : self._transform_user(tweet["user"]),
            "lang"          : tweet["lang"],
            "content"       : tweet["full_text"],
            "favorite_count": tweet["favorite_count"],
            "quote_count"   : tweet["quote_count"],
            "reply_count"   : tweet["reply_count"],
            "retweet_count" : tweet["retweet_count"],
        }

        hashtags = entities.get("hashtags")
        if hashtags:
            tdata["hashtags"] = [t["text"] for t in hashtags]

        mentions = entities.get("user_mentions")
        if mentions:
            tdata["mentions"] = [{
                "id": text.parse_int(u["id_str"]),
                "name": u["screen_name"],
                "nick": u["name"],
            } for u in mentions]

        if "in_reply_to_screen_name" in tweet:
            tdata["reply_to"] = tweet["in_reply_to_screen_name"]

        if "full_text_quoted" in tweet:
            tdata["content_quoted"] = tweet["full_text_quoted"]

        if "author" in tweet:
            tdata["author"] = self._transform_user(tweet["author"])

        return tdata

    def _transform_user(self, user):
        uid = user["id_str"]
        cache = self._user_cache

        if uid not in cache:
            cache[uid] = {
                "id"              : text.parse_int(uid),
                "name"            : user["screen_name"],
                "nick"            : user["name"],
                "description"     : user["description"],
                "location"        : user["location"],
                "date"            : text.parse_datetime(
                    user["created_at"], "%a %b %d %H:%M:%S %z %Y"),
                "verified"        : user.get("verified", False),
                "profile_banner"  : user.get("profile_banner_url", ""),
                "profile_image"   : user.get(
                    "profile_image_url_https", "").replace("_normal.", "."),
                "favourites_count": user["favourites_count"],
                "followers_count" : user["followers_count"],
                "friends_count"   : user["friends_count"],
                "listed_count"    : user["listed_count"],
                "media_count"     : user["media_count"],
                "statuses_count"  : user["statuses_count"],
            }
        return cache[uid]

    def metadata(self):
        """Return general metadata"""
        return {}

    def tweets(self):
        """Yield all relevant tweet objects"""

    def login(self):
        username, password = self._get_auth_info()
        if username:
            self._update_cookies(self._login_impl(username, password))

    @cache(maxage=360*24*3600, keyarg=1)
    def _login_impl(self, username, password):
        self.log.info("Logging in as %s", username)

        url = "https://mobile.twitter.com/i/nojs_router"
        params = {"path": "/login"}
        headers = {"Referer": self.root + "/", "Origin": self.root}
        page = self.request(
            url, method="POST", params=params, headers=headers, data={}).text

        pos = page.index('name="authenticity_token"')
        token = text.extract(page, 'value="', '"', pos)[0]

        url = "https://mobile.twitter.com/sessions"
        data = {
            "authenticity_token"        : token,
            "session[username_or_email]": username,
            "session[password]"         : password,
            "remember_me"               : "1",
            "wfa"                       : "1",
            "commit"                    : "+Log+in+",
            "ui_metrics"                : "",
        }
        response = self.request(url, method="POST", data=data)
        cookies = {
            cookie.name: cookie.value
            for cookie in self.session.cookies
            if cookie.domain == self.cookiedomain
        }

        if "/error" in response.url or "auth_token" not in cookies:
            raise exception.AuthenticationError()
        return cookies


class TwitterTimelineExtractor(TwitterExtractor):
    """Extractor for all images from a user's timeline"""
    subcategory = "timeline"
    pattern = (r"(?:https?://)?(?:www\.|mobile\.)?twitter\.com"
               r"/(?!search)([^/?&#]+)/?(?:$|[?#])")
    test = (
        ("https://twitter.com/supernaturepics", {
            "range": "1-40",
            "url": "0106229d408f4111d9a52c8fd2ad687f64842aa4",
        }),
        ("https://mobile.twitter.com/supernaturepics?p=i"),
    )

    def tweets(self):
        return TwitterAPI(self).timeline_profile(self.user)


class TwitterMediaExtractor(TwitterExtractor):
    """Extractor for all images from a user's Media Tweets"""
    subcategory = "media"
    pattern = (r"(?:https?://)?(?:www\.|mobile\.)?twitter\.com"
               r"/(?!search)([^/?&#]+)/media(?!\w)")
    test = (
        ("https://twitter.com/supernaturepics/media", {
            "range": "1-40",
            "url": "0106229d408f4111d9a52c8fd2ad687f64842aa4",
        }),
        ("https://mobile.twitter.com/supernaturepics/media#t"),
    )

    def tweets(self):
        return TwitterAPI(self).timeline_media(self.user)


class TwitterSearchExtractor(TwitterExtractor):
    """Extractor for all images from a search timeline"""
    subcategory = "search"
    directory_fmt = ("{category}", "Search", "{search}")
    pattern = (r"(?:https?://)?(?:www\.|mobile\.)?twitter\.com"
               r"/search/?\?(?:[^&#]+&)*q=([^&#]+)")
    test = ("https://twitter.com/search?q=nature", {
        "range": "1-40",
        "count": 40,
    })

    def metadata(self):
        return {"search": text.unquote(self.user)}

    def tweets(self):
        return TwitterAPI(self).search(self.user)


class TwitterTweetExtractor(TwitterExtractor):
    """Extractor for images from individual tweets"""
    subcategory = "tweet"
    pattern = (r"(?:https?://)?(?:www\.|mobile\.)?twitter\.com"
               r"/([^/?&#]+|i/web)/status/(\d+)")
    test = (
        ("https://twitter.com/supernaturepics/status/604341487988576256", {
            "url": "0e801d2f98142dd87c3630ded9e4be4a4d63b580",
            "content": "ab05e1d8d21f8d43496df284d31e8b362cd3bcab",
        }),
        # 4 images
        ("https://twitter.com/perrypumas/status/894001459754180609", {
            "url": "c8a262a9698cb733fb27870f5a8f75faf77d79f6",
        }),
        # video
        ("https://twitter.com/perrypumas/status/1065692031626829824", {
            "options": (("videos", True),),
            "pattern": r"https://video.twimg.com/ext_tw_video/.+\.mp4\?tag=5",
        }),
        # content with emoji, newlines, hashtags (#338)
        ("https://twitter.com/playpokemon/status/1263832915173048321", {
            "keyword": {"content": (
                r"re:Gear up for #PokemonSwordShieldEX with special Mystery "
                "Gifts! \n\nYou’ll be able to receive four Galarian form "
                "Pokémon with Hidden Abilities, plus some very useful items. "
                "It’s our \\(Mystery\\) Gift to you, Trainers! \n\n❓🎁➡️ "
            )},
        }),
        # Reply to another tweet (#403)
        ("https://twitter.com/tyson_hesse/status/1103767554424598528", {
            "options": (("videos", "ytdl"),),
            "pattern": r"ytdl:https://twitter.com/i/web.+/1103767554424598528",
        }),
        # 'replies' option (#705)
        ("https://twitter.com/tyson_hesse/status/1103767554424598528", {
            "options": (("replies", False),),
            "count": 0,
        }),
        # /i/web/ URL
        ("https://twitter.com/i/web/status/1155074198240292865", {
            "pattern": r"https://pbs.twimg.com/media/EAel0vUUYAAZ4Bq.jpg:orig",
        }),
        # quoted tweet (#526)
        ("https://twitter.com/Pistachio/status/1222690391817932803", {
            "pattern": r"https://pbs\.twimg\.com/media/EPfMfDUU8AAnByO\.jpg",
        }),
        # TwitPic embeds (#579)
        ("https://twitter.com/i/web/status/112900228289540096", {
            "options": (("twitpic", True),),
            "pattern": r"https://\w+.cloudfront.net/photos/large/\d+.jpg",
            "count": 3,
        }),
    )

    def __init__(self, match):
        TwitterExtractor.__init__(self, match)
        self.tweet_id = match.group(2)

    def tweets(self):
        return TwitterAPI(self).tweet(self.tweet_id)


class TwitterBookmarkExtractor(TwitterExtractor):
    """Extractor for bookmarked tweets"""
    subcategory = "bookmark"
    pattern = r"(?:https?://)?(?:www\.|mobile\.)?twitter\.com/i/bookmarks()"
    test = ("https://twitter.com/i/bookmarks",)

    def tweets(self):
        return TwitterAPI(self).bookmarks()


class TwitterAPI():

    def __init__(self, extractor):
        self.extractor = extractor
        self.headers = {
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejR"
                             "COuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu"
                             "4FA33AGWWjCpTnA",
            "x-guest-token": None,
            "x-twitter-client-language": "en",
            "x-twitter-active-user": "yes",
            "x-csrf-token": None,
            "Origin": "https://twitter.com",
            "Referer": "https://twitter.com/",
        }
        self.params = {
            "include_profile_interstitial_type": "1",
            "include_blocking": "1",
            "include_blocked_by": "1",
            "include_followed_by": "1",
            "include_want_retweets": "1",
            "include_mute_edge": "1",
            "include_can_dm": "1",
            "include_can_media_tag": "1",
            "skip_status": "1",
            "cards_platform": "Web-12",
            "include_cards": "1",
            "include_composer_source": "true",
            "include_ext_alt_text": "true",
            "include_reply_count": "1",
            "tweet_mode": "extended",
            "include_entities": "true",
            "include_user_entities": "true",
            "include_ext_media_color": "true",
            "include_ext_media_availability": "true",
            "send_error_codes": "true",
            "simple_quoted_tweet": "true",
            #  "count": "20",
            "count": "100",
            "cursor": None,
            "ext": "mediaStats,highlightedLabel,cameraMoment",
            "include_quote_count": "true",
        }

        cookies = self.extractor.session.cookies

        # CSRF
        csrf = hashlib.md5(str(time.time()).encode()).hexdigest()
        self.headers["x-csrf-token"] = csrf
        cookies.set("ct0", csrf, domain=".twitter.com")

        if cookies.get("auth_token", domain=".twitter.com"):
            self.headers["x-twitter-auth-type"] = "OAuth2Session"
        else:
            # guest token
            guest_token = _guest_token(self.extractor, self.headers)
            self.headers["x-guest-token"] = guest_token
            cookies.set("gt", guest_token, domain=".twitter.com")

    def tweet(self, tweet_id):
        endpoint = "2/timeline/conversation/{}.json".format(tweet_id)
        for tweet in self._pagination(endpoint):
            if tweet["id_str"] == tweet_id:
                return (tweet,)
        return ()

    def timeline_profile(self, screen_name):
        user = self.user_by_screen_name(screen_name)
        endpoint = "2/timeline/profile/{}.json".format(user["rest_id"])
        return self._pagination(endpoint)

    def timeline_media(self, screen_name):
        user = self.user_by_screen_name(screen_name)
        endpoint = "2/timeline/media/{}.json".format(user["rest_id"])
        return self._pagination(endpoint)

    def search(self, query):
        endpoint = "2/search/adaptive.json"
        params = self.params.copy()
        params["q"] = text.unquote(query)
        return self._pagination(
            endpoint, params, "sq-I-t-", "sq-cursor-bottom")

    def bookmarks(self):
        endpoint = "2/timeline/bookmark.json"
        return self._pagination(endpoint)

    def user_by_screen_name(self, screen_name):
        endpoint = "graphql/-xfUfZsnR_zqjFd-IfrN5A/UserByScreenName"
        params = {
            "variables": '{"screen_name":"' + screen_name + '"'
                         ',"withHighlightedLabel":true}'
        }
        return self._call(endpoint, params)["data"]["user"]

    def _call(self, endpoint, params):
        url = "https://api.twitter.com/" + endpoint
        response = self.extractor.request(
            url, params=params, headers=self.headers, fatal=None)
        if response.status_code < 400:
            return response.json()
        if response.status_code == 429:
            self.extractor.wait(until=response.headers["x-rate-limit-reset"])
            return self._call(endpoint, params)
        raise exception.StopExtraction(
            "%s %s (%s)", response.status_code, response.reason, response.text)

    def _pagination(self, endpoint, params=None,
                    entry_tweet="tweet-", entry_cursor="cursor-bottom-"):
        if params is None:
            params = self.params.copy()

        while True:
            cursor = tweet = None
            data = self._call(endpoint, params)

            instr = data["timeline"]["instructions"]
            if not instr:
                return
            tweets = data["globalObjects"]["tweets"]
            users = data["globalObjects"]["users"]

            for entry in instr[0]["addEntries"]["entries"]:

                if entry["entryId"].startswith(entry_tweet):
                    tid = entry["content"]["item"]["content"]["tweet"]["id"]
                    if tid not in tweets:
                        self.extractor.log.debug(
                            "Skipping unavailable Tweet %s", tid)
                        continue
                    tweet = tweets[tid]
                    tweet["user"] = users[tweet["user_id_str"]]

                    if "quoted_status_id_str" in tweet:
                        quoted = tweets.get(tweet["quoted_status_id_str"])
                        if quoted:
                            tweet["full_text_quoted"] = quoted["full_text"]
                            if "extended_entities" in quoted:
                                tweet["extended_entities"] = \
                                    quoted["extended_entities"]
                    elif "retweeted_status_id_str" in tweet:
                        retweet = tweets.get(tweet["retweeted_status_id_str"])
                        if retweet:
                            tweet["author"] = users[retweet["user_id_str"]]

                    yield tweet

                elif entry["entryId"].startswith(entry_cursor):
                    cursor = entry["content"]["operation"]["cursor"]
                    if not cursor.get("stopOnEmptyResponse"):
                        # keep going even if there are no tweets
                        tweet = True
                    cursor = cursor["value"]

            if "replaceEntry" in instr[-1] :
                cursor = (instr[-1]["replaceEntry"]["entry"]
                          ["content"]["operation"]["cursor"]["value"])

            if not cursor or not tweet:
                return
            params["cursor"] = cursor


@cache(maxage=3600)
def _guest_token(extr, headers):
    return extr.request(
        "https://api.twitter.com/1.1/guest/activate.json",
        method="POST", headers=headers,
    ).json().get("guest_token")
