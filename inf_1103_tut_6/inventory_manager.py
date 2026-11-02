import json
import os

FILENAME = "inventory.json"


class Product:
    def __init__(self, product_id, name, price, stock):
        self._product_id = product_id
        self.name = name
        self._price = float(price)
        self.stock = int(stock)

    @property
    def product_id(self):
        return self._product_id

    def update_stock(self, new_stock):
        """Updates the stock quantity of the product."""
        self.stock = int(new_stock)

    def display_information(self):
        """Displays product details matching the original format."""
        print(
            f"ID: {self._product_id} | Name: {self.name} | "
            f"Price: ${self._price:.2f} | Stock: {self.stock}"
        )

    def to_dict(self):
        """Converts Product object back to a dictionary for JSON saving."""
        return {
            "name": self.name,
            "price": self._price,
            "stock": self.stock
        }

class Inventory:
    def __init__(self, filename=FILENAME):
        self._products = {}
        self.filename = filename
        self.load_from_file()

    def load_from_file(self):
        """Loads inventory data from JSON file or initializes default products."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    data = json.load(file)
                    if data:
                        self._products = {}
                        for pid, details in data.items():
                            self._products[pid] = Product(
                                product_id=pid,
                                name=details["name"],
                                price=details["price"],
                                stock=details["stock"]
                            )
                        print(f"{self.filename} found.")
                        print("Inventory loaded successfully.")
                        return
            except Exception as e:
                print(f"Error loading {self.filename}: {e}")

        # Initialize default products if file doesn't exist or is empty
        default_data = {
            "P001": {"name": "Laptop", "price": 1200.00, "stock": 15},
            "P002": {"name": "Mouse", "price": 25.50, "stock": 40},
            "P003": {"name": "Keyboard", "price": 45.00, "stock": 25},
        }
        self._products = {}
        for pid, details in default_data.items():
            self._products[pid] = Product(
                product_id=pid,
                name=details["name"],
                price=details["price"],
                stock=details["stock"]
            )
        self.save_to_file()
        print(f"{self.filename} initialized with default items.")

    def save_to_file(self):
        """Saves current inventory collection into JSON file."""
        data = {pid: p.to_dict() for pid, p in self._products.items()}
        try:
            with open(self.filename, "w") as file:
                json.dump(data, file, indent=4)
            print("Inventory saved successfully.")
        except Exception as e:
            print(f"Error saving to {self.filename}: {e}")

    def add_product(self, product_id, name, price, stock):
        """Adds a new Product object to the inventory."""
        if product_id in self._products:
            print("Error: Product ID already exists.")
            return False
        self._products[product_id] = Product(product_id, name, price, stock)
        print("\nProduct added successfully!")
        return True

    def get_product(self, product_id):
        """Retrieves a Product object by ID."""
        return self._products.get(product_id)

    def display_all(self):
        """Displays all products stored in the inventory."""
        print("\nCurrent Inventory")
        print("-" * 40)
        if not self._products:
            print("Inventory is currently empty.")
        else:
            for product in self._products.values():
                product.display_information()
        print("-" * 40)

    def search_product(self, product_id):
        """Searches and displays a specific product by its ID."""
        print("\nSearch Product")
        product = self.get_product(product_id)
        if product:
            print("\nProduct Found")
            print("-" * 40)
            print(f"ID: {product_id}")
            print(f"Name: {product.name}")
            print(f"Price: ${product._price:.2f}")
            print(f"Stock: {product.stock}")
            print("-" * 40)
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
    print("INVENTORY MANAGEMENT SYSTEM (OOP)")
    print("=" * 45 + "\n")

    inventory = Inventory()

    while True:
        display_menu()
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            print("\nAdd New Product")
            product_id = input("Product ID: ").strip()
            name = input("Product Name: ").strip()
            try:
                price = float(input("Price: "))
                stock = int(input("Stock Quantity: "))
                inventory.add_product(product_id, name, price, stock)
            except ValueError:
                print("Invalid price or stock quantity input.")
        elif choice == "3":
            print("\nUpdate Stock")
            product_id = input("Enter Product ID: ").strip()
            product = inventory.get_product(product_id)
            if product:
                print("\nProduct Found:")
                print(f"Name: {product.name}")
                print(f"Current Stock: {product.stock}\n")
                try:
                    new_stock = int(input("New Stock Quantity: "))
                    product.update_stock(new_stock)
                    print("\nStock updated successfully!")
                except ValueError:
                    print("Error: Stock must be a valid integer.")
            else:
                print("\nProduct not found.")
        elif choice == "4":
            product_id = input("Enter Product ID: ").strip()
            inventory.search_product(product_id)
        elif choice == "5":
            print("\nSaving inventory...")
            inventory.save_to_file()
        elif choice == "6":
            print("\nSaving inventory before exit...")
            inventory.save_to_file()
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()