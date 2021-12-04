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

import re
import typing

REPLACE_BLANK = [
    [r'RT @[\w]*:', ''],
    [r'@[\w]*', ''],
    [r'https?://[A-Za-z0-9./]*', ''],
]

REMOVE_ITEM = [
    r'https?://[A-Za-z0-9./]*',
]


def _removePatterns(txt: str) -> typing.Union[str, None]:
    removeCounter = 0
    for f in REMOVE_ITEM:
        removeCounter += len(re.findall(f, txt))
    if removeCounter > 0:
        return None
    for f in REPLACE_BLANK:
        txt = re.sub(f[0], f[1], txt)
    return txt


def removePatterns(text: str = None, textList: [str] = None):
    if [text, textList] == [None, None]:
        raise Exception("Function should receive either a string " +
                        "or a string list depending on usage")
    if text is not None:
        return _removePatterns(text)
    filtered = [_removePatterns(t) for t in textList]
    return [v for v in filtered if v is not None]
