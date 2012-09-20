nick = 'MartinsMerodiiClon'
host = 'irc.ircplanet.eu'
channels = ['#nsw-anime-test']
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
# enable = []

# Directories to load user modules from
# e.g. /path/to/my/modules
extra = []

# Services to load: maps channel names to white or black lists
external = {
   '*': ['!'] # default whitelist, allow all
}

# What URL the stream is located
stream_url = "http://5.9.88.35:8000/nsw-anime"

# EOF

