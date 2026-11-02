from abc import ABC, abstractmethod

# 4. Interfaces using abstract base classes[cite: 18]
class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Contract for calculating shipping cost based on product characteristics."""
        pass


# 3. Convert Product into an abstract class[cite: 17]
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
        """Abstract method forcing subclasses to define fulfillment behavior[cite: 17]."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Converts Product object back to a dictionary for JSON saving."""
        pass


# 1.2 & 2.1 Physical Product class with method overriding[cite: 16, 17]
class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.weight = float(weight)

    def display_information(self):
        """Overrides display_information using super() to reuse parent behavior[cite: 17]."""
        super().display_information()
        print(f"  -> Type: Physical Product | Weight: {self.weight} kg")

    def get_fulfilment_info(self) -> str:
        return "Product requires physical shipping and handling."

    def calculate_shipping_cost(self) -> float:
        """Calculates shipping cost based on weight[cite: 18]."""
        return round(2.00 + (1.50 * self.weight), 2)

    def to_dict(self) -> dict:
        return {
            "type": "physical",
            "name": self.name,
            "price": self._price,
            "stock": self.stock,
            "weight": self.weight
        }


# 1.3 & 2.1 Digital Product class with method overriding[cite: 16, 17]
class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.download_size = float(download_size)

    def display_information(self):
        """Overrides display_information using super() to reuse parent behavior[cite: 17]."""
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