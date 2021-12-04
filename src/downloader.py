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

import argparse
import sys
import pandas as pd
from datetime import datetime

from requestrunner import RequestRunner

parser = argparse.ArgumentParser(
    description="Extract tweets for use in the main analysis",
    prog="Data extractor"
)


def _dayType(v: str) -> int:
    """
    Checks `day` command line argument validity on startup and converts
    value.

    :param v: Value read from the command line
    :type v: str
    :raises argparse.ArgumentTypeError: Encountered error while parsing value
    :returns: The converted day after checking
    :rtype: int
    """
    v = int(v)
    if v < 1 or v > 31:
        raise argparse.ArgumentTypeError(
            "Day should be within range [1, 31]"
        )
    return v


def _monthType(v: str) -> int:
    """
    Checks `month` command line argument validity on startup and converts
    value.

    :param v: Value read from the command line
    :type v: str
    :raises argparse.ArgumentTypeError: Encountered error while parsing value
    :returns: The converted month after checking
    :rtype: int
    """
    v = int(v)
    if v < 1 or v > 12:
        raise argparse.ArgumentTypeError(
            "Month should be within range [1, 12]"
        )
    return v


def _yearType(v: str) -> int:
    """
    Checks `year` command line argument validity on startup and converts value.

    :param v: Value read from the command line
    :type v: str
    :raises argparse.ArgumentTypeError: Encountered error while parsing value
    :returns: The converted year after checking
    :rtype: int
    """
    v = int(v)
    curYear = datetime.now().year
    if v < 2006 or v > curYear:
        raise argparse.ArgumentTypeError(
            "Year should be within range [2006, {}]".format(curYear)
        )
    return v


def _amountType(v: str):
    """
    Checks `number` command line argument validity on startup and
    converts value.

    :param v: Value read from the command line
    :type v: str
    :raises argparse.ArgumentTypeError: Encountered error while parsing value
    :returns: The converted amount after checking
    :rtype: int
    """
    v = int(v)
    if v < 1.:
        raise argparse.ArgumentTypeError("Invalid number of tweets")
    return v


def setupParser() -> None:
    """
    Sets up command line argument parser with required options.
    """
    parser.add_argument(
        "-y", "--year",
        metavar="year",
        help="Year to analyze",
        type=_yearType
    )
    parser.add_argument(
        "-m", "--month",
        metavar="month",
        help="Month to analyze",
        type=_monthType
    )
    parser.add_argument(
        "-n", "--number",
        metavar="number",
        help="Number of tweets to extract",
        type=_amountType
    )
    parser.add_argument(
        "-db", "--dayBegin",
        metavar="dayBegin",
        help="Starting day for the time slot",
        type=_dayType,
        default=1
    )
    parser.add_argument(
        "-de", "--dayEnd",
        metavar="dayEnd",
        help="Ending day for the time slot",
        type=_dayType,
        default=-1
    )
    parser.add_argument(
        "-t", "--terms",
        metavar="terms",
        help="Define search term list from text file (terms separated by " +
        " new line '\\n') [defaults to 'terms.txt']",
        default="terms.txt"
    )


def extract(
        year: int,
        month: int,
        startDay: int,
        endDay: int,
        number: int,
        terms: [str]
) -> None:
    """
    Downloads twitter data with the given arguments to file `tweets.csv`.

    :param year: Year from the requested analysis time span
    :type year: int

    :param month: Month from the requested analysis time span
    :type month: int

    :param number: Max number of tweets to extract from time span
    :type number: int

    :param terms: Search terms for the query
    :type terms: [str]
    """
    rr = RequestRunner()
    rr.buildQuery(terms=terms)
    df = pd.DataFrame(
        data=rr.runArchiveQuery(
            year=year,
            month=month,
            dayStart=startDay,
            dayEnd=endDay,
            maxResults=number
        )
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
        startDay=args.dayBegin,
        endDay=args.dayEnd,
        number=args.number,
        terms=searchTerms
    )


if __name__ == "__main__":
    setupParser()
    main()
