#!/usr/bin/env python
# -*- coding: latin-1 -*-

import socket, ssl

from tobcri.settings import settings
from .log import Log
from .event import Event


class IRC:
    def __init__(self, host, port, nick, identity, real_name, channel_pool,
                 use_ssl=False):
        self._host = bytes(host, settings.BOT_ENCODING)
        self._port = port
        self._nick = bytes(nick, settings.BOT_ENCODING)
        self._identity = bytes(identity, settings.BOT_ENCODING)
        self._real_name = bytes(real_name, settings.BOT_ENCODING)
        """
        SSL Support
        """
        if ssl:
            s = self._socket = socket.socket(socket.AF_INET,
                                            socket.SOCK_STREAM)
            self._socket = ssl.wrap_socket(s)
        else:
            self._socket = self._socket = socket.socket(socket.AF_INET,
                                                  socket.SOCK_STREAM)
        self._channel_pool = channel_pool
        self._is_connected = False
        self._log = Log()
        self._pong_initialized = False

    def connect(self):
        """
        Connection with the server
        """
        self._connect_server()
        self._send_nick()
        self._send_user()
        self._initialization()
        return True

    def _initialization(self):
        """
        Waiting for the first PING to join channel pool
        No other queries should be processed
        """

        while not self._pong_initialized:
            self._process_input(process=False)

        """
        Once PONG sent, join all channels
        """
        for channel in self._channel_pool:
            self._join_channel(channel)

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
        self._log.log(b"TEST", b"CHANNEL", cmd)
        self._socket.send(cmd + b"\r\n")

    def _send_privmsg(self, target, message):
        self._send_raw_command(b'PRIVMSG %s %s' % (target, message))


    def _process_input(self, process=True):
        """
        Process any input from the server
        """
        rb = self._socket.recv(1024)
        temp = rb.split(b"\n")
        temp.pop()

        for line in temp:
            line = line.rstrip().split()
            if (line[0] == b"PING"):
                self._send_pong(line[1])
            elif process:
                return self._parse_command(line)

    def _parse_command(self, cmd):
        """
        Parse any given input to create an event
        :return: Event
        """
        if len(cmd) >= 3:
            source = cmd[0][1:].split(b'!')[0]
            action = cmd[1]
            destination = cmd[2]
            arguments = cmd[3:]
            if action in settings.BOT_AVAILABLE_COMMANDS:
                return Event(event_type=action.lower(),
                              source=source,
                              target=destination,
                              arguments=arguments)
        return None

    def _close_connection(self):
        self._socket.close()