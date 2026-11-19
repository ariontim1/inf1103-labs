from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        """Applies a discount to the given order total and returns the discounted total."""
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self.percentage: float = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100.0)


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, discount_amount: float):
        self.threshold: float = threshold
        self.discount_amount: float = discount_amount

    def apply(self, total: float) -> float:
        if total >= self.threshold:
            return total - self.discount_amount
        return total


class StudentDiscount(DiscountStrategy):
    def __init__(self, percentage: float = 5.0):
        self.percentage: float = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100.0)