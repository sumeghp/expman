import tkinter as tk
from tkinter import ttk
from datetime import datetime
import csv
import os

class ExpenseManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Manager")

        # Expense data
        self.expenses = []

        # GUI elements
        self.category_var = tk.StringVar()
        self.amount_var = tk.DoubleVar()
        self.description_var = tk.StringVar()

        # Labels
        ttk.Label(root, text="Category:").grid(column=0, row=0, padx=10, pady=10, sticky=tk.W)
        ttk.Label(root, text="Amount:").grid(column=0, row=1, padx=10, pady=10, sticky=tk.W)
        ttk.Label(root, text="Description:").grid(column=0, row=2, padx=10, pady=10, sticky=tk.W)

        # Entry widgets
        self.category_entry = ttk.Entry(root, textvariable=self.category_var)
        self.category_entry.grid(column=1, row=0, padx=10, pady=10, sticky=tk.W)

        self.amount_entry = ttk.Entry(root, textvariable=self.amount_var)
        self.amount_entry.grid(column=1, row=1, padx=10, pady=10, sticky=tk.W)

        self.description_entry = ttk.Entry(root, textvariable=self.description_var)
        self.description_entry.grid(column=1, row=2, padx=10, pady=10, sticky=tk.W)

        # Button to add expense
        ttk.Button(root, text="Add Expense", command=self.add_expense).grid(column=0, row=3, columnspan=2, pady=10)

        # Display expenses
        self.tree = ttk.Treeview(root, columns=("Timestamp", "Category", "Amount", "Description"), show="headings")
        self.tree.heading("Timestamp", text="Timestamp")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Description", text="Description")
        self.tree.grid(column=0, row=4, columnspan=2, padx=10, pady=10)

        # Load existing expenses from CSV file
        self.load_expenses_from_file("expenses.csv")

        # Debug information
        print("Current working directory:", os.getcwd())

    def add_expense(self):
        category = self.category_var.get()
        amount = self.amount_var.get()
        description = self.description_var.get()

        if category and amount:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            expense = (timestamp, category, amount, description)
            self.expenses.append(expense)

            # Update the Treeview
            self.tree.insert("", "end", values=expense)

            # Save expenses to CSV file after adding a new expense
            self.save_expenses_to_file("expenses.csv")

            # Clear entry fields
            self.category_var.set("")
            self.amount_var.set(0.0)
            self.description_var.set("")

    def save_expenses_to_file(self, filename):
        full_path = os.path.join(os.path.dirname(__file__), filename)
        with open(full_path, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(["Timestamp", "Category", "Amount", "Description"])
            # Write each expense
            for expense in self.expenses:
                writer.writerow(expense)

    def load_expenses_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                # Skip the header
                next(reader, None)
                # Load each expense
                self.expenses = [tuple(row) for row in reader]
                # Update the Treeview with loaded expenses
                for expense in self.expenses:
                    self.tree.insert("", "end", values=expense)
        except FileNotFoundError:
            pass

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseManagerGUI(root)
    root.mainloop()

