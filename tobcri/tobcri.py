#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

class Tobcri():
    def __init__(self):
        self.foo = "Hello World!"


    def __str__(self):
        return self.foo


    def run(self):
        print("I'm running")