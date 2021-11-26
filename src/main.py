#!/usr/bin/env python3

import os
import tweepy

from dotenv import load_dotenv
load_dotenv()


def main():
    print(os.getenv("ACCESS_TOKEN"))


if __name__ == "__main__":
    main()
