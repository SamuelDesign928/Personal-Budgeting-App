import sqlite3


def create_database():
    connection = sqlite3.connect("database/finance.db")

    connection.close()