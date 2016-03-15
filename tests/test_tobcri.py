#!/usr/bin/env python

import unittest
from tobcri import tobcri


class TobcriTestCase(unittest.TestCase):
    def setUp(self):
        self.tobcri = tobcri.Tobcri(
                host="irc.worldnet.net",
                port=7000,
                nick="Hackndo",
                identity="hackndo",
                real_name="Hackn'n'Do",
                channel_pool=[b"#hackndo"],
                use_ssl=True,
                admins=[
                    b"Pixis",
                ])

    def test_true(self):
        self.assertEqual("Hello World!", str(self.tobcri))


if __name__ == "__main__":
    unittest.main()
