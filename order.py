from product import Product
from discounts import DiscountStrategy, NoDiscount


class OrderLine:
    def __init__(self, product: Product, quantity: int):
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        """Calculates the subtotal for this order line."""
        return self.product.price * self.quantity


class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy | None = None):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
        self.discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def set_discount(self, discount: DiscountStrategy) -> None:
        """Updates the discount strategy used by this order."""
        self.discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Order creates and manages its own OrderLine objects internally."""
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        """Calculates the total value of the order and applies the current discount strategy."""
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.discount.apply(total)

    def display_order(self) -> None:
        """Displays order details and all its order lines."""
        print(f"\nOrder ID: {self.order_id}")
        print("-" * 40)
        if not self.order_lines:
            print("No items in this order.")
        else:
            for line in self.order_lines:
                print(f"- {line.product.name} x {line.quantity} = ${line.calculate_subtotal():.2f}")
        print(f"Total Order Value: ${self.calculate_total():.2f}")
        print("-" * 40)