import json
import os

FILENAME = "inventory.json"


def save_inventory(inventory, filename=FILENAME):
    """Saves the current inventory dictionary into inventory.json."""
    try:
        with open(filename, "w") as file:
            json.dump(inventory, file, indent=4)
        print("Inventory saved successfully.")
    except Exception as e:
        print(f"Error saving to {filename}: {e}")


def load_inventory(filename=FILENAME):
    """Loads inventory data from inventory.json if present, or initializes default products."""
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                inventory = json.load(file)
                # If the file exists and contains items, load them
                if inventory:
                    print(f"{filename} found.")
                    print("Inventory loaded successfully.")
                    return inventory
        except Exception as e:
            print(f"Error loading {filename}: {e}")

    # If the file doesn't exist or is empty, initialize default products and write them to file
    inventory = {
        "P001": {"name": "Laptop", "price": 1200.00, "stock": 15},
        "P002": {"name": "Mouse", "price": 25.50, "stock": 40},
        "P003": {"name": "Keyboard", "price": 45.00, "stock": 25},
    }

    # Save default items immediately so inventory.json is created properly
    save_inventory(inventory, filename)
    print(f"{filename} initialized with default items.")
    return inventory


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
    print("=" * 45)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 45 + "\n")

    inventory = load_inventory()

    while True:
        display_menu()
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            display_all(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
        elif choice == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()