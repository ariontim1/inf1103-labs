import json
import os
from inf_1103_tut_6.product import Product

FILENAME = "inventory.json"


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