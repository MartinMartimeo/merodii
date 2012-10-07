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
enable = ['startup', 'nsw']

# Directories to load user modules from
# e.g. /path/to/my/modules
extra = []

# Services to load: maps channel names to white or black lists
external = {
   '*': ['!'] # default whitelist, allow all
}

# Channel to be joined
channels = ['#nsw-anime', '#nsw-anime-test', '#nsw-intern']

# Some configurations
staff_channel = ['#nsw-intern']
main_channel = ['#nsw-anime']

# The Topics
topic_noarg = "%(nick)s - %(sendung_title)s"
topic_warg = "%(nick)s - %(arg)s"
topic_playlist = "DJ Merodii mit der Anime Playlist"

# We want the prefix to be !
prefix = "[!]"

# What URL the stream is located
stream_url = "http://5.9.88.35:8000/"
stream_mount = "nsw-anime"
stream_song = "http://www.nsw-anime.de/modules/mod_shoutcast/info.php?currentSong=1"
sendung_url = "http://www.nsw-anime.de/pic.php?request=text"

# Consider myself
myself = ["Merodii", "merodii"]

# Messages
msg_fliegen = "CuCu und danke für den Fisch"
msg_kekse_nobody = "bewirft %s mit Keksen."
msg_kekse_anybody = "bewirft %s mit Keksen"
msg_kekse_phenny = "mampft alle Kekse selber auf."
msg_kekse_myself = "hüpft zu Merodii und gibt ihr einen Keks."
msg_pluesch_nobody = "plüscht %s."
msg_pluesch_anybody = "plüscht %s."
msg_pluesch_phenny = "findet keinen zum plüschen und kuschelt mit Merodii."
msg_pluesch_myself = "hüpft zu Merodii und kuschelt sie."
msg_hilfe = "Befehle die ich kenne sind fliegen, kekse, pluesch, hilfe, s sendung,tream, zitat"

# Authserv
authserv = True
authserv_account = "Merodii"
authserv_password = "HackMe!"

umode = "x"

# EOF

