from database import *

create_database()

delete_transaction(2)


transactions = get_transactions()

for transaction in transactions:
    print(transaction)
