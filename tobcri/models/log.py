#!/usr/bin/env python

import sys


class Log:

    def __init__(self):
        self.author = ""
        self.channel = ""
        self.message = ""
        self.date = ""

    def log(self, server, author, channel, message):
        line = b'[%s] [%s] %s : %s\n' % (server,
                                         channel,
                                         author,
                                         message)
        sys.stdout.write(line.decode())
