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

import utils
import argparse
import progressbar
import postProcessing
import pandas as pd
import os
from LeIA.leia import SentimentIntensityAnalyzer

parser = argparse.ArgumentParser(
    description="Extract tweets for use in the main analysis",
    prog="Data extractor"
)


def setupParser() -> None:
    """
    Sets up command line argument parser with required options.
    """
    parser.add_argument(
        "-t", "--tweets",
        metavar="tweets",
        help="CSV file containing the ids of the tweets for " +
        "analysis (defaults to tweets.csv)",
        default="tweets.csv"
    )
    parser.add_argument(
        "-s", "--save",
        help="Saves DataFrame of the tweets' full text + raw analysis for " +
        "later use in `analysis.csv`",
        action="store_true"
    )


def main():
    args = parser.parse_args()
    extractor = utils.Extractor(args.tweets)
    textList = extractor.getTextList()
    textList = postProcessing.removePatterns(textList=textList)

    tweets = []
    an = SentimentIntensityAnalyzer()
    print("Generating analysis...")
    for text in progressbar.progressbar(textList):
        analysisObj = an.polarity_scores(text)
        tweets.append({
            "parsed_text": text,
            'pos': analysisObj['pos'],
            'neg': analysisObj['neg'],
            'neu': analysisObj['neu'],
            'compound': analysisObj['compound']
        })
    df = pd.DataFrame.from_dict(tweets)
    df = df[~df.duplicated(keep=False, subset="parsed_text")]
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    # TODO analisar termos como sujeito da frase
    if args.save:
        df.to_csv("analysis.csv")

    print("Data set:")
    print(df.head())

    print("=" * os.get_terminal_size()[0])

    print("Data:")
    print(df.describe())
    df.describe().to_csv("out.data")
    print("Goodbye!")


if __name__ == "__main__":
    setupParser()
    main()
