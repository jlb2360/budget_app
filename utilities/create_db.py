from utilities.db_func import BudgetDB
from datetime import datetime
import os
import logging


def create_db(args):


    if os.path.exists("databases/" + args.db):
        logging.error("Database already exists")


    db = BudgetDB(args.db)

     # frequency: 0 = daily, 1 = weekly, 2 = biweekly, 3 = monthly, 4 = yearly
    
    db.create_table("expected_income", ["name TEXT", "amount REAL", "frequency INTEGER", "category TEXT"])
    db.create_table("actual_income", ["name TEXT", "amount REAL", "category TEXT", "Date TEXT"]) # frequency is not needed for actual income
    db.create_table("expected_expense", ["name TEXT", "amount REAL", "frequency INTEGER", "category TEXT"])
    db.create_table("actual_expense", ["name TEXT", "amount REAL", "category TEXT", "Date TEXT"])


    date = datetime.now().strftime("%Y-%m-%d")
    db.insert("actual_income", {"name": "Savings", "amount": args.s, "category": "Savings", "Date": date})
    db.insert("actual_income", {"name": "Investments", "amount": args.inv, "category": "Investments", "Date": date})

    