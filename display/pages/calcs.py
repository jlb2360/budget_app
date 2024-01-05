import numpy as np
import pandas as pd


def  get_income_overtime(expected_income: pd.DataFrame, actual_income: pd.DataFrame, expected_expenses: pd.DataFrame, invest_per_month=1000.0) -> (dict, dict):
    """
        daily: 0
        weekly: 1
        biweekly: 2
        monthly: 3
        yearly: 4
    """

    daily = expected_income[expected_income["frequency"] == 0]
    weekly = expected_income[expected_income["frequency"] == 1]
    biweekly = expected_income[expected_income["frequency"] == 2]
    monthly = expected_income[expected_income["frequency"] == 3]
    yearly = expected_income[expected_income["frequency"] == 4]

    daily_exp = expected_expenses[expected_expenses["frequency"] == 0]
    weekly_exp = expected_expenses[expected_expenses["frequency"] == 1]
    biweekly_exp = expected_expenses[expected_expenses["frequency"] == 2]
    monthly_exp = expected_expenses[expected_expenses["frequency"] == 3]
    yearly_exp = expected_expenses[expected_expenses["frequency"] == 4]

    savings_dict = {
        "Jan": actual_income["amount"][actual_income["category"] == "Savings"].iloc[0],
        "Feb": 0,
        "Mar": 0,
        "Apr": 0,
        "May": 0,
        "Jun": 0,
        "Jul": 0,
        "Aug": 0,
        "Sep": 0,
        "Oct": 0,
        "Nov": 0,
        "Dec": 0,
    }

    investment_dict = {
       "Jan": actual_income["amount"][actual_income["category"] == "Investments"].iloc[0],
        "Feb": 0,
        "Mar": 0,
        "Apr": 0,
        "May": 0,
        "Jun": 0,
        "Jul": 0,
        "Aug": 0,
        "Sep": 0,
        "Oct": 0,
        "Nov": 0,
        "Dec": 0, 
    }

    prev_month = 0.0
    for k in investment_dict:
        biweekly_const = 2
        if k == "Jun":
            biweekly_const = 3
        if k == "Dec":
            biweekly_const = 3

        yearly_const = 0
        if k == "Dec":
            yearly_const = 1

        investment_dict[k] += biweekly["amount"][biweekly["category"] == "Investments"].sum() * biweekly_const + monthly["amount"][monthly["category"] == "Investments"].sum() + yearly["amount"][yearly["category"] == "Investments"].sum()*yearly_const + compound(prev_month) + invest_per_month

        prev_month = investment_dict[k]

    prev_month = 0.0
    for k in savings_dict:
        biweekly_const = 2
        if k == "Jun":
            biweekly_const = 3
        if k == "Dec":
            biweekly_const = 3

        yearly_const = 0
        if k == "Dec":
            yearly_const = 1

        savings_dict[k] += biweekly["amount"][biweekly["category"] == "Savings"].sum() * biweekly_const + monthly["amount"][monthly["category"] == "Savings"].sum() + yearly["amount"][yearly["category"] == "Savings"].sum()*yearly_const + prev_month

        savings_dict[k] -= biweekly_exp["amount"].sum() * biweekly_const + monthly_exp["amount"].sum() + yearly_exp["amount"].sum()*yearly_const + invest_per_month

        prev_month = savings_dict[k]

    return savings_dict, investment_dict

    
def compound(prev_month: float) -> float:
    interest = 0.07 # 7% interest per year
    increase = prev_month*(1 + interest/12)
    return increase


def income_per_month(expected_income: pd.DataFrame, actual_income: pd.DataFrame) -> (dict, dict):
    daily = expected_income[expected_income["frequency"] == 0]
    weekly = expected_income[expected_income["frequency"] == 1]
    biweekly = expected_income[expected_income["frequency"] == 2]
    monthly = expected_income[expected_income["frequency"] == 3]
    yearly = expected_income[expected_income["frequency"] == 4]

    # drop first two rows from actual income
    act_inc = actual_income.drop([0, 1])

    actual_dict = {
        "Jan": 0,
        "Feb": 0,
        "Mar": 0,
        "Apr": 0,
        "May": 0,
        "Jun": 0,
        "Jul": 0,
        "Aug": 0,
        "Sep": 0,
        "Oct": 0,
        "Nov": 0,
        "Dec": 0,
    }

    expected_dict = {
        "Jan": 0,
        "Feb": 0,
        "Mar": 0,
        "Apr": 0,
        "May": 0,
        "Jun": 0,
        "Jul": 0,
        "Aug": 0,
        "Sep": 0,
        "Oct": 0,
        "Nov": 0,
        "Dec": 0, 
    }

    for k in actual_dict:
        biweekly_const = 2
        if k == "Jun":
            biweekly_const = 3
        if k == "Dec":
            biweekly_const = 3

        yearly_const = 0
        if k == "Dec":
            yearly_const = 1

        bool_arr = np.array([k in str(x)[5:7] for x in act_inc["Date"].values])

        if len(bool_arr) != 0:
            actual_dict[k] += act_inc[bool_arr]["amount"].sum()
        else:
            actual_dict[k] += 0

        expected_dict[k] += biweekly["amount"][biweekly["category"] == "Savings"].sum() * biweekly_const + monthly["amount"][monthly["category"] == "Savings"].sum() + yearly["amount"][yearly["category"] == "Savings"].sum()*yearly_const

    return actual_dict, expected_dict


