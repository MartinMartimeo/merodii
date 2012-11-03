#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
    Change Topic for #nsw-anime, when sendung changes
"""

__author__ = 'MartinMartimeo <martin@martimeo.de>'
__date__ = '18.10.12 - 20:18'

import sys
import threading
import time

from helper.nsw import read_nswinfo


def setup(phenny):
    phenny.last_streaminfo = None
    phenny.last_nextwhen = None
    phenny.last_nextname = None
    phenny.last_modname = None

    def monitor(phenny, config):
        time.sleep(25)
        while True:

            nsw_info = read_nswinfo(config)
            if nsw_info["sendung_mod_name"] != phenny.last_modname \
              or nsw_info["stream_info"] != phenny.last_streaminfo \
              or ((nsw_info["next_sendung_title"] != phenny.last_nextname or nsw_info["next_sendung_when"] != phenny.last_nextwhen) and nsw_info["sendung_mod_name"] in config.myself):
                phenny.last_modname = nsw_info["sendung_mod_name"]
                phenny.last_streaminfo = nsw_info["stream_info"]
                phenny.last_nextwhen = nsw_info["next_sendung_when"]
                phenny.last_nextname = nsw_info["next_sendung_title"]

                topic = ""
                if nsw_info["sendung_mod_name"] in config.myself:
                    topic = config.topic_next
                else:
                    topic = config.topic_noarg
                topic %= nsw_info

                for chan in phenny.config.main_channel:
                    phenny.write(['CHANSERV'], "TOPIC %s %s" % (chan, topic))

            time.sleep(20)

    targs = (phenny, phenny.config)
    t = threading.Thread(target=monitor, args=targs)
    t.start()