#!/usr/bin/env python3

import typing
import os
import tweepy
import calendar

from dotenv import load_dotenv
load_dotenv()


class QueryError(Exception):
    """
    Query building exception.

    Attributes:
        query: Original query with error
    """
    def __init__(self, err: str, query: str = "") -> Exception:
        self.query = query
        super().__init__("Error while building query: {}".format(err))


class RequestRunner():
    def __init__(self, archiveTag="archive", lastMonthTag="30days"):
        # Parameterized values
        self.ARCHIVE_TAG = archiveTag
        self.LAST_MONTH_TAG = lastMonthTag

        # API setup
        self.auth = tweepy.OAuthHandler(
            os.getenv("API_KEY"),
            os.getenv("API_KEY_SECRET")
        )
        self.auth.set_access_token(
            os.getenv("ACCESS_TOKEN"),
            os.getenv("ACCESS_TOKEN_SECRET")
        )
        self.api = tweepy.API(self.auth)

        # API parameters
        self.MAX_PER_MONTH = 25*(10**3)
        self.MAX_QUERY_LEN = 128
        self.MAX_PER_MIN = 30
        self.TIMEOUT = 60/self.MAX_PER_MIN

        # Search global parameter
        self.LANG = "pt"
        self.PLACE_COUNTRY = "BR"
        # TODO check for retweets in post since it's not
        # available for free tiers
        self.OPERATORS = "-has:links lang:{} place_country:{}".format(self.LANG, self.PLACE_COUNTRY)

        # State
        self._definedQuery = ""

    def buildQuery(self, terms: [str]) -> typing.Union[str, None]:
        if len(terms) == 0:
            return None
        jointTerms = " OR ".join(terms)
        query = "({}) {}".format(jointTerms, self.OPERATORS)
        if len(query) > self.MAX_QUERY_LEN:
            raise QueryError("Query too long (> 128 characters)", query)
        self._definedQuery = query
        return query

    def _runArchiveQuery(
            self,
            _archiveQuery: str,
            _year: int,
            _month: int,
            _maxResults: int,
    ) -> [tweepy.models.Status]:
        if _maxResults < 10 or _maxResults > self.MAX_PER_MONTH:
            raise QueryError(
                "maxResults out of range [10, {}]".format(self.MAX_PER_MONTH)
            )

        lastDay = calendar.monthrange(_year, _month)[1]
        args = {
            "label": self.ARCHIVE_TAG,
            "query": _archiveQuery,
            "fromDate": "{:04}{:02}{:02}0000".format(_year, _month, 1),
            "toDate": "{:04}{:02}{:02}2359".format(_year, _month, lastDay)
        }

        return tweepy.Cursor(self.api.search_full_archive, **args).items(_maxResults)

    def runArchiveQuery(
            self,
            year: int,
            month: int,
            maxResults=-1,
    ) -> [dict]:
        if self._definedQuery == "":
            raise QueryError("Query not defined. Run `buildQuery` to set it")

        if maxResults < 1:
            maxResults = 100

        tweets = []
        r = self._runArchiveQuery(
            _archiveQuery=self._definedQuery,
            _year=year,
            _month=month,
            _maxResults=maxResults
        )
        for tweet in r:
            if not tweet.retweeted:
                tweets.append({
                    "id": tweet.id_str,
                    "text": tweet.text
                })
        return tweets
