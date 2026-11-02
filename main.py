from inventory import Inventory
from product import PhysicalProduct, DigitalProduct


def display_menu():
    print("\n--------- MENU ---------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("------------------------")


def main():
    print("=" * 45)
    print("INVENTORY MANAGEMENT SYSTEM (LAB 7 TARGET DESIGN)")
    print("=" * 45 + "\n")

    inventory = Inventory()

    while True:
        display_menu()
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            print("\nAdd New Product")
            product_id = input("Product ID: ").strip()
            name = input("Product Name: ").strip()
            try:
                price = float(input("Price: "))
                stock = int(input("Stock Quantity: "))
                
                prod_type = input("Product Type - Enter '1' for Physical, '2' for Digital: ").strip()
                if prod_type == "1":
                    weight = float(input("Weight (kg): "))
                    new_prod = PhysicalProduct(product_id, name, price, stock, weight)
                    inventory.add_product(new_prod)
                elif prod_type == "2":
                    download_size = float(input("Download Size (MB): "))
                    new_prod = DigitalProduct(product_id, name, price, stock, download_size)
                    inventory.add_product(new_prod)
                else:
                    print("Invalid product type selection. Product not added.")
            except ValueError:
                print("Invalid input for numerical fields.")
        elif choice == "3":
            print("\nUpdate Stock")
            product_id = input("Enter Product ID: ").strip()
            product = inventory.get_product(product_id)
            if product:
                print(f"\nProduct Found: {product.name} (Current Stock: {product.stock})")
                try:
                    new_stock = int(input("New Stock Quantity: "))
                    inventory.update_stock(product_id, new_stock)
                    print("\nStock updated successfully!")
                except ValueError:
                    print("Error: Stock must be a valid integer.")
            else:
                print("\nProduct not found.")
        elif choice == "4":
            product_id = input("Enter Product ID: ").strip()
            inventory.search_product(product_id)
        elif choice == "5":
            print("\nSaving inventory...")
            inventory.save()
        elif choice == "6":
            print("\nSaving inventory before exit...")
            inventory.save()
            print("\nProgram terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()