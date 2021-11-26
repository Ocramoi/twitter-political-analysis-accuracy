#!/usr/bin/env python3

import twint
import argparse
import calendar
import sys
import pandas as pd
from datetime import datetime

parser = argparse.ArgumentParser(
    description="Extract tweets for use in the main analysis",
    prog="Data extractor"
)


def monthType(v: str):
    v = int(v)
    if v < 1 or v > 12:
        raise argparse.ArgumentTypeError(
            "Month should be within range [1, 12]"
        )
    return v


def yearType(v: str):
    v = int(v)
    curYear = datetime.now().year
    if v < 2006 or v > curYear:
        raise argparse.ArgumentTypeError(
            "Year should be within range [2006, {}]".format(curYear)
        )
    return v


def setupParser():
    parser.add_argument(
        "-y", "--year",
        metavar="year",
        help="Year to analyze",
        type=yearType
    )
    parser.add_argument(
        "-m", "--month",
        metavar="month",
        help="Month to analyze",
        type=monthType
    )
    parser.add_argument(
        "-t", "--terms",
        metavar="terms",
        help="Define search term list from text file (terms separated by " +
        " new line '\\n') [defaults to 'terms.txt']",
        default="terms.txt"
    )


def extract(year: int, month: int, terms: [str]):
    lastDay = calendar.monthrange(year, month)[1]
    c = twint.Config()
    c.Since = "{}-{:02}-{:02}".format(year, month, 1)
    c.Until = "{}-{:02}-{:02}".format(year, month, lastDay)
    c.Lang = "pt"
    c.Limit = 20
    c.Pandas = True

    for st in terms:
        c.Search = st

    twint.run.Search(c)
    print(twint.storage.panda.Tweets_df.head())


def main():
    args = parser.parse_args()
    try:
        with open(args.terms, "r") as fTerms:
            searchTerms = fTerms.read().split('\n')
    except FileNotFoundError:
        sys.stderr.write("File not found in the current folder")
        exit(1)
    except Exception as e:
        sys.stderr.write("Unhandled error found! Error message: ")
        sys.stderr.write(str(e) + "\n")
        exit(1)

    extract(year=args.year, month=args.month, terms=searchTerms)


if __name__ == "__main__":
    setupParser()
    main()
