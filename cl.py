import argparse
from datetime import datetime

def InitArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Command Line Budgeting tool")
    parser.add_argument("--db", help="Database name", type=str, default=str(datetime.now().year) + ".db")


    parser.add_argument("--i", "--init", help="Initialize a new budget", action="store_true")
    parser.add_argument("--s", "--savings", help="current savings", type=float, default=0)
    parser.add_argument("--inv", "--investments", help="current investments", type=float, default=0)

    parser.add_argument("--a", "--add", help="Add a new transaction", action="store_true")
    parser.add_argument("--ch", "--change", help="Change a transaction", action="store_true")
    parser.add_argument("--b", "--balance", help="Display current balance", action="store_true")
    parser.add_argument("--c", "--categories", help="Display current categories", action="store_true")
    parser.add_argument("--d", "--delete", help="Delete a transaction", action="store_true")
    parser.add_argument("--di", "--display", help="Display Budget", action="store_true")

    parser.add_argument("-n", "--name", help="Name of the transaction")
    parser.add_argument("-t", "--type", help="Type of transaction (expected income, actual income, expected expense, actual expense)")
    parser.add_argument("-c", "--category", help="Category of transaction")
    parser.add_argument("-am", "--amount", help="Amount of transaction", type=float)
    parser.add_argument("-f", "--frequency", help="Frequency of transaction (daily, weekly, biweekly, monthly, yearly)", type=str)
    parser.add_argument("-d", "--date", help="Date of transaction (YYYY-MM-DD)", type=str, default=datetime.now().strftime("%Y-%m-%d"))

    return parser.parse_args()