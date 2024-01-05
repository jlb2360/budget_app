import argparse
import os
import logging
from datetime import datetime
from utilities.db_func import BudgetDB


def change(args):
    if not os.path.exists("databases/" + args.db):
        logging.error("Database does not exist")
        return

    db = BudgetDB(args.db)

    if args.type == "expected_income":
        db.change_value("expected_income", {"name": args.name, "amount": args.amount, "frequency": args.frequency, "category": args.category})
    elif args.type == "actual_income":
        db.change_value("actual_income", {"name": args.name, "amount": args.amount, "category": args.category, "Date": args.date})
    elif args.type == "expected_expense":
        db.change_value("expected_expense", {"name": args.name, "amount": args.amount, "frequency": args.frequency, "category": args.category})
    elif args.type == "actual_expense":
        db.change_value("actual_expense", {"name": args.name, "amount": args.amount, "category": args.category, "Date": args.date})