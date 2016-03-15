#!/usr/bin/env python


class Event:
    def __init__(self, event_type, source, target, arguments=None):
        self.event_type = event_type
        self.source = source
        self.target = target
        if arguments:
            self.arguments = arguments
        else:
            self.arguments = []
