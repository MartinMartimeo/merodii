#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Open Features für #nsw-anime
"""
from helper.gendou import get_anime

__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '20.09.12 - 23:15'

import subprocess
import sys

from helper.icy import cached_streamname, cached_streaminfos
from helper.nsw import read_sendunginfo, read_nextsendung, read_nswinfo, read_newpage

def stream(phenny, input):
    """
    zeigt das aktuelle Lied auf dem Stream
    """

    info = cached_streamname(phenny.config.stream_url, phenny.config.stream_mount, phenny.config.stream_song)
    phenny.say("Aktuell sendet: %s" % info)
    return
stream.commands = ['stream']
stream.example = "!stream Zeigt die aktuellen Streaminfos an."
stream.priority = 'low'

def song(phenny, input):
    """
    zeigt das aktuelle Lied auf dem Stream
    """

    info = cached_streaminfos(phenny.config.stream_url, phenny.config.stream_mount, phenny.config.stream_song)
    if "song" in info.keys():
        data = get_anime(info["song"])
        if data:
            phenny.say("Aktuell läuft: %(song_artist)s - %(song_title)s (%(song_position)s %(song_anime)s)" % data)
            return
    phenny.say("Aktuell läuft: %s" % info['song'])
    return
song.commands = ['song']
song.example = "!song Zeigt den aktuellen Song an."
song.priority = 'low'




def next(phenny, input):
    """
    zeigt die nächste Sendung an
    """

    info = read_nextsendung()
    phenny.say("Nächste Sendung: %(next_sendung_title)s am %(next_sendung_day)s um %(next_sendung_when)s" % info)
    return
next.commands = ['next']
next.example = "!next Zeigt die nächste Sendung an."
next.priority = 'low'


def sendung(phenny, input):
    """
    zeigt die aktuelle Sendung auf dem Stream
    """

    #info = read_sendunginfo(phenny.config.sendung_url)
    info = read_newpage()
    if not sendung:
        return
    elif "stream_info" in info.keys():
        phenny.say(info["stream_info"])
    elif "sendung_thema" in info.keys():
        phenny.say("%s mit %s seit %s" % (info["sendung_title"], info["sendung_thema"], info["sendung_start"]))
    else:
        phenny.say("%s seit %s" % (info["sendung_title"], info["sendung_start"]))
    return
sendung.commands = ['sendung']
sendung.example = "!sendung Zeigt die aktuelle Sendung an."
sendung.priority = 'low'


def fliegen(phenny, input):
    """
    User wird von Merodii mit einen Abschiedsgruß geschmissen
    """
    phenny.write(['KICK', input.sender, input.nick], phenny.config.msg_fliegen)
    return
fliegen.commands = ['fliegen']
fliegen.example = "!fliegen Lässt dich fliegen."
fliegen.priority = 'low'

def regeln(phenny, input):
    """
    Dummy, just for the help text
    """
    return
regeln.commands = ['regeln']
regeln.example = ["Regeln für den NSW-AnImE IRC-Chat:", "Begegne anderen Chattern mit Respekt und Höflichkeit.", "Halte dich an die Gesetze. Verweise auf illegale, pornografische/erotische oder gewaltverherrlichende Inhalte werden nicht toleriert. Dies betrifft auch animerelevante Verweise, d.h. Links zu Animestreams/-downloads oder auch zu deren Sub-Gruppen werden nicht geduldet. ", "Nehmt nicht alles ernst, was geschrieben wird. Habt ihr jedoch das Gefühl, dass es eine bestimmte Grenze überschreitet, wendet euch ans Team.", "Spammen/Flooding (unnötiges Wiederholen von ein und der selben Nachricht) ist zu unterlassen.", "Links sind grundsätzlich verboten. Ausnahmen sind: www.nsw-anime.de und Profile und Bilder von unserer Seite, sowie jeglicher anderer Content unserer Seite.", "Weiterhin gelten die Regeln des Chatbetreibers: http://ircplanet.eu/rules.html.de"]
regeln.priority = 'low'

def zitat(phenny, input):
    """
    Merodii zitiert eine Berühmte Persönlichkeit
    """
    try:
        while True:
            quote = subprocess.check_output(["fortune", "-s"]).decode("utf-8")
            if quote.find("--") == -1:
                continue
            # Extract Author
            pos_author = quote.find("--") + 2
            author = ""
            for line in quote[pos_author:].split("\n"):
                line = line.strip()
                if line:
                    author += line
            # Extract Line
            pos_author -= 2
            str = ""
            for line in quote[:pos_author].split("\n"):
                line = line.strip()
                if line:
                    str += line + " "
            str += "(" + author + ")"
            phenny.say(str)
            break
    except subprocess.CalledProcessError:
        print("Please install fortune!", sys.stderr)
zitat.commands = ['zitat']
zitat.example = "!zitat Ein Zitat einer berühtem Persöhnlichkeit"
zitat.priority = 'low'

def hilfe(phenny, input):
    """Shows a command's documentation, and possibly an example."""
    name = input.group(2)
    if not name:
        phenny.msg(input.nick, phenny.config.msg_hilfe)
        return

    name = name.lower().strip()

    # Check if key present with example
    has_key = False
    for (key, doc) in list(phenny.doc.items()):
        if doc[1] and isinstance(doc[1], dict) and name in list(doc[1].keys()):
            phenny.msg(input.nick, doc[1][name])
            break
        elif doc[1] and isinstance(doc[1], list) and key == name:
            for line in doc[1]:
                phenny.msg(input.nick, line)
            break
        elif doc[1] and key == name:
            phenny.msg(input.nick, doc[1])
            break
    else:
        phenny.msg(input.nick, "Den Befehl kenn ich nicht :(")
        return
hilfe.commands = ['hilfe']
hilfe.example = '!hilfe zeigt die Hilfe an'
hilfe.priority = 'low'


def dj(phenny, input):
    """
        Ändert das Topic vom NSW Main Channel
    """

    # Check Access
    if input.sender not in phenny.config.staff_channel:
        return

    arg = input.group(2)
    info = read_nswinfo(phenny.config)

    msg = ""
    if not arg:
        msg = phenny.config.topic_noarg
    else:
        msg = phenny.config.topic_warg

    info["arg"] = arg
    info["nick"] = input.nick

    msg %= info

    # Run
    for chan in phenny.config.main_channel:
        phenny.write(['CHANSERV'], "TOPIC %s %s" % (chan, msg))
    return
dj.commands = ['dj']
dj.priority = 'medium'

def pl(phenny, input):
    """
        Zurücksetzen des Topics
    """

    # Check Access
    if input.sender not in phenny.config.staff_channel:
        return

    msg = phenny.config.topic_playlist

    # Run
    for chan in phenny.config.main_channel:
        phenny.write(['CHANSERV'], "TOPIC %s %s" % (chan, msg))
    return
pl.commands = ['pl']
pl.priority = 'medium'


if __name__ == '__main__':
    print(__doc__.strip())
