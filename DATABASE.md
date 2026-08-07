# Database Design

## Overview

The application uses an SQLite database to store all financial information.

The database has been designed using a relational structure to minimise duplicated data and improve maintainability.

All tables support CRUD operations (Create, Read, Update and Delete).

---

# Entity Relationship Diagram

Categories linked with Transactions and Budgets

SavingsGoals (Independent)

---

# Tables

## Transactions

Stores every income and expense entered by the user.

| Column | Type | Description |
|---------|------|-------------|
| id | INTEGER PRIMARY KEY | Unique transaction ID |
| date | TEXT | Transaction date |
| description | TEXT | Short description |
| category_id | INTEGER | References Categories.id |
| amount | REAL | Transaction amount |
| type | TEXT | Income or Expense |
| notes | TEXT | Optional notes |

### Relationships

- category_id → Categories.id

---

## Categories

Stores available spending and income categories.

Examples include:

- Food
- Transport
- Bills
- Salary
- Entertainment
- Shopping

| Column | Type | Description |
|---------|------|-------------|
| id | INTEGER PRIMARY KEY | Unique category ID |
| name | TEXT | Category name |
| icon | TEXT | Optional icon name |
| colour | TEXT | Optional colour value |

---

## Budgets

Stores spending limits for categories.

| Column | Type | Description |
|---------|------|-------------|
| id | INTEGER PRIMARY KEY | Budget ID |
| category_id | INTEGER | References Categories.id |
| amount | REAL | Budget amount |
| period | TEXT | Week, Fortnight, Month or Year |

### Relationships

- category_id → Categories.id

---

## Savings Goals

Stores savings objectives.

| Column | Type | Description |
|---------|------|-------------|
| id | INTEGER PRIMARY KEY | Goal ID |
| name | TEXT | Goal name |
| target_amount | REAL | Savings target |
| current_amount | REAL | Current saved amount |

---

# Foreign Keys

Transactions.category_id
    ↓
Categories.id

Budgets.category_id
    ↓
Categories.id

---

# Design Principles

The database has been designed around the following principles:

- Avoid duplicated information.
- Use foreign keys where appropriate.
- Keep each table responsible for one concept.
- Support future expansion without major redesign.
- Allow all data to be created, read, updated and deleted.

---

# Future Expansion

Potential future tables include:

- Recurring Transactions
- Goal Contributions
- Accounts
- Scheduled Payments
- Investment Portfolio
- Import History
