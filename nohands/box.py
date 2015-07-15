#!/usr/bin/env python
# -*- coding: utf8 -*-

# Copyright (C) 2015 Jesse Butcher
#
# nohands comes with ABSOLUTELY NO WARRANTY.  This is free software, and you
# are welcome to redistribute it under certain conditions.  See the MIT Licence
# for details.

"""
nohands.box
    Box drawing characters.
"""


CM = u'\u2713'  # Check mark

# Unicode characters:
BB = u'\u2610'  # Ballot box
SB = u'\u2588'  # Solid block
E = u''         # Empty
S = u' '        # Plain space
D = u'\u2014'   # Em dash
WD = u'\u3030'  # Wavy dash
VD = u'\uFE31'  # Vertical em dash

# BOX DRAWINGS LIGHT
H1 = u'\u2500'  # [─] HORIZONTAL
V1 = u'\u2502'  # [│] VERTICAL
HV1 = u'\u253C'  # [┼] VERTICAL AND HORIZONTAL
DR1 = u'\u250C'  # [┌] DOWN AND RIGHT
DL1 = u'\u2510'  # [┐] DOWN AND LEFT
UR1 = u'\u2514'  # [└] UP AND RIGHT
UL1 = u'\u2518'  # [┘] UP AND LEFT
VR1 = u'\u251C'  # [├] VERTICAL AND RIGHT
VL1 = u'\u2524'  # [┤] VERTICAL AND LEFT
DH1 = u'\u252C'  # [┬] DOWN AND HORIZONTAL
UH1 = u'\u2534'  # [┴] UP AND HORIZONTAL

# BOX DRAWINGS DOUBLE
H2 = u'\u2550'  # [═] HORIZONTAL
V2 = u'\u2551'  # [║] VERTICAL
HV2 = u'\u256C'  # [╬] VERTICAL AND HORIZONTAL
DR2 = u'\u2554'  # [╔] DOWN AND RIGHT
DL2 = u'\u2557'  # [╗] DOWN AND LEFT
UR2 = u'\u255A'  # [╚] UP AND RIGHT
UL2 = u'\u255D'  # [╝] UP AND LEFT
VR2 = u'\u2560'  # [╠] VERTICAL AND RIGHT
VL2 = u'\u2563'  # [╣] VERTICAL AND LEFT
DH2 = u'\u2566'  # [╦] DOWN AND HORIZONTAL
UH2 = u'\u2569'  # [╩] UP AND HORIZONTAL

# MIXED
VRM = u'\u255F'  # [╟] XX
VLM = u'\u2562'  # [╢] XX
DHM = u'\u2564'  # [╤] XX
UHM = u'\u2567'  # [╧] XX
HVA = u'\u256A'  # [╪] VERTICAL SINGLE AND HORIZONTAL DOUBLE
HVB = u'\u256B'  # [╫] VERTICAL DOUBLE AND HORIZONTAL SINGLE

# vim:fileencoding=utf-8
