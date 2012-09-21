#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Open Features für #nsw-anime
"""
__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '20.09.12 - 23:15'

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
stream.priority = 'low'

def fliegen(phenny, input):
    """
    User wird von Merodii mit einen Abschiedsgruß geschmissen
    """
    phenny.write(['KICK', input.sender, input.nick], phenny.config.msg_fliegen)
    return
fliegen.commands = ['fliegen']
fliegen.priority = 'low'

def fun(phenny, input):
    """
    Merodii wirft Kekse auf einen User der im Chat Online ist, ist der User nicht vorhanden frisst sie die Kekse selber
    Merodii plüscht bestimmten User, ist der User nicht vorhanden plüscht sie Oto
    """
    nick_to = input.match.group(2)
    if nick_to:
        nick_to = nick_to.encode("utf-8")
    action = input.match.group(1)
    nicks = uchan(input.sender)

    if not nick_to:
        msg = getattr(phenny.config, "msg_%s_nobody" % action) % input.nick
    elif nick_to == phenny.nick:
        msg = getattr(phenny.config, "msg_%s_phenny" % action)
    elif nick_to in nicks.keys() and nicks[nick_to]:
        msg = getattr(phenny.config, "msg_%s_anybody" % action) % nick_to
    else:
        msg = getattr(phenny.config, "msg_%s_phenny" % action)
    phenny.action(msg)
    return
fun.commands = ['kekse', 'pluesch']
fun.priority = 'low'


def uchan(chan):
    """
    This is for holding the users in a channel
    """
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
    nick_to = input.match.group(0)
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
    nicks = input.match.group(0)
    channel = input.args[2]
    uchan(channel)
    for nick in nicks.split():
        uchan.data[channel][nick.strip("@%+")] = True
on_names.event = '353'
on_names.rule = r'(.*)'

if __name__ == '__main__':
    print __doc__.strip()
