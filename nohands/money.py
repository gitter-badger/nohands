#!/usr/bin/env python
# -*- coding: utf8 -*-

# Copyright (C) 2015 Jesse Butcher
#
# nohands comes with ABSOLUTELY NO WARRANTY.  This is free software, and you
# are welcome to redistribute it under certain conditions.  See the MIT Licence
# for details.

"""
nohands.money
    A dollar amount that can be expressed in different periods of time.
"""

from nohands.db import Session
from nohands.db.models import *
from nohands.utils import dollars_


class Money(object):
    def __init__(self, value: int=0):

        # The canonical value is annual
        self.value = int(value)
        self.time_periods = Session.query(TimePeriod).all()

    def __getattr__(self, attr: str) -> int:
        attr = attr.replace('_', '-')
        period = Session.query(TimePeriod).filter(TimePeriod.name == attr.title()).one()
        rpt_value = self.value / period.occurrence_per_year
        return rpt_value

    def __str__(self):
        return dollars_(self.value)

    def __bytes__(self):
        return dollars_(self.value)

    def __repr__(self):
        annual = dollars_(self.value)
        monthly = dollars_(self.value / 12)
        return '<Money: value={} annual={} (monthly={})>'.format(self.value, annual, monthly)

    # Implement common integer operations. For uncommon, just use int().
    def __int__(self):
        return self.value

    def __add__(self, other):
        return self.value + other

    def __sub__(self, other):
        return self.value - other

    def __mul__(self, other):
        return self.value * other

    def __truediv__(self, other):
        return self.value / other

    def __radd__(self, other):
        return other + self.value

    def __rsub__(self, other):
        return other - self.value

    def __rmul__(self, other):
        return other * self.value

    def __rtruediv__(self, other):
        return other / self.value


# vim:fileencoding=utf-8
