#!/usr/bin/env python3

import argparse
import sys
import pandas as pd
from datetime import datetime
from requestrunner import RequestRunner

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


def amountType(v: str):
    v = int(v)
    if v < 1.:
        raise argparse.ArgumentTypeError("Invalid number of tweets")
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
        "-n", "--number",
        metavar="number",
        help="Number of tweets to extract",
        type=amountType
    )
    parser.add_argument(
        "-t", "--terms",
        metavar="terms",
        help="Define search term list from text file (terms separated by " +
        " new line '\\n') [defaults to 'terms.txt']",
        default="terms.txt"
    )


def extract(year: int, month: int, number: int, terms: [str]):
    rr = RequestRunner()
    rr.buildQuery(terms=terms)
    df = pd.DataFrame(
        data=rr.runArchiveQuery(year=year, month=month, maxResults=number)
    )
    print(df.head())
    df.to_csv("tweets.csv")


def main():
    args = parser.parse_args()
    try:
        with open(args.terms, "r") as fTerms:
            searchTerms = fTerms.read().split('\n')[:-1]
    except FileNotFoundError:
        sys.stderr.write("File not found in the current folder")
        exit(1)
    except Exception as e:
        sys.stderr.write("Unhandled error found! Error message: ")
        sys.stderr.write(str(e) + "\n")
        exit(1)

    extract(
        year=args.year,
        month=args.month,
        number=args.number,
        terms=searchTerms
    )


if __name__ == "__main__":
    setupParser()
    main()
