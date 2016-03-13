#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time

class Log:

    def __init__(self):
        self.author = ""
        self.channel = ""
        self.message = ""
        self.date = ""

    def log(self, author, channel, message):
        line = b'[%s] [%s] %s : %s\n' % (b"now",
                                         channel,
                                         author,
                                         message)
        sys.stdout.write(line.decode('latin-1'))