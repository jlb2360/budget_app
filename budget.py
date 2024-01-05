from cl import InitArgs
from utilities.create_db import create_db
from utilities.insert import add
from utilities.change import change
from display.app import display
import logging


def main():
    # set logging level to info
    logger = logging.getLogger('simple_example')
    logger.setLevel(level=logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()

    # add formatter to ch
    ch.setFormatter(formatter)
    ch.setLevel(logging.INFO)
    # add ch to logger
    logger.addHandler(ch)

    args = InitArgs()

    if args.i:
        logging.info("Initializing new budget")
        create_db(args)
    
    if args.a:
        freq = {
            "daily": 0,
            "weekly": 1,
            "biweekly": 2,
            "monthly": 3,
            "yearly": 4
        }
        
        if args.type == "expected_income" or args.type == "expected_expense":
            if args.frequency in freq:
                args.frequency = freq[args.frequency]
        add(args.db, args)

    if args.b:
        pass

    if args.d:
        display(args)

    if args.ch:
        change(args)




if __name__ == "__main__":
    main()