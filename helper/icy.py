"""
    Read an icecast stream
"""
__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '20.09.12 - 23:03'

import urllib2

def read_icyinfo(url):

    # Init urllib
    request = urllib2.Request(url)
    request.add_header('Icy-MetaData','1')
    opener = urllib2.build_opener()

    # Read data
    data = opener.open(request, None, 1)
    line = data.readline()
    info = data.info()
    data.close()

    # Parse
    rtn = {}
    for key, value in info.items():
        if key.startswith('icy-'):
            key = key[4:]
            rtn[key] = value

    return rtn




