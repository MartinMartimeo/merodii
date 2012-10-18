#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
    Change Topic for #nsw-anime, when sendung changes
"""

__author__ = 'MartinMartimeo <martin@martimeo.de>'
__date__ = '18.10.12 - 20:18'

import threading
import time

from helper.nsw import read_nswinfo


def setup(phenny):
    phenny.last_starttime = None
    phenny.last_topic = None

    def monitor(phenny, config):
        time.sleep(5)
        while True:

            nsw_info = read_nswinfo(config)
            if nsw_info["sendung_start"] != phenny.last_starttime \
              or (nsw_info["next_sendung_title"] != phenny.last_topic and nsw_info["sendung_mod_name"] in config.myself):
                phenny.last_starttime = nsw_info["next_sendung_title"]
                phenny.last_topic = nsw_info["next_sendung_title"]

                topic = ""
                if nsw_info["sendung_mod_name"] in config.myself:
                    topic = config.topic_next
                else:
                    topic = config.topic_noarg
                topic %= nsw_info

                for chan in phenny.config.main_channel:
                    phenny.write(['CHANSERV'], "TOPIC %s %s" % (chan, topic))

            time.sleep(2.5)

    targs = (phenny, phenny.config)
    t = threading.Thread(target=monitor, args=targs)
    t.start()