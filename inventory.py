from product import Product, PhysicalProduct, DigitalProduct, CanBeShipped
import json
import os

FILENAME = "inventory.json"


class Inventory:
    def __init__(self, filename=FILENAME):
        self._products = []  # Stored as a list matching target UML design
        self.filename = filename
        self.load()

    def load(self):
        """Loads inventory data from JSON file or initializes default products."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    data = json.load(file)
                    if data:
                        self._products = []
                        for pid, details in data.items():
                            prod_type = details.get("type", "physical")
                            if prod_type == "physical":
                                prod = PhysicalProduct(
                                    product_id=pid,
                                    name=details["name"],
                                    price=details["price"],
                                    stock=details["stock"],
                                    weight=details.get("weight", 1.0)
                                )
                            else:
                                prod = DigitalProduct(
                                    product_id=pid,
                                    name=details["name"],
                                    price=details["price"],
                                    stock=details["stock"],
                                    download_size=details.get("download_size", 100.0)
                                )
                            self._products.append(prod)
                        print(f"{self.filename} found and loaded successfully.")
                        return
            except Exception as e:
                print(f"Error loading {self.filename}: {e}")

        # Initialize default products if file doesn't exist or is empty
        default_data = {
            "P001": {"type": "physical", "name": "Laptop", "price": 1200.00, "stock": 15, "weight": 2.5},
            "P002": {"type": "digital", "name": "OS License", "price": 150.00, "stock": 50, "download_size": 4500.0},
            "P003": {"type": "physical", "name": "Keyboard", "price": 45.00, "stock": 25, "weight": 0.8},
        }
        self._products = []
        for pid, details in default_data.items():
            if details["type"] == "physical":
                prod = PhysicalProduct(pid, details["name"], details["price"], details["stock"], details["weight"])
            else:
                prod = DigitalProduct(pid, details["name"], details["price"], details["stock"], details["download_size"])
            self._products.append(prod)
        self.save()
        print(f"{self.filename} initialized with default items.")

    def save(self):
        """Saves current inventory collection into JSON file."""
        data = {p.product_id: p.to_dict() for p in self._products}
        try:
            with open(self.filename, "w") as file:
                json.dump(data, file, indent=4)
            print("Inventory saved successfully.")
        except Exception as e:
            print(f"Error saving to {self.filename}: {e}")

    def add_product(self, product):
        """Adds a new Product object to the inventory list."""
        if self.get_product(product.product_id):
            print("Error: Product ID already exists.")
            return False
        self._products.append(product)
        print("\nProduct added successfully!")
        self.save()
        return True

    def get_product(self, product_id):
        """Retrieves a Product object by ID from the list."""
        for product in self._products:
            if product.product_id == product_id:
                return product
        return None

    def update_stock(self, product_id, new_stock):
        """Updates stock matching UML specification."""
        product = self.get_product(product_id)
        if product:
            product.update_stock(new_stock)
            self.save()
            return True
        return False

    def display_all(self):
        """Displays all products stored in the inventory list."""
        print("\nCurrent Inventory")
        print("-" * 50)
        if not self._products:
            print("Inventory is currently empty.")
        else:
            for product in self._products:
                product.display_information()
                print(f"  -> Fulfillment: {product.get_fulfilment_info()}")
                if isinstance(product, CanBeShipped):
                    print(f"  -> Shipping Cost: ${product.calculate_shipping_cost():.2f}")
                print("-" * 50)

    def search_product(self, product_id):
        """Searches and displays a specific product by its ID."""
        print("\nSearch Product")
        product = self.get_product(product_id)
        if product:
            print("\nProduct Found")
            print("-" * 50)
            product.display_information()
            print(f"  -> Fulfillment: {product.get_fulfilment_info()}")
            if isinstance(product, CanBeShipped):
                print(f"  -> Shipping Cost: ${product.calculate_shipping_cost():.2f}")
            print("-" * 50)
        else:
            print("\nProduct not found.")