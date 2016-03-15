#!/usr/bin/env python

import tobcri
import threading


i = tobcri.Tobcri(
    host="irc.worldnet.net",
    port=7000,
    nick="Hackndo",
    identity="hackndo",
    real_name="Hackn'n'Do",
    channel_pool=[b"#hackndo",
                  b"#0x90r00t"
                  ],
    use_ssl=True,
    ns_password=True,
    admins=[
        b"Pixis",
    ]
)

j = tobcri.Tobcri(
    host="irc.freenode.net",
    port=6667,
    nick="Hackndo",
    identity="hackndo",
    real_name="Hackn'n'Do",
    channel_pool=[b"#hackndo"],
    use_ssl=False,
    admins=[
       b"Pixis",
    ]
)
i.connect()
# t1 = threading.Thread(target=i.connect, args=())
# t2 = threading.Thread(target=j.connect, args=())

# t1.start()
# t2.start()

