import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from discounts import BulkDiscount, NoDiscount, PercentageDiscount, StudentDiscount
from factory import ProductFactory
from inventory import Inventory
from loader import get_positive_float, load_products
from order import Order, OrderLine
from product import DigitalProduct, PhysicalProduct
from supplier import Supplier


class TestLab09(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Global Tech Supplies", "support@globaltech.com")
        self.physical = ProductFactory.create(
            "physical", "P100", "Desk Lamp", 50.0, 10, self.supplier, extra=1.5
        )
        self.digital = ProductFactory.create(
            "digital", "D100", "IDE License", 100.0, 20, self.supplier, extra=250.0
        )

    def test_discount_strategies_and_set_discount(self) -> None:
        order = Order("O001")
        order.add_order_line(self.physical, 5)  # Subtotal = 250.0
        self.assertAlmostEqual(order.calculate_total(), 250.0)

        order.set_discount(BulkDiscount(200.0, 20.0))
        self.assertAlmostEqual(order.calculate_total(), 230.0)

        order.set_discount(PercentageDiscount(10.0))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

        order.set_discount(StudentDiscount(5.0))
        self.assertAlmostEqual(order.calculate_total(), 237.5)

        order.set_discount(NoDiscount())
        self.assertAlmostEqual(order.calculate_total(), 250.0)

    def test_factory_creates_subclasses_and_rejects_unknown_type(self) -> None:
        self.assertIsInstance(self.physical, PhysicalProduct)
        self.assertIsInstance(self.digital, DigitalProduct)

        with self.assertRaises(ValueError):
            ProductFactory.create("service", "S999", "Setup", 30.0, 5, self.supplier)

    def test_product_and_orderline_validation(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P101", "Free Item", 0.0, 5, self.supplier)

        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P102", "Neg Price", -10.0, 5, self.supplier)

        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P103", "Neg Stock", 10.0, -1, self.supplier)

        with self.assertRaises(ValueError):
            self.physical.update_stock(-3)

        order = Order("O002")
        with self.assertRaises(ValueError):
            order.add_order_line(self.physical, 0)

        with self.assertRaises(ValueError):
            OrderLine(self.physical, -2)

    def test_get_positive_float_retries_invalid_inputs(self) -> None:
        buf = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]), redirect_stdout(buf):
            result = get_positive_float("Enter price: ")

        output = buf.getvalue()
        self.assertAlmostEqual(result, 12.5)
        self.assertIn("Please enter a valid number, e.g. 12.50", output)
        self.assertIn("Please enter a number greater than zero.", output)

    def test_load_products_missing_file_and_bad_rows(self) -> None:
        # Missing file check
        buf_missing = io.StringIO()
        with redirect_stdout(buf_missing):
            load_products("non_existent_products.csv", Inventory(), self.supplier)
        missing_out = buf_missing.getvalue()
        self.assertIn("Products file not found:", missing_out)
        self.assertIn("Load attempt finished.", missing_out)

        # CSV with valid and invalid rows using an isolated in-memory-like list via real Inventory?
        # Note: Inventory() loads/saves JSON; use a dedicated test filename via patch or temp file.
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            inv_path = os.path.join(tmpdir, "test_inv.json")
            csv_path = os.path.join(tmpdir, "test_products.csv")
            with open(csv_path, "w", encoding="utf-8", newline="") as f:
                f.write(
                    "product_type,product_id,name,price,stock_quantity\n"
                    "physical,P201,Lamp,25.00,10\n"
                    "digital,D201,Editor,49.90,100\n"
                    "service,S201,Install,30.00,5\n"
                    "physical,P202,Chair,abc,3\n"
                    "physical,P203,Stand,39.50,7\n"
                )

            inv = Inventory(filename=inv_path)
            inv.products.clear()

            buf_csv = io.StringIO()
            with redirect_stdout(buf_csv):
                load_products(csv_path, inv, self.supplier)

            csv_out = buf_csv.getvalue()
            self.assertIn("3 products loaded.", csv_out)
            self.assertIn("Load attempt finished.", csv_out)
            self.assertIsNotNone(inv.find_product("P201"))
            self.assertIsNotNone(inv.find_product("D201"))
            self.assertIsNotNone(inv.find_product("P203"))
            self.assertIsNone(inv.find_product("S201"))
            self.assertIsNone(inv.find_product("P202"))


if __name__ == "__main__":
    unittest.main()