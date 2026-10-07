from datetime import datetime, timedelta


def validate_amount(amount):
    if not isinstance(amount, int):
        raise ValueError("Amount must be an integer.")

    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")


def validate_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except (ValueError, TypeError):
        raise ValueError("Date must be in YYYY-MM-DD format.")


def validate_category_name(name):
    if not isinstance(name, str):
        raise ValueError("Category name must be text.")

    if not name.strip():
        raise ValueError("Category name cannot be empty.")


def validate_period(period):
    valid_periods = ["weekly", "fortnightly", "monthly"]

    if period not in valid_periods:
        raise ValueError(
            "Period must be weekly, fortnightly, or monthly."
        )


def calculate_total_spending(transactions):
    total = 0

    for transaction in transactions:
        total += transaction.amount

    return total


def calculate_spending_by_category(transactions):
    spending = {}

    for transaction in transactions:
        category_id = transaction.category_id

        if category_id not in spending:
            spending[category_id] = 0

        spending[category_id] += transaction.amount

    return spending


def filter_transactions_by_date(transactions, start_date, end_date):
    filtered_transactions = []

    for transaction in transactions:
        if start_date <= transaction.date <= end_date:
            filtered_transactions.append(transaction)

    return filtered_transactions


def calculate_budget_usage(transactions, budget, start_date, end_date):
    period_transactions = filter_transactions_by_date(
        transactions,
        start_date,
        end_date
    )

    category_spending = 0

    for transaction in period_transactions:
        if transaction.category_id == budget.category_id:
            category_spending += transaction.amount

    return category_spending


def calculate_remaining_budget(transactions, budget, start_date, end_date):
    spending = calculate_budget_usage(
        transactions,
        budget,
        start_date,
        end_date
    )

    remaining = budget.amount - spending

    return remaining


def get_period_dates(period, today=None):
    if today is None:
        today = datetime.today()

    if period == "weekly":
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)

    elif period == "fortnightly":
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=13)

    elif period == "monthly":
        start_date = today.replace(day=1)

        if today.month == 12:
            next_month = today.replace(
                year=today.year + 1,
                month=1,
                day=1
            )
        else:
            next_month = today.replace(
                month=today.month + 1,
                day=1
            )

        end_date = next_month - timedelta(days=1)

    else:
        raise ValueError("Invalid budget period.")

    return (
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )