import sqlite3

# Connect to database
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    amount REAL,
    category TEXT
)
""")
conn.commit()

while True:
    print("\n===== Smart AI Expense Tracker =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Total Spending")
    print("4. Delete Expense")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Expense Name: ")
        amount = float(input("Amount (₹): "))

        text = name.lower()

        if any(word in text for word in ["pizza", "burger", "food", "restaurant"]):
            category = "Food"
        elif any(word in text for word in ["uber", "bus", "metro", "taxi"]):
            category = "Transport"
        elif any(word in text for word in ["movie", "game"]):
            category = "Entertainment"
        elif any(word in text for word in ["book", "school", "college"]):
            category = "Education"
        else:
            category = "Other"

        cursor.execute(
            "INSERT INTO expenses(name, amount, category) VALUES(?,?,?)",
            (name, amount, category)
        )
        conn.commit()

        print("\n✅ Expense Saved!")
        print("AI Category:", category)

    elif choice == "2":
        cursor.execute("SELECT * FROM expenses")
        rows = cursor.fetchall()

        if not rows:
            print("\nNo expenses found.")
        else:
            print("\nID | Name | Amount | Category")
            print("-" * 40)
            for row in rows:
                print(f"{row[0]} | {row[1]} | ₹{row[2]} | {row[3]}")

    elif choice == "3":
        cursor.execute("SELECT SUM(amount) FROM expenses")
        total = cursor.fetchone()[0]

        if total is None:
            total = 0

        print(f"\nTotal Spending: ₹{total}")

        if total > 5000:
            print("🤖 AI Tip: Your spending is high. Try reducing unnecessary expenses.")
        else:
            print("🤖 AI Tip: Great job! Keep tracking your expenses.")

    elif choice == "4":
        expense_id = input("Enter Expense ID to delete: ")

        cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        conn.commit()

        print("🗑 Expense Deleted!")

    elif choice == "5":
        print("Goodbye!")
        conn.close()
        break

    else:
        print("Invalid Choice!")