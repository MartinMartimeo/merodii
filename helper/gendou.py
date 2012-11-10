#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
    Reads the anime for a song (provide by genodu.com)
"""
import difflib
import re
import socket
import urllib.request, urllib.parse, urllib.error

__author__ = 'MartinMartimeo <martin@martimeo.de>'
__date__ = '10.11.12 - 18:11'



def get_anime(song):
    """
        Get the Anime for a Song
    """

    # Cached?
    if get_anime.song != song:

        # Build filter
        filter = urllib.parse.urlencode({'filter': song})

        # Init urllib
        request = urllib.request.Request("http://gendou.com/amusic/?%s" % filter)
        opener = urllib.request.build_opener()

        # Read data
        try:
            data = opener.open(request, None, 2)
        except socket.timeout:
            return get_anime.data
        except urllib.error.URLError:
            return get_anime.data

        # Collect Data
        rtn = ""
        while True:
            line = data.readline()
            if not line:
                break
            try:
                line = line.decode("utf-8")
            except UnicodeDecodeError:
                line = "..."
            rtn += " " + line

        # Init Regex
        regex = re.compile(r'<tr[^>]*>\s*<td[^>]*>\s*<a[^>]*>\s*(.+)\s*<\/a>\s*<\/td>\s*<td[^>]*>\s*<a[^>]*>\s*(.+)\s*<\/a>\s*<\/td>\s*<td[^>]*>\s*<a[^>]*>\s*(.+)\s*<\/a>\s*<\/td>\s*<td[^>]*>\s*(.+)\s*<\/td>\s*<td[^>]*>\s*(.+)\s*<\/td>\s*<td[^>]*>\s*(.+)\s*<\/td>\s*<td[^>]*>\s*<a[^>]*>\s*.+\s*<\/a>\s*<a[^>]*>\s*.+\s*<\/a>\s*<a[^>]*>\s*.+\s*<\/a>\s*<\/td>\s*<td[^>]*>.+<\/td>\s*<td[^>]*>\s*<span[^>]*>\s*(.+)\s*<\/span>\s*<\/td>\s*<\/tr>', re.U + re.I)

        # Find All
        song_titles = []
        song_data = {}
        for (song_title, song_anime, song_artist, song_position, song_length, song_size, song_rating) in re.findall(regex, rtn):
            song_data[song_title] = {}
            song_data[song_title]["song_title"] = song_title
            song_data[song_title]["song_anime"] = song_anime
            song_data[song_title]["song_artist"] = song_artist.strip()
            song_data[song_title]["song_position"] = song_position
            song_data[song_title]["song_length"] = song_length
            song_data[song_title]["song_size"] = song_size
            song_data[song_title]["song_rating"] = song_rating.strip()
            song_titles.append(song_title)

        # Get Best Match
        song_title = song.rsplit(" - ", 1)[1]
        song_titles = difflib.get_close_matches(song_title, song_titles, 1)
        if song_titles:
            song_title = song_titles[0]
            get_anime.data = song_data[song_title]
            get_anime.song = song
    return get_anime.data
get_anime.song = None
get_anime.data = None





if __name__ == "__main__":
    print("%s" % get_anime("Bump of chicken - sailing day"))