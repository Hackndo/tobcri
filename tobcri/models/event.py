#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Event:
    def __init__(self, event_type, source, target, arguments=None):
        self._event_type = event_type
        self._source = source
        self._target = target
        if arguments:
            self._arguments = arguments
        else:
            self._arguments = []

    def get_event_type(self):
        return self._event_type

    def get_source(self):
        return self._source

    def get_target(self):
        return self._target

    def get_arguments(self):
        return self._arguments