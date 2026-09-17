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
