#!/usr/bin/env python
# -*- coding: utf8 -*-

# Copyright (C) 2015 Jesse Butcher
#
# nohands comes with ABSOLUTELY NO WARRANTY.  This is free software, and you
# are welcome to redistribute it under certain conditions.  See the MIT Licence
# for details.

"""
nohands.utils
    Miscellaneous utilities.
"""

from typing import TypeVar

from .box import *

AnyNum = TypeVar('AnyNum', int, float)
ListOrFalse = TypeVar('ListOrFalse', list, bool)


def percent_(value: AnyNum=0) -> str:
    value = 0 if not type(value) in AnyNum.__constraints__ else value
    return '{:.1f}%'.format(value * 100)


def dollars_(value: AnyNum=0) -> str:
    value = 0 if not type(value) in AnyNum.__constraints__ else value
    return '${:,.2f}'.format(value / 100)


def present_table(title: str, rows: list, totals: ListOrFalse=False) -> bool:
    """
    Pretty print a table of data.
        Adapted from http://stackoverflow.com/questions/5909873/python-pretty-printing-ascii-tables

    :param rows: A list of namedtuple objects
    :return: None
    """
    # Validate totals arg:
    totals = False if not type(totals) in ListOrFalse.__constraints__ else totals
    totals = False if totals is True else totals  # Eliminate 'True' as a valid 'totals' input, silently.

    # Validate every row list is same length:
    std_len = len(rows[0])
    all_rows = list(rows)
    if totals:
        all_rows.append(totals)
    for r in all_rows:
        if len(r) is not std_len:
            raise ValueError('Uneven row lengths in table. {} != {}'.format(len(r), std_len))

    if len(rows) > 0:
        for i, x in enumerate(rows):
            for j, y in enumerate(x):
                if y == 'True':
                    rows[i][j] = CM
                if y == 'False':
                    rows[i][j] = XM
                if y == 'None':
                    rows[i][j] = '-'

        headers = rows[0]

        # Get max column length
        lens = []
        for i in range(len(rows[0])):
            lens.append(len(max([x[i] for x in rows] + [headers[i]], key=lambda x: len(str(x)))))

        # Set minimum length
        minimum_length = 10
        for i, l in enumerate(lens):
            if l < minimum_length:
                lens[i] = minimum_length

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
        top = "{}{}{}".format(H1, H1, H1)
        top = top.join([H1 * n for n in lens])
        top = DR1 + H1 + top + H1 + DL1
        total_len = len(top)
        padding = total_len - 4
        title = '\033[1m' + title + '\033[0m'
        title = "{:^{padding}}".format(title, padding=padding + 8)  # <-- extra pad b/c of ansi esc chars
        title = V1 + S + title + S + V1
        bottom = "{}{}{}".format(H1, UH1, H1)
        bottom = bottom.join([H1 * n for n in lens])
        bottom = UR1 + H1 + bottom + H1 + UL1
        separator1 = "{}{}{}".format(H1, DH1, H1)
        separator1 = separator1.join([H1 * n for n in lens])
        separator1 = VR1 + H1 + separator1 + H1 + VL1
        separator2 = "{}{}{}".format(H1, HV1, H1)
        separator2 = separator2.join([H1 * n for n in lens])
        separator2 = VR1 + H1 + separator2 + H1 + VL1
        header = h_pattern % tuple(headers)
        header = V1 + S + header + S + V1
        line_l = V1 + S
        line_r = S + V1
        if totals:
            totals = pattern % tuple(totals)
            totals = V1 + S + totals + S + V1

        # Print Table:
        print(top)
        print(title)
        print(separator1)
        print(header)
        print(separator2)
        for line in rows[1:]:
            line = pattern % tuple(line)
            print(line_l + line + line_r)
        if totals:
            print(separator2)
            print(totals)

        print(bottom)

    return True

# vim:fileencoding=utf-8
