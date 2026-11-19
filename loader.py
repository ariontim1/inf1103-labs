import csv
from inventory import Inventory
from supplier import Supplier
from factory import ProductFactory


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    loaded = 0
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header row
            for row_num, row in enumerate(reader, start=2):
                if not row:
                    continue
                try:
                    if len(row) < 5:
                        raise ValueError("Missing required columns.")
                    prod_type = row[0].strip()
                    prod_id = row[1].strip()
                    name = row[2].strip()
                    price = float(row[3].strip())
                    stock = int(row[4].strip())

                    extra = 0.0
                    if len(row) >= 6 and row[5].strip() != "":
                        extra = float(row[5].strip())

                    if inventory.find_product(prod_id) is not None:
                        print(f"Skipping row {row_num}: Product ID '{prod_id}' already exists.")
                        continue

                    product = ProductFactory.create(
                        product_type=prod_type,
                        product_id=prod_id,
                        name=name,
                        price=price,
                        stock_quantity=stock,
                        supplier=supplier,
                        extra=extra,
                    )
                    if inventory.add_product(product):
                        loaded += 1
                except ValueError as e:
                    print(f"Skipping invalid row {row_num} ({row}): {e}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


def get_positive_float(prompt: str) -> float:
    """Prompts until the user enters a valid float greater than zero."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")