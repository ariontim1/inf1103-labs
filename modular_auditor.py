# 1. Initialize the inventory and counter to zero at the start
total_inventory = 0
failed_entries = 0

# 2. Run in a continuous loop asking the user for input
while True:
    user_input = input("Enter a stock quantity (or type 'quit' to exit): ").strip()

    # Check if the user wants to exit
    if user_input.lower() == 'quit':
        break

    # 5. Enforce business rules: Reject negative numbers
    # A negative integer starts with '-' followed by digits
    if user_input.startswith('-') and user_input[1:].isdigit():
        print("Error: Negative numbers are not allowed.")
        failed_entries += 1
        continue

    # 4. Handle invalid input: Reject strings/decimals using .isdigit()
    elif not user_input.isdigit():
        print("Error: Invalid input. Please enter a valid whole number.")
        failed_entries += 1
        continue

    # 3. Accept stock values as integers
    else:
        stock_quantity = int(user_input)
        
        # 6. Manage State: Keep a running total of the inventory
        total_inventory += stock_quantity

        # 7. Trigger Overstock Alert: If total inventory exceeds 500, alert and break immediately
        if total_inventory > 500:
            print("ALERT: Overstock limits exceeded! Total inventory is over 500 units.")
            break

# 8. Reporting: Print final summary statistics
print("\n--- Audit Report ---")
print(f"Total Units Processed: {total_inventory}")
print(f"Number of Failed/Rejected Entries: {failed_entries}")