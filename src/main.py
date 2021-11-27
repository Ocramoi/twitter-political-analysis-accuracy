#!/usr/bin/env python3

import os
import tweepy

from dotenv import load_dotenv
load_dotenv()


def main():
    auth = tweepy.OAuthHandler(os.getenv("API_KEY"), os.getenv("API_KEY_SECRET"))
    auth.set_access_token(
        os.getenv("ACCESS_TOKEN"),
        os.getenv("ACCESS_TOKEN_SECRET")
    )
    api = tweepy.API(auth)

    # print(api.search_30_day(label="research", query="mito"))
    print(api.search_full_archive(label="archive", query="mito", fromDate="202105011200", toDate="20210501120", maxResults=1))


if __name__ == "__main__":
    main()
