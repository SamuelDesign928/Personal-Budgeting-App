# Design

## Overview

The Personal Finance Tracker is a desktop application built with Python,
Tkinter and SQLite.

The application separates data storage, data models, validation and
the graphical interface.

## Architecture

### main.py

Responsible for:
- Creating the Tkinter application
- Navigation
- GUI forms
- Displaying database information
- Handling user interaction

### database.py

Responsible for:
- SQLite connection management
- Database creation
- CRUD operations
- Transactions and rollback handling
- Foreign key enforcement

### models.py

Contains dataclasses representing:
- Category
- Transaction
- Budget

### utils.py

Contains:
- Input validation
- Financial calculations
- Date filtering
- Budget period calculations

## Database

The application uses SQLite with three main tables:

- categories
- transactions
- budgets

Transactions and budgets reference categories through foreign keys.

## Money Handling

Money is stored as integer pence rather than floating-point pounds.

For example:

1000 = £10.00

This avoids floating-point precision problems when working with money.

## Budget Periods

Budgets support:

- Weekly
- Fortnightly
- Monthly

These periods are calendar-based.

A monthly budget applies to the current calendar month,
while weekly and fortnightly budgets use calendar periods rather
than being anchored to the user's payday.

## Dashboard

The Dashboard calculates information from the stored transactions
and budgets rather than maintaining separate copies of financial data.

It displays:
- Total spending
- Current-month spending
- Spending by category
- Budget usage
- Recent transactions