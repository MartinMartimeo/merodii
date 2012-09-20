#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Open Features für #nsw-anime
"""
__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '20.09.12 - 23:15'

from helper.icy import cached_streaminfos

def stream(phenny, input):
    """
    zeigt das aktuelle Lied auf dem Stream
    """

    info = cached_streaminfos(input.stream_url, input.stream_mount)
    phenny.say("Aktuell sendet: %s" % info["description"])
    return
stream.commands = ['stream']
stream.priority = 'low'

def fliegen(phenny, input):
    """
    User wird von Merodii mit einen Abschiedsgruß geschmissen
    """

    phenny.write(['KICK', input.sender, input.nick], input.msg_fliegen)
    return
stream.commands = ['fliegen']
stream.priority = 'low'

def uchan(chan):
    if chan in uchan.data.keys():
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
    uchan.data[input.sender][input.nick] = True
on_part.event = 'PART'
on_part.rule = r'(.*)'

def kekse(phenny, input):
    """
    Merodii wirft Kekse auf einen User der im Chat Online ist, ist der User nicht vorhanden frisst sie die Kekse selber
    """



if __name__ == '__main__':
    print __doc__.strip()
