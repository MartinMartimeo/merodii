"""
    Open Features für #nsw-anime
"""
__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '20.09.12 - 23:15'

from helper.icy import cached_icyinfo

def stream(phenny, input):
    """
    zeigt das aktuelle Lied auf dem Stream
    """

    info = cached_icyinfo(input.stream_url, input.stream_mount)
    phenny.say("Aktuell sendet: %s" % info["description"])
    return
stream.commands = ['stream']
stream.priority = 'low'


if __name__ == '__main__':
    print __doc__.strip()
