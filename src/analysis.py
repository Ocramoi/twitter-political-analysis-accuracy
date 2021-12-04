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

from LeIA.leia import SentimentIntensityAnalyzer


class Analyzer(SentimentIntensityAnalyzer):
    def __init__(self):
        self.sia = super().__init__()

    def _analyzeTweet(self, parsedTweet: str):
        return self.sia.polarity_scores(parsedTweet)

    def analyzeTweet(self, tweet: str):
        return self._analyzeTweet(tweet)
