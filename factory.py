from supplier import Supplier
from product import Product, PhysicalProduct, DigitalProduct


class ProductFactory:
    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        extra: float = 0.0,
    ) -> Product:
        """Creates a Product subclass based on product_type."""
        normalized_type = product_type.strip().lower()
        if normalized_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, extra, supplier)
        elif normalized_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, extra, supplier)
        else:
            raise ValueError(f"Unknown product type: {product_type}")