import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).parent / "transactions.json"


def load_transactions():
    """Load saved transactions from the JSON file."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            transactions = json.load(file)

        if not isinstance(transactions, list):
            print("Warning: Invalid transaction data.")
            return []

        return transactions

    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read transaction data.")
        return []


def save_transactions(transactions):
    """Save transactions to the JSON file."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(transactions, file, indent=4)

        return True

    except OSError:
        print("Error: Could not save your transactions.")
        return False


def get_amount():
    """Ask for a valid positive monetary amount."""
    while True:
        try:
            amount = float(input("Enter amount (KES): "))

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            if not amount < float("inf"):
                print("Please enter a valid finite amount.")
                continue

            return round(amount, 2)

        except ValueError:
            print("Please enter a valid number.")


def add_transaction(transactions):
    """Record a new income or expense."""
    print("\n--- Add Transaction ---")
    print("1. Income")
    print("2. Expense")

    choice = input("Choose transaction type: ").strip()

    if choice not in ("1", "2"):
        print("Invalid transaction type.")
        return

    amount = get_amount()

    category = input("Enter category: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    description = input("Enter description: ").strip()

    transaction = {
        "id": max(
            (item.get("id", 0) for item in transactions),
            default=0
        ) + 1,
        "type": "Income" if choice == "1" else "Expense",
        "amount": amount,
        "category": category.title(),
        "description": description or "No description",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    transactions.append(transaction)

    if save_transactions(transactions):
        print("\nTransaction saved successfully!")
        print(f"Transaction ID: {transaction['id']}")


def view_transactions(transactions):
    """Display all recorded transactions."""
    print("\n--- Transaction History ---")

    if not transactions:
        print("No transactions recorded yet.")
        return

    print("-" * 85)
    print(
        f"{'ID':<5}{'Type':<12}{'Amount (KES)':<16}"
        f"{'Category':<18}{'Date':<22}"
    )
    print("-" * 85)

    for transaction in transactions:
        print(
            f"{transaction['id']:<5}"
            f"{transaction['type']:<12}"
            f"{transaction['amount']:<16.2f}"
            f"{transaction['category']:<18}"
            f"{transaction['date']:<22}"
        )
        print(f"     Description: {transaction['description']}")

    print("-" * 85)


def view_summary(transactions):
    """Calculate income, expenses and remaining balance."""
    total_income = sum(
        item["amount"]
        for item in transactions
        if item["type"] == "Income"
    )

    total_expenses = sum(
        item["amount"]
        for item in transactions
        if item["type"] == "Expense"
    )

    balance = total_income - total_expenses

    print("\n--- Financial Summary ---")
    print(f"Total income:    KES {total_income:,.2f}")
    print(f"Total expenses:  KES {total_expenses:,.2f}")
    print(f"Current balance: KES {balance:,.2f}")

    if balance < 0:
        print("Warning: Your recorded expenses exceed your income!")


def search_by_category(transactions):
    """Find transactions matching a category."""
    print("\n--- Search Transactions ---")

    category = input("Enter category to search: ").strip().casefold()

    if not category:
        print("Please enter a category.")
        return

    matches = [
        item for item in transactions
        if category in item["category"].casefold()
    ]

    if not matches:
        print("No matching transactions found.")
        return

    print(f"\nFound {len(matches)} matching transaction(s):")

    for item in matches:
        print(
            f"ID: {item['id']} | "
            f"{item['type']} | "
            f"KES {item['amount']:.2f} | "
            f"{item['category']} | "
            f"{item['description']}"
        )


def delete_transaction(transactions):
    """Delete a transaction using its ID."""
    print("\n--- Delete Transaction ---")

    if not transactions:
        print("There are no transactions to delete.")
        return

    view_transactions(transactions)

    try:
        transaction_id = int(input("\nEnter transaction ID to delete: "))
    except ValueError:
        print("Please enter a valid transaction ID.")
        return

    transaction = next(
        (
            item for item in transactions
            if item["id"] == transaction_id
        ),
        None
    )

    if transaction is None:
        print("Transaction not found.")
        return

    confirmation = input(
        f"Delete '{transaction['description']}'? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":
        print("Deletion cancelled.")
        return

    updated_transactions = [
        item for item in transactions
        if item["id"] != transaction_id
    ]

    if save_transactions(updated_transactions):
        transactions[:] = updated_transactions
        print("Transaction deleted successfully!")


def display_menu():
    """Display the main menu."""
    print("\n" + "=" * 35)
    print("       POCKETLEDGER")
    print("   Personal Finance Tracker")
    print("=" * 35)
    print("1. Add income or expense")
    print("2. View transaction history")
    print("3. View financial summary")
    print("4. Search by category")
    print("5. Delete a transaction")
    print("6. Exit")
    print("=" * 35)


def main():
    transactions = load_transactions()

    print("\nWelcome to PocketLedger!")
    print("Take control of your money, one transaction at a time.")

    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_transaction(transactions)

        elif choice == "2":
            view_transactions(transactions)

        elif choice == "3":
            view_summary(transactions)

        elif choice == "4":
            search_by_category(transactions)

        elif choice == "5":
            delete_transaction(transactions)

        elif choice == "6":
            print("\nThank you for using PocketLedger. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a number from 1 to 6.")


if __name__ == "__main__":
    main()