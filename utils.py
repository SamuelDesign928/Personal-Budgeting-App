from datetime import datetime


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