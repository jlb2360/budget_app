import dash
from dash import html, dcc, Dash
from datetime import datetime
import pandas as pd


from utilities.db_func import BudgetDB
from display.pages.calcs import get_income_overtime, income_per_month, expense_per_month, month_category_breakdown_expenses, month_category_breakdown_income



dash.register_page(__name__)

def layout(year=datetime.now().year, month=datetime.now().month):
    month_name = datetime.now().strftime("%B")
    db = BudgetDB(str(year)+".db")

    # get expected income
    exp_income = db.retrieve_table("expected_income")
    ei_df = pd.DataFrame(exp_income, columns=["name", "amount", "frequency", "category"])

    # get actual income
    act_income = db.retrieve_table("actual_income")
    ai_df = pd.DataFrame(act_income, columns=["name", "amount", "category", "Date"])

    # get expected expense
    exp_expense = db.retrieve_table("expected_expense")
    ee_df = pd.DataFrame(exp_expense, columns=["name", "amount", "frequency", "category"])

    # get actual expense
    act_expense = db.retrieve_table("actual_expense")
    ae_df = pd.DataFrame(act_expense, columns=["name", "amount", "category", "Date"])

    actual_income, expected_income = month_category_breakdown_income(ei_df, ai_df, str(month))

    actual_expense, expected_expense = month_category_breakdown_expenses(ee_df, ae_df, str(month))

    return html.Div([
        html.H1(str(year) + ' Budget ' + str(month_name)),
        html.Div([
            html.H3("Income Breakdown"),
            dcc.Graph(
                id='income_breakdown',
                figure={
                    'data': [
                        {'x': list(actual_income.keys()), 'y': list(actual_income.values()), 'type': 'bar', 'name': 'Actual'},
                        {'x': list(expected_income.keys()), 'y': list(expected_income.values()), 'type': 'bar', 'name': 'Expected'},
                    ],
                    'layout': {
                        'title': 'Income Breakdown',
                        'yaxis': {
                            'title': 'Amount ($)'
                        }
                    }
                }
            ),
        ]),
        html.Div([
            html.H3("Expense Breakdown"),
            dcc.Graph(
                id='expense_breakdown',
                figure={
                    'data': [
                        {'x': list(actual_expense.keys()), 'y': list(actual_expense.values()), 'type': 'bar', 'name': 'Actual'},
                        {'x': list(expected_expense.keys()), 'y': list(expected_expense.values()), 'type': 'bar', 'name': 'Expected'},
                    ],
                    'layout': {
                        'title': 'Expense Breakdown',
                        'yaxis': {
                            'title': 'Amount ($)'
                        }
                    }
                }
            ),
        ]),
    ])

