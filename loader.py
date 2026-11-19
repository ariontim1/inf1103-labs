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

                    product = ProductFactory.create(
                        product_type=prod_type,
                        product_id=prod_id,
                        name=name,
                        price=price,
                        stock_quantity=stock,
                        supplier=supplier,
                    )
                    if inventory.add_product(product):
                        loaded += 1
                except ValueError as e:
                    print(f"Skipping invalid row {row_num} ({row}): {e}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")