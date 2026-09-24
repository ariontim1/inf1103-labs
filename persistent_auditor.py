def get_valid_input():
    """
    Handles the prompt, input validation, and business rules.
    Returns a valid integer, a "quit" signal, or None for invalid inputs.
    """
    user_input = input("Enter a stock quantity (or type 'quit' to exit): ").strip()

    # Check if the user wants to exit
    if user_input.lower() == 'quit':
        return 'quit'

    # Enforce business rules: Reject negative numbers
    if user_input.startswith('-') and user_input[1:].isdigit():
        print("Error: Negative numbers are not allowed.")
        return None

    # Handle invalid input: Reject strings/decimals using .isdigit()
    elif not user_input.isdigit():
        print("Error: Invalid input. Please enter a valid whole number.")
        return None

    # Accept stock values as integers
    else:
        return int(user_input)

def process_delivery(current_total, new_value):
    """
    Calculates the new total and returns it.
    """
    return current_total + new_value

def calculate_tax(amount):
    """
    Takes a delivery amount and returns the tax (10% of that specific delivery).
    """
    return amount * 0.10

def generate_report(total_units, failed_attempts):
    """
    A dedicated function to print the final summary.
    """
    print("\n--- Audit Summary Report ---")
    print(f"Total Units Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")

def main():
    # Initialize the inventory and counters to zero at the start
    total_inventory = 0
    failed_entries = 0

    # Run in a continuous loop
    while True:
        result = get_valid_input()

        # Route 1: User requested to exit
        if result == 'quit':
            break

        # Route 2: Input was bad/negative (Increment failed entries counter)
        elif result is None:
            failed_entries += 1
            continue

        # Route 3: Input is valid
        else:
            stock_quantity = result
            
            # Calculate and display the tax for this specific delivery
            tax = calculate_tax(stock_quantity)
            print(f"Delivery tax (10%): {tax:.2f}")

            # Update the state of our running total inventory
            total_inventory = process_delivery(total_inventory, stock_quantity)

            # Trigger Overstock Alert: If total inventory exceeds 500, alert and break immediately
            if total_inventory > 500:
                print(f"ALERT: Overstock limits exceeded! Total inventory is over 500 units ({total_inventory}).")
                break

    # After exiting the loop, print the final summary statistics
    generate_report(total_inventory, failed_entries)


# This line ensures the program executes cleanly when you run the script file
if __name__ == "__main__":
    main()
