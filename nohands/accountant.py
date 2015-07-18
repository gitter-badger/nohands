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
        self.time_periods = Session.query(TimePeriod).all()

        # TODO: It should be possible to use a hybrid expression to achieve these.
        #   but I haven't been able to figure it out yet.
        self.total_expenses_monthly = 0
        for e in self.expenses:
            self.total_expenses_monthly += e.monthly_amount

        self.total_expenses_annual = 0
        for e in self.expenses:
            self.total_expenses_annual += e.annual_amount

        self.total_gross_annual = 0
        for e in self.earners:
            self.total_gross_annual += e.gross_annual

        # MINISTRY:
        self.total_aux_annual = 0
        for e in self.ministries:
            self.total_aux_annual += e.annual_amount
        self.total_aux_monthly = 0
        for e in self.ministries:
            self.total_aux_monthly += e.monthly_amount
        self.total_aux_pct = 0
        self.crunch_giving_numbers()
        self.fst_pct = C.giving_goal_pct - self.total_aux_pct
        self.fst_annual = self.total_gross_annual * self.fst_pct
        self.fst_monthly = self.fst_annual / C.MPY
        self.hb_amount = C.giving_holdback_pct * self.fst_monthly
        self.hb_monthly = self.fst_monthly - self.hb_amount
        self.hb_total = self.hb_amount * C.MPY
        self.total_ministry_pct = self.total_aux_pct + self.fst_pct
        self.total_ministry_annual = self.total_aux_annual + self.fst_annual
        self.total_ministry_monthly = self.total_aux_monthly + self.fst_monthly

        self.total_net_annual_income = 0
        for e in self.earners:
            self.total_net_annual_income += e.net_annual

        # SAVINGS:
        self.annual_savings = C.savings_pct * self.total_net_annual_income
        self.monthly_savings = self.annual_savings / C.MPY

        # WAA:
        # waa_subtotal is effectively all bills, including giving (but not the holdback).
        self.waa_subtotal = self.total_expenses_monthly + self.total_ministry_monthly - self.hb_amount
        self.waa_total_monthly = self.waa_subtotal * C.waa_multiplier
        self.waa_total_annual = self.waa_total_monthly * C.MPY
        print(dollars_(self.waa_total_monthly))
        print(dollars_(self.waa_total_annual))
        self.crunch_deposits()

    def crunch_deposits(self):
        actual_earners = []
        for e in self.earners:
            if e.gross_annual > 0:
                earner_container = [e]
                actual_earners.append(earner_container)

                waa_contrib_monthly = self.waa_total_monthly * e.percentage
                waa_contrib_annual = waa_contrib_monthly * C.MPY
                waa_contrib_check = waa_contrib_annual / e.time_period.occurrence_per_year
                print(percent_(e.percentage))
                print(dollars_(waa_contrib_monthly))
                print(dollars_(waa_contrib_check))

    def report_deposits(self):
        pass

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
                str(e.time_period.occurrence_per_year),
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
                str(e.time_period.name),
                str(e.has_auto_pay),
                str(e.auto_pay_enabled),
                dollars_(e.monthly_amount),
                dollars_(e.annual_amount),
            ]
            rows.append(values)
        present_table('Expenses', rows)
        print('Total Annual Expenses:  {}'.format(dollars_(self.total_expenses_annual)))
        print('Total Monthly Expenses:  {}'.format(dollars_(self.total_expenses_monthly)))

    def crunch_giving_numbers(self):
        for m in self.ministries:
            percentage = m.annual_amount / self.total_gross_annual
            self.total_aux_pct += percentage

    def report_giving(self):
        common_headers = ['Name', 'Percentage', 'Term', 'Annual', 'Monthly']

        # Auxiliary Ministries:
        aux_rows = [
            common_headers,
        ]
        for m in self.ministries:
            values = [
                m.name,
                percent_(m.annual_amount / self.total_gross_annual),
                str(m.time_period.name),
                dollars_(m.annual_amount),
                dollars_(m.monthly_amount),
            ]
            aux_rows.append(values)
        aux_totals = [
            'Subtotals',
            percent_(self.total_aux_pct),
            '',  # Blank
            dollars_(self.total_aux_annual),
            dollars_(self.total_aux_monthly),
        ]
        present_table('Auxiliary Ministries', aux_rows, aux_totals)

        # FST:
        fst_row = ['FST',
                   percent_(self.fst_pct),
                   C.fst_period,
                   dollars_(self.fst_annual),
                   dollars_(self.fst_monthly),
                   ]
        fst_rows = [
            common_headers,
            fst_row
        ]
        present_table('FST', fst_rows)

        # FST Holdback:
        hb_rows = [
            ['Percentage', 'Amount', 'Monthly Check', 'Year-end Check'],
            [percent_(C.giving_holdback_pct),
             dollars_(self.hb_amount),
             dollars_(self.hb_monthly),
             dollars_(self.hb_total),
             ],
        ]
        present_table('FST Holdback', hb_rows)

        # Ministry Summary:
        aux_totals[0] = 'Aux'
        rows = [
            common_headers,
            aux_totals,
            fst_row,
        ]
        for r in rows:
            r.pop(2)  # Drop the "Term" column
        grand_totals = [
            'Total',
            percent_(self.total_ministry_pct),
            dollars_(self.total_ministry_annual),
            dollars_(self.total_ministry_monthly),
        ]
        present_table('Ministry Summary', rows, grand_totals)

    def report_savings(self):
        rows = [
            ['% off Net', 'Annual', 'Monthly'],
            [percent_(C.savings_pct),
             dollars_(self.annual_savings),
             dollars_(self.monthly_savings)],
        ]
        present_table('Savings', rows)


# vim:fileencoding=utf-8
