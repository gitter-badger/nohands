#!/usr/bin/env python
# -*- coding: utf8 -*-

# Copyright (C) 2015 Garden City Group, LLC
#
# ga_gcginc comes with ABSOLUTELY NO WARRANTY.  This is free software, and you
# are welcome to redistribute it under certain conditions.  See the MIT Licence
# for details.

"""
nohands.db.models:
    database model definitions
"""

import inflect
from sqlalchemy import Column, ForeignKey, func, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String, Boolean

from nohands.config import GlobalConfig
from nohands.db import Base, Session


__all__ = ['PayPeriod', 'Term', 'Earner', 'Expense', 'Ministry', 'CreditAccount']

C = GlobalConfig()

Inflector = inflect.engine()
p = Inflector.plural


class PayPeriod(Base):
    """ PayPeriod """
    __tablename__ = p('pay_period')

    # column definitions
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    checks_year = Column(Integer)

    # Pretty print
    def __str__(self):
        return '<PayPeriod: "{}">'.format(self.name)

    def __repr__(self):
        return '<PayPeriod: "{}">'.format(self.name)


class Term(Base):
    """ Term """
    __tablename__ = p('term')

    # column definitions
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    occurrence_year = Column(Integer)

    # Pretty print
    def __str__(self):
        return '<Term: "{}">'.format(self.name)

    def __repr__(self):
        return '<Term: "{}">'.format(self.name)


class Earner(Base):
    """ Earner """
    __tablename__ = p('earner')

    # column definitions
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    gross_annual = Column(Integer)
    pay_period_id = Column(Integer, ForeignKey('pay_periods.id'))
    net_paycheck = Column(Integer)

    pay_period = relationship('PayPeriod', backref=p('earner'))

    @hybrid_property
    def percentage(self):
        my_ga = self.gross_annual or 0
        grand_sum = func.sum(Earner.gross_annual).label('grand_sum')
        qry = Session.query(grand_sum).one()
        sum_ga = qry.grand_sum
        return my_ga / sum_ga

    @hybrid_property
    def gross_paycheck(self):
        return self.gross_annual / self.pay_period.checks_year

    @hybrid_property
    def waa_contrib(self):
        return '<NotImplemented>'

    @hybrid_property
    def net_annual(self):
        return self.pay_period.checks_year * self.net_paycheck

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
    term_id = Column(Integer, ForeignKey('terms.id'))
    has_auto_pay = Column(Boolean)
    auto_pay_enabled = Column(Boolean)
    amount = Column(Integer)

    term = relationship('Term', backref=p('expense'))

    @hybrid_property
    def annual_amount(self):
        return self.amount * self.term.occurrence_year

    # # noinspection PyMethodParameters
    # @annual_amount.expression
    # def annual_amount(cls):
    #     return select([sum(cls.amount * Term.occurrence_year)]).\
    #         where(cls.term_id == Term.id).\
    #         label('annual_amount')
    #
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
    term_id = Column(Integer, ForeignKey('terms.id'))
    amount = Column(Integer)

    term = relationship('Term', backref=p('ministry'))

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
    term_id = Column(Integer, ForeignKey('terms.id'))
    has_auto_pay = Column(Boolean)
    auto_pay_enabled = Column(Boolean)

    term = relationship('Term', backref=p('credit_account'))

    # Pretty print
    def __str__(self):
        return '<CreditAccount: "{}">'.format(self.name)

    def __repr__(self):
        return '<CreditAccount: "{}">'.format(self.name)


# vim:fileencoding=utf-8
