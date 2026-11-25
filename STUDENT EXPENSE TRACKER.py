DATA_FILE = Path(__file__).with_name("expenses.csv")
FIELDS = ["date", "category", "description", "amount"]
CATEGORIES = ("Food", "Travel", "Study", "Personal", "Other")
 
 
def load_expenses(path=DATA_FILE):
    """Load expense rows from CSV, returning an empty list when absent."""
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as file:
        rows = []
        for row in csv.DictReader(file):
            try:
                amount = float(row["amount"])
                date.fromisoformat(row["date"])
                if not math.isfinite(amount) or amount <= 0 or row["category"] not in CATEGORIES:
                    continue
                rows.append({**row, "amount": amount})
            except (ValueError, KeyError, TypeError):
                continue
        return rows
 
 
def save_expenses(expenses, path=DATA_FILE):
    """Save all expenses to a CSV file."""
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        for expense in expenses:
            writer.writerow({**expense, "amount": f"{expense['amount']:.2f}"})
 
 
def add_expense(expenses):
    """Collect and append one validated expense."""
    try:
        entry_date = input("Date (YYYY-MM-DD, blank for today): ").strip()
        entry_date = entry_date or date.today().isoformat()
        date.fromisoformat(entry_date)
        print("Categories:", ", ".join(CATEGORIES))
        category = input("Category: ").strip().title()
        if category not in CATEGORIES:
            print("Unknown category. Choose one from the list.")
            return
        description = input("Description: ").strip()
        if not description:
            print("Description cannot be empty.")
            return
        amount = float(input("Amount (₹): "))
        if not math.isfinite(amount) or amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Invalid date or amount. Expense was not added.")
        return
 
    expenses.append({"date": entry_date, "category": category,
                     "description": description, "amount": amount})
    save_expenses(expenses)
    print("Expense saved.")
 
 
def show_expenses(expenses):
    """Display all entries in a readable table."""
    if not expenses:
        print("No expenses recorded.")
        return
    print(f"{'#':<4}{'Date':<13}{'Category':<12}{'Description':<28}{'Amount (₹)':>12}")
    print("-" * 69)
    for number, item in enumerate(expenses, start=1):
        print(f"{number:<4}{item['date']:<13}{item['category']:<12}"
              f"{item['description'][:26]:<28}{item['amount']:>12.2f}")
    print(f"{'Total':<57}{sum(x['amount'] for x in expenses):>12.2f}")
 
 
def show_summary(expenses):
    """Calculate total and category-wise spending."""
    if not expenses:
        print("No expenses to summarize.")
        return
    totals = {}
    for item in expenses:
        totals[item["category"]] = totals.get(item["category"], 0) + item["amount"]
    print(f"Total spending: ₹{sum(totals.values()):.2f}")
    for category in CATEGORIES:
        if category in totals:
            print(f"{category:<10} ₹{totals[category]:.2f}")
 
 
def delete_expense(expenses):
    """Delete a selected expense by its displayed number."""
    if not expenses:
        print("No expenses to delete.")
        return
    show_expenses(expenses)
    try:
        number = int(input("Enter the entry number to delete: "))
        if number < 1 or number > len(expenses):
            print("Entry number is outside the list.")
            return
    except ValueError:
        print("Enter a whole number.")
        return
    removed = expenses.pop(number - 1)
    save_expenses(expenses)
    print(f"Deleted {removed['description']} (₹{removed['amount']:.2f}).")
 
 
def import_csv(expenses):
    """Import rows from a user-specified CSV file."""
    filename = input("CSV filename to import: ").strip().strip('"')
    path = Path(filename)
    if not path.is_absolute():
        path = Path(__file__).parent / path
    imported = load_expenses(path)
    if not imported:
        print("No valid rows found. Expected date,category,description,amount.")
        return
    expenses.extend(imported)
    save_expenses(expenses)
    print(f"Imported {len(imported)} expense(s).")
 
 
def main():
    expenses = load_expenses()
    actions = {"1": add_expense, "2": show_expenses,
               "3": show_summary, "4": delete_expense,
               "6": import_csv}
    while True:
        print("\nSTUDENT EXPENSE TRACKER")
        print("1. Add expense  2. View expenses  3. Summary")
        print("4. Delete expense  5. Exit  6. Import CSV")
        choice = input("Choose an option: ").strip()
        if choice == "5":
            print("Data saved. Goodbye.")
            break
        action = actions.get(choice)
        if action:
            action(expenses)
        else:
            print("Invalid option. Choose 1 to 6.")
 
 
if __name__ == "__main__":
    main()
