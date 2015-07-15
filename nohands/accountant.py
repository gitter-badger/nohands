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
from sqlalchemy import func

from nohands.config import GlobalConfig
from nohands.db import Session
from nohands.db.models import *
from nohands.utils import percent_, dollars_, present_table


C = GlobalConfig()


class Accountant(object):
    def __init__(self):
        # Load in data
        self.credit_accounts = Session.query(CreditAccount).all()
        self.earners = Session.query(Earner).all()
        self.earner_count = Session.query(
            func.count(Earner.id).label('earner_count'))\
            .filter(Earner.gross_annual > 0).one().earner_count
        self.expenses = Session.query(Expense).all()
        self.ministries = Session.query(Ministry).all()
        self.pay_periods = Session.query(PayPeriod).all()
        self.terms = Session.query(Term).all()

        # TODO: It should be possible to use a hybrid expression to achieve these.
        #   but I haven't been able to figure it out yet.
        self.total_monthly_expenses = 0
        for e in self.expenses:
            self.total_monthly_expenses += e.monthly_amount

        self.total_annual_expenses = 0
        for e in self.expenses:
            self.total_annual_expenses += e.annual_amount

    def report_earners(self):
        rows = [
            ['Name', 'Gross Annual', 'Percentage', 'Checks/Year', 'Gross Paycheck',
             'WAA Contrib', 'Net Paycheck', 'Net Income']
        ]
        for e in self.earners:
            values = [
                e.name,
                dollars_(e.gross_annual),
                percent_(e.percentage),
                str(e.pay_period.checks_year),
                dollars_(e.gross_paycheck),
                str(e.waa_contrib),
                dollars_(e.net_paycheck),
                dollars_(e.net_annual),
            ]
            rows.append(values)
        present_table(rows)

    def report_expenses(self):
        rows = [
            ['Name', 'URL', 'Term', 'Auto-Payable', 'Auto-Payed', 'Monthly', 'Annual']
        ]
        for e in self.expenses:
            values = [
                e.name,
                str(e.url),
                str(e.term.name),
                str(e.has_auto_pay),
                str(e.auto_pay_enabled),
                dollars_(e.monthly_amount),
                dollars_(e.annual_amount),
            ]
            rows.append(values)
        present_table(rows)
        print('Total Annual Expenses:  {}'.format(dollars_(self.total_annual_expenses)))
        print('Total Monthly Expenses:  {}'.format(dollars_(self.total_monthly_expenses)))

# vim:fileencoding=utf-8
