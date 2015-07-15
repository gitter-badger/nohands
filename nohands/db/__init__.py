#!/usr/bin/env python
# -*- coding: utf8 -*-

# Copyright (C) 2015 Jesse Butcher
#
# nohands comes with ABSOLUTELY NO WARRANTY.  This is free software, and you
# are welcome to redistribute it under certain conditions.  See the MIT Licence
# for details.

"""
nohands.db:
    This module provides an interface to a database that contains mostly static configuration info.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from nohands.config import GlobalConfig


C = GlobalConfig()
session_factory = sessionmaker()

# ################################################################################

Session = scoped_session(session_factory)
Base = declarative_base()

from nohands.db.models import *

Engine = create_engine(C.db_cx
                       # , echo=True
                       )

Session.configure(bind=Engine)
Base.metadata.create_all(Engine)

# vim:fileencoding=utf-8
