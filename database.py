import sqlite3


def create_database():
    connection = sqlite3.connect("database/finance.db")
    cursor = connection.cursor()

    # Enable foreign key enforcement
    cursor.execute("PRAGMA foreign_keys = ON")

    # Create categories table
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS categories ("
        "id INTEGER PRIMARY KEY, "
        "name TEXT NOT NULL"
        ")"
    )

    # Create transactions table
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

    # Create budgets table
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS budgets ("
        "id INTEGER PRIMARY KEY, "
        "category_id INTEGER NOT NULL, "
        "amount INTEGER NOT NULL, "
        "period TEXT NOT NULL, "
        "FOREIGN KEY (category_id) REFERENCES categories(id)"
        ")"
    )

    connection.commit()
    connection.close()


# CRUD operations

def add_category(name):
    connection = sqlite3.connect("database/finance.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO categories (name) VALUES (?)",
        (name,)
    )

    connection.commit()
    connection.close()


def get_categories():
    connection = sqlite3.connect("database/finance.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall()

    connection.close()

    return categories


def update_category(category_id, new_name):
    connection = sqlite3.connect("database/finance.db")
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE categories SET name = ? WHERE id = ?",
        (new_name, category_id)
    )

    connection.commit()
    connection.close()


def delete_category(category_id):
    connection = sqlite3.connect("database/finance.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM categories WHERE id = ?",
        (category_id,)
    )

    connection.commit()
    connection.close()