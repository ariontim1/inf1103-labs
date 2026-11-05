from product import Product

class OrderLine:
    def __init__(self, product: Product, quantity: int):
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        """Calculates the subtotal for this order line."""
        return self.product._price * self.quantity


class Order:
    def __init__(self, order_id: str):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Order creates and manages its own OrderLine objects internally."""
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        """Calculates the total value of the order by summing all line subtotals."""
        total = 0.0
        for line in self.order_lines:
            total += line.calculate_subtotal()
        return total

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