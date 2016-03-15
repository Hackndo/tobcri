#!/usr/bin/env python

import socket
import ssl
from tobcri.settings import settings
from tobcri.models.log import Log
from tobcri.models.event import Event


class IRC:
    def __init__(self, host, port, nick, identity, real_name, channel_pool,
                 use_ssl=False, ns_password=False):
        self._host = bytes(host, settings.BOT_ENCODING)
        self._port = port
        self._nick = bytes(nick, settings.BOT_ENCODING)
        self._identity = bytes(identity, settings.BOT_ENCODING)
        self._real_name = bytes(real_name, settings.BOT_ENCODING)
        """
        SSL Support
        """
        self._init_socket(use_ssl=use_ssl)

        self._channel_pool = channel_pool
        self._is_connected = False
        self._log = Log()
        self._pong_initialized = False
        self._ns_password = ns_password

    def connect(self):
        """
        Connection with the server
        """
        self._connect_server()
        self._send_nick()
        if self._ns_password:
            self._send_password()
        self._send_user()
        return True

    def _init_socket(self, use_ssl=False):
        if use_ssl:
            s = self._socket = socket.socket(socket.AF_INET,
                                             socket.SOCK_STREAM)
            self._socket = ssl.wrap_socket(s)
        else:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def _process_input(self, process=True):
        """
        Process any input from the server
        """
        read_buffer = self._socket.recv(settings.BUFFER_READ)

        temp = read_buffer.split(b"\n")
        temp.pop()

        for line in temp:
            line = line.rstrip().split()
            print(line)
            return self._parse_command(line)

        return None

    def _parse_command(self, cmd):
        """
        Parse any given input to create an event
        :return: Event
        """
        if cmd[0] == b"PING":
            return Event(event_type=cmd[0].lower(),
                         source=b"",
                         target=b"",
                         arguments=[cmd[1]])
        elif len(cmd) > 2 and chr(cmd[0][0]) == ":":
            source = cmd[0][1:].split(b"!")[0]

            action = cmd[1]
            if cmd[1].decode().isnumeric():
                destination = []
                arguments = cmd[2:]
            else:
                destination = cmd[2]
                arguments = cmd[3:]

            if (action in settings.SERVER_AVAILABLE_COMMANDS or
                    action in settings.SERVER_VALID_RETURN_CODES):
                # If action is valid
                return Event(event_type=action.lower(),
                             source=source,
                             target=destination,
                             arguments=arguments)
        return None

    def _connect_server(self):
        """
        Connect the socket
        """
        self._socket.connect((self._host, self._port))

    def _send_nick(self):
        """
        Send NICK to server
        """
        self._send_raw_command(b"NICK %s" % self._nick)

    def _send_password(self):
        """
        Send NICK to server
        """
        self._send_privmsg(b"nickserv", b"IDENTIFY %s" % settings.BOT_PASSWORD)

    def _send_user(self):
        """
        Send USER to server
        """
        self._send_raw_command(b"USER %s %s junk :%s" % (self._identity,
                                                         self._host,
                                                         self._real_name))

    def _send_pong(self, token):
        """
        Send PONG to server with given token
        """
        self._send_raw_command(b"PONG %s" % token)
        self._pong_initialized = True

    def _join_channel(self, channel):
        """
        Send a JOIN request to join a channel on current server
        """
        self._send_raw_command(b"JOIN %s" % channel)

    def _send_raw_command(self, cmd):
        """
        Send raw bytes data to the server
        """
        self._log.log(self._host, b"TEST", b"CHANNEL", cmd)
        self._socket.send(cmd + b"\r\n")

    def _send_privmsg(self, target, message):
        self._send_raw_command(b'PRIVMSG %s %s' % (target, message))

    def _close_connection(self):
        self._socket.close()
