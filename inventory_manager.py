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