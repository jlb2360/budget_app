import dash
from dash import html, dcc, Input, Output
import pandas as pd
from datetime import datetime


from utilities.db_func import BudgetDB
from display.pages.calcs import get_income_overtime, income_per_month, expense_per_month


dash.register_page(__name__)


def layout(year=datetime.now().year):

    db = BudgetDB(str(year)+".db")

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


    savings_overtime, investment_overtime = get_income_overtime(ei_df, ai_df, ee_df)

    actual_income_per_month, excepted_income_per_month = income_per_month(ei_df, ai_df)
    actual_expense_per_month, excepted_expense_per_month = expense_per_month(ee_df, ae_df)


    return html.Div([
        html.H1(str(year) + ' Budget'),
         html.Div([
            html.H3("Savings and Investments Overtime"),
            dcc.Graph(
                id='savings_overtime',
                figure={
                    'data': [
                        {'x': list(savings_overtime.keys()), 'y': list(savings_overtime.values()), 'type': 'line', 'name': 'Savings'},
                        {'x': list(investment_overtime.keys()), 'y': list(investment_overtime.values()), 'type': 'line', 'name': 'Investments'},
                    ],
                    'layout': {
                        'title': 'Savings and Investments Overtime',
                        'yaxis': {
                            'title': 'Amount ($)'
                        }
                    }
                }
            ),
            "Investment Each Month: ",
            dcc.Input(id='investment_per_month', value='0.0', type='text')
        ]),

        html.Div([
            html.H3("Income and Expenses Per Month"),
            dcc.Graph(
                id='income+expenses_per_month',
                figure={
                    'data': [
                        {'x': list(actual_income_per_month.keys()), 'y': list(actual_income_per_month.values()), 'type': 'bar', 'name': 'Actual Income'},
                        {'x': list(excepted_income_per_month.keys()), 'y': list(excepted_income_per_month.values()), 'type': 'bar', 'name': 'Expected Income'},
                        {'x': list(actual_expense_per_month.keys()), 'y': list(actual_expense_per_month.values()), 'type': 'bar', 'name': 'Actual Expenses'},
                        {'x': list(excepted_expense_per_month.keys()), 'y': list(excepted_expense_per_month.values()), 'type': 'bar', 'name': 'Expected Expenses'},
                    ],
                    'layout': {
                        'title': 'Income And Expenses Per Month',
                        'yaxis': {
                            'title': 'Amount ($)'
                        }
                    }
                }
            )
        ]),
    ])


@dash.callback(
    Output(component_id='savings_overtime', component_property='figure'),
    Input(component_id='investment_per_month', component_property='value')
)
def update_output_div(input_value):
    savings_overtime, investment_overtime = get_income_overtime(ei_df, ai_df, ee_df, invest_per_month=float(input_value))

    return {
        'data': [
            {'x': list(savings_overtime.keys()), 'y': list(savings_overtime.values()), 'type': 'line', 'name': 'Savings'},
            {'x': list(investment_overtime.keys()), 'y': list(investment_overtime.values()), 'type': 'line', 'name': 'Investments'},
        ],
        'layout': {
            'title': 'Savings and Investments Overtime'
        }
    }


