import json
import os

#this loads the inventory / or you can start with a new one
def load_data():
    if os.path.exists("inventory.json"):
        with open("inventory.json", "r") as file:
            try:
                return json.load(file)
            except:
                print("File empty, starting new.")
                return []
    return []

#save inventory to file
def save_data(data):
    with open("inventory.json", "w") as file:
        json.dump(data, file, indent=4)

#you can add a new item heree
def add_item(data):
    item_id = input("ID: ")
    for item in data:
        if item["id"] == item_id:
            print("ID already used, try again.")
            return
    if len(item_id.strip()) == 0:
        print("ID should not be empty.")
        return

    name = input("Name: ")
    if len(name.strip()) == 0:
        print("Name should not be empty.")
        return
    
    try:
        price = round(float(input("Price: ")), 2)
        quantity = int(input("Quantity: "))
    except:
        print("Enter numbers for price and quantity.")
        return

    save_now = input("Save now? (Y/N): ").upper()
    if save_now == "Y":
        item = {"id": item_id, "name": name, "price": price, "quantity": quantity}
        data.append(item)
        save_data(data)
        print("saved")
    else:
        print("Save failed.")

#all items in inventory
def view_items(data):
    if not data:
        print("No items found.")
        return
    print("--- Inventory ---")
    for item in data:
        print(f"ID: {item['id']} / Name: {item['name']} / £{item['price']} / Quantity: {item['quantity']}")
    print()

#update item
def update_item(data):
    item_id = input("enter ID to update: ")
    for item in data:
        if item["id"] == item_id:
            print("Leave blank to skip update.")
            name = input("New name: ")
            price = input("New price: ")
            qty = input("New quantity: ")

            
            if name:
                if len(name.strip()) == 0:
                    print("Name failed to update. Name should not be empty, please try again.")
                else:
                    item["name"] = name
            if price:
                try:
                    item["price"] = round(float(price), 2)
                except:
                    print("Price has failed to update. Please try again with a number.")
            if qty:
                try:
                    item["quantity"] = int(qty)
                except:
                    print("Quantity failed to update. Please try again with an integer")
                    return
            print("Item updated.")
            save_data(data)
            return
    print("ID not found.")

#search by ID
def search_item(data):
    search = input("Search ID: ").lower()
    found = False
    for item in data:
        if search in item["id"].lower():
            print(f"ID: {item['id']} / Name: {item['name']} / £{item['price']} / Qty: {item['quantity']}")
            found = True
    if not found:
        print("No items found.")

#clear all
def clear_inventory(data):
    confirm = input("Clear all items? (Y/N): ").upper()
    if confirm == "Y": 
        data.clear()
        save_data(data)
        print("Inventory cleared.")
    else:
        print("Cancelled.")

#delete single item
def delete_item(data):
    item_id = input("Enter ID to delete: ")
    for item in data:
        if item["id"] == item_id:
            confirm = input(f"Are you sure you want to delete '{item['name']}'? (Y/N): ").upper()
            if confirm == "Y":
                data.remove(item)
                save_data(data)
                print("Item deleted.")
                return
            else:
                print("Cancelled.")
                return
    print("ID not found.")

#low stock report
def low_stock_report(data):
    print("--- Low Stock Report (below 5) ---")
    found = False
    for item in data:
        if item["quantity"] < 5:
            print(f"{item['name']} - Qty: {item['quantity']}")
            found = True
    if not found:
        print("No low-stock items.")


#menu
def main():
    data = load_data()

#all options you can add more if u like but these are just the basic ones for now
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("1. Add Item")
        print("2. View Items")
        print("3. Update Item")
        print("4. Search Item")
        print("5. Delete Item")
        print("6. Clear Inventory")
        print("7. Low Stock Report")
        print("8. Manual Save")
        print("0: Exit")
        print("====================") #seperator makes it more visually appealing

#if u want to add more options above make sure u change the options below too
        option = input("Choose: ")

        if option == "1":
            add_item(data)

        elif option == "2":
            view_items(data)

        elif option == "3":
            update_item(data)

        elif option == "4":
            search_item(data)

        elif option == "5":
            delete_item(data)

        elif option == "6":
            clear_inventory(data)

        elif option == "7":
            low_stock_report(data)

        elif option == "8":
            save_data(data)
            print("Saved.")

        elif option == "0":
            break

        else:
            print("Invalid Option.") #if an undefined option is entered like 9 it would fail

        input("Press enter to continue.")

main()