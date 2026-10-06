import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from database import *
from utils import *
from datetime import date

valid_periods = ["weekly", "fortnightly", "monthly"]


class FinanceApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Personal Finance Tracker")
        self.geometry("900x600")
        self.minsize(700, 500)

        self.create_widgets()

    def create_widgets(self):
        # Navigation
        navigation = ttk.Frame(self)
        navigation.pack(side="left", fill="y", padx=10, pady=10)

        # Main content area
        self.content = ttk.Frame(self)
        self.content.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Navigation buttons
        ttk.Button(navigation, text="Dashboard", command=self.show_dashboard).pack(fill="x", pady=5)
        ttk.Button(navigation, text="Transactions", command=self.show_transactions).pack(fill="x", pady=5)
        ttk.Button(navigation, text="Budgets", command=self.show_budgets).pack(fill="x", pady=5)
        ttk.Button(navigation, text="Categories", command=self.show_categories).pack(fill="x", pady=5)

        # Start on dashboard
        self.show_dashboard()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # ---------------------------------------------------------
    # Dashboard
    # ---------------------------------------------------------

    def show_dashboard(self):
        self.clear_content()

        ttk.Label(self.content, text="Dashboard", font=("Arial", 20)).pack(pady=20)
        ttk.Label(self.content, text="Dashboard coming soon.").pack()

    # ---------------------------------------------------------
    # Categories
    # ---------------------------------------------------------

    def show_categories(self):
        self.clear_content()

        ttk.Label(self.content, text="Categories", font=("Arial", 20)).pack(pady=(10, 20))

        # Category name input
        form = ttk.Frame(self.content)
        form.pack(fill="x", pady=10)

        ttk.Label(form, text="Category name:").grid(row=0, column=0, padx=5)

        self.category_name_entry = ttk.Entry(form)
        self.category_name_entry.grid(row=0, column=1, padx=5)

        ttk.Button(form, text="Add", command=self.add_category_from_gui).grid(row=0, column=2, padx=5)
        ttk.Button(form, text="Update", command=self.update_category_from_gui).grid(row=0, column=3, padx=5)
        ttk.Button(form, text="Delete", command=self.delete_category_from_gui).grid(row=0, column=4, padx=5)

        # Category table
        self.category_tree = ttk.Treeview(
            self.content,
            columns=("id", "name"),
            show="headings"
        )

        self.category_tree.heading("id", text="ID")
        self.category_tree.heading("name", text="Category")
        self.category_tree.column("id", width=80)
        self.category_tree.column("name", width=250)

        self.category_tree.pack(fill="both", expand=True, pady=10)
        self.category_tree.bind("<<TreeviewSelect>>", self.select_category)

        self.refresh_categories()

    def refresh_categories(self):
        # Remove existing rows
        for item in self.category_tree.get_children():
            self.category_tree.delete(item)

        # Get categories from database and add them to the table
        for category in get_categories():
            self.category_tree.insert(
                "",
                "end",
                iid=str(category.id),
                values=(category.id, category.name)
            )

    def category_name_taken(self, name, ignore_id=None):
        # Names are used as dropdown labels, so two categories with the
        # same name would make one of them impossible to pick.
        wanted = name.strip().lower()

        for category in get_categories():
            if category.id != ignore_id and category.name.strip().lower() == wanted:
                return True

        return False

    def select_category(self, event=None):
        selected = self.category_tree.selection()

        if not selected:
            return

        item = self.category_tree.item(selected[0])
        category_name = item["values"][1]

        self.category_name_entry.delete(0, tk.END)
        self.category_name_entry.insert(0, category_name)

    def add_category_from_gui(self):
        name = self.category_name_entry.get()

        try:
            validate_category_name(name)

            if self.category_name_taken(name):
                raise ValueError("A category with that name already exists.")

            add_category(name.strip())

        except ValueError as error:
            messagebox.showerror("Invalid category", str(error))
            return

        self.category_name_entry.delete(0, tk.END)
        self.refresh_categories()

    def update_category_from_gui(self):
        selected = self.category_tree.selection()

        if not selected:
            messagebox.showwarning("No category selected", "Select a category to update.")
            return

        category_id = int(selected[0])
        new_name = self.category_name_entry.get()

        try:
            validate_category_name(new_name)

            if self.category_name_taken(new_name, ignore_id=category_id):
                raise ValueError("A category with that name already exists.")

            update_category(category_id, new_name.strip())

        except ValueError as error:
            messagebox.showerror("Invalid category", str(error))
            return

        self.refresh_categories()

    def delete_category_from_gui(self):
        selected = self.category_tree.selection()

        if not selected:
            messagebox.showwarning("No category selected", "Select a category to delete.")
            return

        category_id = int(selected[0])

        confirmed = messagebox.askyesno(
            "Delete category",
            "Are you sure you want to delete this category?"
        )

        if not confirmed:
            return

        try:
            delete_category(category_id)

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Cannot delete category",
                "This category is still used by transactions or budgets."
            )
            return

        self.category_name_entry.delete(0, tk.END)
        self.refresh_categories()

    # ---------------------------------------------------------
    # Transactions
    # ---------------------------------------------------------

    def show_transactions(self):
        self.clear_content()

        ttk.Label(self.content, text="Transactions", font=("Arial", 20)).pack(pady=(10, 20))

        # Form
        form = ttk.Frame(self.content)
        form.pack(fill="x", pady=10)

        # Category
        ttk.Label(form, text="Category:").grid(row=0, column=0, padx=5, pady=5)
        self.transaction_category = ttk.Combobox(form, state="readonly")
        self.transaction_category.grid(row=0, column=1, padx=5, pady=5)

        # Amount
        ttk.Label(form, text="Amount (pence):").grid(row=0, column=2, padx=5, pady=5)
        self.transaction_amount_entry = ttk.Entry(form)
        self.transaction_amount_entry.grid(row=0, column=3, padx=5, pady=5)

        # Date
        ttk.Label(form, text="Date:").grid(row=1, column=0, padx=5, pady=5)
        self.transaction_date_entry = ttk.Entry(form)
        self.transaction_date_entry.grid(row=1, column=1, padx=5, pady=5)
        self.transaction_date_entry.insert(0, date.today().isoformat())

        # Description
        ttk.Label(form, text="Description:").grid(row=1, column=2, padx=5, pady=5)
        self.transaction_description_entry = ttk.Entry(form)
        self.transaction_description_entry.grid(row=1, column=3, padx=5, pady=5)

        # Buttons
        ttk.Button(form, text="Add", command=self.add_transaction_from_gui).grid(row=2, column=0, padx=5, pady=10)
        ttk.Button(form, text="Update", command=self.update_transaction_from_gui).grid(row=2, column=1, padx=5, pady=10)
        ttk.Button(form, text="Delete", command=self.delete_transaction_from_gui).grid(row=2, column=2, padx=5, pady=10)

        # Transaction table
        self.transaction_tree = ttk.Treeview(
            self.content,
            columns=("id", "category", "amount", "date", "description"),
            show="headings"
        )

        self.transaction_tree.heading("id", text="ID")
        self.transaction_tree.heading("category", text="Category")
        self.transaction_tree.heading("amount", text="Amount")
        self.transaction_tree.heading("date", text="Date")
        self.transaction_tree.heading("description", text="Description")

        self.transaction_tree.column("id", width=50)
        self.transaction_tree.column("category", width=120)
        self.transaction_tree.column("amount", width=100)
        self.transaction_tree.column("date", width=100)
        self.transaction_tree.column("description", width=250)

        self.transaction_tree.pack(fill="both", expand=True, pady=10)
        self.transaction_tree.bind("<<TreeviewSelect>>", self.select_transaction)

        self.refresh_transaction_categories()
        self.refresh_transactions()

    def refresh_transaction_categories(self):
        categories = get_categories()

        self.category_lookup = {
            category.name: category.id
            for category in categories
        }

        self.transaction_category["values"] = list(self.category_lookup.keys())

        if categories:
            self.transaction_category.current(0)
        else:
            self.transaction_category.set("")

    def refresh_transactions(self):
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)

        categories = {
            category.id: category.name
            for category in get_categories()
        }

        for transaction in get_transactions():
            category_name = categories.get(transaction.category_id, "Unknown")
            amount = f"£{transaction.amount / 100:.2f}"

            self.transaction_tree.insert(
                "",
                "end",
                iid=str(transaction.id),
                values=(
                    transaction.id,
                    category_name,
                    amount,
                    transaction.date,
                    transaction.description or ""
                )
            )

    def select_transaction(self, event=None):
        selected = self.transaction_tree.selection()

        if not selected:
            return

        transaction_id = int(selected[0])

        transaction = next(
            (t for t in get_transactions() if t.id == transaction_id),
            None
        )

        if transaction is None:
            return

        category_names = {
            category.id: category.name
            for category in get_categories()
        }

        category_name = category_names.get(transaction.category_id)

        if category_name in self.category_lookup:
            self.transaction_category.set(category_name)

        self.transaction_amount_entry.delete(0, tk.END)
        self.transaction_amount_entry.insert(0, str(transaction.amount))

        self.transaction_date_entry.delete(0, tk.END)
        self.transaction_date_entry.insert(0, transaction.date)

        self.transaction_description_entry.delete(0, tk.END)
        self.transaction_description_entry.insert(0, transaction.description or "")

    def get_transaction_form_data(self):
        category_name = self.transaction_category.get()
        amount_text = self.transaction_amount_entry.get()
        transaction_date = self.transaction_date_entry.get()
        description = self.transaction_description_entry.get()

        if not self.category_lookup:
            raise ValueError("Create a category first (Categories screen).")

        if category_name not in self.category_lookup:
            raise ValueError("Please select a category.")

        try:
            amount = int(amount_text)
        except ValueError:
            raise ValueError("Amount must be a whole number of pence.")

        validate_amount(amount)
        validate_date(transaction_date)

        category_id = self.category_lookup[category_name]

        return (category_id, amount, transaction_date, description)

    def add_transaction_from_gui(self):
        try:
            (
                category_id,
                amount,
                transaction_date,
                description
            ) = self.get_transaction_form_data()

            add_transaction(category_id, amount, transaction_date, description)

        except ValueError as error:
            messagebox.showerror("Invalid transaction", str(error))
            return

        self.refresh_transactions()

        self.transaction_amount_entry.delete(0, tk.END)
        self.transaction_description_entry.delete(0, tk.END)

    def update_transaction_from_gui(self):
        selected = self.transaction_tree.selection()

        if not selected:
            messagebox.showwarning("No transaction selected", "Select a transaction to update.")
            return

        transaction_id = int(selected[0])

        try:
            (
                category_id,
                amount,
                transaction_date,
                description
            ) = self.get_transaction_form_data()

            update_transaction(
                transaction_id,
                category_id,
                amount,
                transaction_date,
                description
            )

        except ValueError as error:
            messagebox.showerror("Invalid transaction", str(error))
            return

        self.refresh_transactions()

    def delete_transaction_from_gui(self):
        selected = self.transaction_tree.selection()

        if not selected:
            messagebox.showwarning("No transaction selected", "Select a transaction to delete.")
            return

        transaction_id = int(selected[0])

        confirmed = messagebox.askyesno(
            "Delete transaction",
            "Are you sure you want to delete this transaction?"
        )

        if not confirmed:
            return

        delete_transaction(transaction_id)

        self.refresh_transactions()

        self.transaction_amount_entry.delete(0, tk.END)
        self.transaction_description_entry.delete(0, tk.END)

    # ---------------------------------------------------------
    # Budgets
    # ---------------------------------------------------------

    def show_budgets(self):
        self.clear_content()

        ttk.Label(self.content, text="Budgets", font=("Arial", 20)).pack(pady=(10, 20))

        # Form
        form = ttk.Frame(self.content)
        form.pack(fill="x", pady=10)

        # Category
        ttk.Label(form, text="Category:").grid(row=0, column=0, padx=5, pady=5)
        self.budget_category = ttk.Combobox(form, state="readonly")
        self.budget_category.grid(row=0, column=1, padx=5, pady=5)

        # Amount
        ttk.Label(form, text="Amount (pence):").grid(row=0, column=2, padx=5, pady=5)
        self.budget_amount_entry = ttk.Entry(form)
        self.budget_amount_entry.grid(row=0, column=3, padx=5, pady=5)

        # Period
        ttk.Label(form, text="Period:").grid(row=1, column=0, padx=5, pady=5)
        self.budget_period = ttk.Combobox(form, state="readonly", values=valid_periods)
        self.budget_period.grid(row=1, column=1, padx=5, pady=5)
        self.budget_period.current(1)  # default: monthly

        # Buttons
        ttk.Button(form, text="Add", command=self.add_budget_from_gui).grid(row=2, column=0, padx=5, pady=10)
        ttk.Button(form, text="Update", command=self.update_budget_from_gui).grid(row=2, column=1, padx=5, pady=10)
        ttk.Button(form, text="Delete", command=self.delete_budget_from_gui).grid(row=2, column=2, padx=5, pady=10)

        # Budget table
        self.budget_tree = ttk.Treeview(
            self.content,
            columns=("id", "category", "amount", "period"),
            show="headings"
        )

        self.budget_tree.heading("id", text="ID")
        self.budget_tree.heading("category", text="Category")
        self.budget_tree.heading("amount", text="Budget")
        self.budget_tree.heading("period", text="Period")

        self.budget_tree.column("id", width=50)
        self.budget_tree.column("category", width=150)
        self.budget_tree.column("amount", width=100)
        self.budget_tree.column("period", width=100)

        self.budget_tree.pack(fill="both", expand=True, pady=10)
        self.budget_tree.bind("<<TreeviewSelect>>", self.select_budget)

        self.refresh_budget_categories()
        self.refresh_budgets()

    def refresh_budget_categories(self):
        categories = get_categories()

        self.budget_category_lookup = {
            category.name: category.id
            for category in categories
        }

        self.budget_category["values"] = list(self.budget_category_lookup.keys())

        if categories:
            self.budget_category.current(0)
        else:
            self.budget_category.set("")

    def refresh_budgets(self):
        for item in self.budget_tree.get_children():
            self.budget_tree.delete(item)

        categories = {
            category.id: category.name
            for category in get_categories()
        }

        for budget in get_budgets():
            category_name = categories.get(budget.category_id, "Unknown")
            amount = f"£{budget.amount / 100:.2f}"

            self.budget_tree.insert(
                "",
                "end",
                iid=str(budget.id),
                values=(budget.id, category_name, amount, budget.period)
            )

    def select_budget(self, event=None):
        selected = self.budget_tree.selection()

        if not selected:
            return

        budget_id = int(selected[0])

        budget = next(
            (b for b in get_budgets() if b.id == budget_id),
            None
        )

        if budget is None:
            return

        category_names = {
            category.id: category.name
            for category in get_categories()
        }

        category_name = category_names.get(budget.category_id)

        if category_name in self.budget_category_lookup:
            self.budget_category.set(category_name)

        self.budget_amount_entry.delete(0, tk.END)
        self.budget_amount_entry.insert(0, str(budget.amount))

        self.budget_period.set(budget.period)

    def budget_exists(self, category_id, period, ignore_id=None):
        # One budget per category per period, otherwise the totals
        # we build later would be ambiguous.
        for budget in get_budgets():
            if (
                budget.category_id == category_id
                and budget.period == period
                and budget.id != ignore_id
            ):
                return True

        return False

    def get_budget_form_data(self):
        category_name = self.budget_category.get()
        amount_text = self.budget_amount_entry.get()
        period = self.budget_period.get()

        if not self.budget_category_lookup:
            raise ValueError("Create a category first (Categories screen).")

        if category_name not in self.budget_category_lookup:
            raise ValueError("Please select a category.")

        try:
            amount = int(amount_text)
        except ValueError:
            raise ValueError("Amount must be a whole number of pence.")

        validate_amount(amount)

        if period not in valid_periods:
            raise ValueError("Please select a period.")

        category_id = self.budget_category_lookup[category_name]

        return (category_id, amount, period)

    def add_budget_from_gui(self):
        try:
            category_id, amount, period = self.get_budget_form_data()

            if self.budget_exists(category_id, period):
                raise ValueError(f"That category already has a {period} budget.")

            add_budget(category_id, amount, period)

        except ValueError as error:
            messagebox.showerror("Invalid budget", str(error))
            return

        self.refresh_budgets()
        self.budget_amount_entry.delete(0, tk.END)

    def update_budget_from_gui(self):
        selected = self.budget_tree.selection()

        if not selected:
            messagebox.showwarning("No budget selected", "Select a budget to update.")
            return

        budget_id = int(selected[0])
        try:
            category_id, amount, period = self.get_budget_form_data()

            if self.budget_exists(category_id, period, ignore_id=budget_id):
                raise ValueError(f"That category already has a {period} budget.")

            update_budget(budget_id, category_id, amount, period)

        except ValueError as error:
            messagebox.showerror("Invalid budget", str(error))
            return

        self.refresh_budgets()

    def delete_budget_from_gui(self):
        selected = self.budget_tree.selection()

        if not selected:
            messagebox.showwarning("No budget selected", "Select a budget to delete.")
            return

        budget_id = int(selected[0])

        confirmed = messagebox.askyesno(
            "Delete budget",
            "Are you sure you want to delete this budget?"
        )

        if not confirmed:
            return

        delete_budget(budget_id)

        self.refresh_budgets()
        self.budget_amount_entry.delete(0, tk.END)


def main():
    create_database()

    app = FinanceApp()
    app.mainloop()


if __name__ == "__main__":
    main()