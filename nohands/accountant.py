#!/usr/bin/env python
# -*- coding: utf8 -*-

# Copyright (C) 2015 Garden City Group, LLC
#
# ga_gcginc comes with ABSOLUTELY NO WARRANTY.  This is free software, and you
# are welcome to redistribute it under certain conditions.  See the MIT Licence
# for details.

"""
nohands.accountant
    This is the main worker.
"""


from nohands.db.models import *


class Accountant(object):
    def __init__(self):
        self.foobar = Term()

    def helloworld(self):
        print('Hello world')

# vim:fileencoding=utf-8
