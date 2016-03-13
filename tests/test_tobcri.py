#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from tobcri import tobcri

class TobcriTestCase(unittest.TestCase):

    def setUp(self):
        self.tobcri = tobcri.Tobcri()

    def test_true(self):
        self.assertEqual('Hello World!', str(self.tobcri))

if __name__ == '__main__':
    unittest.main()