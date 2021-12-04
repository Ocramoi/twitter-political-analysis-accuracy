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

import os
import tweepy
import csv
import time
import progressbar
import sys

from dotenv import load_dotenv
load_dotenv()


class Extractor():
    def __init__(self, filename: str = None):
        # API setup
        auth = tweepy.OAuthHandler(
            os.getenv("API_KEY"),
            os.getenv("API_KEY_SECRET")
        )
        auth.set_access_token(
            os.getenv("ACCESS_TOKEN"),
            os.getenv("ACCESS_TOKEN_SECRET")
        )
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        self.timeout = (15*60)/900
        self.tweetIdList: [str] = []
        self.tweetTextList: [str] = []
        if filename is not None:
            self.getTweetIdList(filename)

    def textFromId(self, _id: str):
        data = self.api.get_status(
            _id,
            trim_user=True,
            tweet_mode="extended"
        )._json
        return data["full_text"]

    def getTweetIdList(self, filename: str) -> [str]:
        print("Extracting ids form list...")
        self.tweetIdList.clear()
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.tweetIdList.append(row["id"])
        return self.tweetIdList

    def getTextList(self):
        print("Extracting text from tweets...")
        self.tweetTextList.clear()
        for _id in progressbar.progressbar(self.tweetIdList):
            try:
                text = self.textFromId(_id)
                self.tweetTextList.append(text)
                time.sleep(self.timeout * 1.1)
            except Exception as e:
                sys.stderr.write(
                    "\a\nCouldn't fetch tweet with ID: {}".format(_id) +
                    "\nError found: " + str(e)
                )
                continue
        return self.tweetTextList
