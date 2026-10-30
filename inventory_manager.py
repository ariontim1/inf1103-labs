from abc import ABC, abstractmethod
import json
import os

FILENAME = "inventory.json"


# 4. Interfaces using abstract base classes
class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Contract for calculating shipping cost based on product characteristics."""
        pass


# 3. Convert Product into an abstract class
class Product(ABC):
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
        """Displays base product details."""
        print(
            f"ID: {self._product_id} | Name: {self.name} | "
            f"Price: ${self._price:.2f} | Stock: {self.stock}"
        )

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Abstract method forcing subclasses to define fulfillment behavior."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Converts Product object back to a dictionary for JSON saving."""
        pass


# 1.2 & 2.1 Create a Physical Product class with method overriding
class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.weight = float(weight)

    def display_information(self):
        """Overrides display_information using super() to reuse parent behavior."""
        super().display_information()
        print(f"  -> Type: Physical Product | Weight: {self.weight} kg")

    def get_fulfilment_info(self) -> str:
        return "Product requires physical shipping and handling."

    def calculate_shipping_cost(self) -> float:
        """Calculates shipping cost based on weight (e.g., $2.00 base + $1.50 per kg)."""
        return round(2.00 + (1.50 * self.weight), 2)

    def to_dict(self) -> dict:
        return {
            "type": "physical",
            "name": self.name,
            "price": self._price,
            "stock": self.stock,
            "weight": self.weight
        }


# 1.3 & 2.1 Create a Digital Product class with method overriding
class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.download_size = float(download_size)

    def display_information(self):
        """Overrides display_information using super() to reuse parent behavior."""
        super().display_information()
        print(f"  -> Type: Digital Product | Download Size: {self.download_size} MB")

    def get_fulfilment_info(self) -> str:
        return "Product is delivered digitally via download link."

    def to_dict(self) -> dict:
        return {
            "type": "digital",
            "name": self.name,
            "price": self._price,
            "stock": self.stock,
            "download_size": self.download_size
        }


class Inventory:
    def __init__(self, filename=FILENAME):
        self._products = {}
        self.filename = filename
        self.load_from_file()

    def load_from_file(self):
        """Loads inventory data from JSON file and restores correct subclasses."""
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
        """Saves current inventory collection into JSON file preserving product types."""
        data = {pid: p.to_dict() for pid, p in self._products.items()}
        try:
            with open(self.filename, "w") as file:
                json.dump(data, file, indent=4)
            print("Inventory saved successfully.")
        except Exception as e:
            print(f"Error saving to {self.filename}: {e}")

    def add_product(self, product):
        """Adds a new Product subclass object to the inventory."""
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
        """Displays all products stored in the inventory along with fulfillment info and shipping if applicable."""
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
    print("INVENTORY MANAGEMENT SYSTEM (LAB 7)")
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
                
                prod_type = input("Product Type - Enter '1' for Physical, '2' for Digital: ").strip()
                if prod_type == "1":
                    weight = float(input("Weight (kg): "))
                    new_prod = PhysicalProduct(product_id, name, price, stock, weight)
                    inventory.add_product(new_prod)
                elif prod_type == "2":
                    download_size = float(input("Download Size (MB): "))
                    new_prod = DigitalProduct(product_id, name, price, stock, download_size)
                    inventory.add_product(new_prod)
                else:
                    print("Invalid product type selection. Product not added.")
            except ValueError:
                print("Invalid input for numerical fields (price, stock, weight, or size).")
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
                    inventory.save_to_file()
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