from supplier import Supplier
from product import Product, CanBeShipped
from factory import ProductFactory
import json
import os

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
                with open(self.filename, "r") as file:
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