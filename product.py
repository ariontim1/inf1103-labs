from abc import ABC, abstractmethod
from supplier import Supplier

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Interface method for calculating shipping cost."""
        pass


class Product(ABC):
    def __init__(self, product_id, name, price, stock, supplier: Supplier):
        self._product_id = product_id
        self._name = name
        self._price = float(price)
        self._stock = int(stock)
        self._supplier = supplier

    @property
    def price(self) -> float:
        return self._price

    @property
    def product_id(self):
        return self._product_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        self._stock = int(value)

    def update_stock(self, new_stock):
        """Updates the stock quantity of the product."""
        self.stock = int(new_stock)

    def display_information(self):
        """Displays base product details matching UML design."""
        print(
            f"ID: {self._product_id} | Name: {self._name} | "
            f"Price: ${self._price:.2f} | Stock: {self._stock}"
        )
        print("Supplier Information:")
        self._supplier.display_information()

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Abstract method defining fulfillment behavior."""
        pass

    def to_dict(self) -> dict:
        """Converts Product object back to a dictionary for JSON saving."""
        return {
            "name": self._name,
            "price": self._price,
            "stock": self._stock
        }


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight, supplier: Supplier):
        super().__init__(product_id, name, price, stock, supplier)
        self._weight = float(weight)

    def display_information(self):
        super().display_information()
        print(f"  -> Type: Physical Product | Weight: {self._weight} kg")

    def get_fulfilment_info(self) -> str:
        return "Product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return round(2.00 + (1.50 * self._weight), 2)

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"type": "physical", "weight": self._weight})
        return d


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size, supplier: Supplier):
        super().__init__(product_id, name, price, stock, supplier)
        self._download_size = float(download_size)

    def display_information(self):
        super().display_information()
        print(f"  -> Type: Digital Product | Download Size: {self._download_size} MB")

    def get_fulfilment_info(self) -> str:
        return "Product is delivered digitally."

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"type": "digital", "download_size": self._download_size})
        return d