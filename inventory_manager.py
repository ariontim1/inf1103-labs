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

