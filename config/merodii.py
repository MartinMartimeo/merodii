#!/usr/bin/env python
# -*- coding: utf-8 -*-

nick = 'Otochan'
host = 'irc.ircplanet.eu'
owner = 'MartinMartimeo'
name = 'Merodiis Otochan - Phennybot for #nsw-anime by MartinMartimeo - https://github.com/MartinMartimeo/merodii'

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
enable = ['startup', 'nsw', 'topic', 'fun']

# Directories to load user modules from
# e.g. /path/to/my/modules
extra = []

# Services to load: maps channel names to white or black lists
external = {
   '*': ['!'] # default whitelist, allow all
}

# Channel to be joined
# channels = ['#nsw-anime', '#nsw-anime-test', '#NSW-Intern']
channels = ['#nsw-otochan']

# Some configurations
#staff_channel = ['#NSW-Intern']
staff_channel = ['#nsw-otochan']
#main_channel = ['#nsw-anime']
main_channel = ['#nsw-otochan']

# Fun actions
fun_uri = {'host': 'localhost', 'user': 'merodii', 'passwd': 'passwd', 'db': 'irc'}
fun_table = 'irc_actions'

# The Topics
topic_noarg = "%(stream_info)s"
topic_warg = "%(nick)s - %(arg)s"
topic_playlist = "Aktuell sendet DJ Merodii mit der Anime Playlist"
topic_next = "Aktuell sendet DJ Merodii mit der Anime Playlist - Nächste Sendung: %(next_sendung_title)s "

# We want the prefix to be !
prefix = "[!]"

# What URL the stream is located
stream_url = "http://5.9.88.35:8000/"
stream_mount = "nsw-anime"
stream_song = "http://alt.nsw-anime.de/modules/mod_shoutcast/info.php?currentSong=1"
sendung_url = "http://alt.nsw-anime.de/pic.php?request=text"
modding_url = "http://alt.nsw-anime.de/pic.php?request=pic"

# Consider myself
myself = ["Merodii", "merodii", "Playlist_top"]

# Messages
msg_fliegen = "CuCu und danke für den Fisch"
msg_hilfe = "Befehle die ich kenne sind fliegen, kekse, pluesch, hilfe, stream, sendung, next, zitat"

# Authserv
authserv = True
authserv_account = "Merodii"
authserv_password = "HackMe!"

umode = "x"

# EOF

