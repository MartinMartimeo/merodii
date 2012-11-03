#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Fun Actions from a database

    CREATE TABLE IF NOT EXISTS `irc_actions` (
      `action_ident` varchar(20) NOT NULL DEFAULT '',
      `action_text_normal` text NOT NULL,
      `action_text_me` text NOT NULL,
      `action_text_anybody` text NOT NULL,
      `action_text_nobody` text NOT NULL,
      PRIMARY KEY (`action_ident`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '03.11.12 - 20:00'

import oursql

def get_cursor(uri):

    if uri['host'] in get_cursor.conns.keys():
        return get_cursor.conns[uri['host']].cursor(oursql.DictCursor)

    get_cursor.conns[uri['host']] = oursql.connect(**uri)
    return get_cursor.conns[uri['host']].cursor(oursql.DictCursor)
get_cursor.conns = {}

def fun(phenny, input):
    """
    Ließt eine Fun aktion aus der Datenbank
    """

    # To Nick?
    nick_to = input.match.group(2)
    if nick_to:
        nick_to = nick_to.strip()

        args = nick_to.split()
        if len(args) > 1:
            nick_to = args[0].strip()

    # In Chan?
    action = input.match.group(1).strip()
    nicks = uchan(input.sender)
    if isinstance(nicks, list):
        phenny.write(['NAMES', input.sender])
        return

    # Setting parameter
    para = {'anick': input.nick, 'chan': input.sender, 'me': phenny.nick}
    if not nick_to:
        atype = "normal"
        para['nick'] = input.nick
    elif nick_to == phenny.nick or nick_to in phenny.config.myself:
        atype = "me"
        para['nick'] = phenny.nick
    elif nick_to in list(nicks.keys()) and nicks[nick_to]:
        atype = "anybody"
        para['nick'] = nick_to
    else:
        atype = "nobody"
        para['nick'] = input.nick
    table = phenny.config.fun_table

    # Query Action
    cursor = get_cursor(phenny.config.fun_uri)
    cursor.execute('SELECT action_text_%s as text FROM %s WHERE action_ident LIKE ?' % (atype, table), action)
    msg = cursor.fetchone()['text']

    phenny.action(msg)
    return
fun.rule = r'\?(.+)\s+(.*)'
fun.priority = 'low'



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