import json
import os

FILE_NAME = "inventory.json"


# clears the terminal screen (Windows + macOS/Linux)
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# this loads the inventory or creates a new one if the file does not exist
def load_data():
    if not os.path.exists(FILE_NAME):
        print("File does not exist, creating new file.")
        with open(FILE_NAME, "w") as file:
            json.dump([], file, indent=4)
        return []

    try:
        with open(FILE_NAME, "r") as file:
            if os.path.getsize(FILE_NAME) == 0:
                return []
            return json.load(file)
    except json.JSONDecodeError:
        print("Error: File does not meet the required JSON format.")
        return []


# save inventory to file
def save_data(data):
    data = sorted(data, key=lambda x: int(x["id"]))
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)
    return data


# add a new inventory item
def add_item(data):
    while True:
        invalid_id = False
        item_id = input("ID: ").strip()

        if not item_id:
            print("ID should not be empty.")
            invalid_id = True

        for item in data:
            if item["id"] == item_id:
                print("Item ID already exists.")
                invalid_id = True
                break

        if not invalid_id:
            break

    while True:
        name = input("Name: ").strip()
        if name:
            break
        print("Name should not be empty.")

    while True:
        try:
            price = round(float(input("Price: ")), 2)
            if price <= 0:
                print("Price must be greater than zero.")
            else:
                break
        except ValueError:
            print("Invalid input. Price must be a number.")

    while True:
        try:
            quantity = int(input("Quantity: "))
            if quantity < 0:
                print("Quantity must not be below zero.")
            else:
                break
        except ValueError:
            print("Invalid input. Quantity must be an integer.")

    confirm = input("Add item? (Y/N): ").upper()
    if confirm == "Y":
        data.append({
            "id": item_id,
            "name": name,
            "price": price,
            "quantity": quantity
        })
        print("Item added.")
        return save_data(data)

    print("Cancelled.")
    return data


# display all items in inventory
def view_items(data):
    if not data:
        print("No items found.")
        return

    print("--- Inventory ---")
    for item in data:
        print(
            f"ID: {item['id']} | "
            f"Name: {item['name']} | "
            f"£{item['price']:.2f} | "
            f"Qty: {item['quantity']}"
        )


# update an existing item by ID
def update_item(data):
    item_id = input("Enter ID to update: ").strip()

    for item in data:
        if item["id"] == item_id:
            print("Leave blank to skip update.")

            name = input("New name: ").strip()
            if name:
                item["name"] = name

            while True:
                price = input("New price: ").strip()
                if not price:
                    break
                try:
                    price = float(price)
                    if price > 0:
                        item["price"] = round(price, 2)
                        break
                except ValueError:
                    pass
                print("Invalid price.")

            while True:
                quantity = input("New quantity: ").strip()
                if not quantity:
                    break
                try:
                    quantity = int(quantity)
                    if quantity >= 0:
                        item["quantity"] = quantity
                        break
                except ValueError:
                    pass
                print("Invalid quantity.")

            print("Item updated.")
            return save_data(data)

    print("ID not found.")
    return data


# search inventory by name or ID
def search_item(data):
    option = input("Search by name or ID: ").lower().strip()
    if option not in ["name", "id"]:
        print("Invalid search option.")
        return

    search = input(f"Enter {option}: ").lower().strip()
    found = False

    for item in data:
        if search in item[option].lower():
            print(
                f"ID: {item['id']} | "
                f"Name: {item['name']} | "
                f"£{item['price']:.2f} | "
                f"Qty: {item['quantity']}"
            )
            found = True

    if not found:
        print("Item not found.")


# delete a single item
def delete_item(data):
    item_id = input("Enter ID to delete: ").strip()

    for item in data:
        if item["id"] == item_id:
            confirm = input(f"Delete '{item['name']}'? (Y/N): ").upper()
            if confirm == "Y":
                data.remove(item)
                print("Item deleted.")
                return save_data(data)
            print("Cancelled.")
            return data

    print("ID not found.")
    return data


# report items with low stock
def low_stock_report(data):
    print("--- Low Stock Report (Below 5) ---")
    found = False

    for item in data:
        if item["quantity"] < 5:
            print(f"{item['name']} - Quantity: {item['quantity']}")
            found = True

    if not found:
        print("No low-stock items.")



# clear all items from inventory
def clear_all_items(data):
    if not data:
        print("Inventory is already empty.")
        return data

    confirm = input("Are you sure you want to clear ALL items? (Y/N): ").upper()
    if confirm == "Y":
        data.clear()
        save_data(data)
        print("All items cleared.")
        return data

    print("Clear cancelled.")
    return data


# main menu loop
def main():
    data = load_data()

    while True:
        clear_screen()

        print("INVENTORY MANAGEMENT SYSTEM") # Better for clarity 
        print("===========================")
        print("1. Add Item")
        print("2. View Stock")
        print("3. Update Item")
        print("4. Search Item")
        print("5. Delete Item")
        print("6. Save & Exit")
        print("7. Low Stock Report")
        print("8. Clear All Items") # keeping it user friendly by allowing quick options to remove items.
        print("9. Close Programme")
        print("===========================")

        option = input("Choose: ").strip()
        clear_screen()

        if option == "1":
            data = add_item(data)

        elif option == "2":
            view_items(data)

        elif option == "3":
            data = update_item(data)

        elif option == "4":
            search_item(data)

        elif option == "5":
            data = delete_item(data)

        elif option == "6":
            save_data(data)
            print("Data saved. Exiting.")
            break

        elif option == "7":
            low_stock_report(data)

        elif option == "8":
            data = clear_all_items(data)

        elif option == "9":
            print("Programme closed.")
            break

        else:
            print("Invalid option.")

        input("\nPress Enter to continue...")


# ensures the program only runs when executed directly
if __name__ == "__main__":
    main()
