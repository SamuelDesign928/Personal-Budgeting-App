# Database

The application uses SQLite.

## Tables

### categories

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| name | TEXT | Category name |

### transactions

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| category_id | INTEGER | References categories.id |
| amount | INTEGER | Amount in pence |
| date | TEXT | Date in YYYY-MM-DD format |
| description | TEXT | Optional description |

### budgets

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| category_id | INTEGER | References categories.id |
| amount | INTEGER | Budget amount in pence |
| period | TEXT | weekly, fortnightly or monthly |

## Relationships

A category can have multiple transactions.

A category can have multiple budgets, provided they use
different periods.

Transactions and budgets cannot reference a category that
does not exist.

Categories cannot be deleted while they are referenced by
transactions or budgets.

## Money

Money is stored as integer pence.

For example:

£25.50 → 2550
£100.00 → 10000