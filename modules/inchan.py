"""
    Remembers the people in channel
"""
__author__ = 'MartinMartimeo <martin@martimeo.de>'
__date__ = '21.09.12 - 20:04'



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