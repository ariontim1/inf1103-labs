import json
import os

FILENAME = "inventory.json"


def load_inventory(filename=FILENAME):
    """Loads inventory data from inventory.json if present, or sets default products."""
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                inventory = json.load(file)
                print(f"{filename} found.")
                print("Inventory loaded successfully.")
                return inventory
        except Exception as e:
            print(f"Error loading {filename}: {e}")

    # Initial default products if inventory.json does not exist
    print(f"{filename} not found. Initializing with default products.")
    return {
        "P001": {"name": "Laptop", "price": 1200.00, "stock": 15},
        "P002": {"name": "Mouse", "price": 25.50, "stock": 40},
        "P003": {"name": "Keyboard", "price": 45.00, "stock": 25},
    }

def save_inventory(inventory, filename=FILENAME):
    """Saves the current inventory dictionary to inventory.json."""
    try:
        with open(filename, "w") as file:
            json.dump(inventory, file, indent=4)
        print(f"Inventory saved successfully to {filename}.")
    except Exception as e:
        print(f"Error saving to {filename}: {e}")

def display_all(inventory):
    """Displays all products stored in the inventory dictionary."""
    print("\nCurrent Inventory")
    print("-" * 40)
    if not inventory:
        print("Inventory is currently empty.")
    else:
        for product_id, details in inventory.items():
            print(
                f"ID: {product_id} | Name: {details['name']} | "
                f"Price: ${details['price']:.2f} | Stock: {details['stock']}"
            )
    print("-" * 40)

def add_product(inventory):
    """Prompts for new product attributes and adds it to the inventory dictionary."""
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()

    if product_id in inventory:
        print("Error: Product ID already exists.")
        return

    name = input("Product Name: ").strip()

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid price or stock quantity input.")
        return

    inventory[product_id] = {"name": name, "price": price, "stock": stock}
    print("\nProduct added successfully!")


def update_stock(inventory):
    """Updates the stock quantity of an existing product."""
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()

    if product_id in inventory:
        product = inventory[product_id]
        print("\nProduct Found:")
        print(f"Name: {product['name']}")
        print(f"Current Stock: {product['stock']}\n")

        try:
            new_stock = int(input("New Stock Quantity: "))
            product["stock"] = new_stock
            print("\nStock updated successfully!")
        except ValueError:
            print("Error: Stock must be a valid integer.")
    else:
        print("\nProduct not found.")


def search_product(inventory):
    """Searches and displays a specific product by its ID."""
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    if product_id in inventory:
        product = inventory[product_id]
        print("\nProduct Found")
        print("-" * 40)
        print(f"ID: {product_id}")
        print(f"Name: {product['name']}")
        print(f"Price: ${product['price']:.2f}")
        print(f"Stock: {product['stock']}")
    else:
        print("\nProduct not found.")


def display_menu():
    """Prints the main user interface menu options."""
    print("\n--------- MENU ---------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("------------------------")

    
def main():
    # Load History from startup
    inventory = load_inventory()
    failed_entries = 0

    if history:
        print(f"Loaded {len(history)} previous transaction(s). Starting Total: {sum(history)} units.\n")
    else:
        print("No prior inventory data found. Starting fresh.\n")

    # Run in a continuous loop
    while True:
        result = get_valid_input()

        # Route 1: User requested to exit
        if result == 'quit':
            save_inventory(history)
            break

        # Route 2: Input was bad/negative (Increment failed entries counter)
        elif result is None:
            failed_entries += 1
            continue

        # Route 3: Input is valid
        else:
            stock_quantity = result

            # Track every valid transaction amount in history list
            history.append(stock_quantity)
            
            # Calculate and display the tax for this specific delivery
            tax = calculate_tax(stock_quantity)
            print(f"Delivery tax (10%): {tax:.2f}")

            # Update the state of our running total inventory
            total_inventory = sum(history)

            # Trigger Overstock Alert: If total inventory exceeds 500, alert and break immediately
            if total_inventory > 500:
                print(f"ALERT: Overstock limits exceeded! Total inventory is over 500 units ({total_inventory}).")
                save_inventory(history)
                break

    # After exiting the loop, print the final summary statistics
    generate_report(history, failed_entries)


# This line ensures the program executes cleanly when you run the script file
if __name__ == "__main__":
    main()
