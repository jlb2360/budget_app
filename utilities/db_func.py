"""
This file contains functions that are used to interact with the database.
"""

"""
Layout of the class:

1. Helper functions (create tables, etc.)

2. Insertion and Deletions of data

3. Retrieval of data for display
"""

import sqlite3
import os
import logging


class BudgetDB():
    def __init__(self, db_name):
        self.db_name = "databases/" + db_name # expected to be a year, e.g. 2021.db

        if not os.path.exists("databases"):
            os.mkdir("databases")
        
        if not os.path.exists(self.db_name):
            open(self.db_name, "w").close()

        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()

        # categories that tells us where to put the money
        self.income_categories = [
                "Savings", 
                "Investments",
                "Other"
            ]
        self.expense_categories = [
                "God",
                "Housing",
                "Groceries",
                "Restaurants",
                "Entertainment",
                "Transportation",
                "Health",
                "Pets",
                "Personal_Care",
                "Clothing",
                "Gifts",
                "Utilities",
                "Insurance",
                "Education",
                "Personal",
            ]
        
        self.freq = [0, 1, 2, 3, 4]



    "1. Helper functions"
    def create_table(self, table_name: str, columns: list) -> None:
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(columns)})''')
        self.conn.commit()

    def delete_table(self, table_name: str) -> None:
        self.c.execute(f'''DROP TABLE IF EXISTS {table_name}''')
        self.conn.commit()

    "2. Insertion and Deletions of data"
    def insert(self, table_name: str, values: dict) -> None:
        if (table_name == "expected_income") and values["category"] in self.income_categories:
            self.c.execute(f'''INSERT INTO {table_name} VALUES (?, ?, ?, ?)''', (values["name"], values["amount"], values["frequency"], values["category"]))
        elif (table_name == "actual_income") and values["category"] in self.income_categories:
            self.c.execute(f'''INSERT INTO {table_name} VALUES (?, ?, ?, ?)''', (values["name"], values["amount"], values["category"], values["Date"]))
        elif (table_name == "expected_expense") and values["category"] in self.expense_categories:
            self.c.execute(f'''INSERT INTO {table_name} VALUES (?, ?, ?, ?)''', (values["name"], values["amount"], values["frequency"], values["category"]))
        elif (table_name == "actual_expense") and values["category"] in self.expense_categories:
            self.c.execute(f'''INSERT INTO {table_name} VALUES (?, ?, ?, ?)''', (values["name"], values["amount"], values["category"], values["Date"]))
        else:
            logging.error("Invalid category or table name")
            raise ValueError("Invalid category or table name")
        
        self.conn.commit()

    def delete_value(self, table_name: str, columns: [str], values: [float]) -> None:
        self.c.execute(f'''DELETE FROM {table_name} WHERE {columns} = {values}''')
        self.conn.commit()

    def delete_name(self, table_name: str, columns: [str], values: [str]) -> None:
        self.c.execute(f'''DELETE FROM {table_name} WHERE {columns} = "{values}"''')
        self.conn.commit()

    def change_value(self, table_name: str, values: dict) -> None:
        for k, v in values.items():
            self.c.execute(f'''UPDATE {table_name} SET {k} = "{v}" WHERE name = "{values["name"]}"''')
        self.conn.commit()

    "3. Retrieval of data for display"
    def retrieve_table(self, table_name: str) -> [str]:
        self.c.execute(f'''SELECT * FROM {table_name}''')
        return self.c.fetchall()
