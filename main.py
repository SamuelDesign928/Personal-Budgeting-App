import sqlite3
from database import *


create_database()

print("=== CATEGORIES ===")

add_category("Food")
add_category("Transport")

print("After adding:")
print(get_categories())

update_category(1, "Groceries")

print("After updating category 1:")
print(get_categories())


print("\n=== TRANSACTIONS ===")

add_transaction(1, 2500, "2026-09-18", "Weekly groceries")
add_transaction(2, 500, "2026-09-18", "Bus fare")

print("After adding:")
print(get_transactions())

update_transaction(1, 3000, "2026-09-18", "Updated groceries")

print("After updating transaction 1:")
print(get_transactions())


print("\n=== BUDGETS ===")

add_budget(1, 20000, "monthly")
add_budget(2, 5000, "monthly")

print("After adding:")
print(get_budget())

update_budget(1, 25000, "monthly")

print("After updating budget 1:")
print(get_budget())


print("\n=== FOREIGN KEY TEST ===")

try:
    add_transaction(9999, 1000, "2026-09-18", "Invalid category")
except sqlite3.IntegrityError:
    print("Foreign key protection works.")


print("\n=== DELETE TESTS ===")

delete_budget(2)

print("After deleting budget 2:")
print(get_budget())

delete_transaction(2)

print("After deleting transaction 2:")
print(get_transactions())


print("\n=== CATEGORY DELETE TEST ===")

try:
    delete_category(1)
except sqlite3.IntegrityError:
    print("Category deletion correctly blocked because it has related records.")


print("\n=== FINAL DATABASE STATE ===")

print("Categories:")
print(get_categories())

print("Transactions:")
print(get_transactions())

print("Budgets:")
print(get_budget())