#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Open Features für #nsw-anime
"""
__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '20.09.12 - 23:15'

import subprocess
import sys

from helper.icy import cached_streaminfos

def stream(phenny, input):
    """
    zeigt das aktuelle Lied auf dem Stream
    """

    info = cached_streaminfos(phenny.config.stream_url, phenny.config.stream_mount)
    phenny.say("Aktuell sendet: %s" % info["description"])
    return
stream.commands = ['stream']
stream.example = "!stream Zeigt aktuellen Song an."
stream.priority = 'low'

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
        print("Please install fortune!", file=sys.stderr)


zitat.commands = ['zitat']
zitat.example = "!zitat Ein Zitat einer berühtem Persöhnlichkeit"
zitat.priority = 'low'


def fun(phenny, input):
    """
    Merodii wirft Kekse auf einen User der im Chat Online ist, ist der User nicht vorhanden frisst sie die Kekse selber
    Merodii plüscht bestimmten User, ist der User nicht vorhanden plüscht sie Oto
    """
    nick_to = input.match.group(2)
    if nick_to:
        nick_to = nick_to.strip()
    action = input.match.group(1).strip()
    nicks = uchan(input.sender)

    if not nick_to:
        msg = getattr(phenny.config, "msg_%s_nobody" % action) % input.nick
    elif nick_to == phenny.nick:
        msg = getattr(phenny.config, "msg_%s_phenny" % action)
    elif nick_to in list(nicks.keys()) and nicks[nick_to]:
        msg = getattr(phenny.config, "msg_%s_anybody" % action) % nick_to
    else:
        msg = getattr(phenny.config, "msg_%s_phenny" % action)
    phenny.action(msg)
    return
fun.commands = ['kekse', 'pluesch']
fun.example = {'kekse': "!kekse <Nick> bewirft denjenigen mit Keksen.", 'pluesch': "!pluesch <Nick> plüscht denjenigen."}
fun.priority = 'low'


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


def uchan(chan):
    """
    This is for holding the users in a channel
    """
    if chan in list(uchan.data.keys()):
        return uchan.data[chan]
    uchan.data[chan] = {}
    return []
uchan.data = {}

def on_join(phenny, input):
    """
    recognize an user
    """
    uchan(input.sender)
    uchan.data[input.sender][input.nick] = True
on_join.event = 'JOIN'
on_join.rule = r'(.*)'

def on_part(phenny, input):
    """
    remove an user
    """
    uchan(input.sender)
    uchan.data[input.sender][input.nick] = False
on_part.event = 'PART'
on_part.rule = r'(.*)'

def on_quit(phenny, input):
    """
    remove an user
    """
    uchan(input.sender)
    uchan.data[input.sender][input.nick] = False
on_quit.event = 'QUIT'
on_quit.rule = r'(.*)'

def on_nick(phenny, input):
    """
    renames an user
    """
    nick_from = input.nick
    nick_to = input.match.group(0).strip()
    uchan(input.sender)
    uchan.data[input.sender][nick_from] = False
    uchan.data[input.sender][nick_to] = True
on_nick.event = 'NICK'
on_nick.rule = r'(.*)'

def on_kick(phenny, input):
    """
    gone user
    """
    nick = input.args[1]
    uchan(input.sender)
    uchan.data[input.sender][nick] = False
on_kick.event = 'KICK'
on_kick.rule = r'(.*)'

def on_names(phenny, input):
    """
    list user
    """
    nicks = input.match.group(0).strip()
    channel = input.args[2].strip()
    uchan(channel)
    for nick in nicks.split():
        uchan.data[channel][nick.strip("@%+")] = True
on_names.event = '353'
on_names.rule = r'(.*)'

if __name__ == '__main__':
    print(__doc__.strip())
