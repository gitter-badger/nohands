#!/usr/bin/env python
# -*- coding: utf8 -*-

# Copyright (C) 2015 Garden City Group, LLC
#
# ga_gcginc comes with ABSOLUTELY NO WARRANTY.  This is free software, and you
# are welcome to redistribute it under certain conditions.  See the MIT Licence
# for details.

"""
nohands.utils
    Miscellaneous utilities.
"""

from typing import TypeVar

from nohands.box import *

AnyNum = TypeVar('AnyNum', int, float)


def percent_(value: AnyNum=0) -> str:
    value = 0 if not type(value) in AnyNum.__constraints__ else value
    return '{:.1f}%'.format(value * 100)


def dollars_(value: AnyNum=0) -> str:
    value = 0 if not type(value) in AnyNum.__constraints__ else value
    return '${:,.2f}'.format(value / 100)


def present_table(rows):
    """
    Pretty print a table of data.
        Adapted from http://stackoverflow.com/questions/5909873/python-pretty-printing-ascii-tables

    :param rows: A list of namedtuple objects
    :return: None
    """

    if len(rows) > 1:
        for i, x in enumerate(rows):
            for j, y in enumerate(x):
                if y == 'True':
                    rows[i][j] = CM
                if y == 'False':
                    rows[i][j] = u'\u2717'
                if y == 'None':
                    rows[i][j] = '-'

        headers = rows[0]
        lens = []
        for i in range(len(rows[0])):
            lens.append(len(max([x[i] for x in rows] + [headers[i]], key=lambda x: len(str(x)))))

        formats = []
        h_formats = []

        for i in range(len(rows[0])):
            if isinstance(rows[0][i], int):
                formats.append("%%%dd" % lens[i])
            else:
                formats.append("%%-%ds" % lens[i])
            h_formats.append("%%-%ds" % lens[i])

        # Formatting:
        pattern = "{}{}{}".format(S, V1, S)
        pattern = pattern.join(formats)
        h_pattern = pattern
        top = "{}{}{}".format(H1, DH1, H1)
        top = top.join([H1 * n for n in lens])
        top = DR1 + H1 + top + H1 + DL1
        bottom = "{}{}{}".format(H1, UH1, H1)
        bottom = bottom.join([H1 * n for n in lens])
        bottom = UR1 + H1 + bottom + H1 + UL1
        separator = "{}{}{}".format(H1, HV1, H1)
        separator = separator.join([H1 * n for n in lens])
        separator = VR1 + H1 + separator + H1 + VL1
        header = h_pattern % tuple(headers)
        header = V1 + S + header + S + V1
        line_l = V1 + S
        line_r = S + V1

        # Print Table:
        print(top)
        print(header)
        print(separator)
        for line in rows[1:]:
            line = pattern % tuple(line)
            print(line_l + line + line_r)
        print(bottom)
        print()

    elif len(rows) == 1:
        # row = rows[0]
        # h_width = len(max(row._fields,key=lambda x: len(x)))
        # for i in range(len(row)):
        #     print("%*s = %s" % (h_width, row._fields[i], row[i]))
        pass

# vim:fileencoding=utf-8
