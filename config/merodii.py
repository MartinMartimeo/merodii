#!/usr/bin/env python
# -*- coding: utf-8 -*-

nick = 'MartinsMerodiiClon'
host = 'irc.ircplanet.eu'
channels = ['#nsw-anime', '#nsw-anime-test']
owner = 'MartinMartimeo'

# password is the NickServ password, serverpass is the server password
# password = 'example'
# serverpass = 'serverpass'

# These are people who will be able to use admin.py's functions...
admins = [owner]
# But admin.py is disabled by default, as follows:
exclude = ['admin']

# If you want to enumerate a list of modules rather than disabling
# some, use "enable = ['example']", which takes precedent over exclude
# 
enable = ['startup', 'nsw']

# Directories to load user modules from
# e.g. /path/to/my/modules
extra = []

# Services to load: maps channel names to white or black lists
external = {
   '*': ['!'] # default whitelist, allow all
}

# We want the prefix to be !
prefix = "[!]"

# What URL the stream is located
stream_url = "http://5.9.88.35:8000/"
stream_mount = "nsw-anime"

# Messages
msg_fliegen = "CuCu und danke für den Fisch"
msg_kekse_nobody = "bewirft %s mit Keksen."
msg_kekse_anybody = "bewirft %s mit Keksen"
msg_kekse_phenny = "mampft alle Kekse selber auf."
msg_pluesch_nobody = "plüscht %s."
msg_pluesch_anybody = "plüscht %s."
msg_pluesch_phenny = "kuschelt mit Otochan."
msg_hilfe = "Befehle die ich kenne sind fliegen, kekse, pluesch, hilfe, stream, glaskugel, zitat"
# EOF

