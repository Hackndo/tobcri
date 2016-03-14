#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from tobcri import IRC
from .settings import settings


def protect(f):
    def protectFunction(*args, **kwargs):
        admins, source = args[0]._admins, args[1]
        if source not in admins:
            return args[0]._unauthorized(*args[1:])
        return f(*args, **kwargs)
    return protectFunction

class Tobcri:
    cmds = {
        b'hello': 'say_hello',
        b'quit': 'quit',
        b'cmd': 'send_command',
    }

    def __init__(self, host, port, nick, identity, real_name, channel_pool,
                 use_ssl=False, admins=None):
        self._irc = IRC(host, port, nick, identity, real_name, channel_pool,
                        use_ssl)
        self._is_connected = False
        self._admins = admins


    def connect(self):
        self._is_connected = self._irc.connect()
        if self._is_connected:
            self._main_loop()



    def _main_loop(self):
        """
        Main loop awaiting for events
        """
        while self._is_connected:
            e = self._irc._process_input(process=True)
            if e is not None:
                self._process_event(e)
        self._irc._close_connection()

    def _process_event(self, e):
        m = (b"on_" + e._event_type).decode(settings.BOT_ENCODING)
        if hasattr(self, m):
            getattr(self, m)(e)

    def on_privmsg(self, e):
        source = e.get_source()
        target = e.get_target()
        arguments = e.get_arguments()

        if not Tobcri.is_channel(target):
            target = source

        self._process_command(source, target, arguments)


    def on_kick(self, e):
        target = e.get_target()
        self._irc._join_channel(target)

    def _process_command(self, source, target, arguments):
        print("Processing command")
        print(arguments)
        is_command = arguments and chr(arguments[0][1]) == '!'
        if is_command:
            cmd = arguments and arguments[0][2:]
            if cmd in self.cmds.keys():
                getattr(self, self.cmds[cmd])(source, target, arguments[1:])


    def say_hello(self, source, target, arguments=None):
        self._irc._send_privmsg(target=target,
                                message=b' '.join(arguments))

    @protect
    def send_command(self, source, target, arguments=None):
        self._irc._send_raw_command(b' '.join(arguments))


    @protect
    def quit(self, source, target, arguments=None):
        self._irc._send_privmsg(target=target, message=b'Adieu monde cruel')
        self._is_connected = False

    def _unauthorized(self, source, target, arguments=None):
        self._irc._send_privmsg(target=target,
                                message=b'Unauthorized')


    @staticmethod
    def is_channel(string):
        return string and string[0] in b"#&+!"