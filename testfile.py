#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tobcri, threading


i = tobcri.Tobcri(host="irc.worldnet.net",
                port=7000,
                nick="Hackndo",
                identity="hackndo",
                real_name="Hackn'n'Do",
                channel_pool=[
                    b"#hackndo",
                    b"#0x90r00t",
                    b"#hackndo2"],
                use_ssl=True,
                admins=[
                    b"Pixis",]
                )

j = tobcri.Tobcri(host="irc.hackerzvoice.net",
               port=6667,
               nick="Hackndo",
               identity="hackndo",
               real_name="Hackn'n'Do",
               channel_pool=[
                   b"#0x90r00t",
                   b"#hackndo2"],
               use_ssl=False)

i.connect()
exit()
t1 = threading.Thread(target=i.connect, args=())
t2 = threading.Thread(target=j.connect, args=())

t1.start()
t2.start()