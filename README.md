# Personal Finance Tracker

A desktop personal finance application built with Python, Tkinter
and SQLite.

The application allows users to manage spending categories,
record transactions, create budgets with weekly, fortnightly or monthly periods and view financial
summaries through a dashboard.

## Features

- Category management
- Transaction management
- Budget management
- Weekly, fortnightly and monthly budgets
- Spending calculations
- Spending by category
- Current-month spending
- Budget usage tracking
- Recent transaction history
- SQLite persistence
- Input validation
- Foreign-key protection
- Transaction rollback handling

## Dashboard

The Dashboard provides an overview of the user's finances,
including total spending, current-month spending, spending by
category, budget progress and recent transactions.

## Technology

- Python
- Tkinter
- SQL
- Dataclasses

No third-party Python packages are required.

## Running the Application

### Requirements

Python 3.7 or higher

### Start the application

Clone the repository and enter the project directory:

```bash
python main.py


## How to Use

When the application is first opened, an empty database is created automatically.

### 1. Create Categories

Start by opening the **Categories** section and creating the categories you want to use for your spending.

For example:

- Food
- Transport
- Entertainment
- Groceries

Categories must be created before they can be assigned to transactions or budgets.

### 2. Add Transactions

Open **Transactions** to record your spending.

Each transaction contains:

- **Category** — what the spending was for
- **Amount** — the amount spent
- **Date** — when the spending occurred
- **Description** — an optional note

Amounts are entered in **pence**, rather than pounds.

For example:

```text
2500 = £25.00
1250 = £12.50
500 = £5.00