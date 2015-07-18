#!/usr/bin/env python
# -*- coding: utf8 -*-

# Copyright (C) 2015 Jesse Butcher
#
# nohands comes with ABSOLUTELY NO WARRANTY.  This is free software, and you
# are welcome to redistribute it under certain conditions.  See the MIT Licence
# for details.

"""
nohands.db.models:
    database model definitions
"""

import inflect
from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String, Boolean

from nohands.config import GlobalConfig
from nohands.db import Base, Session


__all__ = ['TimePeriod', 'Earner', 'Expense', 'Ministry', 'CreditAccount']

C = GlobalConfig()

Inflector = inflect.engine()
p = Inflector.plural


class TimePeriod(Base):
    """ TimePeriod """
    __tablename__ = p('time_period')

    # column definitions
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    occurrence_per_year = Column(Integer)

    # Pretty print
    def __str__(self):
        return '<TimePeriod: "{}">'.format(self.name)

    def __repr__(self):
        return '<TimePeriod: "{}">'.format(self.name)


class Earner(Base):
    """ Earner """
    __tablename__ = p('earner')

    # column definitions
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    gross_annual = Column(Integer)
    time_period_id = Column(Integer, ForeignKey('time_periods.id'))
    net_paycheck = Column(Integer)

    time_period = relationship('TimePeriod', backref=p('earner'))

    @hybrid_property
    def percentage(self):
        my_ga = self.gross_annual or 0
        grand_sum = func.sum(Earner.gross_annual).label('grand_sum')
        qry = Session.query(grand_sum).one()
        sum_ga = qry.grand_sum
        return my_ga / sum_ga

    @hybrid_property
    def gross_paycheck(self):
        return self.gross_annual / self.time_period.occurrence_per_year

    @hybrid_property
    def waa_contrib(self):
        return '<NotImplemented>'

    @hybrid_property
    def net_annual(self):
        return self.time_period.occurrence_per_year * self.net_paycheck

    @hybrid_property
    def net_monthly(self):
        return self.net_annual / C.MPY

    # Pretty print
    def __str__(self):
        return '<Earner: "{}">'.format(self.name)

    def __repr__(self):
        return '<Earner: "{}">'.format(self.name)


class Expense(Base):
    """ Expense """
    __tablename__ = p('expense')

    # column definitions
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    url = Column(String)
    time_period_id = Column(Integer, ForeignKey('time_periods.id'))
    has_auto_pay = Column(Boolean)
    auto_pay_enabled = Column(Boolean)
    amount = Column(Integer)

    time_period = relationship('TimePeriod', backref=p('expense'))

    @hybrid_property
    def annual_amount(self):
        return self.amount * self.time_period.occurrence_per_year

    # TODO: Find a way to make this work.
    # # noinspection PyMethodParameters
    # @annual_amount.expression
    # def annual_amount(cls):
    #     return select([sum(cls.amount * TimePeriod.occurrence_per_year)]).\
    #         where(cls.time_period_id == TimePeriod.id).\
    #         label('annual_amount')

    @hybrid_property
    def monthly_amount(self):
        return self.annual_amount / C.MPY

    # Pretty print
    def __str__(self):
        return '<Expense: "{}">'.format(self.name)

    def __repr__(self):
        return '<Expense: "{}">'.format(self.name)


class Ministry(Base):
    """ Ministry """
    __tablename__ = p('ministry')

    # column definitions
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    time_period_id = Column(Integer, ForeignKey('time_periods.id'))
    amount = Column(Integer)

    time_period = relationship('TimePeriod', backref=p('ministry'))

    @hybrid_property
    def annual_amount(self):
        return self.amount * self.time_period.occurrence_per_year

    @hybrid_property
    def monthly_amount(self):
        return self.annual_amount / C.MPY

    # Pretty print
    def __str__(self):
        return '<Ministry: "{}">'.format(self.name)

    def __repr__(self):
        return '<Ministry: "{}">'.format(self.name)


class CreditAccount(Base):
    """ CreditAccount """
    __tablename__ = p('credit_account')

    # column definitions
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    url = Column(String)
    time_period_id = Column(Integer, ForeignKey('time_periods.id'))
    has_auto_pay = Column(Boolean)
    auto_pay_enabled = Column(Boolean)

    time_period = relationship('TimePeriod', backref=p('credit_account'))

    # Pretty print
    def __str__(self):
        return '<CreditAccount: "{}">'.format(self.name)

    def __repr__(self):
        return '<CreditAccount: "{}">'.format(self.name)


# vim:fileencoding=utf-8
