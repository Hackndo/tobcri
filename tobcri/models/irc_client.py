#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tobcri import IRC
from tobcri.settings import settings


class IRC_Client:

    cmds = {b'hello': 'say_hello',
            b'quit': 'quit',
            }

    def __init__(self, host, port, nick, identity, real_name, channel_pool,
                 use_ssl=False):
        self._irc = IRC(host, port, nick, identity, real_name, channel_pool,
                        use_ssl)
        self._is_connected = False


    def connect(self):
        self._is_connected = self._irc.connect()


    def main_loop(self):
        """
        Main loop awaiting for events
        """
        while self._is_connected:
            e = self._irc._process_input(process=True)
            if e is not None:
                self._process_event(e)

    def _process_event(self, e):
        m = (b"on_" + e._event_type).decode(settings.BOT_ENCODING)
        if hasattr(self, m):
            getattr(self, m)(e)

    def on_privmsg(self, e):
        source = e.get_source()
        target = e.get_target()
        arguments = e.get_arguments()

        if not IRC_Client.is_channel(target):
            target = source

        self._process_command(target, arguments)


    def on_kick(self, e):
        target = e.get_target()
        self._irc._join_channel(target)

    def _process_command(self, target, arguments):
        print("Processing command")
        print(arguments)
        print(chr(arguments[0][1]))
        is_command = arguments and chr(arguments[0][1]) == '!'
        if is_command:
            cmd = arguments and arguments[0][2:]
            if cmd in self.cmds.keys():
                getattr(self, self.cmds[cmd])(target, arguments[1:])


    def say_hello(self, target, arguments):
        self._irc._send_privmsg(target=target,
                                message=b' '.join(arguments))


    def quit(self, target, arguments):
        self._irc._send_privmsg(target=target, message=b'Adieu monde cruel')
        self.disconnect()

    def disconnect(self):
        self._irc._close_connection()
        self._is_connected = False

    @staticmethod
    def is_channel(string):
        return string and string[0] in b"#&+!"