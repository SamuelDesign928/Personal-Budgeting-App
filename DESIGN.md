# Application Design

## Overview

The Personal Finance Tracker is a desktop application built using Python, Tkinter and SQLite.

The application follows a modular architecture, separating the user interface, business logic and database layer.

This approach improves maintainability, readability and future expansion.

---

# Architecture


|        Tkinter GUI        |


|     Business Logic        |


|     Database Layer        |


|         SQLite            |


---

# Module Structure

## Module 1

Database

Responsibilities

- Connect to SQLite
- Create database
- Create tables
- CRUD functions
- Execute SQL safely

---

## Module 2

Transactions

Responsibilities

- Add transaction
- Edit transaction
- Delete transaction
- Search transactions
- View transaction history

---

## Module 3

Categories

Responsibilities

- Manage spending categories
- Manage income categories
- Prevent duplicate categories

---

## Module 4

Budgets

Responsibilities

- Create budgets
- Track remaining budget
- Calculate percentage spent
- Support different budget periods

---

## Module 5

Dashboard

Responsibilities

- Display financial summary
- Show current balance
- Display recent transactions
- Show spending charts
- Display monthly statistics

---

## Module 6

Savings Goals

Responsibilities

- Create savings goals
- Track progress
- Display completion percentage

---

## Module 7

Reports

Responsibilities

- Generate monthly reports
- Category analysis
- Spending trends
- Export data

---

## Module 8

Settings

Responsibilities

- Theme
- Currency
- Default preferences
- Backup database

---

# User Interface

The application uses a single main window.

Navigation changes the displayed page rather than opening multiple windows.


|                    Personal Finance                  |

| Dashboard | Transactions | Budgets | Reports | ...  |


|               Active Page Content                |



---

# Folder Structure

FinanceTracker/

    main.py

    database.py

    models.py

    ui.py

    utils.py

    database/

    pages/

    assets/

    docs/

---

# Design Principles

The application is designed using the following principles:

- Single Responsibility Principle
- Modular architecture
- Reusable components
- Separation of concerns
- Scalable database design
- Easy future expansion

---

# Planned Development Order

Phase 1

- Database
- Transactions

Phase 2

- Categories
- Budgets

Phase 3

- Dashboard
- Savings Goals

Phase 4

- Reports
- Settings
- Polish
- Documentation

---

# Future Improvements

Potential future enhancements include:

- User authentication
- Multiple accounts
- CSV import/export
- Automatic recurring transactions
- Investment tracking
- Receipt image storage
- Financial forecasting
- Dark mode
