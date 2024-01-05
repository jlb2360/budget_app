"""
    This file is a display written in dash. Should be rewritten in htmx with go backend.
"""

import dash
from dash import dcc
from dash import html, Dash

import numpy as np
import pandas as pd

from utilities.db_func import BudgetDB
from display.pages.calcs import get_income_overtime, income_per_month, expense_per_month


def display(args):
    db = BudgetDB(args.db)

    # get expected income
    exp_income = db.retrieve_table("expected_income")
    global ei_df
    ei_df = pd.DataFrame(exp_income, columns=["name", "amount", "frequency", "category"])

    # get actual income
    act_income = db.retrieve_table("actual_income")
    global ai_df
    ai_df = pd.DataFrame(act_income, columns=["name", "amount", "category", "Date"])

    # get expected expense
    exp_expense = db.retrieve_table("expected_expense")
    global ee_df
    ee_df = pd.DataFrame(exp_expense, columns=["name", "amount", "frequency", "category"])

    # get actual expense
    act_expense = db.retrieve_table("actual_expense")
    global ae_df
    ae_df = pd.DataFrame(act_expense, columns=["name", "amount", "category", "Date"])


    app = Dash(__name__, use_pages=True)

    app.layout = html.Div([
        html.H1('Multi-page app with Dash Pages'),
        html.Div([
            html.Div(
                dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
            ) for page in dash.page_registry.values()
        ]),
        dash.page_container
    ])

    app.run(debug=True)

