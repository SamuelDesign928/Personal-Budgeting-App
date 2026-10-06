import sqlite3
from contextlib import contextmanager
from models import Category, Transaction, Budget


def get_connection():
    connection = sqlite3.connect("database/finance.db")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


@contextmanager
def database_connection():
    connection = get_connection()

    try:
        yield connection
        connection.commit()
    except:
        connection.rollback()
        raise
    finally:
        connection.close()


def create_database():
    with database_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS categories ("
            "id INTEGER PRIMARY KEY, "
            "name TEXT NOT NULL"
            ")"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS transactions ("
            "id INTEGER PRIMARY KEY, "
            "category_id INTEGER NOT NULL, "
            "amount INTEGER NOT NULL, "
            "date TEXT NOT NULL, "
            "description TEXT, "
            "FOREIGN KEY (category_id) REFERENCES categories(id)"
            ")"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS budgets ("
            "id INTEGER PRIMARY KEY, "
            "category_id INTEGER NOT NULL, "
            "amount INTEGER NOT NULL, "
            "period TEXT NOT NULL, "
            "FOREIGN KEY (category_id) REFERENCES categories(id)"
            ")"
        )


# CRUD operations for categories

def add_category(name):
    with database_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO categories (name) VALUES (?)",
            (name,)
        )


def get_categories():
    with database_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT id, name FROM categories")
        rows = cursor.fetchall()

        categories = []
        for row in rows:
            category = Category(id=row[0], name=row[1])
            categories.append(category)

        return categories


def update_category(category_id, new_name):
    with database_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE categories SET name = ? WHERE id = ?",
            (new_name, category_id)
        )


def delete_category(category_id):
    with database_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM categories WHERE id = ?",
            (category_id,)
        )


# CRUD operations for transactions

def add_transaction(category_id, amount, date, description):
    with database_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO transactions "
            "(category_id, amount, date, description) "
            "VALUES (?, ?, ?, ?)",
            (category_id, amount, date, description)
        )


def get_transactions():
    with database_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id, category_id, amount, date, description "
            "FROM transactions"
        )
        rows = cursor.fetchall()

        transactions = []
        for row in rows:
            transaction = Transaction(
                id=row[0],
                category_id=row[1],
                amount=row[2],
                date=row[3],
                description=row[4],
            )
            transactions.append(transaction)

        return transactions


def update_transaction(transaction_id, amount, date, description):
    with database_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE transactions "
            "SET amount = ?, date = ?, description = ? "
            "WHERE id = ?",
            (amount, date, description, transaction_id)
        )


def delete_transaction(transaction_id):
    with database_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM transactions WHERE id = ?",
            (transaction_id,)
        )


def add_budget(category_id, amount, period):
    with database_connection() as connection:
        cursor = connection.cursor()
    
        cursor.execute(
            "INSERT INTO budgets "
            "(category_id, amount, period) "
            "VALUES (?, ?, ?)",
            (category_id, amount, period)
        )

def get_budgets():
    with database_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id, category_id, amount, period "
            "FROM budgets"
        )
        rows = cursor.fetchall()

        budgets = []
        for row in rows:
            budget = Budget(
                id=row[0],
                category_id=row[1],
                amount=row[2],
                period=row[3],
            )
            budgets.append(budget)

        return budgets

def update_budget(budget_id, amount, period):
    with database_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE budgets "
            "SET amount = ?, period = ? "
            "WHERE id = ?",
            (amount, period, budget_id)
        )

def delete_budget(budget_id):
    with database_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM budgets WHERE id = ?",
            (budget_id,)
        )