import json
import os
from factory import ProductFactory
from product import CanBeShipped, Product
from supplier import Supplier

FILENAME = "inventory.json"


class Inventory:
    def __init__(self, filename: str = FILENAME):
        """Aggregation collection with type hint"""
        self.products: list[Product] = []
        self.filename: str = filename
        self.default_supplier: Supplier = Supplier("S001", "TechCorp Supplies", "support@techcorp.com")
        self.load()

    def load(self) -> None:
        """Loads inventory data from JSON file or initializes default products."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    if data:
                        self.products = []
                        for pid, details in data.items():
                            prod_type = details.get("type", "physical")
                            extra = (
                                float(details.get("weight", 1.0))
                                if prod_type == "physical"
                                else float(details.get("download_size", 100.0))
                            )
                            prod = ProductFactory.create(
                                product_type=prod_type,
                                product_id=pid,
                                name=details["name"],
                                price=details["price"],
                                stock_quantity=details["stock"],
                                supplier=self.default_supplier,
                                extra=extra,
                            )
                            self.products.append(prod)
                        print(f"{self.filename} found and loaded successfully.")
                        return
            except Exception as e:
                print(f"Error loading {self.filename}: {e}")

        default_data = {
            "P001": {"type": "physical", "name": "Laptop", "price": 1200.00, "stock": 15, "weight": 2.5},
            "P002": {"type": "digital", "name": "OS License", "price": 150.00, "stock": 50, "download_size": 4500.0},
            "P003": {"type": "physical", "name": "Keyboard", "price": 45.00, "stock": 25, "weight": 0.8},
        }
        self.products = []
        for pid, details in default_data.items():
            extra = details["weight"] if details["type"] == "physical" else details["download_size"]
            prod = ProductFactory.create(
                product_type=details["type"],
                product_id=pid,
                name=details["name"],
                price=details["price"],
                stock_quantity=details["stock"],
                supplier=self.default_supplier,
                extra=extra,
            )
            self.products.append(prod)
        self.save()
        print(f"{self.filename} initialized with default items.")

    def save(self) -> None:
        """Saves current products to the JSON file."""
        data = {}
        for prod in self.products:
            is_physical = isinstance(prod, CanBeShipped) or getattr(prod, "product_type", "") == "physical"
            entry = {
                "type": "physical" if is_physical else "digital",
                "name": getattr(prod, "name", ""),
                "price": getattr(prod, "price", 0.0),
                "stock": getattr(prod, "stock", getattr(prod, "stock_quantity", 0)),
            }
            if is_physical:
                entry["weight"] = getattr(prod, "weight", 1.0)
            else:
                entry["download_size"] = getattr(prod, "download_size", 100.0)
            pid = getattr(prod, "product_id", getattr(prod, "id", ""))
            data[pid] = entry

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def display_all(self) -> None:
        """Displays all products currently in inventory."""
        if not self.products:
            print("No products in inventory.")
            return
        print("\n--- Inventory Products ---")
        for prod in self.products:
            pid = getattr(prod, "product_id", getattr(prod, "id", "N/A"))
            name = getattr(prod, "name", "N/A")
            price = getattr(prod, "price", 0.0)
            stock = getattr(prod, "stock", getattr(prod, "stock_quantity", 0))
            if hasattr(prod, "weight"):
                extra_info = f"Physical | Weight: {prod.weight} kg"
            elif hasattr(prod, "download_size"):
                extra_info = f"Digital | Size: {prod.download_size} MB"
            else:
                extra_info = type(prod).__name__
            print(f"[{pid}] {name} - ${price:.2f} | Stock: {stock} | {extra_info}")

    def add_product(self, product: Product) -> bool:
        """Adds a product to inventory if its ID is unique."""
        pid = getattr(product, "product_id", getattr(product, "id", None))
        if pid and self.find_product(pid) is not None:
            print(f"Product ID '{pid}' already exists.")
            return False
        self.products.append(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        """Finds a product by ID."""
        for prod in self.products:
            pid = getattr(prod, "product_id", getattr(prod, "id", None))
            if pid == product_id:
                return prod
        return None

    def update_stock(self, product_id: str, new_stock: int) -> bool:
        """Updates stock quantity for a matching product after validating stock >= 0."""
        if new_stock < 0:
            raise ValueError("Stock quantity cannot be negative.")
        prod = self.find_product(product_id)
        if prod is None:
            print(f"Product '{product_id}' not found.")
            return False
        if hasattr(prod, "stock"):
            prod.stock = new_stock
        elif hasattr(prod, "stock_quantity"):
            prod.stock_quantity = new_stock
        return True

    def search_product(self, product_id: str) -> Product | None:
        """Searches for a product by ID and prints its details."""
        prod = self.find_product(product_id)
        if prod is None:
            print(f"\nProduct '{product_id}' not found.")
            return None
        pid = getattr(prod, "product_id", getattr(prod, "id", "N/A"))
        name = getattr(prod, "name", "N/A")
        price = getattr(prod, "price", 0.0)
        stock = getattr(prod, "stock", getattr(prod, "stock_quantity", 0))
        if hasattr(prod, "weight"):
            extra_info = f"Physical | Weight: {prod.weight} kg"
        elif hasattr(prod, "download_size"):
            extra_info = f"Digital | Size: {prod.download_size} MB"
        else:
            extra_info = type(prod).__name__
        print(f"\nFound: [{pid}] {name} - ${price:.2f} | Stock: {stock} | {extra_info}")
        return prod