#!/usr/bin/env python3

"""
+---------------------------------------+
|          Marco Toledo, 2021           |
|             BCC@ICMC-USP              |
| marcoantonioribeirodetoledo@gmail.com |
|             mardt@usp.br              |
+---------------------------------------+

Licensed over GPL-v3, check ../LICENSE for more info
"""

import typing
import os
import tweepy
import calendar
import sys
import time

from dotenv import load_dotenv
load_dotenv()


class QueryError(Exception):
    """
    Query building exception.

    Attributes:
        query: Original query with error
    """
    def __init__(self, err: str, query: str = "") -> Exception:
        """
        Throws QuerryError with specified error message and sets
        intance's query

        :param err: Error message for the exception
        :type err: str

        :param query: Query that threw the given error [optional]
        :type query: str
        """
        self.query = query
        super().__init__("Error while building query: {}".format(err))


class RequestRunner():
    """
    Holds methods for building and running queries.
    """
    def __init__(self,
                 archiveTag: str = "archive",
                 lastMonthTag: str = "30days"):
        """
        :param archiveTag: Tag for the archive search sandbox as stated on the developer console
        :type archiveTag: str

        :param lastMonthTag: Tag for the "last 30 days" search sandbox as stated on the developer console
        :type lastMonthTag: str
        """

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
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)

        # API parameters
        self.MAX_PER_MONTH = 5*(10**3)
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
        """
        Builds and saves query based on the given search terms.

        :param terms: Defined search terms
        :type terms: [str]

        :returns: Copy of the saved query if successful, otherwise None object
        :rtype: typing.Union[str, None]
        """
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
            _dayStart: int,
            _dayEnd: int,
            _maxResults: int,
    ) -> tweepy.models.ResultSet:
        """
        Internal archive query runner utility.

        :param _archiveQuery: Initialized and formated search query
        :type _archiveQuery: str

        :param _year: Year for the analyzed time span
        :type _year: int

        :param _month: Month for the analyzed time span
        :type _month: int

        :param _dayStart: Start day for the analyzed time span
        (defaults to 1)
        :type _dayStart: int

        :param _dayEnd: End day for the analyzed time span
        (defaults to last day of the month)
        :type _dayEnd: int

        :param _maxResults: Maximum number of returned tweets
        [resolves to min(size of found_tweets, _maxResults)]
        :type _maxResults: int

        :returns: ResultSet of found tweets
        :rtype: tweepy.models.ResultSet
        """
        if _maxResults < 10 or _maxResults > self.MAX_PER_MONTH:
            raise QueryError(
                "maxResults out of range [10, {}]".format(self.MAX_PER_MONTH)
            )

        args = {
            "label": self.ARCHIVE_TAG,
            "query": _archiveQuery,
            "fromDate": "{:04}{:02}{:02}0000".format(_year, _month, _dayStart),
            "toDate": "{:04}{:02}{:02}2359".format(_year, _month, _dayEnd)
        }

        return tweepy.Cursor(
            self.api.search_full_archive,
            **args
        ).items(_maxResults)

    def runArchiveQuery(
            self,
            year: int,
            month: int,
            dayStart: int = 1,
            dayEnd: int = -1,
            maxResults: int = -1,
    ) -> [dict]:
        """
        Archive query facility.

        :param year: Year for the analyzed time span
        :type year: int

        :param month: Month for the analyzed time span
        :type month: int

        :param dayStart: Start day for the analyzed time span
        (defaults to 1)
        :type dayStart: int

        :param dayEnd: End day for the analyzed time span
        (defaults to last day of the month)
        :type dayEnd: int

        :param maxResults: Maximum number of returned tweets
        (defaults to maximum monthly quota on < 0)
        :type maxResults: int

        :returns: List of dicts containing the truncated text from the
        tweet and its id_str
        :rtype: [dict]
        """
        if self._definedQuery == "":
            raise QueryError("Query not defined. Run `buildQuery` to set it")

        if dayEnd < 1:
            dayEnd = calendar.monthrange(year, month)[1]
        if dayEnd < dayStart:
            raise QueryError("Invalid dates! Start date should come before end date")

        if maxResults < 1:
            maxResults = self.MAX_PER_MONTH
        if dayStart < 1:
            dayStart = 1

        print("✓ Running query...")
        r = self._runArchiveQuery(
            _archiveQuery=self._definedQuery,
            _year=year,
            _month=month,
            _dayStart=dayStart,
            _dayEnd=dayEnd,
            _maxResults=maxResults
        )

        print("✓ Storing data...")
        tweets = []
        for tweet in r:
            try:
                if not tweet.retweeted:
                    tweets.append({
                        "id": tweet.id_str,
                        "text": tweet.text
                    })
            except Exception:
                sys.stderr.write("Request rate met, retyring in 61 seconds...")
                time.sleep(61)
        return tweets
