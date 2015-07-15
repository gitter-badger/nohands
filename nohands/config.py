#!/usr/bin/env python
# -*- coding: utf8 -*-

# Copyright (C) 2015 Garden City Group, LLC
#
# webstats comes with ABSOLUTELY NO WARRANTY.  This is free software, and you
# are welcome to redistribute it under certain conditions.  See the MIT Licence
# for details.

"""
nohands.config:
    This tool pulls in config options and creates globals.
"""

import os
import re
import configparser
from xdg import BaseDirectory
# from nohands.options import CLIOptions as O


def dir_check(directory):
    """ Check if directory exists, if not then create it. """
    # http://stackoverflow.com/questions/273192/...
    #   python-best-way-to-create-directory-if-it-doesnt-exist-for-file-write

    # print("Checking if \"{}\" exists... ".format(directory), end='')
    try:
        os.makedirs(directory)
        # print("FALSE. Created directory.")
        print("Directory did not exist. Created \"{}\"".format(directory))
    except OSError:
        if not os.path.isdir(directory):
            raise
        # print("TRUE. Directory exists.")


class GlobalConfig:
    """ The all-knowing, omniscient 'G'. """

    def __init__(self):
        """ Constructor """

        self.project_name = 'nohands'

        xdg_config_home = os.path.abspath(BaseDirectory.xdg_config_home)
        xdg_data_home = os.path.abspath(BaseDirectory.xdg_data_home)
        self.config_home = os.path.join(xdg_config_home, self.project_name)
        self.data_home = os.path.join(xdg_data_home, self.project_name)
        dir_check(self.config_home)
        dir_check(self.data_home)

        self.config_file = os.path.join(self.config_home, "config.ini")

        self.config = configparser.ConfigParser()
        # And if settings.cfg doesn't exist, init a blank one.
        if not os.path.exists(self.config_file):
            print("Config file missing. Initializing new, blank one.")
            with open(self.config_file, "w") as fp:
                fp.write("[Settings]\n" +
                         "db_cx = postgresql+psycopg2://nohands:***@localhost/nohands\n" +
                         "waa_contrib = 1.2\n" +
                         "savings_pct = 14%\n" +
                         "\n"
                         )

        self.config.read(self.config_file)

        # -------------------
        # CONFIG FILE:
        # -------------------
        # [Settings]
        self.db_cx = self.config.get('Settings', 'db_cx')
        self.waa_contrib = self.config.getfloat('Settings', 'waa_contrib')
        self.savings_pct = self.config.getint('Settings', 'savings_pct') / 100

        # -------------------
        # CONSTANTS:
        # -------------------
        self.MPY = 12  # Months per year
        self.ACCTS = {  # TODO: Move to config.ini or db.
            'WAA': '5666',
            'FFG': '1311',
            'Savings (General)': '4640',
            'Savings (Rainy)': '2384'
        }

        # -------------------
        # Regex objects:
        # -------------------
        # ASCII printable characters
        ascii_chars = ''.join(map(chr, range(32, 127)))
        self.ascii_char_re = re.compile('[{}]'.format(re.escape(ascii_chars)))


# vim:fileencoding=utf-8
