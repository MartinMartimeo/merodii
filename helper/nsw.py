#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
    Read some infos from nsw
"""
__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '21.09.12 - 19:32'

import re
import socket
import time

import urllib.request, urllib.error, urllib.parse

from helper.unescape import unescape

def read_nextsendung():
    """
        Ließt die nächste stattfindene Sendung aus
    """

    if read_nextsendung.last < time.time() - read_nextsendung.time or not read_nextsendung.data:

        # Init urllib
        request = urllib.request.Request("http://www.nsw-anime.de/")
        opener = urllib.request.build_opener()

        # Read data
        try:
            data = opener.open(request, None, 2)
        except socket.timeout:
            return read_nextsendung.data

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

        # Compile Regex
        regex_list = re.compile(r'<h3[^>]*>\s*NSW-Sendeplan\s*<\/h3[^>]*>\s*<ul[^>]*>((?:\s*<li[^>]*>\s*<a[^>]*>(?:.*)<\/a>\s*<br[^>]*>\s*(?:.*)\s*<br[^>]*>\s*<\/li[^>]*>\s*)+)', re.U + re.I)
        regex_li = re.compile(r'<li[^>]*>\s*<a[^>]*>(.*)<\/a>\s*<br[^>]*>\s*((\d+)\.\s*.*\s*\((\d+):(\d+)\))\s*<br[^>]*>\s*<\/li[^>]*>', re.U + re.I)

        # Parse
        match_list = re.search(regex_list, rtn)
        if match_list:
            list = match_list.group(1)

            a_time_hour = time.localtime().tm_min
            a_time_day = time.localtime().tm_mday
            for (title, when, when_day, when_time_hour, when_time_min) in re.findall(regex_li, list):
                if int(when_day) <= a_time_day and int(when_time_hour) <= a_time_hour:
                    continue
                read_nextsendung.data = {'title': title, 'when': when}
                read_nextsendung.last = time.time()
                break

    return read_nextsendung.data
read_nextsendung.last = 0
read_nextsendung.time = 60
read_nextsendung.data = None






def read_moddinginfo(url):
    """
        Ließt Sendungstitel, Sendungsthema, Uhrzeit aus
    """

    if read_moddinginfo.last < time.time() - read_moddinginfo.time or not read_moddinginfo.data:

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

        print("%s" % rtn)

        # Parse
        (sendung_mod_image, sendung_image, sendung_start_date, sendung_start_time) = rtn.strip().split(" ")
        sendung_mod_name = " ".join(sendung_mod_image.split(".")[:-1]).strip()
        read_moddinginfo.data = {'sendung_mod_image': sendung_mod_image, 'sendung_image': sendung_image, 'sendung_start_date': sendung_start_date.strip(), 'sendung_start_time': sendung_start_time, 'sendung_mod_name': sendung_mod_name}
        read_moddinginfo.last = time.time()
    return read_moddinginfo.data
read_moddinginfo.last = 0
read_moddinginfo.time = 60
read_moddinginfo.data = None

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
        read_sendunginfo.last = time.time()
    return read_sendunginfo.data
read_sendunginfo.last = 0
read_sendunginfo.time = 60
read_sendunginfo.data = None

if __name__ == "__main__":
    print("%s" % read_nextsendung())