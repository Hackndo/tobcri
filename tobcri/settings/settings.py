#!/usr/bin/env python

from tobcri.settings.local_settings import PASSWORD

DEBUG = True
BOT_PASSWORD = PASSWORD
BOT_CHANNELS = []
BOT_ENCODING = "utf-8"

SERVER_VALID_RETURN_CODES = (
    b"001",
    b"433"
)
SERVER_AVAILABLE_COMMANDS = (
    b"ADMIN",
    b"AWAY",
    b"CNOTICE",
    b"CPRIVMSG",
    b"CONNECT",
    b"DIE",
    b"ENCAP",
    b"ERROR",
    b"HELP",
    b"INFORMATION",
    b"INVITE",
    b"ISON",
    b"JOIN",
    b"KICK",
    b"KILL",
    b"KNOCK",
    b"LINKS",
    b"LIST",
    b"LUSERS",
    b"MODE",
    b"MOTD",
    b"NAMES",
    b"NAMESX",
    b"NICK",
    b"NOTICE",
    b"OPER",
    b"PART",
    b"PASS",
    b"PING",
    b"PONG",
    b"PRIVMSG",
    b"QUIT",
    b"REHASH",
    b"RESTART",
    b"RULES",
    b"SERVER",
    b"SERVICE",
    b"SERVLIST",
    b"SQUERY",
    b"SQUIT",
    b"SETNAME",
    b"SILENCE",
    b"STATS",
    b"SUMMON",
    b"TIME",
    b"TOPIC",
    b"TRACE",
    b"UHNAMES",
    b"USER",
    b"USERHOST",
    b"USERIP",
    b"USERS",
    b"VERSION",
    b"WALLOPS",
    b"WATCH",
    b"WHO",
    b"WHOIS",
    b"WHOWAS")

MESSAGE_HANDLERS = ()

FILE_LOGGER_FILENAME = "stdout"


MAX_BUFFER_SIZE = 16*1024  # 16kB
BUFFER_READ = 1*1024  # 16kB
