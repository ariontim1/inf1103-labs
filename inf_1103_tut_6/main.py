from inventory import Inventory


def display_menu():
    """Prints the main user interface menu options."""
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
    print("INVENTORY MANAGEMENT SYSTEM (OOP)")
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
                inventory.add_product(product_id, name, price, stock)
            except ValueError:
                print("Invalid price or stock quantity input.")
        elif choice == "3":
            print("\nUpdate Stock")
            product_id = input("Enter Product ID: ").strip()
            product = inventory.get_product(product_id)
            if product:
                print("\nProduct Found:")
                print(f"Name: {product.name}")
                print(f"Current Stock: {product.stock}\n")
                try:
                    new_stock = int(input("New Stock Quantity: "))
                    product.update_stock(new_stock)
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
            inventory.save_to_file()
        elif choice == "6":
            print("\nSaving inventory before exit...")
            inventory.save_to_file()
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()