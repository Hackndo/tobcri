#!/usr/bin/env python

from tobcri.tobcri import Tobcri

if __name__ == "__main__":
    i = Tobcri(
        host="irc.worldnet.net",
        port=7000,
        nick="Hackndo",
        identity="hackndo",
        real_name="Hackn'n'Do",
        channel_pool=[
            b"#hackndo",
            b"#0x90r00t",
            b"#hackndo2"
        ],
        use_ssl=True,
        admins=[
            b"Pixis",
        ]
    )
    i.connect()