def expense_per_month(expected_expenses: pd.DataFrame, actual_expenses: pd.DataFrame) -> (dict, dict):
    daily = expected_expenses[expected_expenses["frequency"] == 0]
    weekly = expected_expenses[expected_expenses["frequency"] == 1]
    biweekly = expected_expenses[expected_expenses["frequency"] == 2]
    monthly = expected_expenses[expected_expenses["frequency"] == 3]
    yearly = expected_expenses[expected_expenses["frequency"] == 4]

    

    actual_dict = {
        "Jan": 0,
        "Feb": 0,
        "Mar": 0,
        "Apr": 0,
        "May": 0,
        "Jun": 0,
        "Jul": 0,
        "Aug": 0,
        "Sep": 0,
        "Oct": 0,
        "Nov": 0,
        "Dec": 0,
    }

    expected_dict = {
        "Jan": 0,
        "Feb": 0,
        "Mar": 0,
        "Apr": 0,
        "May": 0,
        "Jun": 0,
        "Jul": 0,
        "Aug": 0,
        "Sep": 0,
        "Oct": 0,
        "Nov": 0,
        "Dec": 0, 
    }

    for k in actual_dict:
        biweekly_const = 2
        if k == "Jun":
            biweekly_const = 3
        if k == "Dec":
            biweekly_const = 3

        yearly_const = 0
        if k == "Dec":
            yearly_const = 1

        if k == "Jan":
            knum = "1"
        elif k == "Feb":
            knum = "2"
        elif k == "Mar":
            knum = "3"
        elif k == "Apr":
            knum = "4"
        elif k == "May":
            knum = "5"
        elif k == "Jun":
            knum = "6"
        elif k == "Jul":
            knum = "7"
        elif k == "Aug":
            knum = "8"
        elif k == "Sep":
            knum = "9"
        elif k == "Oct":
            knum = "10"
        elif k == "Nov":
            knum = "11"
        elif k == "Dec":
            knum = "12"
                

        bool_arr = np.array([knum in str(x)[5:7] for x in actual_expenses["Date"].values])

        if len(bool_arr) != 0:
            actual_dict[k] += actual_expenses[bool_arr]["amount"].sum()
        else:
            actual_dict[k] += 0

        expected_dict[k] += biweekly["amount"].sum() * biweekly_const + monthly["amount"].sum() + yearly["amount"].sum()*yearly_const

    return actual_dict, expected_dict
        


def month_category_breakdown_income(expected_income: pd.DataFrame, actual_income: pd.DataFrame, month: str)->dict:
    if len(month) == 1:
        month = "0" + month

   # drop first two rows from actual income
    actual_income = actual_income.drop([0, 1]) 

    if len(actual_income) != 0:
        bool_arr = np.array([month in str(x)[5:7] for x in actual_income["Date"].values])
        if len(bool_arr) != 0:
            act_inc = actual_income[bool_arr]
        else:
            act_inc = pd.DataFrame(columns=["name", "amount", "category", "Date"])
    else:
        act_inc = pd.DataFrame(columns=["name", "amount", "category", "Date"])




    daily = expected_income[expected_income["frequency"] == 0]
    weekly = expected_income[expected_income["frequency"] == 1]
    biweekly = expected_income[expected_income["frequency"] == 2]
    monthly = expected_income[expected_income["frequency"] == 3]
    yearly = expected_income[expected_income["frequency"] == 4]

    actual_dict = {
        "Savings": 0,
        "Investments": 0,
    }

    expected_dict = {
        "Savings": 0,
        "Investments": 0,
    }

    for k in actual_dict:
        

        actual_dict[k] += act_inc[act_inc["category"] == k]["amount"].sum()

        expected_dict[k] += biweekly[biweekly["category"] == k]["amount"].sum() * 2 + monthly[monthly["category"] == k]["amount"].sum()


    return actual_dict, expected_dict

def month_category_breakdown_expenses(expected_expenses: pd.DataFrame, actual_expenses: pd.DataFrame, month: str)->dict:
    if len(actual_expenses) != 0:
        bool_arr = np.array([month in str(x)[5:7] for x in actual_expenses["Date"].values])
        if len(bool_arr) != 0:
            act_inc = actual_expenses[bool_arr]
        else:
            act_inc = pd.DataFrame(columns=["name", "amount", "category", "Date"])
    else:
        act_inc = pd.DataFrame(columns=["name", "amount", "category", "Date"])


    daily = expected_expenses[expected_expenses["frequency"] == 0]
    weekly = expected_expenses[expected_expenses["frequency"] == 1]
    biweekly = expected_expenses[expected_expenses["frequency"] == 2]
    monthly = expected_expenses[expected_expenses["frequency"] == 3]
    yearly = expected_expenses[expected_expenses["frequency"] == 4]

    actual_dict = {
        "God": 0,
        "Housing": 0,
        "Groceries": 0,
        "Restaurants": 0,
        "Entertainment": 0,
        "Transportation": 0,
        "Health": 0,
        "Pets": 0,
        "Personal_Care": 0,
        "Clothing": 0,
        "Gifts": 0,
        "Utilities": 0,
        "Insurance": 0,
        "Education": 0,
        "Personal": 0,
    }

    expected_dict = {
        "God": 0,
        "Housing": 0,
        "Groceries": 0,
        "Restaurants": 0,
        "Entertainment": 0,
        "Transportation": 0,
        "Health": 0,
        "Pets": 0,
        "Personal_Care": 0,
        "Clothing": 0,
        "Gifts": 0,
        "Utilities": 0,
        "Insurance": 0,
        "Education": 0,
        "Personal": 0,
    }

    for k in actual_dict:
        

        actual_dict[k] += actual_expenses[actual_expenses["category"] == k]["amount"].sum()

        expected_dict[k] += biweekly[biweekly["category"] == k]["amount"].sum() * 2 + monthly[monthly["category"] == k]["amount"].sum()

    return actual_dict, expected_dict

    