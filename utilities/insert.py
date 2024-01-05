import argparse
import os
import logging
from datetime import datetime
from utilities.db_func import BudgetDB

def add(db_name: str, args: argparse.Namespace) -> None:
    
    if not os.path.exists("databases/" + db_name):
        logging.error("Database does not exist")
        return
    
    if not args.amount:
        logging.error("Amount not specified")
        return
    
    if not args.name:
        logging.error("Name not specified")
        return
    
    if not args.category:
        logging.error("Category not specified")
        return
    
    db = BudgetDB(db_name)

    
    if (args.frequency not in db.freq) and (args.type == "expected_income" or args.type == "expected_expense"):
        logging.error("Frequency not recognized")
        return


    if args.type == "expected_income":
        db.insert("expected_income", {"name": args.name, "amount": args.amount, "frequency": args.frequency, "category": args.category})
    elif args.type == "actual_income":
        date = datetime.now().strftime("%Y-%m-%d")
        db.insert("actual_income", {"name": args.name, "amount": args.amount, "category": args.category, "Date": date})
    elif args.type == "expected_expense":
        db.insert("expected_expense", {"name": args.name, "amount": args.amount, "frequency": args.frequency, "category": args.category})
    elif args.type == "actual_expense":
        date = datetime.now().strftime("%Y-%m-%d")
        db.insert("actual_expense", {"name": args.name, "amount": args.amount, "category": args.category, "Date": date})

    
