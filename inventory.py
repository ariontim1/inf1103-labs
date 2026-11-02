from product import Product, PhysicalProduct, DigitalProduct, CanBeShipped
import json
import os

FILENAME = "inventory.json"


class Inventory:
    def __init__(self, filename=FILENAME):
        self._products = {}
        self.filename = filename
        self.load_from_file()

    def load_from_file(self):
        """Loads inventory data from JSON file and restores correct subclasses[cite: 19]."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    data = json.load(file)
                    if data:
                        self._products = {}
                        for pid, details in data.items():
                            prod_type = details.get("type")
                            if prod_type == "physical":
                                self._products[pid] = PhysicalProduct(
                                    product_id=pid,
                                    name=details["name"],
                                    price=details["price"],
                                    stock=details["stock"],
                                    weight=details["weight"]
                                )
                            elif prod_type == "digital":
                                self._products[pid] = DigitalProduct(
                                    product_id=pid,
                                    name=details["name"],
                                    price=details["price"],
                                    stock=details["stock"],
                                    download_size=details["download_size"]
                                )
                        print(f"{self.filename} found.")
                        print("Inventory loaded successfully with product types.")
                        return
            except Exception as e:
                print(f"Error loading {self.filename}: {e}")

        # Initialize default products if file doesn't exist or is empty
        default_data = {
            "P001": {"type": "physical", "name": "Gaming Laptop", "price": 1200.00, "stock": 15, "weight": 2.5},
            "P002": {"type": "digital", "name": "Antivirus License", "price": 45.50, "stock": 100, "download_size": 250.0},
            "P003": {"type": "physical", "name": "Mechanical Keyboard", "price": 85.00, "stock": 25, "weight": 0.9},
        }
        self._products = {}
        for pid, details in default_data.items():
            if details["type"] == "physical":
                self._products[pid] = PhysicalProduct(pid, details["name"], details["price"], details["stock"], details["weight"])
            elif details["type"] == "digital":
                self._products[pid] = DigitalProduct(pid, details["name"], details["price"], details["stock"], details["download_size"])
        
        self.save_to_file()
        print(f"{self.filename} initialized with default typed items.")

    def save_to_file(self):
        """Saves current inventory collection into JSON file preserving product types[cite: 19]."""
        data = {pid: p.to_dict() for pid, p in self._products.items()}
        try:
            with open(self.filename, "w") as file:
                json.dump(data, file, indent=4)
            print("Inventory saved successfully.")
        except Exception as e:
            print(f"Error saving to {self.filename}: {e}")

    def add_product(self, product):
        """Adds a new Product subclass object to the inventory[cite: 19]."""
        if product.product_id in self._products:
            print("Error: Product ID already exists.")
            return False
        self._products[product.product_id] = product
        print("\nProduct added successfully!")
        self.save_to_file()
        return True

    def get_product(self, product_id):
        """Retrieves a Product object by ID."""
        return self._products.get(product_id)

    def display_all(self):
        """Displays all products stored in the inventory along with fulfillment and shipping info[cite: 19]."""
        print("\nCurrent Inventory")
        print("-" * 50)
        if not self._products:
            print("Inventory is currently empty.")
        else:
            for product in self._products.values():
                product.display_information()
                print(f"  -> Fulfillment: {product.get_fulfilment_info()}")
                if isinstance(product, CanBeShipped):
                    print(f"  -> Shipping Cost: ${product.calculate_shipping_cost():.2f}")
                print("-" * 50)

    def search_product(self, product_id):
        """Searches and displays a specific product by its ID[cite: 19]."""
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