#!/usr/bin/env python

from tobcri import IRC


def protect(f):
    def protectFunction(*args, **kwargs):
        admins, source = args[0]._admins, args[1]
        if source not in admins:
            return args[0]._unauthorized(*args[1:])
        return f(*args, **kwargs)

    return protectFunction


class Tobcri:
    cmds = {
        b"hello": "say_hello",
        b"quit": "quit",
        b"cmd": "send_command",
    }

    def __init__(self, host, port, nick, identity, real_name, channel_pool,
                 use_ssl=False, ns_password=False, admins=None):
        self._irc = IRC(host, port, nick, identity, real_name, channel_pool,
                        use_ssl, ns_password)
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
            e = self._irc._process_input()
            if e is not None:
                self._process_event(e)
        self._irc._close_connection()

    def _process_event(self, e):
        if e.event_type == b"PING".lower():
            self._irc._send_pong(e.arguments[0])
        elif e.event_type == b"001":  # Success
            for channel in self._irc._channel_pool:
                self._irc._join_channel(channel)
        elif e.event_type == b"433":  # Success
            self._irc._nick = b"".join((self._irc._nick, b"_"))
            self._irc._send_nick()
        else:
            m = b"".join((b"on_", e.event_type)).decode()
            if hasattr(self, m):
                getattr(self, m)(e)

    def on_privmsg(self, e):
        source = e.source
        target = e.target
        arguments = e.arguments

        if not Tobcri.is_channel(target):
            target = source

        self._process_command(source, target, arguments)

    def on_kick(self, e):
        target = e.get_target()
        self._irc._join_channel(target)

    def _process_command(self, source, target, arguments):
        print("Processing command")
        print(arguments)
        is_command = arguments and arguments[0].startswith(b":!")
        if is_command:
            cmd = arguments and arguments[0][2:]
            if cmd in self.cmds.keys():
                getattr(self, self.cmds[cmd])(source, target, arguments[1:])

    def say_hello(self, source, target, arguments=None):
        self._irc._send_privmsg(target=target,
                                message=b" ".join(arguments))

    @protect
    def send_command(self, source, target, arguments=None):
        self._irc._send_raw_command(b" ".join(arguments))

    @protect
    def quit(self, source, target, arguments=None):
        self._irc._send_privmsg(target=target, message=b"Adieu monde cruel")
        self._is_connected = False

    def _unauthorized(self, source, target, arguments=None):
        self._irc._send_privmsg(target=target,
                                message=b"Unauthorized")

    @staticmethod
    def is_channel(string):
        return string and string[0] in b"#&+!"
