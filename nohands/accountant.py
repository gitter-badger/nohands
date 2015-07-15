#!/usr/bin/env python
# -*- coding: utf8 -*-

# Copyright (C) 2015 Jesse Butcher
#
# nohands comes with ABSOLUTELY NO WARRANTY.  This is free software, and you
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

        self.total_gross_annual = 0
        for e in self.earners:
            self.total_gross_annual += e.gross_annual

        self.total_ministry_annual = 0
        for e in self.ministries:
            self.total_ministry_annual += e.annual_amount

        self.total_ministry_monthly = 0
        for e in self.ministries:
            self.total_ministry_monthly += e.monthly_amount

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
        present_table('Income', rows)

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
        present_table('Expenses', rows)
        print('Total Annual Expenses:  {}'.format(dollars_(self.total_annual_expenses)))
        print('Total Monthly Expenses:  {}'.format(dollars_(self.total_monthly_expenses)))

    def report_giving(self):
        headers = ['Name', 'Percentage', 'Term', 'Annual', 'Monthly']
        aux_rows = [
            headers,
        ]
        pct_tally = 0

        # Auxiliary Ministries:
        for m in self.ministries:
            percentage = m.annual_amount / self.total_gross_annual
            pct_tally += percentage
            values = [
                m.name,
                percent_(percentage),
                str(m.term.name),
                dollars_(m.annual_amount),
                dollars_(m.monthly_amount),
            ]
            aux_rows.append(values)
        aux_totals = [
            'Subtotals',
            percent_(pct_tally),
            '',
            dollars_(self.total_ministry_annual),
            dollars_(self.total_ministry_monthly),
        ]
        present_table('Auxiliary Ministries', aux_rows, aux_totals)

        # FST:
        fst_pct = C.giving_goal_pct - pct_tally
        fst_annual = self.total_gross_annual * fst_pct
        fst_monthly = fst_annual / C.MPY
        fst_row = ['FST',
                   percent_(fst_pct),
                   C.fst_term,
                   dollars_(fst_annual),
                   dollars_(fst_monthly),
                   ]
        fst_rows = [
            headers,
            fst_row
        ]
        present_table('FST', fst_rows)

        # Ministry Summary:
        aux_totals[0] = 'Aux'
        rows = [
            headers,
            aux_totals,
            fst_row,
        ]
        for r in rows:
            r.pop(2)  # Drop the "Term" column
        grand_totals = [
            'Total',
            percent_(pct_tally + fst_pct),
            dollars_(self.total_ministry_annual + fst_annual),
            dollars_(self.total_ministry_monthly + fst_monthly),
        ]
        present_table('Ministry Summary', rows, grand_totals)


# vim:fileencoding=utf-8
