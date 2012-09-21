#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Read an icecast stream
"""
__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '20.09.12 - 23:03'

import re
import time
import urllib.request, urllib.error, urllib.parse

def read_icyinfo(url):
    """
        Ließt die Informationen aus dem icecast stream
    """

    # Init urllib
    request = urllib.request.Request(url)
    request.add_header('Icy-MetaData','1')
    opener = urllib.request.build_opener()

    # Read data
    data = opener.open(request, None, 1)
    line = data.readline()
    info = data.info()
    data.close()

    # Parse
    rtn = {}
    for key, value in list(info.items()):
        if key.startswith('icy-'):
            key = key[4:]
            rtn[key] = value

    return rtn

def read_nswstreaminfo(url):
    """
        Ließt den aktuellen Song aus
    """

    # Init urllib
    request = urllib.request.Request(url)
    opener = urllib.request.build_opener()


    # Regex
    regex = re.compile(r'<div[^>]*>(.*)<\/div>', re.U + re.I)

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
    match = re.search(regex, rtn)
    if not match:
        return None
    song = match.group(1)
    return song

def read_xslinfo(url):

    # Init urllib
    request = urllib.request.Request(url)
    opener = urllib.request.build_opener()

    # Regex
    regex_key = re.compile(r'<td[^>]*>(.*)<\/td>', re.U + re.I)
    regex_value = re.compile(r'<td\s[^>]*class=\"streamdata\">(.*)<\/td>', re.U + re.I)

    # Read data
    data = opener.open(request, None, 1)
    info = {}
    while True:
        line_key = data.readline()
        if not line_key:
            break
        line_key = line_key.decode("utf-8")
        match = re.search(regex_key, line_key)
        if not match:
            continue
        key = match.group(1).lower().replace(" ", "-")
        line_value = data.readline()
        if not line_value:
            break
        line_value = line_value.decode("utf-8")
        match = re.search(regex_value, line_value)
        if not match:
            continue
        value = match.group(1)
        info[key] = value

    # parse
    return info


def cached_streaminfos(url, mount, song=None):
    """
        Cached die icyinfo, sodass nur einmal in der Minute abgefragt wird

        @todo consider reading to be async and always return cached data
    """

    # Update if old or non existant
    if cached_streaminfos.last < time.time() - cached_streaminfos.time or not cached_streaminfos.data:
        cached_streaminfos.info = read_icyinfo("%s/%s" % (url, mount))
        cached_streaminfos.data = read_xslinfo("%s/status.xsl?mount=/%s" % (url, mount))
        cached_streaminfos.song = {"song": read_nswstreaminfo(song)}
        cached_streaminfos.last = time.time()

    return dict(list(cached_streaminfos.data.items()) + list(cached_streaminfos.info.items()) + list(cached_streaminfos.song.items()))
cached_streaminfos.last = 0
cached_streaminfos.data = None
cached_streaminfos.song = None
cached_streaminfos.info = None
cached_streaminfos.time = 30 # 1/2 minute

def cached_streamname(url, mount, song=None):
    """
        Gibt zurück was für eine aktuelle Statio angezeigt werden würde
    """

    data = cached_streaminfos(url, mount, song)
    if "name" in data.keys() and "song" in data.keys():
        return data["name"] + " mit: " + data["song"]
    if "description" in data.keys() and "song" in data.keys():
        return data["description"] + " mit: " + data["song"]
    if "name" in data.keys():
        return data["name"]
    if "description" in data.keys():
        return data["description"]

    return None

if __name__ == "__main__":
    print ("%s" % cached_streamname("http://5.9.88.35:8000/", "nsw-anime", "http://www.nsw-anime.de/modules/mod_shoutcast/info.php?currentSong=1"))