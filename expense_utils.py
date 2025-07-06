import csv
import datetime

def add_expense_details():
    """
    Allow the user to enter multiple expenses in one go.
    Returns a list of expense dictionaries.
    """
    expenses = []
    while True:
        while True:
            date = input("Enter the date of the expense (YYYY-MM-DD): ")
            try:
                datetime.datetime.strptime(date, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
                date = input("Enter the date of the expense (YYYY-MM-DD): ")
        category = input("Enter the category of the expense (e.g., Food, Travel): ")
        amount = input("Enter the amount spent: ")
        while True:
            try:
                float(amount)
                break
            except ValueError:
                print("Invalid input. Please enter a numeric value for the amount.")
                amount = input("Enter the amount spent: ")
        description = input("Enter a brief description of the expense: ")
        expenses.append({
            "date": date,
            "category": category,
            "amount": amount,
            "description": description
        })
        more = input("Add another expense? (y/n): ").strip().lower()
        if more != 'y':
            break
    return expenses

def display_all_expenses(expenses):
    """
    Display all stored expenses with date, category, amount, and description.
    :param expenses: List of expense dictionaries.
    """
    if not expenses:
        print("No expenses to display.")
        return
    for idx, expense in enumerate(expenses, 1):
        # Validate required fields
        date = expense.get('date')
        category = expense.get('category')
        amount = expense.get('amount')
        description = expense.get('description')
        if not all([date, category, amount, description]):
            print(f"Expense {idx} is incomplete and will be skipped.")
            continue
        print(f"Expense {idx}:")
        print(f"  Date       : {date}")
        print(f"  Category   : {category}")
        print(f"  Amount     : {amount}")
        print(f"  Description: {description}")
        print("-" * 30)

def input_monthly_budget():
    """
    Prompt the user to enter the total amount they want to budget for the month.
    Returns the budget as a float.
    """
    while True:
        budget_input = input("Enter your total monthly budget amount: ")
        try:
            budget = float(budget_input)
            if budget < 0:
                print("Budget cannot be negative. Please enter a valid amount.")
                continue
            return budget
        except ValueError:
            print("Invalid input. Please enter a numeric value for the budget.")

def check_budget_status(expenses, monthly_budget):
    """
    Calculate total expenses and compare with the user's monthly budget.
    Display a warning if the budget is exceeded, otherwise show remaining balance.
    :param expenses: List of expense dictionaries.
    :param monthly_budget: User's monthly budget (float).
    """
    total = 0.0
    for expense in expenses:
        if not isinstance(expense, dict):
            print("Warning: Skipping invalid expense entry (not a dictionary).")
            continue
        try:
            amount = float(expense.get('amount', 0))
        except (ValueError, TypeError):
            continue  # Skip invalid amounts
        total += amount
    print(f"Total expenses so far: {total}")
    if total > monthly_budget:
        print("You have exceeded your budget!")
    else:
        remaining = monthly_budget - total
        print(f"You have {remaining} left for the month.")

def save_expenses_to_csv(expenses, filename):
    """
    Save all expenses to a CSV file, with each row containing date, category, amount, and description.
    :param expenses: List of expense dictionaries.
    :param filename: Name of the CSV file to save expenses to.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['Date', 'Category', 'Amount', 'Description'])
        for expense in expenses:
            date = expense.get('date', '')
            category = expense.get('category', '')
            amount = expense.get('amount', '')
            description = expense.get('description', '')
            writer.writerow([date, category, amount, description])
    print(f"Expenses have been saved to {filename}.")

def load_expenses_from_csv(filename):
    """
    Load expenses from a CSV file and return a list of expense dictionaries.
    :param filename: Name of the CSV file to load expenses from.
    :return: List of expense dictionaries.
    """

    expenses = []
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                expenses.append({
                    'date': row.get('Date', ''),
                    'category': row.get('Category', ''),
                    'amount': row.get('Amount', ''),
                    'description': row.get('Description', '')
                })
    except FileNotFoundError:
        pass  # No file exists yet, return empty list
    return expenses

def main_menu():
    """
    Display a menu for the user to choose actions.
    Returns the user's choice as an integer (1-5).
    """
    while True:
        print("\nPersonal Expense Tracker Menu:")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Track budget")
        print("4. Save expenses")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ").strip()
        if choice in {'1', '2', '3', '4', '5'}:
            return int(choice)
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

def run_expense_tracker():
    """
    Main loop to run the expense tracker menu and handle user choices.
    """
    expenses = load_expenses_from_csv("expenses.csv")
    budget = None
    while True:
        choice = main_menu()
        if choice == 1:
            new_expenses = add_expense_details()
            if new_expenses:
                expenses.extend(new_expenses)
        elif choice == 2:
            display_all_expenses(expenses)
        elif choice == 3:
            if budget is None:
                budget = input_monthly_budget()
            check_budget_status(expenses, budget)
        elif choice == 4:
            save_expenses_to_csv(expenses, "expenses.csv")
        elif choice == 5:
            save_expenses_to_csv(expenses, "expenses.csv")
            print("Exiting. Your expenses have been saved.")
            break