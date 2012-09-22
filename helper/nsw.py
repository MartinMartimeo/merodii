#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
    Read some infos from nsw
"""
__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '21.09.12 - 19:32'

import time

import urllib.request, urllib.error, urllib.parse

from helper.html import unescape


def read_sendunginfo(url):
    """
        Ließt Sendungstitel, Sendungsthema, Uhrzeit aus
    """

    if read_sendunginfo.last < time.time() - read_sendunginfo.time or not read_sendunginfo.data:

        # Init urllib
        request = urllib.request.Request(url)
        opener = urllib.request.build_opener()

        # Read data
        data = opener.open(request, None, 1)
        rtn = ""
        while True:
            line = data.readline()
            if not line:
                break
            line = line.decode("utf-8")
            rtn += " " + line

        # Parse
        (sendung_title, sendung_thema, sendung_start) = rtn.split("$")
        sendung_title = unescape(sendung_title.strip())
        sendung_thema = unescape(sendung_thema.strip())
        read_sendunginfo.data = {'sendung_title': sendung_title, 'sendung_thema': sendung_thema, 'sendung_start': sendung_start.strip()}
    return read_sendunginfo.data
read_sendunginfo.last = 0
read_sendunginfo.time = 60
read_sendunginfo.data = None

if __name__ == "__main__":
    print("%s" % read_sendunginfo("http://www.nsw-anime.de/pic.php?request=text"))